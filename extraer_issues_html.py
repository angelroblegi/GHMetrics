<div class="row g-3">
    @foreach (var cel in Model.CelulasDisponibles)
    {
        var seleccionada = Model.Input.CelulasIds.Contains(cel.Id);

        decimal? porcentaje = null;

        if (Model.Input.Porcentajes.TryGetValue(cel.Id, out var porcentajeGuardado))
        {
            porcentaje = porcentajeGuardado;
        }

        <div class="col-md-6">
            <div class="border rounded p-3">

                <div class="form-check mb-2">
                    <input class="form-check-input"
                           type="checkbox"
                           name="Input.CelulasIds"
                           value="@cel.Id"
                           id="cel_@cel.Id"
                           checked="@seleccionada" />

                    <label class="form-check-label fw-semibold"
                           for="cel_@cel.Id">
                        @cel.Nombre
                    </label>
                </div>

                <label class="form-label small mb-1">
                    Porcentaje de participación
                </label>

                <div class="input-group">
                    <input type="number"
                           class="form-control"
                           name="Input.Porcentajes[@cel.Id]"
                           value="@porcentaje"
                           min="0"
                           max="100"
                           step="0.01"
                           placeholder="0.00" />

                    <span class="input-group-text">%</span>
                </div>

            </div>
        </div>
    }
</div>

<span asp-validation-for="Input.CelulasIds"
      class="text-danger small"></span>
