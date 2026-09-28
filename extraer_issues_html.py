private EditarConsultorViewModel MapToInput(ConsultorViewModel c)
{
    var input = new EditarConsultorViewModel
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

    // Cargar los porcentajes actuales de este consultor
    foreach (var celula in CelulasDisponibles)
    {
        var miembro = celula.Miembros
            .FirstOrDefault(m => m.ConsultorId == c.Id);

        if (miembro is not null)
        {
            input.Porcentajes[celula.Id] = miembro.PorcentajeParticipacion;
        }
    }

    return input;
}
