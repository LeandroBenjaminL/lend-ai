# Backup Engineer — Patterns

### 3-2-1 Rule
- 3 copias de los datos
- 2 medios diferentes (ej: disco + cloud)
- 1 copia offsite

### PostgreSQL backup
```bash
# Full backup diario
pg_dump -Fc -Z 9 mydb > /backups/db_$(date +%Y%m%d).dump

# WAL archiving (point-in-time recovery)
archive_command = 'cp %p /backups/wal/%f'
```

### Restic backup script
```bash
restic backup /data --repo s3:backups/prod
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6
restic prune
```

### DRP checkboxes
- [ ] RPO definido (ej: 1 hora)
- [ ] RTO definido (ej: 4 horas)
- [ ] Backups automáticos funcionando
- [ ] Restore test < 30 días
- [ ] DRP documentado
- [ ] Contactos de emergencia actualizados
