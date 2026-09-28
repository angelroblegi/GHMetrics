using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using CommanCenter.Portal.Models;
using CommanCenter.Portal.Services;
using System.Net;
using System.Net.Http.Headers;

namespace CommanCenter.Portal.Pages.DataTeam;

[Authorize(Roles = "Admin,Supervisor,Senior")]
public class DetalleConsultorModel : PageModel
{
    private readonly IApiClient _api;
    private readonly IImageStorageService _imagenes;
    private readonly ILogger<DetalleConsultorModel> _logger;

    private static readonly string[] ExtensionesPermitidas = { ".jpg", ".jpeg", ".png", ".gif", ".webp" };
    private static readonly string[] ExtensionesPdfPermitidas = { ".pdf" };
    private const long TamanoMaximoBytes = 5 * 1024 * 1024; // 5 MB
    private const long TamanoMaximoHojaVidaBytes = 10 * 1024 * 1024; // 10 MB

    [BindProperty(SupportsGet = true)] public int Id { get; set; }
    [BindProperty] public EditarConsultorViewModel Input { get; set; } = new();
    [BindProperty] public IFormFile? Foto { get; set; }
    [BindProperty] public IFormFile? HojaVidaPdf { get; set; }

    public List<CelulaViewModel> CelulasDisponibles { get; set; } = [];
    public ConsultorViewModel? ConsultorActual { get; set; }

    /// <summary>Solo Admin y Supervisor pueden editar; Senior solo visualiza.</summary>
    public bool PuedeEditar => User.IsInRole("Admin") || User.IsInRole("Supervisor");

    public string? Error { get; set; }
    public string? HojaVidaError { get; set; }

    /// <summary>
    /// URL de la foto lista para mostrar en la vista (con SAS token si aplica).
    /// Input.FotoUrl SIEMPRE guarda la URL base (sin token), que es la que se persiste en BD.
    /// </summary>
    public string? FotoUrlParaMostrar { get; set; }

    public DetalleConsultorModel(IApiClient api, IImageStorageService imagenes, ILogger<DetalleConsultorModel> logger)
    {
        _api = api;
        _imagenes = imagenes;
        _logger = logger;
    }

    public async Task<IActionResult> OnGetAsync()
    {
        Error = TempData["Error"] as string;
        await CargarCelulasAsync();

        var token = HttpContext.Session.GetString("jwt_token");
        var cargado = await CargarConsultorAsync(token, mapInput: true);
        if (!cargado)
        {
            Error ??= "No se encontró el consultor.";
            return Page();
        }

        FotoUrlParaMostrar = _imagenes.ObtenerUrlConSas(Input.FotoUrl);
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        await CargarCelulasAsync();
        FotoUrlParaMostrar = _imagenes.ObtenerUrlConSas(Input.FotoUrl);

        if (!PuedeEditar)
        {
            Error = "No tiene permisos para editar consultores.";
            return Page();
        }

        var token = HttpContext.Session.GetString("jwt_token");
        await CargarConsultorAsync(token, mapInput: false);

        if (!ModelState.IsValid)
        {
            Error = "Revise los campos obligatorios marcados.";
            return Page();
        }

        // La foto es opcional al editar: si no se sube una nueva, se conserva la actual.
        if (Foto is { Length: > 0 })
        {
            var (fotoUrl, errorFoto) = await GuardarImagenAsync(Foto);
            if (errorFoto is not null)
            {
                Error = errorFoto;
                return Page();
            }
            Input.FotoUrl = fotoUrl;
            FotoUrlParaMostrar = _imagenes.ObtenerUrlConSas(Input.FotoUrl);
        }

        var body = new
        {
            Input.Id,
            Input.Cedula,
            Input.Nombre,
            Input.Apellido,
            Input.Email,
            Input.Celular,
            Input.Cargo,
            Input.Rol,
            Input.Capacidad,
            Input.Empresa,
            Input.Direccion,
            Input.Barrio,
            Input.Ciudad,
            Input.ContactoEmergenciaNombre,
            Input.ContactoEmergenciaTelefono,
            Input.Estado,
            Input.FechaIngreso,
            Input.FechaNacimiento,
            Input.Observaciones,
            Input.FotoUrl,
            Input.Habilitado,
            // Esta p\u00e1gina no gestiona el % de participaci\u00f3n (eso se hace en Gestionar C\u00e9lula);
            // se env\u00eda null para que la API conserve el valor vigente de cada membres\u00eda.
            Celulas = Input.CelulasIds.Select(id => new { CelulaId = id, PorcentajeParticipacion = (decimal?)null })
        };

        var result = await _api.PutAsync<ConsultorViewModel>($"api/colaboradores/{Id}", body, token);

        if (result?.Exitoso == true)
        {
            _logger.LogInformation("Colaborador {Id} actualizado desde el Portal", Id);
            TempData["Success"] = $"Colaborador {Input.Nombre} {Input.Apellido} actualizado correctamente.";
            return RedirectToPage("/DataTeam/DirectorioColaboradores");
        }

        Error = result?.Mensaje ?? "No se pudo actualizar el colaborador.";
        return Page();
    }

