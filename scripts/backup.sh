#!/usr/bin/env bash
# ============================================================================
# backup.sh — Sistema de backup para Data-Analyst Ecosystem
# ============================================================================
# Crea snapshots automáticos del directorio de instalación antes de
# operaciones destructivas (install/sync/upgrade) y bajo demanda.
#
# Uso:
#   backup.sh create                    → Crear snapshot
#   backup.sh list                      → Listar backups
#   backup.sh restore <backup_name>     → Restaurar un backup
#   backup.sh pin <backup_name>         → Pinear backup (no se borra con prune)
#   backup.sh unpin <backup_name>       → Despinear
#   backup.sh prune                     → Forzar poda manual
# ============================================================================

set -euo pipefail

# ============================================================================
# Configuración
# ============================================================================

# El directorio de instalación del ecosistema
DATA_ANALYST_HOME="${DATA_ANALYST_HOME:-${HOME}/.data-analyst}"

# Donde se guardan los backups
BACKUP_DIR="${DATA_ANALYST_HOME}/backups"

# Cantidad de backups a conservar (los más viejos se borran)
KEEP_LAST=5

# Versión del ecosistema (se lee de git si está disponible, sino default)
ECOSYSTEM_VERSION="0.1.0"

# ============================================================================
# Colores (compatibles con install.sh)
# ============================================================================

setup_colors() {
    if [ -t 1 ] && [ "${TERM:-}" != "dumb" ]; then
        RED='\033[0;31m'
        GREEN='\033[0;32m'
        YELLOW='\033[1;33m'
        BLUE='\033[0;34m'
        CYAN='\033[0;36m'
        MAGENTA='\033[0;35m'
        BOLD='\033[1m'
        DIM='\033[2m'
        NC='\033[0m'
    else
        RED='' GREEN='' YELLOW='' BLUE='' CYAN='' MAGENTA='' BOLD='' DIM='' NC=''
    fi
}

setup_colors

# ============================================================================
# Logging
# ============================================================================

info()    { echo -e "${BLUE}[info]${NC}    $*"; }
success() { echo -e "${GREEN}[ok]${NC}      $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC}    $*"; }
error()   { echo -e "${RED}[error]${NC}   $*" >&2; }
fatal()   { error "$@"; exit 1; }
step()    { echo -e "\n${CYAN}${BOLD}==>${NC} ${BOLD}$*${NC}"; }

# ============================================================================
# Mostrar ayuda
# ============================================================================

show_help() {
    cat <<EOF
${BOLD}Data-Analyst Ecosystem — Sistema de Backup${NC}

Uso: backup.sh <comando> [argumentos]

Comandos:
  create                    Crear un snapshot del ecosistema
  list                      Listar todos los backups disponibles
  restore <backup_name>     Restaurar archivos desde un backup
  pin <backup_name>         Pinear un backup (no se borra con prune)
  unpin <backup_name>       Despinear un backup
  prune                     Forzar poda (borrar backups viejos no pineados)

Argumentos:
  backup_name    Nombre del backup (ej: backup-20260508-011246)
                 Se puede pasar con o sin extensión y path completo.

Ejemplos:
  backup.sh create
  backup.sh list
  backup.sh restore backup-20260508-011246
  backup.sh pin backup-20260508-011246.tar.gz
  backup.sh unpin backup-20260508-011246
  backup.sh prune

EOF
}

# ============================================================================
# Detectar versión del ecosistema
# ============================================================================

detect_version() {
    local git_dir="${DATA_ANALYST_HOME}/.git"
    if [ -d "$git_dir" ]; then
        local detected
        detected=$(git -C "${DATA_ANALYST_HOME}" describe --tags --always 2>/dev/null || true)
        if [ -n "$detected" ]; then
            ECOSYSTEM_VERSION="$detected"
            return
        fi
    fi
    if [ -f "${DATA_ANALYST_HOME}/VERSION" ]; then
        ECOSYSTEM_VERSION=$(tr -d ' \n' < "${DATA_ANALYST_HOME}/VERSION")
    fi
    # Si no hay nada, queda el default 0.1.0
}

# ============================================================================
# Calcular fingerprint del contenido actual
# ============================================================================
# Toma todos los archivos del source (excluyendo backups, .git, caches),
# calcula SHA256 de cada uno y genera un hash combinado.
# Esto permite detectar si hubo cambios desde el último backup.

