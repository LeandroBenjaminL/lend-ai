# /chrome connect
_Conecta el Data-Analyst Agent a tu Google Chrome_

## ¿Para qué?

Cuando activás Chrome Debugging, el agente puede:
- Navegar a páginas web con **tus sesiones iniciadas**
- Tomar **screenshots** de lo que ves
- Hacer clic, llenar formularios, extraer datos
- Ejecutar JavaScript en la consola del browser
- Todo con TU Chrome, tus cookies, tus logins

## Cómo activarlo

### Paso 1 — Cerra todas las ventanas de Chrome

Asegurate de que Chrome esté completamente cerrado.

### Paso 2 — Abrí PowerShell y ejecutá:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="$env:TEMP\chrome-profile"
```

Chrome se va a abrir con una ventana nueva. **Dejala abierta.**

### Paso 3 — Verificá la conexión

En WSL (Linux), ejecutá:
```bash
curl http://localhost:9222/json/version
```

Si ves un JSON con info de Chrome → ✅ Conectado.

### Paso 4 — Usalo

Ahora cuando hables con Data-Analyst, podés pedirle things como:
- "Entrá a Gmail y mostrame los últimos 5 emails"
- "Andá a la página de Wikipedia de tal cosa y resumímela"
- "Tomá una screenshot de esta web y explicame qué veo"
- "Buscar esto en Google y contame los resultados"

## Troubleshooting

| Problema | Solución |
|----------|----------|
| `curl: connection refused` | Chrome no está corriendo con `--remote-debugging-port=9222` |
| `error: no such file or directory` | Cambiá la ruta de Chrome.exe si está en otro lado |
| Chrome no abre | Probá `"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"` |
| WSL no encuentra Windows | Probá con la IP de Windows: `http://172.x.x.1:9222` |

## Ver también
- [powershell.md](powershell.md) — más comandos para Windows
