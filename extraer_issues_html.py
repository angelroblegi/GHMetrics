Id	int	no	4	10   	0    	no	(n/a)	(n/a)	NULL
Cedula	nvarchar	no	60	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Nombre	nvarchar	no	200	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Apellido	nvarchar	no	200	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Email	nvarchar	no	400	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Telefono	nvarchar	no	40	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Celular	nvarchar	no	40	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Cargo	nvarchar	no	300	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Rol	nvarchar	no	200	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Tecnologia	nvarchar	no	200	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
NivelSeniority	nvarchar	no	100	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Capacidad	nvarchar	no	100	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Empresa	nvarchar	no	300	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Direccion	nvarchar	no	500	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Barrio	nvarchar	no	200	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
ContactoEmergenciaNombre	nvarchar	no	300	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
ContactoEmergenciaTelefono	nvarchar	no	40	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Estado	nvarchar	no	40	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
FechaIngreso	date	no	3	10   	0    	yes	(n/a)	(n/a)	NULL
FechaNacimiento	date	no	3	10   	0    	yes	(n/a)	(n/a)	NULL
Habilitado	bit	no	1	     	     	no	(n/a)	(n/a)	NULL
FotoUrl	nvarchar	no	1000	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Observaciones	nvarchar	no	-1	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
Activo	bit	no	1	     	     	no	(n/a)	(n/a)	NULL
FechaCreacion	datetime2	no	8	27   	7    	no	(n/a)	(n/a)	NULL
FechaModificacion	datetime2	no	8	27   	7    	yes	(n/a)	(n/a)	NULL
CreadoPor	nvarchar	no	900	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
ModificadoPor	nvarchar	no	900	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
HojaVidaContenido	varbinary	no	-1	     	     	yes	no	yes	NULL
HojaVidaContentType	nvarchar	no	200	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
HojaVidaFechaCarga	datetime2	no	8	27   	7    	yes	(n/a)	(n/a)	NULL
HojaVidaFechaExpiracion	datetime2	no	8	27   	7    	yes	(n/a)	(n/a)	NULL
HojaVidaNombreArchivo	nvarchar	no	520	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
MotivoDeshabilitacion	nvarchar	no	1000	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
FechaDeshabilitacion	datetime2	no	8	27   	7    	yes	(n/a)	(n/a)	NULL
Ciudad	nvarchar	no	200	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
HojaVidaBlobName	nvarchar	no	600	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
HojaVidaUrl	nvarchar	no	1000	     	     	yes	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
HabilidadesTecnicasJson	nvarchar	no	4000	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
RolesTecnicosJson	nvarchar	no	2000	     	     	no	(n/a)	(n/a)	SQL_Latin1_General_CP1_CI_AS
