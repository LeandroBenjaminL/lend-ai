---
description: Verificar estado del servidor Engram remoto (Tailscale + SSH + keepalive)
agent: devops
subtask: true
---

# /engram-server

Verificá que el servidor de Engram esté andando: Tailscale conectado, SSH respondiendo, keepalive activo.

## Uso

```
/engram-server              → chequeo completo
/engram-server status       → solo estado resumido
/engram-server tailscale    → solo conexión Tailscale
/engram-server ssh          → solo SSH server
/engram-server keepalive    → solo servicio keepalive
```

## FLUJO

1. **Tailscale**: verificá que `tailscale status` muestre la máquina servidora
2. **SSH**: conectate por SSH a la IP del servidor y ejecutá `echo OK`
3. **Keepalive**: verificá que `wsl-keepalive.service` esté activo en el servidor
4. **Engram**: ejecutá el wrapper remoto y verificá que responda con JSON

## CONFIG REFERENCIA

| Componente | Dónde |
|---|---|
| IP servidor | `100.94.219.17` |
| Clave SSH | `~/.ssh/engram-server` |
| Wrapper | `/home/leandro/.lend-ai/engram-wrapper.sh` |
| Keepalive | `wsl-keepalive.service` en systemd |
| DB | `~/.engram/engram.db` (WAL mode) |

## REGLAS

- No modifiques nada — solo verificá
- Mostrá ✅ / ❌ / ⚠️ para cada componente
- Si algo falla, mostrá el error crudo y sugerí cómo arreglarlo

## Ver también

- `/health` — chequeo general del ecosistema
- `engram-sync.md` — sincronización de memoria entre máquinas
