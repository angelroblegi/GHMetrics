SET XACT_ABORT ON;

BEGIN TRY

    BEGIN TRANSACTION;

    ------------------------------------------------------------
    -- DATOS A CARGAR
    -- Cada fila representa UN consultor independiente.
    -- Los duplicados NO se agrupan.
    ------------------------------------------------------------

    DECLARE @Datos TABLE
    (
        RowNum INT IDENTITY(1,1),
        Cedula NVARCHAR(60),
        Nombre NVARCHAR(200),
        Apellido NVARCHAR(200),
        Email NVARCHAR(400),
        Celular NVARCHAR(40),
        Cargo NVARCHAR(300),
        Rol NVARCHAR(200),
        Empresa NVARCHAR(300),
        Ciudad NVARCHAR(200),
        FechaIngreso DATE,
        FechaNacimiento DATE,
        Direccion NVARCHAR(500),
        Barrio NVARCHAR(200),
        ContactoEmergenciaNombre NVARCHAR(300),
        ContactoEmergenciaTelefono NVARCHAR(40),
        Celula NVARCHAR(200),
        PorcentajeParticipacion DECIMAL(5,2),
        Estado NVARCHAR(40)
    );

    INSERT INTO @Datos
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
        Celula,
        PorcentajeParticipacion,
        Estado
    )
    VALUES

    -- 1
    (
        N'1085297237',
        N'Viviana Andrea',
        N'López Rodriguez',
        N'vlopez@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER TÉCNICO',
        N'PO Técnico',
        N'AEL',
        N'Santa Marta',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'MindShift',
        100,
        N'Activo'
    ),

    -- 2
    (
        N'779729',
        N'Cecilio Rafael de la Trinidad',
        N'Maraima Nava',
        N'ctrinidad@aportesenlinea.com',
        N'3234894092',
        N'ANALISTA III SCRUM MASTER',
        N'Agil Coach',
        N'MICHAEL PAGE',
        N'Sabaneta',
        '2023-08-17',
        '1974-05-03',
        N'CR35A, #77SUR-71. Torre 1, Apto.415. Fuente Clara',
        N'Lomas de San José.',
        N'Milagros Guerra',
        N'3142926978',
        N'Wakanda',
        50,
        N'Activo'
    ),

    -- 3
    (
        N'80075269',
        N'Saulo Ferney',
        N'Barbosa Pulido',
        N'sbarbosa@aportesenlinea.com',
        N'3102359084',
        N'COORDINADOR ARQUITECTO DE SOFTWARE',
        N'Arquitecto',
        N'AEL',
        N'Bogotá',
        '2019-11-01',
        NULL,
        N'Calle 92 # 11 - 32 Apt 304 Edificio Cervantes IV',
        N'Chicó Norte',
        NULL,
        NULL,
        N'MindShift',
        100,
        N'Activo'
    ),

    -- 4
    (
        N'52964246',
        N'Sandra Rocio',
        N'Tovar Avendano',
        N'stovar@aportesenlinea.com',
        NULL,
        N'DIRECTOR SERVICIOS ESPECIALIZADOS',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        '2008-08-11',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Enterprise Team',
        100,
        N'Activo'
    ),

    -- 5
    (
        N'80127568',
        N'Robert Ricardo',
        N'Ramirez Rojas',
        N'rramirez@aportesenlinea.com',
        NULL,
        N'GERENTE DE TRANSFORMACIÓN DIGITAL',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'DEVSECOPS',
        100,
        N'Activo'
    ),

    -- 6
    (
        N'1023026324',
        N'Paula Andrea',
        N'Rojas Suarez',
        N'gyc09705@aportesenlinea.com',
        NULL,
        N'ANALISTA II PRODUCT OWNER TÉCNICO',
        N'PO Técnico',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Wakanda',
        100,
        N'Activo'
    ),

    -- 7
    (
        N'52765886',
        N'Monica Astrid',
        N'Gutierrez Gutierrez',
        N'mgutierrez@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER TÉCNICO',
        N'PO Técnico',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Polaris Software Team',
        50,
        N'Activo'
    ),

    -- 8
    (
        N'52765886',
        N'Monica Astrid',
        N'Gutierrez Gutierrez',
        N'mgutierrez@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER TÉCNICO',
        N'PO Técnico',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Data Stargazers',
        50,
        N'Activo'
    ),

    -- 9
    (
        N'1033776027',
        N'Miguel Angel',
        N'Martinez Mendoza',
        N'mmartinez@aportesenlinea.com',
        NULL,
        N'ANALISTA II QA',
        N'QA',
        N'AEL',
        N'Bogotá',
        '2019-11-01',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Transversal Calidad',
        100,
        N'Activo'
    ),

    -- 10
    (
        N'1082843183',
        N'Karol Briyette',
        N'Rubiano Rojas',
        N'ebarros@aportesenlinea.com',
        NULL,
        N'DIRECTOR AGILISMO Y GESTION DEL CONOCIMIENTO',
        N'PO Funcional',
        N'AEL',
        N'Bogotá',
        '2019-11-01',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Aurora',
        50,
        N'Activo'
    ),

    -- 11
    (
        N'1014199932',
        N'David Guillermo',
        N'Peña',
        N'dpena@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER FUNCIONAL OPERACIONES',
        N'PO Funcional',
        N'AEL',
        N'Bogota',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Bon Voyage',
        100,
        N'Activo'
    ),

    -- 12
    (
        N'1022353132',
        N'Leidy Marcela',
        N'Franco Morales',
        N'lfranco@aportesenlinea.com',
        NULL,
        N'ANALISTA III INNOVACION Y PRODUCTIVIDAD',
        N'PO Funcional',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'DEVSECOPS',
        100,
        N'Activo'
    ),

    -- 13
    (
        N'1010215539',
        N'Laura Andrea',
        N'Avila',
        N'lavila@aportesenlinea.com',
        NULL,
        N'DIRECTOR DE INNOVACIÓN',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Maya',
        100,
        N'Activo'
    ),

    -- 14
    (
        N'80088963',
        N'Diego Guillermo',
        N'Montenegro Revelo',
        N'dmontenegro@aportesenlinea.com',
        NULL,
        N'GERENTE DE SOLUCIONES CLIENTES CORPORATIVOS',
        N'Sponsor',
        N'AEL',
        N'Bogota',
        '2014-12-15',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Bon Voyage',
        100,
        N'Activo'
    ),

    -- 15
    (
        N'1026288243',
        N'Juan Camilo',
        N'Hurtado Orjuela',
        N'jchurtado@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER FUNCIONAL SERVICIO',
        N'PO Funcional',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Wakanda',
        100,
        N'Activo'
    ),

    -- 16
    (
        N'1105786797',
        N'Leidy Johana',
        N'Ruiz Gutierrez',
        N'gyc06197@aportesenlinea.com',
        NULL,
        N'ANALISTA II QA',
        N'QA',
        N'AEL',
        N'Bogotá',
        '2018-12-03',
        '2025-12-06',
        NULL,
        NULL,
        NULL,
        NULL,
        N'Enterprise Team',
        100,
        N'Activo'
    ),

    -- 17
    (
        N'1053773898',
        N'Jhon James',
        N'Grisales Parra',
        N'jgrisales@aportesenlinea.com',
        N'3173669738',
        N'ANALISTA II INGENIERO DE DESARROLLO SEMI-SENIOR',
        N'Ingeniero',
        N'PERIFERIA IT',
        N'Dosquebradas',
        '2024-12-26',
        '1986-03-22',
        N'CRA 29 # 40A-134, Molivento 2, Torre 1, Apto 407',
        N'VILLAVENTO',
        N'DIEGO GRISALES',
        N'3148114563',
        N'Data Stargazers',
        50,
        N'Activo'
    ),

    -- 18
    (
        N'1030569638',
        N'Ismael',
        N'Ruiz Ovalle',
        N'iruizo@aportesenlinea.com',
        NULL,
        N'ANALISTA III SOPORTE',
        N'PO Funcional',
        N'AEL',
        N'bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Polaris Software Team',
        100,
        N'Activo'
    ),

    -- 19
    (
        N'52414874',
        N'Ingrid Milena',
        N'Manrique Porras',
        N'imanrique@aportesenlinea.com',
        NULL,
        N'GERENTE DE SERVICIOS',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        '2020-05-11',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'MindShift',
        100,
        N'Activo'
    ),

    -- 20
    (
        N'79568718',
        N'Hugo',
        N'Bermudez Diaz',
        N'hbermudez@aportesenlinea.com',
        N'3013685229',
        N'COORDINADOR ARQUITECTO DE DATOS',
        N'Arquitecto',
        N'AEL',
        N'Bogotá',
        '2022-02-07',
        NULL,
        N'Calle 148 No. 94 A 60 Apto 710',
        N'La Campiña',
        NULL,
        NULL,
        N'Enterprise Team',
        50,
        N'Activo'
    ),

    -- 21
    (
        N'79568718',
        N'Hugo',
        N'Bermudez Diaz',
        N'hbermudez@aportesenlinea.com',
        N'3013685229',
        N'COORDINADOR ARQUITECTO DE DATOS',
        N'Arquitecto',
        N'AEL',
        N'Bogotá',
        '2022-02-07',
        NULL,
        N'Calle 148 No. 94 A 60 Apto 710',
        N'La Campiña',
        NULL,
        NULL,
        N'Wakanda',
        50,
        N'Activo'
    ),

    -- 22
    (
        N'1072666410',
        N'Esneider',
        N'Gualtero Hernández',
        N'egualtero@aportesenlinea.com',
        N'3118003660',
        N'ANALISTA III SCRUM MASTER',
        N'Scrum Master',
        N'AEL',
        N'Bogotá',
        '2019-11-01',
        '2023-07-25',
        N'calle 59 # 13-30 Torre norte apto 1401',
        N'Chapinero Central',
        NULL,
        NULL,
        N'Maya',
        50,
        N'Activo'
    ),

    -- 23
    (
        N'80127568',
        N'Robert Ricardo',
        N'Ramirez Rojas',
        N'rramirez@aportesenlinea.com',
        NULL,
        N'GERENTE DE TRANSFORMACIÓN DIGITAL',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Aurora',
        100,
        N'Activo'
    ),

    -- 24
    (
        N'80088963',
        N'Diego Guillermo',
        N'Montenegro Revelo',
        N'dmontenegro@aportesenlinea.com',
        NULL,
        N'GERENTE DE SOLUCIONES CLIENTES CORPORATIVOS',
        N'Sponsor',
        N'AEL',
        N'Bogota',
        '2014-12-15',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Data Stargazers',
        100,
        N'Activo'
    ),

    -- 25
    (
        N'53006451',
        N'Diana Milena',
        N'Saavedra Ferrer',
        N'dsaavedra@aportesenlinea.com',
        NULL,
        N'ANALISTA III GESTION DE PRODUCTO',
        N'PO Técnico',
        N'AEL',
        N'Bogota',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Enterprise Team',
        100,
        N'Activo'
    ),

    -- 26
    (
        N'1012403476',
        N'David Fernando',
        N'Delgado Guacaneme',
        N'gyc03252@aportesenlinea.com',
        NULL,
        N'ANALISTA II ASEGURAMIENTO DE CALIDAD SEMI SENIOR',
        N'QA',
        N'AEL',
        N'Cali',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Wakanda',
        100,
        N'Activo'
    ),

    -- 27
    (
        N'1026294015',
        N'Harold Steven',
        N'Lopez Rubio',
        N'hlopez@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER FUNCIONAL SERVICIO',
        N'PO Funcional',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'MindShift',
        100,
        N'Activo'
    ),

    -- 28
    (
        N'1023900544',
        N'Daniel Fernando',
        N'Parra',
        N'dparra@aportesenlinea.com',
        NULL,
        N'ANALISTA II INGENIERO DE CALIDAD Y AUTOMATIZACIÓN SEMI-SENIOR',
        N'Ingeniero',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Transversal Calidad',
        100,
        N'Activo'
    ),

    -- 29
    (
        N'1032458577',
        N'Cristhian David',
        N'Amezquita Castro',
        N'camezquita@aportesenlinea.com',
        NULL,
        N'COORDINADOR QA Y DEVSECOPS',
        N'Coordinador',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'DEVSECOPS',
        100,
        N'Activo'
    ),

    -- 30
    (
        N'1022355992',
        N'Cesar Augusto',
        N'Pachon Porras',
        N'cpachon@aportesenlinea.com',
        NULL,
        N'COORDINADOR DE DESARROLLO DE NEGOCIO',
        N'PO Funcional',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Data Stargazers',
        100,
        N'Activo'
    ),

    -- 31
    (
        N'1128417080',
        N'Cesar Adelmo',
        N'Muñoz Henao',
        N'cahenao@aportesenlinea.com',
        NULL,
        N'ANALISTA III PRODUCT OWNER FUNCIONAL SERVICIO',
        N'PO Funcional',
        N'AEL',
        N'Medellin',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Enterprise Team',
        100,
        N'Activo'
    ),

    -- 32
    (
        N'52533807',
        N'Angela María',
        N'Juyó Rondón',
        N'ajuyo@aportesenlinea.com',
        NULL,
        N'COORDINADOR OPERACIONES TI',
        N'StakeHolder Operaciones TI',
        N'AEL',
        N'Cartagena',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Polaris Software Team',
        100,
        N'Activo'
    ),

    -- 33
    (
        N'1020713148',
        N'Maria Kamila',
        N'Redondo Gordillo',
        N'mredondo@aportesenlinea.com',
        NULL,
        N'DIRECTOR SERVICIOS DE CONTACTO',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Wakanda',
        100,
        N'Activo'
    ),

    -- 34
    (
        N'79694723',
        N'Alexander',
        N'Castro Morales',
        N'acastro@aportesenlinea.com',
        NULL,
        N'DIRECTOR DE DESARROLLO',
        N'Director',
        N'AEL',
        N'Bogotá',
        '2023-04-10',
        '2023-07-12',
        NULL,
        NULL,
        NULL,
        NULL,
        N'Direccion Desarrollo',
        50,
        N'Activo'
    ),

    -- 35
    (
        N'80127568',
        N'Robert Ricardo',
        N'Ramirez Rojas',
        N'rramirez@aportesenlinea.com',
        NULL,
        N'GERENTE DE TRANSFORMACIÓN DIGITAL',
        N'Sponsor',
        N'AEL',
        N'Bogotá',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        N'Nova',
        100,
        N'Activo'
    ),

    -- 36
    (
        N'1019075102',
        N'Alejandra',
        N'Xiomara Jimenez',
        N'ajimenez@aportesenlinea.com',
        N'301 488 8581',
        N'ANALISTA III SCRUM MASTER',
        N'Scrum Master',
        N'SOPHOS',
        N'Bello',
        NULL,
        '1992-10-03',
        N'Diagonal 54 # 17 – 100, apto 1230',
        N'Poblado niquia',
        NULL,
        NULL,
        N'Data Stargazers',
        50,
        N'Activo'
    ),

    -- 37
    (
        N'1070004328',
        N'Kenneth Daniel',
        N'Valderrama Parra',
        N'kvalderrama@aportesenlinea.com',
        N'3102307476',
        N'ANALISTA II QA',
        N'QA',
        N'SQA',
        N'Cajicá',
        NULL,
        '1986-04-05',
        N'Carrera 6 #5 - 87 sur',
        N'El Prado',
        NULL,
        N'3103740269',
        N'Enterprise Team',
        100,
        N'Activo'
    ),

    -- 38
    (
        N'103792318',
        N'Stiven',
        N'Londoño Agudelo',
        N'slondono@aportesenlinea.com',
        N'3117791672',
        N'COORDINADOR ARQUITECTO DE SOFTWARE',
        N'Arquitecto',
        N'SOPHOS',
        N'Envigado',
        '2026-06-09',
        '1988-12-25',
        N'Calle 40A sur #24B 105',
        N'La Mina',
        N'Catalina Acevedo Montoya',
        N'3105064745',
        N'Polaris Software Team',
        50,
        N'Activo'
    );


    ------------------------------------------------------------
    -- VARIABLES PARA RECORRER CADA FILA
    ------------------------------------------------------------

    DECLARE
        @RowNum INT,
        @Cedula NVARCHAR(60),
        @Nombre NVARCHAR(200),
        @Apellido NVARCHAR(200),
        @Email NVARCHAR(400),
        @Celular NVARCHAR(40),
        @Cargo NVARCHAR(300),
        @Rol NVARCHAR(200),
        @Empresa NVARCHAR(300),
        @Ciudad NVARCHAR(200),
        @FechaIngreso DATE,
        @FechaNacimiento DATE,
        @Direccion NVARCHAR(500),
        @Barrio NVARCHAR(200),
        @ContactoEmergenciaNombre NVARCHAR(300),
        @ContactoEmergenciaTelefono NVARCHAR(40),
        @Celula NVARCHAR(200),
        @PorcentajeParticipacion DECIMAL(5,2),
        @Estado NVARCHAR(40),
        @ConsultorId INT,
        @CelulaId INT;


    ------------------------------------------------------------
    -- CURSOR
    -- Cada fila del Excel se convierte en un Consultor NUEVO.
    ------------------------------------------------------------

    DECLARE cur_consultores CURSOR LOCAL FAST_FORWARD FOR
        SELECT
            RowNum,
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
            Celula,
            PorcentajeParticipacion,
            Estado
        FROM @Datos
        ORDER BY RowNum;


    OPEN cur_consultores;

    FETCH NEXT FROM cur_consultores INTO
        @RowNum,
        @Cedula,
        @Nombre,
        @Apellido,
        @Email,
        @Celular,
        @Cargo,
        @Rol,
        @Empresa,
        @Ciudad,
        @FechaIngreso,
        @FechaNacimiento,
        @Direccion,
        @Barrio,
        @ContactoEmergenciaNombre,
        @ContactoEmergenciaTelefono,
        @Celula,
        @PorcentajeParticipacion,
        @Estado;


    WHILE @@FETCH_STATUS = 0
    BEGIN

        --------------------------------------------------------
        -- BUSCAR ID DE LA CÉLULA POR NOMBRE
        --------------------------------------------------------

        SELECT @CelulaId = Id
        FROM dbo.Celulas
        WHERE LTRIM(RTRIM(Nombre)) = LTRIM(RTRIM(@Celula));

        IF @CelulaId IS NULL
        BEGIN
            THROW 50001,
                'No se encontró la célula especificada para una de las filas.',
                1;
        END;


        --------------------------------------------------------
        -- INSERTAR CONSULTOR
        --------------------------------------------------------

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
            @Cedula,
            @Nombre,
            @Apellido,
            @Email,
            @Celular,
            @Cargo,
            @Rol,
            @Empresa,
            @Ciudad,
            @FechaIngreso,
            @FechaNacimiento,
            @Direccion,
            @Barrio,
            @ContactoEmergenciaNombre,
            @ContactoEmergenciaTelefono,
            @Estado
        );


        SET @ConsultorId = SCOPE_IDENTITY();


        --------------------------------------------------------
        -- INSERTAR RELACIÓN CON LA CÉLULA
        --------------------------------------------------------

        INSERT INTO dbo.CelulaMiembros
        (
            ConsultorId,
            CelulaId,
            PorcentajeParticipacion
        )
        VALUES
        (
            @ConsultorId,
            @CelulaId,
            @PorcentajeParticipacion
        );


        PRINT
            'Fila ' + CAST(@RowNum AS VARCHAR(10)) +
            ' cargada. ConsultorId = ' + CAST(@ConsultorId AS VARCHAR(20)) +
            ', Célula = ' + @Celula +
            ', CelulaId = ' + CAST(@CelulaId AS VARCHAR(20));


        FETCH NEXT FROM cur_consultores INTO
            @RowNum,
            @Cedula,
            @Nombre,
            @Apellido,
            @Email,
            @Celular,
            @Cargo,
            @Rol,
            @Empresa,
            @Ciudad,
            @FechaIngreso,
            @FechaNacimiento,
            @Direccion,
            @Barrio,
            @ContactoEmergenciaNombre,
            @ContactoEmergenciaTelefono,
            @Celula,
            @PorcentajeParticipacion,
            @Estado;

    END;


    CLOSE cur_consultores;
    DEALLOCATE cur_consultores;


    ------------------------------------------------------------
    -- SI TODO SALIÓ BIEN, CONFIRMAR
    ------------------------------------------------------------

    COMMIT TRANSACTION;

    PRINT '==============================================';
    PRINT 'CARGA COMPLETADA CORRECTAMENTE';
    PRINT '38 registros de Consultores procesados.';
    PRINT '==============================================';


END TRY
BEGIN CATCH

    IF CURSOR_STATUS('local', 'cur_consultores') >= 0
        CLOSE cur_consultores;

    IF CURSOR_STATUS('local', 'cur_consultores') >= -1
        DEALLOCATE cur_consultores;

    IF XACT_STATE() <> 0
        ROLLBACK TRANSACTION;

    PRINT '==============================================';
    PRINT 'ERROR EN LA CARGA';
    PRINT '==============================================';
    PRINT 'Mensaje: ' + ERROR_MESSAGE();
    PRINT 'Línea: ' + CAST(ERROR_LINE() AS VARCHAR(20));
    PRINT '==============================================';

    THROW;

END CATCH;
