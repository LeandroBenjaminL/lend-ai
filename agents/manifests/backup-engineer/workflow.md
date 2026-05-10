# Backup Engineer — Workflow

1. Definir RPO (cuántos datos puedo perder) y RTO (cuánto tardo en recuperar)
2. Diseñar backup strategy según criticidad
3. Automatizar backups (cron, systemd timer)
4. Cifrar backups (gpg, age, s3 encryption)
5. Verificar backups periódicamente (restore test)
6. Documentar DRP paso a paso
7. Probar DR al menos 1 vez por trimestre
