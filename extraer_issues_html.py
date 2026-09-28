namespace CommanCenter.Portal.Models;

using System.ComponentModel.DataAnnotations;

public class CelulaViewModel
{
    public int Id { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string? Descripcion { get; set; }
    public string Color { get; set; } = "#28a745";
    public string? ImagenUrl { get; set; }
    public bool Activo { get; set; }
    public int TotalMiembros { get; set; }
    public string? NombreLider { get; set; }
    public DateTime FechaCreacion { get; set; }
    public List<MiembroCelulaViewModel> Miembros { get; set; } = [];
}

public class MiembroCelulaViewModel
{
    public int ConsultorId { get; set; }
    public string NombreCompleto { get; set; } = string.Empty;
    public string? Cargo { get; set; }
    public bool EsLider { get; set; }
    public decimal? PorcentajeParticipacion { get; set; }
}

public class ConsultorViewModel
{
    public int Id { get; set; }
    public string? Cedula { get; set; }
    public string Nombre { get; set; } = string.Empty;
    public string Apellido { get; set; } = string.Empty;
    public string NombreCompleto => $"{Nombre} {Apellido}";
    public string Email { get; set; } = string.Empty;
    public string? Celular { get; set; }
    public string? Cargo { get; set; }
    public string? Rol { get; set; }
    public string? Capacidad { get; set; }
    public List<string> HabilidadesTecnicas { get; set; } = [];
    public List<string> RolesTecnicos { get; set; } = [];
    public List<string> CategoriasTecnicas { get; set; } = [];
    public string? Empresa { get; set; }
    public string? Direccion { get; set; }
    public string? Barrio { get; set; }
    public string? Ciudad { get; set; }
    public string? ContactoEmergenciaNombre { get; set; }
    public string? ContactoEmergenciaTelefono { get; set; }
    public string Estado { get; set; } = "Activo";
    public DateTime? FechaIngreso { get; set; }
    public DateTime? FechaNacimiento { get; set; }
    public bool Habilitado { get; set; }
    public string? FotoUrl { get; set; }
    public string? Observaciones { get; set; }
    public string? CelulaNombre { get; set; }
    public List<string> Celulas { get; set; } = [];
    public List<int> CelulasIds { get; set; } = [];
    public string? MotivoDeshabilitacion { get; set; }
    public DateTime? FechaDeshabilitacion { get; set; }
    public bool TieneHojaVida { get; set; }
    public string? HojaVidaNombreArchivo { get; set; }
    public DateTime? HojaVidaFechaCarga { get; set; }
    public DateTime? HojaVidaFechaExpiracion { get; set; }
    public DateTime FechaCreacion { get; set; }
}

public class HojaVidaConsultorViewModel
{
    public int ConsultorId { get; set; }
    public string NombreArchivo { get; set; } = string.Empty;
    public DateTime FechaCarga { get; set; }
    public DateTime? FechaExpiracion { get; set; }
}

public class CapacidadesTecnicasViewModel
{
    public int ColaboradorId { get; set; }
    public List<string> HabilidadesTecnicas { get; set; } = [];
    public List<string> RolesTecnicos { get; set; } = [];
    public List<string> CategoriasTecnicas { get; set; } = [];
    public bool TieneHojaVida { get; set; }
    public string? HojaVidaNombreArchivo { get; set; }
}

public class CatalogoCapacidadesTecnicasViewModel
{
    public List<string> HabilidadesTecnicas { get; set; } = [];
    public List<string> RolesTecnicos { get; set; } = [];
    public List<string> CategoriasTecnicas { get; set; } = [];
    public List<CategoriaCapacidadTecnicaViewModel> Categorias { get; set; } = [];
}

public class CategoriaCapacidadTecnicaViewModel
{
    public string Nombre { get; set; } = string.Empty;
    public List<string> Habilidades { get; set; } = [];
}

public class ActualizarCapacidadesTecnicasInput
{
    public List<string> HabilidadesTecnicas { get; set; } = [];
    public List<string> RolesTecnicos { get; set; } = [];
    public List<string> CategoriasTecnicas { get; set; } = [];
}

/// <summary>Datos del formulario para crear un consultor desde el Portal.</summary>
public class CrearConsultorViewModel
{
    [Required(ErrorMessage = "La cédula es obligatoria.")]
    public string Cedula { get; set; } = string.Empty;

