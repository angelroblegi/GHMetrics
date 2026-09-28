using CommanCenter.API.Application.DTOs.Common;
using CommanCenter.API.Application.DTOs.Consultores;
using CommanCenter.API.Application.Interfaces;
using CommanCenter.API.Domain.Entities;
using CommanCenter.API.Domain.Interfaces;
using CommanCenter.API.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using System.Text.Json;

namespace CommanCenter.API.Application.Services;

public class ConsultorService : IConsultorService
{
    private const int HojaVidaMaxBytes = 10 * 1024 * 1024;
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    private readonly IConsultorRepository _repo;
    private readonly IAuditoriaRepository _auditoria;
    private readonly IExcelExportService _excel;
    private readonly IHojaVidaStorageService _hojaVidaStorage;
    private readonly ILogger<ConsultorService> _logger;
    private readonly AppDbContext _db;

    public ConsultorService(
        IConsultorRepository repo,
        IAuditoriaRepository auditoria,
        IExcelExportService excel,
        IHojaVidaStorageService hojaVidaStorage,
        AppDbContext db,
        ILogger<ConsultorService> logger)
    {
        _repo = repo;
        _auditoria = auditoria;
        _excel = excel;
        _hojaVidaStorage = hojaVidaStorage;
        _db = db;
        _logger = logger;
    }

    public async Task<ApiResponse<IEnumerable<ConsultorDto>>> GetAllAsync(ColaboradorFiltroDto? filtro = null)
    {
        try
        {
            var consultores = await _repo.GetHabilitadosAsync();
            var dtos = AplicarFiltros(consultores.Select(MapToDto), filtro);
            return ApiResponse<IEnumerable<ConsultorDto>>.Ok(dtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error al obtener consultores");
            return ApiResponse<IEnumerable<ConsultorDto>>.Fail("Error interno al obtener consultores.");
        }
    }

    public async Task<byte[]> ExportarExcelAsync()
    {
        var consultores = await _repo.GetHabilitadosAsync();
        return _excel.GenerarDirectorio(consultores);
    }

    public async Task<ApiResponse<IEnumerable<ConsultorDto>>> GetDeshabilitadosAsync()
    {
        try
        {
            var consultores = await _repo.GetDeshabilitadosAsync();
            var dtos = consultores.Select(MapToDto);
            return ApiResponse<IEnumerable<ConsultorDto>>.Ok(dtos);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error al obtener consultores deshabilitados");
            return ApiResponse<IEnumerable<ConsultorDto>>.Fail("Error interno al obtener consultores deshabilitados.");
        }
    }

    public async Task<ApiResponse<ConsultorDto>> GetByIdAsync(int id)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<ConsultorDto>.NotFound("Consultor");

        return ApiResponse<ConsultorDto>.Ok(MapToDto(consultor));
    }

    public async Task<ApiResponse<ConsultorDto>> CrearAsync(CrearConsultorDto dto, string usuarioId)
    {
        try
        {
            var existente = await _repo.GetByEmailAsync(dto.Email);
            if (existente is not null)
                return ApiResponse<ConsultorDto>.Fail($"Ya existe un consultor con el email {dto.Email}.");

            var consultor = new Consultor
            {
                Cedula = dto.Cedula?.Trim(),
                Nombre = dto.Nombre.Trim(),
                Apellido = dto.Apellido.Trim(),
                Email = dto.Email.Trim().ToLower(),
                Celular = dto.Celular,
                Cargo = dto.Cargo,
                Rol = dto.Rol,
                Capacidad = dto.Capacidad,
                HabilidadesTecnicasJson = "[]",
                RolesTecnicosJson = "[]",
                Empresa = dto.Empresa,
                Direccion = dto.Direccion,
                Barrio = dto.Barrio,
                Ciudad = dto.Ciudad,
                ContactoEmergenciaNombre = dto.ContactoEmergenciaNombre,
                ContactoEmergenciaTelefono = dto.ContactoEmergenciaTelefono,
                Estado = string.IsNullOrWhiteSpace(dto.Estado) ? "Activo" : dto.Estado.Trim(),
                FechaIngreso = dto.FechaIngreso,
                FechaNacimiento = dto.FechaNacimiento,
                Observaciones = dto.Observaciones,
                FotoUrl = dto.FotoUrl,
                CreadoPor = usuarioId
            };

            // Asignar a una o varias células (sin duplicados), con su % de participación
            foreach (var asignacion in dto.Celulas.GroupBy(c => c.CelulaId).Select(g => g.First()))
            {
                consultor.Celulas.Add(new CelulaMiembro
                {
                    CelulaId = asignacion.CelulaId,
                    PorcentajeParticipacion = asignacion.PorcentajeParticipacion
                });
            }

            var creado = await _repo.AddAsync(consultor);
            await _repo.SaveChangesAsync();

            var celulaIdsCreacion = dto.Celulas.Select(c => c.CelulaId).Distinct().ToList();
            await _auditoria.RegistrarAsync("DataTeam", "CREATE", "Consultor",
                creado.Id.ToString(), null,
                $"{creado.Nombre} {creado.Apellido} | Células: {(celulaIdsCreacion.Count > 0 ? string.Join(",", celulaIdsCreacion) : "ninguna")}",
                usuarioId, null, null);

            _logger.LogInformation("Consultor {Id} creado por {Usuario} y asignado a {Total} célula(s)",
                creado.Id, usuarioId, celulaIdsCreacion.Count);
            return ApiResponse<ConsultorDto>.Ok(MapToDto(creado), "Consultor creado exitosamente.");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error al crear consultor");
            return ApiResponse<ConsultorDto>.Fail("Error interno al crear el consultor.");
        }
    }

