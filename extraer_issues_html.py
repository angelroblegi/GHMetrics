Celulas = Input.CelulasIds
    .Distinct()
    .Select(id => new
    {
        CelulaId = id,
        PorcentajeParticipacion =
            Input.Porcentajes.TryGetValue(id, out var porcentaje)
                ? porcentaje
                : null
    })