    public async Task<IActionResult> OnPostCargarHojaVidaAsync()
    {
        await CargarCelulasAsync();

        // Esta acción solo valida el archivo de hoja de vida, no el formulario completo de edición.
        var inputKeys = ModelState.Keys.Where(k => k.StartsWith("Input.", StringComparison.OrdinalIgnoreCase)).ToList();
        foreach (var key in inputKeys)
            ModelState.Remove(key);

        if (!PuedeEditar)
        {
            Error = "No tiene permisos para cargar hoja de vida.";
            return Page();
        }

        var token = HttpContext.Session.GetString("jwt_token");
        var consultorCargado = await CargarConsultorAsync(token, mapInput: true);
        if (!consultorCargado)
            return Page();

        if (HojaVidaPdf is null || HojaVidaPdf.Length == 0)
        {
            HojaVidaError = "Debe seleccionar un archivo PDF.";
            return Page();
        }

        if (!EsPdfValido(HojaVidaPdf))
        {
            HojaVidaError = "Solo se permiten archivos PDF (.pdf).";
            return Page();
        }

        if (HojaVidaPdf.Length > TamanoMaximoHojaVidaBytes)
        {
            HojaVidaError = "La hoja de vida supera el tamaño máximo recomendado de 10 MB.";
            return Page();
        }

        using var content = new MultipartFormDataContent();
        await using var stream = HojaVidaPdf.OpenReadStream();
        using var archivo = new StreamContent(stream);
        archivo.Headers.ContentType = new MediaTypeHeaderValue("application/pdf");
        content.Add(archivo, "archivo", HojaVidaPdf.FileName);

        var result = await _api.PostMultipartAsync<HojaVidaConsultorViewModel>($"api/colaboradores/{Id}/capacidades/hoja-vida", content, token);
        if (result?.Exitoso == true)
        {
            TempData["Success"] = "Hoja de vida cargada exitosamente";
            return RedirectToPage(new { id = Id });
        }

        HojaVidaError = result?.Mensaje ?? "No se pudo cargar la hoja de vida.";
        return Page();
    }

    public async Task<IActionResult> OnGetDescargarHojaVidaAsync()
    {
        var token = HttpContext.Session.GetString("jwt_token");
        var result = await _api.DownloadDetailedAsync($"api/colaboradores/{Id}/capacidades/hoja-vida", token);

        if (result?.Exitoso == true && result.Contenido is not null)
        {
            return File(result.Contenido, result.ContentType, result.NombreArchivo);
        }

        if (result?.StatusCode == HttpStatusCode.NotFound)
        {
            TempData["Error"] = result.Mensaje ?? "No existe hoja de vida disponible para este consultor.";
            return RedirectToPage(new { id = Id });
        }

        TempData["Error"] = result?.Mensaje ?? "No se pudo descargar la hoja de vida.";
        return RedirectToPage(new { id = Id });
    }

    private static EditarConsultorViewModel MapToInput(ConsultorViewModel c) => new()
    {
        Id = c.Id,
        Cedula = c.Cedula ?? string.Empty,
        Nombre = c.Nombre,
        Apellido = c.Apellido,
        Email = c.Email,
        Celular = c.Celular ?? string.Empty,
        Cargo = c.Cargo ?? string.Empty,
        Rol = c.Rol,
        Capacidad = c.Capacidad,
        Empresa = c.Empresa ?? string.Empty,
        Direccion = c.Direccion,
        Barrio = c.Barrio,
        Ciudad = c.Ciudad,
        ContactoEmergenciaNombre = c.ContactoEmergenciaNombre,
        ContactoEmergenciaTelefono = c.ContactoEmergenciaTelefono,
        Estado = string.IsNullOrWhiteSpace(c.Estado) ? "Activo" : c.Estado,
        FechaIngreso = c.FechaIngreso,
        FechaNacimiento = c.FechaNacimiento,
        Observaciones = c.Observaciones,
        FotoUrl = c.FotoUrl,
        Habilitado = c.Habilitado,
        CelulasIds = c.CelulasIds
    };

    private async Task<(string? ruta, string? error)> GuardarImagenAsync(IFormFile imagen)
    {
        var extension = Path.GetExtension(imagen.FileName).ToLowerInvariant();
        if (!ExtensionesPermitidas.Contains(extension))
            return (null, "Formato de imagen no permitido. Use JPG, PNG, GIF o WEBP.");

        if (imagen.Length > TamanoMaximoBytes)
            return (null, "La imagen supera el tamaño máximo de 5 MB.");

        var nombreArchivo = $"consultor_{Guid.NewGuid():N}{extension}";
        await using var stream = imagen.OpenReadStream();
        var url = await _imagenes.SubirAsync(stream, nombreArchivo, "consultores", imagen.ContentType);
        return (url, null);
    }

    private async Task CargarCelulasAsync()
    {
        var token = HttpContext.Session.GetString("jwt_token");
        var result = await _api.GetAsync<List<CelulaViewModel>>("api/celulas", token);
        if (result?.Exitoso == true && result.Data is not null)
            CelulasDisponibles = result.Data;
    }

    private async Task<bool> CargarConsultorAsync(string? token, bool mapInput)
    {
        var result = await _api.GetAsync<ConsultorViewModel>($"api/colaboradores/{Id}", token);
        if (result?.Exitoso != true || result.Data is null)
        {
            Error = result?.Mensaje ?? "No se encontró el consultor.";
            return false;
        }

        ConsultorActual = result.Data;
        if (mapInput)
            Input = MapToInput(result.Data);

        return true;
    }

    private static bool EsPdfValido(IFormFile archivo)
    {
        var extension = Path.GetExtension(archivo.FileName).ToLowerInvariant();
        if (!ExtensionesPdfPermitidas.Contains(extension))
            return false;

        if (string.IsNullOrWhiteSpace(archivo.ContentType))
            return true;

        return archivo.ContentType.Equals("application/pdf", StringComparison.OrdinalIgnoreCase)
            || archivo.ContentType.Equals("application/x-pdf", StringComparison.OrdinalIgnoreCase);
    }
}