    public async Task<ApiResponse<ConsultorDto>> ActualizarAsync(int id, ActualizarConsultorDto dto, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<ConsultorDto>.NotFound("Consultor");

        var anterior = $"{consultor.Nombre} {consultor.Apellido}";

        consultor.Cedula = dto.Cedula?.Trim();
        consultor.Nombre = dto.Nombre.Trim();
        consultor.Apellido = dto.Apellido.Trim();
        consultor.Email = dto.Email.Trim().ToLower();
        consultor.Celular = dto.Celular;
        consultor.Cargo = dto.Cargo;
        consultor.Rol = dto.Rol;
        consultor.Capacidad = dto.Capacidad;
        consultor.Empresa = dto.Empresa;
        consultor.Direccion = dto.Direccion;
        consultor.Barrio = dto.Barrio;
        consultor.Ciudad = dto.Ciudad;
        consultor.ContactoEmergenciaNombre = dto.ContactoEmergenciaNombre;
        consultor.ContactoEmergenciaTelefono = dto.ContactoEmergenciaTelefono;
        consultor.Estado = string.IsNullOrWhiteSpace(dto.Estado) ? "Activo" : dto.Estado.Trim();
        consultor.FechaIngreso = dto.FechaIngreso;
        consultor.FechaNacimiento = dto.FechaNacimiento;
        consultor.Habilitado = dto.Habilitado;
        consultor.Observaciones = dto.Observaciones;
        if (!string.IsNullOrWhiteSpace(dto.FotoUrl))
            consultor.FotoUrl = dto.FotoUrl;
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        // Sincronizar células: eliminar las que ya no están en el DTO, agregar las nuevas
        // (con su % de participación) y actualizar el % de las que ya existían si vino informado.
        var asignacionesNuevas = dto.Celulas.GroupBy(c => c.CelulaId).Select(g => g.First()).ToList();
        var celulaIdsNuevas = asignacionesNuevas.Select(a => a.CelulaId).ToList();

        foreach (var cm in consultor.Celulas.Where(cm => !celulaIdsNuevas.Contains(cm.CelulaId)).ToList())
            consultor.Celulas.Remove(cm);

        foreach (var asignacion in asignacionesNuevas)
        {
            var existente = consultor.Celulas.FirstOrDefault(cm => cm.CelulaId == asignacion.CelulaId);
            if (existente is null)
                consultor.Celulas.Add(new Domain.Entities.CelulaMiembro
                {
                    CelulaId = asignacion.CelulaId,
                    PorcentajeParticipacion = asignacion.PorcentajeParticipacion
                });
            else if (asignacion.PorcentajeParticipacion.HasValue)
                existente.PorcentajeParticipacion = asignacion.PorcentajeParticipacion;
        }

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();

        await _auditoria.RegistrarAsync("DataTeam", "UPDATE", "Consultor",
            id.ToString(), anterior, $"{consultor.Nombre} {consultor.Apellido}", usuarioId, null, null);

        return ApiResponse<ConsultorDto>.Ok(MapToDto(consultor), "Consultor actualizado exitosamente.");
    }

