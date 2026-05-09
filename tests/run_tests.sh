#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────────────────────
# run_tests.sh — Corre la suite de tests del ecosistema Data Analyst
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Data Analyst Ecosystem — Test Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Project dir: ${PROJECT_DIR}"
echo ""

# ── Detectar / activar virtualenv ────────────────────────────────────────────

if [ -n "${VIRTUAL_ENV:-}" ]; then
    echo "[✓] Virtualenv activo: ${VIRTUAL_ENV}"
elif [ -f "${PROJECT_DIR}/.venv/bin/activate" ]; then
    echo "[*] Activando .venv..."
    # shellcheck disable=SC1091
    source "${PROJECT_DIR}/.venv/bin/activate"
elif [ -f "${PROJECT_DIR}/venv/bin/activate" ]; then
    echo "[*] Activando venv..."
    # shellcheck disable=SC1091
    source "${PROJECT_DIR}/venv/bin/activate"
else
    echo "[!] No se encontró virtualenv. Usando Python del sistema."
fi

echo "   Python: $(python3 --version 2>&1)"
echo ""

# ── Verificar dependencias ──────────────────────────────────────────────────

echo "[*] Verificando dependencias..."

MISSING=""

if ! python3 -c "import pytest" 2>/dev/null; then
    MISSING="${MISSING} pytest"
fi

if ! python3 -c "import yaml" 2>/dev/null; then
    MISSING="${MISSING} pyyaml"
fi

if [ -n "${MISSING}" ]; then
    echo "[!] Faltan dependencias:${MISSING}"
    echo "    Instalando con pip..."
    pip install pytest pyyaml
    echo "[✓] Dependencias instaladas."
else
    echo "[✓] Todas las dependencias están instaladas."
fi

echo ""

# ── Verificar que el directorio tests/ existe ────────────────────────────────

if [ ! -d "${SCRIPT_DIR}" ]; then
    echo "[✗] Error: No se encuentra el directorio tests/ en ${SCRIPT_DIR}"
    exit 1
fi

# ── Correr tests ─────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Ejecutando pytest..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cd "${PROJECT_DIR}"

# Capturar errores de importación temprano
echo "[*] Verificando que los módulos se importan correctamente..."
python3 -c "
import sys
sys.path.insert(0, '${SCRIPT_DIR}')
try:
    import conftest
    print('[✓] conftest.py importado correctamente')
except Exception as e:
    print(f'[✗] Error importando conftest.py: {e}')
    sys.exit(1)
" || {
    echo ""
    echo "╔══════════════════════════════════════════════════╗"
    echo "║  ERROR: Falló la importación de conftest.py     ║"
    echo "║  Revisá que las rutas en las fixtures           ║"
    echo "║  apunten a los directorios correctos.           ║"
    echo "╚══════════════════════════════════════════════════╝"
    exit 1
}

echo ""

# Ejecutar pytest
# --tb=short: muestra tracebacks cortos
# -v: verbose
# --strict-markers: valida que los markers estén registrados en pytest.ini
exec python3 -m pytest "${SCRIPT_DIR}" -v --tb=short --strict-markers "$@"
