foreach (var cm in consultor.Celulas
    .Where(cm => !celulaIdsNuevas.Contains(cm.CelulaId))
    .ToList())
{
    _db.CelulaMiembros.Remove(cm);
}
