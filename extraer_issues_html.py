@page "{id:int}"
@model CommanCenter.Portal.Pages.DataTeam.DetalleConsultorModel
@{
    ViewData["Title"] = Model.PuedeEditar ? "Editar colaborador" : "Perfil del colaborador";
    var soloLectura = !Model.PuedeEditar;
    var consultor = Model.ConsultorActual;
    var mostrarRetencion = consultor is not null
        && !string.Equals(consultor.Estado, "Activo", StringComparison.OrdinalIgnoreCase)
        && consultor.HojaVidaFechaExpiracion.HasValue;
}

@section Styles {
    <style>
        .avatar-lg {
            width: 120px; height: 120px; border-radius: 50%;
            object-fit: cover; background: #6366f1;
            display: inline-flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 700; font-size: 2.2rem;
        }
    </style>
}

<div class="d-flex justify-content-between align-items-center mb-4">
    <h2 class="fw-bold mb-0">@ViewData["Title"]</h2>
    <a asp-page="/DataTeam/DirectorioColaboradores" class="btn btn-outline-secondary btn-sm">
        <i class="bi bi-arrow-left me-1"></i>Volver
    </a>
</div>

@if (!string.IsNullOrEmpty(Model.Error))
{
    <div class="alert alert-danger">@Model.Error</div>
}

@if (TempData["Success"] is string success && !string.IsNullOrWhiteSpace(success))
{
    <div class="alert alert-success">@success</div>
}