compute_fingerprint() {
    local source_dir="$1"

    # Usar -prune para excluir directorios completos en cualquier nivel del árbol.
    # xargs puede devolver código 123 si algún sha256sum falla (permisos, binarios).
    # Por eso capturamos con || true para no romper set -euo pipefail.
    local fp
    fp=$(find "${source_dir}" \
        \( -name ".git" -prune \) -o \
        \( -name "node_modules" -prune \) -o \
        \( -name ".mypy_cache" -prune \) -o \
        \( -name ".ruff_cache" -prune \) -o \
        \( -name "__pycache__" -prune \) -o \
        \( -name "dist" -prune \) -o \
        \( -name "backups" -prune \) -o \
        -type f \
        -not -name "*.pyc" \
        -not -name ".DS_Store" \
        -not -name "*.pyo" \
        2>/dev/null \
        | sort \
        | xargs -d '\n' sha256sum 2>/dev/null \
        | sha256sum \
        | cut -d' ' -f1) || true
    echo "$fp"
}

# ============================================================================
# Obtener el fingerprint del último backup
# ============================================================================

get_last_fingerprint() {
    local last_backup
    last_backup=$(ls -t "${BACKUP_DIR}"/backup-*.tar.gz 2>/dev/null | head -1 || true)
    if [ -z "$last_backup" ]; then
        echo ""
        return
    fi

    tar -xzf "$last_backup" -C /tmp ./manifest.json 2>/dev/null || {
        echo ""
        return
    }

    if [ -f "/tmp/manifest.json" ]; then
        local fp
        fp=$(python3 -c "
import json
try:
    with open('/tmp/manifest.json') as f:
        m = json.load(f)
    print(m.get('fingerprint', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")
        rm -f /tmp/manifest.json
        echo "$fp"
    else
        echo ""
    fi
}

# ============================================================================
# Generar manifest.json con el listado de archivos y checksums
# ============================================================================

generate_manifest() {
    local source_dir="$1"
    local fingerprint="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    python3 -c "
import json, os, hashlib

source = os.path.expanduser('$source_dir')
backup_dir = os.path.expanduser('${BACKUP_DIR}')

# Directorios a excluir a cualquier nivel del árbol
EXCLUDE_DIRS = {
    '.git', 'node_modules', '.mypy_cache', '.ruff_cache',
    '__pycache__', 'dist', 'backups',
}
EXCLUDE_EXT = {'.pyc', '.pyo'}
EXCLUDE_FILES = {'.DS_Store'}

files = []
for root, dirs, fnames in os.walk(source):
    # Podar directorios excluidos in-place para que os.walk no entre
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

    # Verificar si estamos dentro del directorio de backups
    abs_root = os.path.abspath(root)
    if abs_root == backup_dir or abs_root.startswith(backup_dir + os.sep):
        continue

    for fname in sorted(fnames):
        if fname in EXCLUDE_FILES:
            continue
        ext = os.path.splitext(fname)[1].lower()
        if ext in EXCLUDE_EXT:
            continue
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, source)
        try:
            with open(fpath, 'rb') as f:
                chksum = hashlib.sha256(f.read()).hexdigest()
            fstat = os.stat(fpath)
            files.append({
                'path': relpath,
                'sha256': chksum,
                'size': fstat.st_size,
                'mode': oct(fstat.st_mode)[-3:]
            })
        except (OSError, IOError):
            pass

manifest = {
    'ecosystem': 'data-analyst-ecosystem',
    'version': '${ECOSYSTEM_VERSION}',
    'timestamp': '$timestamp',
    'fingerprint': '$fingerprint',
    'total_files': len(files),
    'files': files
}

print(json.dumps(manifest, indent=2))
"
}

# ============================================================================
# Comando: create — Crear un snapshot
# ============================================================================

cmd_create() {
    step "Creando backup del ecosistema"

    # Verificar que el directorio de instalación exista
    if [ ! -d "${DATA_ANALYST_HOME}" ]; then
        fatal "No se encuentra el directorio de instalación: ${DATA_ANALYST_HOME}"
    fi

    # Asegurar que el directorio de backups exista
    mkdir -p "${BACKUP_DIR}"

    # Detectar versión
    detect_version
    info "Versión detectada: ${ECOSYSTEM_VERSION}"

    # Calcular fingerprint del contenido actual
    info "Calculando checksum del contenido..."
    local fingerprint
    fingerprint="$(compute_fingerprint "${DATA_ANALYST_HOME}")"
    info "Fingerprint: ${fingerprint}"

    # Verificar dedup contra el último backup
    local last_fp
    last_fp="$(get_last_fingerprint)"
    if [ -n "$last_fp" ] && [ "$last_fp" = "$fingerprint" ]; then
        success "Sin cambios desde el último backup — no se crea duplicado"
        return 0
    fi

    # Generar nombre del backup
    local timestamp
    timestamp=$(date +%Y%m%d-%H%M%S)
    local backup_name="backup-${timestamp}"
    local backup_file="${BACKUP_DIR}/${backup_name}.tar.gz"

    info "Creando backup: ${backup_name}"

    # Generar manifest.json con la lista de archivos y checksums
    info "Generando manifiesto..."
    local manifest_file
    manifest_file=$(mktemp)
    generate_manifest "${DATA_ANALYST_HOME}" "${fingerprint}" > "${manifest_file}"

    # Copiar manifest al source dir con nombre temporal para incluirlo en el tar
    local manifest_src="${DATA_ANALYST_HOME}/.__backup_manifest_tmp__.json"
    cp "${manifest_file}" "${manifest_src}"

    # Crear el tar.gz en /tmp primero para evitar que tar se queje
    # de que el archivo de salida está dentro del source dir
    local tmp_archive
    tmp_archive=$(mktemp)
    info "Comprimiendo archivos..."

    pushd "${DATA_ANALYST_HOME}" > /dev/null

    tar czf "${tmp_archive}" \
        --exclude="backups" \
        --exclude=".git" \
        --exclude="node_modules" \
        --exclude=".mypy_cache" \
        --exclude=".ruff_cache" \
        --exclude="__pycache__" \
        --exclude="dist" \
        --exclude="*.pyc" \
        --exclude="*.pyo" \
        --exclude=".DS_Store" \
        --transform='s|.__backup_manifest_tmp__.json|manifest.json|' \
        . 2>/dev/null || {
        popd > /dev/null
        rm -f "${manifest_src}" "${manifest_file}" "${tmp_archive}"
        fatal "Error al crear el archivo tar.gz"
    }

    popd > /dev/null

    # Mover el archivo temp a su ubicación final
    mv "${tmp_archive}" "${backup_file}" 2>/dev/null || {
        rm -f "${manifest_src}" "${manifest_file}" "${tmp_archive}"
        fatal "Error al mover el backup a ${backup_file}"
    }

    # Limpiar archivos temporales
    rm -f "${manifest_src}" "${manifest_file}"

    if [ ! -f "${backup_file}" ]; then
        fatal "No se pudo crear el archivo de backup"
    fi

    local backup_size
    backup_size=$(du -h "${backup_file}" | cut -f1)
    success "Backup creado: ${backup_file} (${backup_size})"

    # Poda automática después de crear
    cmd_prune "silent"
}

# ============================================================================
# Comando: list — Listar backups
# ============================================================================

cmd_list() {
    step "Backups disponibles en ${BACKUP_DIR}"

    if [ ! -d "${BACKUP_DIR}" ]; then
        info "No hay directorio de backups todavía."
        info "Creá el primer backup con: backup.sh create"
        return 0
    fi

    # Usar array para evitar problemas con pipe
    local backups=()
    while IFS= read -r f; do
        backups+=("$f")
    done < <(ls -1 "${BACKUP_DIR}"/backup-*.tar.gz 2>/dev/null | sort -r || true)

    if [ ${#backups[@]} -eq 0 ]; then
        info "No hay backups disponibles."
        info "Creá el primer backup con: backup.sh create"
        return 0
    fi

    echo ""
    printf "  ${BOLD}%-30s %12s %8s  %s${NC}\n" "BACKUP" "FECHA" "TAMAÑO" "ESTADO"
    printf "  ${DIM}%-30s %12s %8s  %s${NC}\n"  "------" "-----" "------" "------"

    local count=0
    local pinned_count=0
    for backup in "${backups[@]}"; do
        count=$((count + 1))
        local name
        name=$(basename "${backup}" .tar.gz)
        local date_part="${name#backup-}"
        date_part="${date_part:0:8}"
        local formatted_date="${date_part:0:4}-${date_part:4:2}-${date_part:6:2}"
        local size
        size=$(du -h "${backup}" | cut -f1)

        if [ -f "${BACKUP_DIR}/${name}.pinned" ]; then
            pinned_count=$((pinned_count + 1))
            printf "  %-30s %12s %8s  ${GREEN}📌 pineado${NC}\n" "${name}" "${formatted_date}" "${size}"
        else
            printf "  %-30s %12s %8s\n" "${name}" "${formatted_date}" "${size}"
        fi
    done

    echo ""
    info "Total: ${count} backups (${pinned_count} pineados) | Retención: últimos ${KEEP_LAST} automáticos"
    echo ""
}

# ============================================================================
# Comando: restore — Restaurar desde un backup
# ============================================================================

cmd_restore() {
    local backup_name="${1:-}"

    if [ -z "$backup_name" ]; then
        error "Uso: backup.sh restore <backup_name>"
        info "Ejemplo: backup.sh restore backup-20260508-011246"
        info "Usá 'backup.sh list' para ver los disponibles."
        exit 1
    fi

    # Normalizar nombre: si no tiene extensión, agregarla
    local base_name
    base_name="$(basename "${backup_name%.tar.gz}")"
    local backup_file="${BACKUP_DIR}/${base_name}.tar.gz"

    if [ ! -f "$backup_file" ]; then
        error "No se encuentra el backup: ${backup_file}"
        info "Usá 'backup.sh list' para ver los disponibles."
        exit 1
    fi

    step "Restaurando desde: ${base_name}"

    # Extraer manifest.json para mostrar metadata
    local manifest_data
    manifest_data=$(tar -xzf "${backup_file}" -C /tmp ./manifest.json 2>/dev/null && cat /tmp/manifest.json 2>/dev/null || echo "")
    rm -f /tmp/manifest.json

    if [ -n "$manifest_data" ]; then
        local backup_version backup_timestamp backup_files
        backup_version=$(echo "$manifest_data" | python3 -c "
import json,sys
m=json.load(sys.stdin)
print(m.get('version','?'))
" 2>/dev/null || echo "?")
        backup_timestamp=$(echo "$manifest_data" | python3 -c "
import json,sys
m=json.load(sys.stdin)
print(m.get('timestamp','?'))
" 2>/dev/null || echo "?")
        backup_files=$(echo "$manifest_data" | python3 -c "
import json,sys
m=json.load(sys.stdin)
print(m.get('total_files','?'))
" 2>/dev/null || echo "?")
        echo ""
        echo -e "  ${BOLD}Manifiesto del backup:${NC}"
        echo -e "  Versión:    ${backup_version}"
        echo -e "  Fecha:      ${backup_timestamp}"
        echo -e "  Archivos:   ${backup_files}"
        echo ""
    fi

    # Preguntar confirmación
    echo -e "${YELLOW}⚠  Esto va a SOBREESCRIBIR los archivos actuales en ${DATA_ANALYST_HOME}${NC}"
    read -p "  ¿Estás seguro? (s/N): " confirm
    if [[ ! "$confirm" =~ ^[sS]$ ]]; then
        info "Restauración cancelada."
        return 0
    fi

    # Extraer a un directorio temporal primero
    info "Extrayendo archivos..."
    local temp_restore
    temp_restore=$(mktemp -d)

    tar -xzf "${backup_file}" -C "${temp_restore}" 2>/dev/null || {
        rm -rf "${temp_restore}"
        fatal "Error al extraer el backup. El archivo puede estar corrupto."
    }

    # Copiar archivos al installation dir (excluyendo manifest.json)
    info "Copiando archivos a ${DATA_ANALYST_HOME}..."
    if command -v rsync &>/dev/null; then
        rsync -a --delete --exclude='manifest.json' "${temp_restore}/" "${DATA_ANALYST_HOME}/" 2>/dev/null || {
            warn "rsync falló, usando cp como fallback..."
            find "${temp_restore}" -type f -not -name 'manifest.json' | while read -r f; do
                local relpath="${f#${temp_restore}/}"
                local dest="${DATA_ANALYST_HOME}/${relpath}"
                mkdir -p "$(dirname "${dest}")"
                cp "${f}" "${dest}"
            done
        }
    else
        find "${temp_restore}" -type f -not -name 'manifest.json' | while read -r f; do
            local relpath="${f#${temp_restore}/}"
            local dest="${DATA_ANALYST_HOME}/${relpath}"
            mkdir -p "$(dirname "${dest}")"
            cp "${f}" "${dest}"
        done
    fi

    rm -rf "${temp_restore}"
    success "Restauración completada en ${DATA_ANALYST_HOME}"
}

# ============================================================================
# Comando: pin — Pinear un backup para que no se borre con prune
# ============================================================================

cmd_pin() {
    local backup_name="${1:-}"

    if [ -z "$backup_name" ]; then
        error "Uso: backup.sh pin <backup_name>"
        info "Ejemplo: backup.sh pin backup-20260508-011246"
        exit 1
    fi

    local base_name
    base_name="$(basename "${backup_name%.tar.gz}")"
    local backup_file="${BACKUP_DIR}/${base_name}.tar.gz"
    local pin_file="${BACKUP_DIR}/${base_name}.pinned"

    if [ ! -f "$backup_file" ]; then
        error "No se encuentra el backup: ${backup_file}"
        info "Usá 'backup.sh list' para ver los disponibles."
        exit 1
    fi

    if [ -f "$pin_file" ]; then
        warn "El backup ya está pineado: ${base_name}"
        return 0
    fi

    touch "$pin_file"
    success "Backup pineado: ${base_name} (no se borrará con prune)"
}

# ============================================================================
# Comando: unpin — Despinear un backup
# ============================================================================

cmd_unpin() {
    local backup_name="${1:-}"

    if [ -z "$backup_name" ]; then
        error "Uso: backup.sh unpin <backup_name>"
        info "Ejemplo: backup.sh unpin backup-20260508-011246"
        exit 1
    fi

    local base_name
    base_name="$(basename "${backup_name%.tar.gz}")"
    local pin_file="${BACKUP_DIR}/${base_name}.pinned"

    if [ ! -f "$pin_file" ]; then
        warn "El backup no está pineado: ${base_name}"
        return 0
    fi

    rm -f "$pin_file"
    success "Backup despineado: ${base_name}"
}

# ============================================================================
# Comando: prune — Poda de backups viejos
# ============================================================================
# Mantiene solo los últimos KEEP_LAST backups NO pineados.
# Los backups pineados se conservan siempre.

cmd_prune() {
    local mode="${1:-}"

    if [ "$mode" != "silent" ]; then
        step "Podando backups viejos"
    fi

    if [ ! -d "${BACKUP_DIR}" ]; then
        [ "$mode" != "silent" ] && info "No hay directorio de backups."
        return 0
    fi

    # Listar backups NO pineados ordenados por fecha (más nuevo primero)
    local unpinned=()
    while IFS= read -r f; do
        unpinned+=("$f")
    done < <(for f in "${BACKUP_DIR}"/backup-*.tar.gz; do
        [ -f "$f" ] || continue
        local base
        base=$(basename "$f" .tar.gz)
        if [ ! -f "${BACKUP_DIR}/${base}.pinned" ]; then
            echo "$f"
        fi
    done 2>/dev/null | sort -r)

    local total=${#unpinned[@]}

    if [ "$total" -le "$KEEP_LAST" ]; then
        [ "$mode" != "silent" ] && success "No hay backups viejos para podar (${total}/${KEEP_LAST})"
        return 0
    fi

    # Los primeros KEEP_LAST se conservan, el resto se borra
    local deleted=0
    local i=0
    for b in "${unpinned[@]}"; do
        i=$((i + 1))
        if [ "$i" -le "$KEEP_LAST" ]; then
            continue
        fi
        local base
        base=$(basename "$b" .tar.gz)
        rm -f "$b" "${BACKUP_DIR}/${base}.pinned" 2>/dev/null || true
        deleted=$((deleted + 1))
        [ "$mode" != "silent" ] && info "  Eliminado: $(basename "$b")"
    done

    if [ "$mode" != "silent" ]; then
        success "Poda completa: ${deleted} backups eliminados, ${KEEP_LAST} conservados"
    fi
}

# ============================================================================
# Main
# ============================================================================

main() {
    local cmd="${1:-}"

    if [ -z "$cmd" ] || [ "$cmd" = "-h" ] || [ "$cmd" = "--help" ]; then
        show_help
        exit 0
    fi

    case "$cmd" in
        create)
            cmd_create
            ;;
        list)
            cmd_list
            ;;
        restore)
            cmd_restore "${2:-}"
            ;;
        pin)
            cmd_pin "${2:-}"
            ;;
        unpin)
            cmd_unpin "${2:-}"
            ;;
        prune)
            cmd_prune
            ;;
        *)
            error "Comando desconocido: ${cmd}"
            info "Usá 'backup.sh --help' para ver los comandos disponibles."
            exit 1
            ;;
    esac
}

main "$@"