    [Required(ErrorMessage = "El nombre es obligatorio.")]
    public string Nombre { get; set; } = string.Empty;

    [Required(ErrorMessage = "El apellido es obligatorio.")]
    public string Apellido { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo es obligatorio.")]
    [EmailAddress(ErrorMessage = "El correo no es válido.")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "El celular es obligatorio.")]
    public string Celular { get; set; } = string.Empty;

    [Required(ErrorMessage = "El cargo es obligatorio.")]
    public string Cargo { get; set; } = string.Empty;

    public string? Rol { get; set; }
    public string? Capacidad { get; set; }

    [Required(ErrorMessage = "La empresa es obligatoria.")]
    public string Empresa { get; set; } = string.Empty;

    public string? Direccion { get; set; }
    public string? Barrio { get; set; }
    public string? Ciudad { get; set; }
    public string? ContactoEmergenciaNombre { get; set; }
    public string? ContactoEmergenciaTelefono { get; set; }
    public string Estado { get; set; } = "Activo";

    [Required(ErrorMessage = "La fecha de ingreso es obligatoria.")]
    public DateTime? FechaIngreso { get; set; }

    [Required(ErrorMessage = "La fecha de nacimiento es obligatoria.")]
    public DateTime? FechaNacimiento { get; set; }

    public string? Observaciones { get; set; }

    /// <summary>Células seleccionadas (una o varias), con su % de participación opcional.</summary>
    [MinLength(1, ErrorMessage = "Debe seleccionar al menos una célula.")]
    public List<CelulaAsignacionInput> Celulas { get; set; } = [];
}

/// <summary>Asignación de un colaborador a una célula, con su % de participación opcional.</summary>
public class CelulaAsignacionInput
{
    public int CelulaId { get; set; }

    [Range(0, 100, ErrorMessage = "El porcentaje de participación debe estar entre 0 y 100.")]
    public decimal? PorcentajeParticipacion { get; set; }
}

/// <summary>Datos del formulario para editar un consultor existente desde el Portal.</summary>
public class EditarConsultorViewModel
{
    public int Id { get; set; }

    [Required(ErrorMessage = "La cédula es obligatoria.")]
    public string Cedula { get; set; } = string.Empty;

    [Required(ErrorMessage = "El nombre es obligatorio.")]
    public string Nombre { get; set; } = string.Empty;

    [Required(ErrorMessage = "El apellido es obligatorio.")]
    public string Apellido { get; set; } = string.Empty;

    [Required(ErrorMessage = "El correo es obligatorio.")]
    [EmailAddress(ErrorMessage = "El correo no es válido.")]
    public string Email { get; set; } = string.Empty;

    [Required(ErrorMessage = "El celular es obligatorio.")]
    public string Celular { get; set; } = string.Empty;

    [Required(ErrorMessage = "El cargo es obligatorio.")]
    public string Cargo { get; set; } = string.Empty;

    public string? Rol { get; set; }
    public string? Capacidad { get; set; }

    [Required(ErrorMessage = "La empresa es obligatoria.")]
    public string Empresa { get; set; } = string.Empty;

    public string? Direccion { get; set; }
    public string? Barrio { get; set; }
    public string? Ciudad { get; set; }
    public string? ContactoEmergenciaNombre { get; set; }
    public string? ContactoEmergenciaTelefono { get; set; }
    public string Estado { get; set; } = "Activo";

    [Required(ErrorMessage = "La fecha de ingreso es obligatoria.")]
    public DateTime? FechaIngreso { get; set; }

    [Required(ErrorMessage = "La fecha de nacimiento es obligatoria.")]
    public DateTime? FechaNacimiento { get; set; }

    public string? Observaciones { get; set; }
    public string? FotoUrl { get; set; }
    public bool Habilitado { get; set; } = true;