<div class="card shadow-sm">
    <div class="card-body">
        <form method="post" enctype="multipart/form-data" id="detalleConsultorForm">
            @Html.AntiForgeryToken()
            <input type="hidden" asp-for="Input.Id" />
            <input type="hidden" asp-for="Input.FotoUrl" />

            <div class="row g-3">
                <div class="col-12 text-center mb-2">
                    @if (!string.IsNullOrEmpty(Model.FotoUrlParaMostrar))
                    {
                        <img src="@Model.FotoUrlParaMostrar" alt="@Model.Input.Nombre" class="avatar-lg" />
                    }
                    else
                    {
                        <span class="avatar-lg">@(!string.IsNullOrWhiteSpace(Model.Input.Nombre) ? Model.Input.Nombre[0].ToString() : "?")</span>
                    }
                </div>

                <div class="col-12">
                    <div class="border rounded-3 p-3 bg-light">
                        <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                            <div>
                                <h6 class="fw-bold mb-1">Hoja de Vida (Capacidades)</h6>
                                <p class="text-muted small mb-2">Carga y descarga el PDF asociado al colaborador.</p>
                            </div>
                            @if (consultor?.TieneHojaVida == true)
                            {
                                <a asp-page-handler="DescargarHojaVida" asp-route-id="@Model.Id" class="btn btn-outline-primary btn-sm">
                                    <i class="bi bi-download me-1"></i>Descargar hoja de vida
                                </a>
                            }
                        </div>

                        @if (!string.IsNullOrEmpty(Model.HojaVidaError))
                        {
                            <div class="alert alert-danger py-2 mb-3">@Model.HojaVidaError</div>
                        }

                        <div class="small mb-2">
                            @if (consultor?.TieneHojaVida == true)
                            {
                                <div><span class="fw-semibold">Archivo actual:</span> @consultor.HojaVidaNombreArchivo</div>
                                <div><span class="fw-semibold">Fecha de carga:</span> @(consultor.HojaVidaFechaCarga?.ToString("dd/MM/yyyy HH:mm") ?? "-")</div>
                            }
                            else
                            {
                                <div class="text-muted">No hay hoja de vida cargada.</div>
                            }
                        </div>

                        @if (mostrarRetencion)
                        {
                            <div class="alert alert-warning py-2 mb-3">
                                <i class="bi bi-hourglass-split me-1"></i>
                                Disponible hasta: @consultor!.HojaVidaFechaExpiracion!.Value.ToString("dd/MM/yyyy")
                            </div>
                        }

                        @if (!soloLectura)
                        {
                            <div class="row g-2 align-items-end">
                                <div class="col-md-7">
                                    <label class="form-label mb-1">Seleccionar PDF</label>
                                    <input asp-for="HojaVidaPdf" id="hojaVidaPdfInput" type="file" class="form-control" accept=".pdf,application/pdf" />
                                    <div class="form-text">Solo PDF. Tamaño máximo recomendado: 10 MB.</div>
                                    <div id="hojaVidaClientError" class="text-danger small mt-1 d-none"></div>
                                </div>
                                <div class="col-md-5">
                                    <button type="submit" asp-page-handler="CargarHojaVida" id="btnCargarHojaVida" class="btn btn-primary w-100" formnovalidate>
                                        <span id="hojaVidaSpinner" class="spinner-border spinner-border-sm me-2 d-none" role="status" aria-hidden="true"></span>
                                        Cargar hoja de vida
                                    </button>
                                </div>
                            </div>
                        }
                    </div>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Cédula <span class="text-danger">*</span></label>
                    <input asp-for="Input.Cedula" class="form-control" required maxlength="30" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Cedula" class="text-danger small"></span>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Nombre <span class="text-danger">*</span></label>
                    <input asp-for="Input.Nombre" class="form-control" required maxlength="100" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Nombre" class="text-danger small"></span>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Apellido <span class="text-danger">*</span></label>
                    <input asp-for="Input.Apellido" class="form-control" required maxlength="100" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Apellido" class="text-danger small"></span>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Email <span class="text-danger">*</span></label>
                    <input asp-for="Input.Email" type="email" class="form-control" required readonly="@soloLectura" />
                    <span asp-validation-for="Input.Email" class="text-danger small"></span>
                </div>
                <div class="col-md-3">
                    <label class="form-label">Celular <span class="text-danger">*</span></label>
                    <input asp-for="Input.Celular" class="form-control" required maxlength="20" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Celular" class="text-danger small"></span>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Cargo <span class="text-danger">*</span></label>
                    <input asp-for="Input.Cargo" class="form-control" required maxlength="150" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Cargo" class="text-danger small"></span>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Empresa <span class="text-danger">*</span></label>
                    <input asp-for="Input.Empresa" class="form-control" required maxlength="150" readonly="@soloLectura" />
                    <span asp-validation-for="Input.Empresa" class="text-danger small"></span>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Estado <span class="text-danger">*</span></label>
                    <select asp-for="Input.Estado" class="form-select" disabled="@soloLectura">
                        <option value="Activo">Activo</option>
                        <option value="Retirado">Retirado</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Fecha de ingreso <span class="text-danger">*</span></label>
                    <input asp-for="Input.FechaIngreso" type="date" class="form-control" required readonly="@soloLectura" />
                    <span asp-validation-for="Input.FechaIngreso" class="text-danger small"></span>
                </div>
                <div class="col-md-4">
                    <label class="form-label">Fecha de nacimiento <span class="text-danger">*</span></label>
                    <input asp-for="Input.FechaNacimiento" type="date" class="form-control" required readonly="@soloLectura" />
                    <span asp-validation-for="Input.FechaNacimiento" class="text-danger small"></span>
                </div>
                <div class="col-md-8">
                    <label class="form-label">Dirección</label>
                    <input asp-for="Input.Direccion" class="form-control" maxlength="250" readonly="@soloLectura" />
                </div>
                <div class="col-md-4">
                    <label class="form-label">Barrio</label>
                    <input asp-for="Input.Barrio" class="form-control" maxlength="100" readonly="@soloLectura" />
                </div>
                <div class="col-md-4">
                    <label class="form-label">Ciudad</label>
                    <input asp-for="Input.Ciudad" class="form-control" maxlength="100" readonly="@soloLectura" />
                </div>
                <div class="col-md-6">
                    <label class="form-label">Contacto de emergencia (nombre)</label>
                    <input asp-for="Input.ContactoEmergenciaNombre" class="form-control" maxlength="150" readonly="@soloLectura" />
                </div>
                <div class="col-md-6">
                    <label class="form-label">Contacto de emergencia (teléfono)</label>
                    <input asp-for="Input.ContactoEmergenciaTelefono" class="form-control" maxlength="20" readonly="@soloLectura" />
                </div>

                <div class="col-12">
                    <label class="form-label">
                        Células <span class="text-danger">*</span>
                    </label>
                    @if (Model.CelulasDisponibles.Count == 0)
                    {
                        <div class="alert alert-warning py-2 small mb-0">No hay células disponibles.</div>
                    }
                    else if (soloLectura)
                    {
                        <div class="d-flex flex-wrap gap-2">
                            @foreach (var cel in Model.CelulasDisponibles.Where(x => Model.Input.CelulasIds.Contains(x.Id)))
                            {
                                <span class="badge text-dark" style="background:@cel.Color;">@cel.Nombre</span>
                            }
                        </div>
                    }
                    else
                    {
                        <div class="d-flex flex-wrap gap-3">
                            @foreach (var cel in Model.CelulasDisponibles)
                            {
                                <div class="form-check">
                                    <input class="form-check-input" type="checkbox" name="Input.CelulasIds"
                                           value="@cel.Id" id="cel_@cel.Id"
                                           checked="@Model.Input.CelulasIds.Contains(cel.Id)" />
                                    <label class="form-check-label" for="cel_@cel.Id">@cel.Nombre</label>
                                </div>
                            }
                        </div>
                        <span asp-validation-for="Input.CelulasIds" class="text-danger small"></span>
                    }
                </div>

                <div class="col-12">
                    <label class="form-label">Observaciones</label>
                    <textarea asp-for="Input.Observaciones" class="form-control" rows="2" readonly="@soloLectura"></textarea>
                </div>

                @if (!soloLectura)
                {
                    <div class="col-md-6">
                        <label class="form-label">Cambiar foto de perfil <span class="text-muted small">(opcional)</span></label>
                        <input asp-for="Foto" type="file" class="form-control" accept="image/*" />
                        <span class="text-muted small">JPG, PNG, GIF o WEBP. Máximo 5 MB.</span>
                    </div>
                }
            </div>

            @if (!soloLectura)
            {
                <div class="mt-4 d-flex gap-2">
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-check-lg me-1"></i>Guardar cambios
                    </button>
                    <a asp-page="/DataTeam/DirectorioColaboradores" class="btn btn-outline-secondary">Cancelar</a>
                </div>
            }
        </form>
    </div>
