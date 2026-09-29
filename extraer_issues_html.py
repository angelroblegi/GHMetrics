BEGIN TRANSACTION;

DECLARE @ConsultorId INT;

INSERT INTO dbo.Consultores
(
    Cedula,
    Nombre,
    Apellido,
    Email,
    Celular,
    Cargo,
    Rol,
    Empresa,
    Ciudad,
    FechaIngreso,
    FechaNacimiento,
    Direccion,
    Barrio,
    ContactoEmergenciaNombre,
    ContactoEmergenciaTelefono,
    Estado
)
VALUES
(
    'CEDULA',
    'NOMBRE',
    'APELLIDO',
    'EMAIL',
    'CELULAR',
    'CARGO',
    'ROL',
    'EMPRESA',
    'CIUDAD',
    '2025-02-10',
    '1999-10-05',
    'DIRECCION',
    'BARRIO',
    'CONTACTO',
    'TELEFONO_CONTACTO',
    'Activo'
);

SET @ConsultorId = SCOPE_IDENTITY();

INSERT INTO dbo.CelulaMiembros
(
    ConsultorId,
    CelulaId,
    PorcentajeParticipacion
)
VALUES
(
    @ConsultorId,
    3,
    100
);

COMMIT TRANSACTION;