    public async Task<ApiResponse<bool>> DeshabilitarAsync(int id, string? razon, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<bool>.NotFound("Consultor");

        if (!consultor.Habilitado)
            return ApiResponse<bool>.Fail("El consultor ya se encuentra deshabilitado.");

        consultor.Habilitado = false;
        consultor.MotivoDeshabilitacion = razon?.Trim();
        consultor.FechaDeshabilitacion = DateTime.UtcNow;
        if (consultor.HojaVidaContenido is not null)
            consultor.HojaVidaFechaExpiracion = DateTime.UtcNow.AddMonths(3);
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();

        await _auditoria.RegistrarAsync("DataTeam", "DISABLE", "Consultor",
            id.ToString(), "Habilitado=true",
            $"Habilitado=false | Motivo: {razon?.Trim() ?? "N/A"}", usuarioId, null, null);

        _logger.LogWarning("Consultor {Id} deshabilitado por {Usuario}. Motivo: {Motivo}",
            id, usuarioId, razon?.Trim() ?? "No especificado");

        return ApiResponse<bool>.Ok(true, "Consultor deshabilitado.");
    }

    public async Task<ApiResponse<bool>> RehabilitarAsync(int id, string? razon, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<bool>.NotFound("Consultor");

        if (consultor.Habilitado)
            return ApiResponse<bool>.Fail("El consultor ya se encuentra habilitado.");

        var motivoAnterior = consultor.MotivoDeshabilitacion;
        consultor.Habilitado = true;
        consultor.MotivoDeshabilitacion = null;
        consultor.FechaDeshabilitacion = null;
        consultor.HojaVidaFechaExpiracion = null;
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();

        await _auditoria.RegistrarAsync("DataTeam", "ENABLE", "Consultor",
            id.ToString(), $"Habilitado=false | Motivo: {motivoAnterior}",
            "Habilitado=true", usuarioId, null, null);

        _logger.LogInformation("Consultor {Id} rehabilitado por {Usuario}", id, usuarioId);

        return ApiResponse<bool>.Ok(true, "Consultor rehabilitado.");
    }

    public async Task<ApiResponse<bool>> EliminarAsync(int id, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<bool>.NotFound("Consultor");

        consultor.Activo = false;
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();

        await _auditoria.RegistrarAsync("DataTeam", "DELETE", "Consultor",
            id.ToString(), consultor.Email, null, usuarioId, null, null);

        return ApiResponse<bool>.Ok(true, "Consultor eliminado.");
    }

    public async Task<ApiResponse<IEnumerable<ConsultorDto>>> GetByCelulaAsync(int celulaId)
    {
        var consultores = await _repo.GetByCelulaAsync(celulaId);
        return ApiResponse<IEnumerable<ConsultorDto>>.Ok(consultores.Select(MapToDto));
    }

    public async Task<ApiResponse<ConsultorHojaVidaDto>> CargarHojaVidaAsync(int id, IFormFile archivo, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<ConsultorHojaVidaDto>.NotFound("Consultor");

        if (archivo is null || archivo.Length == 0)
            return ApiResponse<ConsultorHojaVidaDto>.Fail("Debe adjuntar un archivo PDF.");

        if (archivo.Length > HojaVidaMaxBytes)
            return ApiResponse<ConsultorHojaVidaDto>.Fail("El archivo supera el tamaño máximo permitido (10 MB).");

        var extension = Path.GetExtension(archivo.FileName);
        if (!".pdf".Equals(extension, StringComparison.OrdinalIgnoreCase))
            return ApiResponse<ConsultorHojaVidaDto>.Fail("Solo se permiten archivos con extensión .pdf.");

        byte[] contenido;
        await using (var ms = new MemoryStream())
        {
            await archivo.CopyToAsync(ms);
            contenido = ms.ToArray();
        }

        if (!EsPdf(contenido))
            return ApiResponse<ConsultorHojaVidaDto>.Fail("El archivo cargado no es un PDF válido.");

        await using var stream = new MemoryStream(contenido);
        var subida = await _hojaVidaStorage.SubirAsync(
            consultor.Id,
            archivo.FileName,
            stream,
            "application/pdf");

        if (!subida.Exitoso || string.IsNullOrWhiteSpace(subida.BlobName))
            return ApiResponse<ConsultorHojaVidaDto>.Fail(subida.Error ?? "No fue posible guardar la hoja de vida.");

        if (!string.IsNullOrWhiteSpace(consultor.HojaVidaBlobName))
            await _hojaVidaStorage.EliminarAsync(consultor.HojaVidaBlobName);

        consultor.HojaVidaContenido = null;
        consultor.HojaVidaContentType = "application/pdf";
        consultor.HojaVidaNombreArchivo = Path.GetFileName(archivo.FileName);
        consultor.HojaVidaBlobName = subida.BlobName;
        consultor.HojaVidaUrl = subida.Url;
        consultor.HojaVidaFechaCarga = DateTime.UtcNow;
        consultor.HojaVidaFechaExpiracion = consultor.Habilitado ? null : DateTime.UtcNow.AddMonths(3);
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();

        await _auditoria.RegistrarAsync("DataTeam", "UPLOAD", "ConsultorHojaVida",
            id.ToString(), null, consultor.HojaVidaNombreArchivo, usuarioId, null, null);

        return ApiResponse<ConsultorHojaVidaDto>.Ok(new ConsultorHojaVidaDto
        {
            ConsultorId = consultor.Id,
            NombreArchivo = consultor.HojaVidaNombreArchivo!,
            FechaCarga = consultor.HojaVidaFechaCarga!.Value,
            FechaExpiracion = consultor.HojaVidaFechaExpiracion
        }, "Hoja de vida cargada exitosamente.");
    }