</div>

@section Scripts {
    <script>
        (function () {
            const form = document.getElementById("detalleConsultorForm");
            const input = document.getElementById("hojaVidaPdfInput");
            const btnCargar = document.getElementById("btnCargarHojaVida");
            const spinner = document.getElementById("hojaVidaSpinner");
            const error = document.getElementById("hojaVidaClientError");
            const maxBytes = 10 * 1024 * 1024;

            if (!form || !input || !btnCargar || !spinner || !error) return;

            function validarArchivo() {
                const file = input.files && input.files.length > 0 ? input.files[0] : null;
                if (!file) {
                    error.classList.add("d-none");
                    error.textContent = "";
                    return true;
                }

                const nombre = (file.name || "").toLowerCase();
                const esPdf = nombre.endsWith(".pdf");
                if (!esPdf) {
                    error.textContent = "Solo se permiten archivos PDF (.pdf).";
                    error.classList.remove("d-none");
                    return false;
                }

                if (file.size > maxBytes) {
                    error.textContent = "El archivo supera el tamaño máximo recomendado de 10 MB.";
                    error.classList.remove("d-none");
                    return false;
                }

                error.classList.add("d-none");
                error.textContent = "";
                return true;
            }

            input.addEventListener("change", validarArchivo);

            form.addEventListener("submit", function (event) {
                if (!event.submitter || event.submitter.id !== "btnCargarHojaVida") return;

                if (!validarArchivo()) {
                    event.preventDefault();
                    return;
                }

                btnCargar.disabled = true;
                spinner.classList.remove("d-none");
            });
        })();
    </script>
}