    [MinLength(1, ErrorMessage = "Debe seleccionar al menos una célula.")]
    public List<int> CelulasIds { get; set; } = [];
}

/// <summary>Usuario del sistema (login por nombre, no por correo).</summary>
public class UsuarioViewModel
{
    public string Id { get; set; } = string.Empty;
    public string Usuario { get; set; } = string.Empty;
    public List<string> Roles { get; set; } = [];
}

/// <summary>Datos del formulario para crear un usuario desde el Portal.</summary>
public class CrearUsuarioInput
{
    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "El nombre de usuario es obligatorio.")]
    public string Usuario { get; set; } = string.Empty;

    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "La contraseña es obligatoria.")]
    [System.ComponentModel.DataAnnotations.MinLength(8, ErrorMessage = "Mínimo 8 caracteres.")]
    public string Password { get; set; } = string.Empty;

    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "El rol es obligatorio.")]
    public string Rol { get; set; } = string.Empty;
}

/// <summary>Datos del formulario para crear una célula desde el Portal.</summary>
public class CrearCelulaInput
{
    [System.ComponentModel.DataAnnotations.Required(ErrorMessage = "El nombre es obligatorio.")]
    [System.ComponentModel.DataAnnotations.MaxLength(100)]
    public string Nombre { get; set; } = string.Empty;

    [System.ComponentModel.DataAnnotations.MaxLength(500)]
    public string? Descripcion { get; set; }

    public string Color { get; set; } = "#28a745";
}

/// <summary>Vista previa de un correo automatizado (cumpleaños o reporte mensual).</summary>
public class PreviewCorreoViewModel
{
    public string Titulo { get; set; } = string.Empty;
    public string Periodo { get; set; } = string.Empty;
    public List<string> Destinatarios { get; set; } = [];
    public int Total { get; set; }
    public string Adjunto { get; set; } = string.Empty;
    public List<PreviewItemViewModel> Items { get; set; } = [];
}

public class PreviewItemViewModel
{
    public string Detalle { get; set; } = string.Empty;
    public string Nombre { get; set; } = string.Empty;
    public string Apellido { get; set; } = string.Empty;
    public string Cargo { get; set; } = string.Empty;
    public string Celula { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Empresa { get; set; } = string.Empty;
    public string Ciudad { get; set; } = string.Empty;
}

/// <summary>
/// Directorio de colaboradores: ficha completa por persona, agrupada por célula.
/// No confundir con un futuro "Organigrama" (árbol jerárquico visual de la empresa) —
/// esa es una historia de usuario distinta.
/// </summary>
public class DirectorioCelulaViewModel
{
    public int CelulaId { get; set; }
    public string CelulaNombre { get; set; } = string.Empty;
    public string? Color { get; set; }
    public List<DirectorioColaboradorViewModel> Colaboradores { get; set; } = [];
}

public class DirectorioColaboradorViewModel
{
    public int ConsultorId { get; set; }
    public string? Cedula { get; set; }
    public string NombreCompleto { get; set; } = string.Empty;
    public string? Cargo { get; set; }
    public string CelulaNombre { get; set; } = string.Empty;
    public string? Rol { get; set; }
    public List<string> HabilidadesTecnicas { get; set; } = [];
    public List<string> RolesTecnicos { get; set; } = [];
    public List<string> CategoriasTecnicas { get; set; } = [];
    public bool TieneHojaVida { get; set; }
    public string? HojaVidaNombreArchivo { get; set; }
    public bool EsLider { get; set; }
    public decimal? PorcentajeParticipacion { get; set; }
    public string? Lider { get; set; }
    public string? Empresa { get; set; }
    public string? Ciudad { get; set; }
    public string? Direccion { get; set; }
    public string? Barrio { get; set; }
    public DateTime? FechaCumpleanos { get; set; }
    public DateTime? FechaIngreso { get; set; }
}

/// <summary>Registro de auditoría: quién hizo qué y cuándo.</summary>
public class AuditoriaLogViewModel
{
    public int Id { get; set; }
    public DateTime Fecha { get; set; }
    public string? Usuario { get; set; }
    public string? UsuarioEmail { get; set; }
    public string? IpAddress { get; set; }
    public string? UserAgent { get; set; }
    public string Modulo { get; set; } = string.Empty;
    public string Accion { get; set; } = string.Empty;
    public string Entidad { get; set; } = string.Empty;
    public string? EntidadId { get; set; }
    public string? ValorAnterior { get; set; }
    public string? ValorNuevo { get; set; }
    public bool Exitoso { get; set; }
    public string? Error { get; set; }
}
