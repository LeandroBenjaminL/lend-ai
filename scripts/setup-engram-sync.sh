#!/bin/bash
# ─────────────────────────────────────────────────────────────
# setup-engram-sync.sh
# Sincroniza Engram entre PCs vía OneDrive (cloud sync)
#
# Uso:
#   ./scripts/setup-engram-sync.sh
#
# En cada PC:
#   1. Cloná/clonaste el repo (git clone ...)
#   2. Corré este script
#   3. Listo — ~/.engram apunta a OneDrive/engram-data/
#
# Si OneDrive no sincronizó el .db todavía, el script avisa.
# ─────────────────────────────────────────────────────────────
set -e

# ─── Colores ───
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # Sin color

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   Engram Sync — Configuración OneDrive   ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
echo ""

# ─── 1. Detectar Windows user ───
if command -v cmd.exe &> /dev/null; then
    WIN_USER=$(cmd.exe /c echo %USERNAME% 2>/dev/null | tr -d '\r\n')
elif command -v powershell.exe &> /dev/null; then
    WIN_USER=$(powershell.exe -Command '$env:USERNAME' 2>/dev/null | tr -d '\r\n')
else
    # Fallback: buscar en /mnt/c/Users/ el primer directorio no-sistema
    WIN_USER=""
    for d in /mnt/c/Users/*/; do
        d=$(basename "$d")
        case "$d" in
            "All Users"|"Default"|"Default User"|"Public"|"desktop.ini") continue ;;
            *) WIN_USER="$d"; break ;;
        esac
    done
fi

if [ -z "$WIN_USER" ]; then
    echo -e "${ROJO}❌ No se pudo detectar el usuario de Windows.${NC}"
    echo "   Buscá manualmente: ls /mnt/c/Users/"
    echo "   Y ajustá el symlink a mano:"
    echo "     ln -s /mnt/c/Users/TU_USER/OneDrive/engram-data ~/.engram"
    exit 1
fi

echo -e "${VERDE}✔${NC} Windows user detectado: ${CYAN}$WIN_USER${NC}"

# ─── 2. Buscar OneDrive ───
ONEDRIVE=""
for possible in \
    "/mnt/c/Users/$WIN_USER/OneDrive" \
    "/mnt/c/Users/$WIN_USER/OneDrive - Personal" \
    "/mnt/c/Users/$WIN_USER/OneDrive - Empresa" \
    "/mnt/c/Users/$WIN_USER/OneDrive/OneDrive" \
    "/mnt/c/Users/$WIN_USER/OneDrive - Corporativo"; do
    if [ -d "$possible" ]; then
        ONEDRIVE="$possible"
        break
    fi
done

if [ -z "$ONEDRIVE" ]; then
    echo -e "${ROJO}❌ No se encontró carpeta de OneDrive.${NC}"
    echo "   Verificá que OneDrive esté instalado y sincronizando en Windows."
    echo "   Después creá el symlink manualmente:"
    echo "     ln -s /mnt/c/Users/$WIN_USER/OneDrive/engram-data ~/.engram"
    exit 1
fi

echo -e "${VERDE}✔${NC} OneDrive encontrado: ${CYAN}$ONEDRIVE${NC}"
DATA_DIR="$ONEDRIVE/engram-data"

# ─── 3. Crear carpeta en OneDrive si no existe ───
mkdir -p "$DATA_DIR"
echo -e "${VERDE}✔${NC} Carpeta lista: ${CYAN}$DATA_DIR${NC}"

# ─── 4. Si ~/.engram existe y NO es symlink → backup ───
if [ -e ~/.engram ] && [ ! -L ~/.engram ]; then
    BACKUP="$HOME/.engram.local-backup"
    echo -e "${AMARILLO}⚠ Backup de ~/.engram existente → $BACKUP${NC}"
    mv ~/.engram "$BACKUP"
fi

# ─── 5. Si ya hay symlink, lo borramos y recreamos ───
[ -L ~/.engram ] && rm ~/.engram

# ─── 6. Crear symlink ───
ln -s "$DATA_DIR" ~/.engram
echo -e "${VERDE}✔${NC} Symlink creado: ${CYAN}~/.engram → $DATA_DIR${NC}"

# ─── 7. Verificar ───
echo ""
echo -e "${CYAN}📋 Verificación:${NC}"
ls -la ~/.engram/
echo ""

# ─── 8. Warn si el DB no está sincronizado ───
if [ ! -f "$DATA_DIR/engram.db" ]; then
    echo -e "${AMARILLO}⚠ Atención:${NC} OneDrive no sincronizó aún el archivo engram.db."
    echo "   Si esta PC YA tiene datos en Engram, se creará un DB nuevo."
    echo "   Esperá a que OneDrive termine de sincronizar y corré el script de nuevo."
    echo ""
    echo "   Si es la PRIMERA PC que configurás: ignorá este warning."
    echo "   El DB se creará automáticamente al usar opencode."
else
    echo -e "${VERDE}✅ Engram sync listo. El DB ya está sincronizado.${NC}"
fi

echo ""
echo -e "${VERDE}✔ Hecho. Reiniciá opencode para que tome el cambio.${NC}"
echo ""
