DEFAULT on column FechaAsignacion	DF__CelulaMie__Fecha__73852659	(n/a)	(n/a)	(n/a)	(n/a)	(getutcdate())
FOREIGN KEY	FK_CelulaMiembros_Celula	Cascade	No Action	Enabled	Is_For_Replication	CelulaId
 	 	 	 	 	 	REFERENCES dateteamdb.dbo.Celulas (Id)
FOREIGN KEY	FK_CelulaMiembros_Consultor	No Action	No Action	Enabled	Is_For_Replication	ConsultorId
 	 	 	 	 	 	REFERENCES dateteamdb.dbo.Consultores (Id)
PRIMARY KEY (clustered)	PK_CelulaMiembros	(n/a)	(n/a)	(n/a)	(n/a)	Id