    public async Task<(bool Exitoso, string? Mensaje, byte[]? Contenido, string? ContentType, string? NombreArchivo)> DescargarHojaVidaAsync(int id)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return (false, "Consultor no encontrado.", null, null, null);

        if (!string.IsNullOrWhiteSpace(consultor.HojaVidaBlobName))
        {
            var descarga = await _hojaVidaStorage.DescargarAsync(consultor.HojaVidaBlobName);
            if (!descarga.Exitoso || descarga.Contenido is null)
                return (false, descarga.Error ?? "No fue posible descargar la hoja de vida.", null, null, null);

            return (
                true,
                null,
                descarga.Contenido,
                descarga.ContentType ?? "application/pdf",
                string.IsNullOrWhiteSpace(consultor.HojaVidaNombreArchivo) ? $"hoja_vida_{consultor.Id}.pdf" : consultor.HojaVidaNombreArchivo
            );
        }

        if (consultor.HojaVidaContenido is null || consultor.HojaVidaContenido.Length == 0)
            return (false, "El consultor no tiene hoja de vida cargada.", null, null, null);

        return (
            true,
            null,
            consultor.HojaVidaContenido,
            string.IsNullOrWhiteSpace(consultor.HojaVidaContentType) ? "application/pdf" : consultor.HojaVidaContentType,
            string.IsNullOrWhiteSpace(consultor.HojaVidaNombreArchivo) ? $"hoja_vida_{consultor.Id}.pdf" : consultor.HojaVidaNombreArchivo
        );
    }

    public async Task<ApiResponse<CapacidadesTecnicasDto>> GetCapacidadesTecnicasAsync(int id)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        return consultor is null
            ? ApiResponse<CapacidadesTecnicasDto>.NotFound("Colaborador")
            : ApiResponse<CapacidadesTecnicasDto>.Ok(MapCapacidades(consultor));
    }

    public async Task<ApiResponse<CapacidadesTecnicasDto>> GetMisCapacidadesTecnicasAsync(string email)
    {
        var consultor = await _repo.GetByEmailAsync(email);
        return consultor is null
            ? ApiResponse<CapacidadesTecnicasDto>.NotFound("Colaborador asociado al usuario")
            : ApiResponse<CapacidadesTecnicasDto>.Ok(MapCapacidades(consultor));
    }

    public async Task<ApiResponse<CapacidadesTecnicasDto>> ActualizarMisCapacidadesTecnicasAsync(
        string email, ActualizarCapacidadesTecnicasDto dto, string usuarioId)
    {
        var consultor = await _repo.GetByEmailAsync(email);
        return consultor is null
            ? ApiResponse<CapacidadesTecnicasDto>.NotFound("Colaborador asociado al usuario")
            : await ActualizarCapacidadesTecnicasAsync(consultor.Id, dto, usuarioId);
    }

    public async Task<ApiResponse<ConsultorHojaVidaDto>> CargarMiHojaVidaAsync(
        string email, IFormFile archivo, string usuarioId)
    {
        var consultor = await _repo.GetByEmailAsync(email);
        return consultor is null
            ? ApiResponse<ConsultorHojaVidaDto>.NotFound("Colaborador asociado al usuario")
            : await CargarHojaVidaAsync(consultor.Id, archivo, usuarioId);
    }

    public async Task<(bool Exitoso, string? Mensaje, byte[]? Contenido, string? ContentType, string? NombreArchivo)> DescargarMiHojaVidaAsync(string email)
    {
        var consultor = await _repo.GetByEmailAsync(email);
        return consultor is null
            ? (false, "No existe un colaborador asociado al usuario autenticado.", null, null, null)
            : await DescargarHojaVidaAsync(consultor.Id);
    }

    public async Task<ApiResponse<CapacidadesTecnicasDto>> ActualizarCapacidadesTecnicasAsync(
        int id, ActualizarCapacidadesTecnicasDto dto, string usuarioId)
    {
        var consultor = await _repo.GetByIdWithCelulasAsync(id);
        if (consultor is null)
            return ApiResponse<CapacidadesTecnicasDto>.NotFound("Colaborador");

        var habilidades = NormalizarLista(dto.HabilidadesTecnicas);
        var categorias = NormalizarLista(dto.CategoriasTecnicas.Count > 0
            ? dto.CategoriasTecnicas
            : dto.RolesTecnicos);
        var catalogo = await _db.CategoriasTecnicas
            .Include(x => x.Habilidades)
            .Where(x => categorias.Contains(x.Nombre))
            .ToListAsync();
        var categoriasNoRegistradas = categorias.Where(c => !catalogo.Any(x =>
            x.Nombre.Equals(c, StringComparison.OrdinalIgnoreCase))).ToList();
        if (categoriasNoRegistradas.Count > 0)
            return ApiResponse<CapacidadesTecnicasDto>.Fail(
                $"Las categorías no están registradas: {string.Join(", ", categoriasNoRegistradas)}.");

        var habilidadesNoPermitidas = habilidades.Where(h => !catalogo.Any(categoria =>
            categoria.Habilidades.Any(x => x.Nombre.Equals(h, StringComparison.OrdinalIgnoreCase)))).ToList();
        if (habilidadesNoPermitidas.Count > 0)
            return ApiResponse<CapacidadesTecnicasDto>.Fail(
                $"Las habilidades no corresponden a las categorías seleccionadas: {string.Join(", ", habilidadesNoPermitidas)}.");

        consultor.HabilidadesTecnicasJson = JsonSerializer.Serialize(habilidades, JsonOptions);
        consultor.RolesTecnicosJson = JsonSerializer.Serialize(categorias, JsonOptions);
        consultor.FechaModificacion = DateTime.UtcNow;
        consultor.ModificadoPor = usuarioId;

        await _repo.UpdateAsync(consultor);
        await _repo.SaveChangesAsync();
        await _auditoria.RegistrarAsync("DataTeam", "UPDATE", "CapacidadesTecnicas",
            id.ToString(), null,
            $"Categorías: {string.Join(", ", categorias)} | Habilidades: {string.Join(", ", habilidades)}",
            usuarioId, null, null);

        return ApiResponse<CapacidadesTecnicasDto>.Ok(
            MapCapacidades(consultor), "Capacidades técnicas actualizadas exitosamente.");
    }

    private static ConsultorDto MapToDto(Consultor c) => new()
    {
        Id = c.Id,
        Cedula = c.Cedula,
        Nombre = c.Nombre,
        Apellido = c.Apellido,
        Email = c.Email,
        Celular = c.Celular,
        Cargo = c.Cargo,
        Rol = c.Rol,
        Capacidad = c.Capacidad,
        HabilidadesTecnicas = DeserializarLista(c.HabilidadesTecnicasJson),
        RolesTecnicos = DeserializarLista(c.RolesTecnicosJson),
        CategoriasTecnicas = DeserializarLista(c.RolesTecnicosJson),
        Empresa = c.Empresa,
        Direccion = c.Direccion,
        Barrio = c.Barrio,
        Ciudad = c.Ciudad,
        ContactoEmergenciaNombre = c.ContactoEmergenciaNombre,
        ContactoEmergenciaTelefono = c.ContactoEmergenciaTelefono,
        Estado = c.Estado,
        FechaIngreso = c.FechaIngreso,
        FechaNacimiento = c.FechaNacimiento,
        Habilitado = c.Habilitado,
        FotoUrl = c.FotoUrl,
        Observaciones = c.Observaciones,
        TieneHojaVida = !string.IsNullOrWhiteSpace(c.HojaVidaBlobName)
            || (c.HojaVidaContenido is not null && c.HojaVidaContenido.Length > 0),
        HojaVidaNombreArchivo = c.HojaVidaNombreArchivo,
        HojaVidaUrl = c.HojaVidaUrl,
        HojaVidaFechaCarga = c.HojaVidaFechaCarga,
        HojaVidaFechaExpiracion = c.HojaVidaFechaExpiracion,
        FechaCreacion = c.FechaCreacion,
        MotivoDeshabilitacion = c.MotivoDeshabilitacion,
        FechaDeshabilitacion = c.FechaDeshabilitacion,
        Celulas = c.Celulas.Select(cm => cm.Celula?.Nombre ?? "").Where(n => n != "").ToList(),
        CelulasIds = c.Celulas.Select(cm => cm.CelulaId).ToList()
    };

    private static CapacidadesTecnicasDto MapCapacidades(Consultor consultor) => new()
    {
        ColaboradorId = consultor.Id,
        HabilidadesTecnicas = DeserializarLista(consultor.HabilidadesTecnicasJson),
        RolesTecnicos = DeserializarLista(consultor.RolesTecnicosJson),
        CategoriasTecnicas = DeserializarLista(consultor.RolesTecnicosJson),
        TieneHojaVida = !string.IsNullOrWhiteSpace(consultor.HojaVidaBlobName)
            || (consultor.HojaVidaContenido is not null && consultor.HojaVidaContenido.Length > 0),
        HojaVidaNombreArchivo = consultor.HojaVidaNombreArchivo
    };

    private static IEnumerable<ConsultorDto> AplicarFiltros(
        IEnumerable<ConsultorDto> colaboradores, ColaboradorFiltroDto? filtro)
    {
        if (filtro is null)
            return colaboradores;

        return colaboradores
            .Where(c => Contiene(c.Cedula, filtro.Cedula))
            .Where(c => Contiene(c.NombreCompleto, filtro.Nombre))
            .Where(c => Contiene(c.Email, filtro.Email))
            .Where(c => Contiene(c.Cargo, filtro.Cargo))
            .Where(c => Contiene(c.Rol, filtro.Rol))
            .Where(c => Contiene(c.Empresa, filtro.Empresa))
            .Where(c => Contiene(c.Ciudad, filtro.Ciudad))
            .Where(c => string.IsNullOrWhiteSpace(filtro.Celula)
                || c.Celulas.Any(x => x.Contains(filtro.Celula, StringComparison.OrdinalIgnoreCase)))
            .Where(c => string.IsNullOrWhiteSpace(filtro.Habilidad)
                || c.HabilidadesTecnicas.Any(x => x.Contains(filtro.Habilidad, StringComparison.OrdinalIgnoreCase)))
            .Where(c => string.IsNullOrWhiteSpace(filtro.Categoria)
                || c.CategoriasTecnicas.Any(x => x.Contains(filtro.Categoria, StringComparison.OrdinalIgnoreCase)))
            .Where(c => !filtro.TieneHojaVida.HasValue || c.TieneHojaVida == filtro.TieneHojaVida.Value);
    }

    private static bool Contiene(string? valor, string? filtro) =>
        string.IsNullOrWhiteSpace(filtro)
        || (valor?.Contains(filtro, StringComparison.OrdinalIgnoreCase) ?? false);

    private static List<string> NormalizarLista(IEnumerable<string>? valores) =>
        valores?
            .Where(x => !string.IsNullOrWhiteSpace(x))
            .Select(x => x.Trim())
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .OrderBy(x => x)
            .ToList() ?? new List<string>();

    private static List<string> DeserializarLista(string? json)
    {
        if (string.IsNullOrWhiteSpace(json))
            return new List<string>();

        try
        {
            return JsonSerializer.Deserialize<List<string>>(json, JsonOptions) ?? new List<string>();
        }
        catch (JsonException)
        {
            return new List<string>();
        }
    }

    private static bool EsPdf(byte[] contenido)
    {
        if (contenido.Length < 5)
            return false;

        return contenido[0] == 0x25 // %
            && contenido[1] == 0x50 // P
            && contenido[2] == 0x44 // D
            && contenido[3] == 0x46 // F
            && contenido[4] == 0x2D; // -
    }
}
