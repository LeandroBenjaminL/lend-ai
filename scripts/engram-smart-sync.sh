#!/usr/bin/env bash
# ============================================================================
# Engram Smart Sync — Sincronización inteligente de memoria entre máquinas
# ============================================================================
# Uso:
#   engram-smart-sync push   → Subir tus cambios a git
#   engram-smart-sync pull   → Bajar cambios de otras máquinas
#   engram-smart-sync status → Ver estado
#   engram-smart-sync auto   → Pull + push automático
#
# Engram sigue funcionando exactamente igual. Este script solo coordina
# el sync vía git usando los chunks que genera `engram sync`.
# ============================================================================

set -uo pipefail

ENGRAM_DIR="$HOME/.engram"
GIT_MSG="sync engram $(date '+%Y-%m-%d %H:%M')"

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${CYAN}[info]${NC}    $*"; }
success() { echo -e "${GREEN}[ok]${NC}      $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC}    $*"; }
error()   { echo -e "${RED}[error]${NC}   $*" >&2; }

# ============================================================================
# Verificar que Engram CLI existe
# ============================================================================
check_engram() {
    if ! command -v engram &>/dev/null; then
        error "Engram CLI no encontrado. Instalalo primero."
        exit 1
    fi
}

# ============================================================================
# Verificar que ~/.engram es un repo git
# ============================================================================
check_git_repo() {
    if [ ! -d "${ENGRAM_DIR}/.git" ]; then
        error "~/.engram no es un repo git. Configurá el sync primero:"
        error "  cd ~/.engram && git init && git remote add origin <url>"
        exit 1
    fi
}

# ============================================================================
# PULL: Traer cambios de otras máquinas
# ============================================================================
cmd_pull() {
    info "📡 Smart Sync → PULL (trayendo memorias de otras máquinas)"

    cd "${ENGRAM_DIR}" || exit 1

    # 1. Git pull (trae chunks nuevos)
    if git pull --ff-only 2>&1; then
        success "Git: cambios remotos descargados"
    else
        warn "Git pull falló (sin conexión? sin cambios remotos?)"
        return 0
    fi

    # 2. Importar chunks nuevos al .db local
    if engram sync --import 2>&1; then
        success "Memorias importadas al .db local"
    else
        warn "No había chunks nuevos para importar"
    fi

    success "✅ PULL completado — tus memorias están al día"
}

# ============================================================================
# PUSH: Subir tus cambios a git
# ============================================================================
cmd_push() {
    info "📡 Smart Sync → PUSH (subiendo tus memorias)"

    cd "${ENGRAM_DIR}" || exit 1

    # 1. Exportar solo lo nuevo a chunks (--all para exportar TODOS los proyectos)
    info "Exportando memorias nuevas a chunks..."
    engram sync --all 2>&1 || {
        warn "engram sync no exportó nada nuevo (todo estaba sincronizado?)"
    }

    # 2. Agregar los chunks a git
    if [ -d ".engram" ]; then
        git add .engram/ 2>/dev/null || true
        if git diff --cached --quiet 2>/dev/null; then
            info "No hay cambios nuevos para subir"
            success "✅ PUSH — nada que subir, todo sincronizado"
            return 0
        fi
        git commit -m "${GIT_MSG}" 2>&1 || true
    fi

    # 3. Push a GitHub
    if git push 2>&1; then
        success "✅ Memorias subidas a GitHub"
    else
        error "❌ Push falló. Revisá conexión o permisos."
        return 1
    fi

    success "✅ PUSH completado — tus memorias están en la nube"
}

# ============================================================================
# STATUS: Ver estado del sync
# ============================================================================
cmd_status() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║   📡 Engram Smart Sync — Estado              ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo ""

    # Git status
    cd "${ENGRAM_DIR}" || exit 1
    echo -e "  ${CYAN}📁 Repo:${NC}      ${ENGRAM_DIR}"
    echo -e "  ${CYAN}🔗 Remote:${NC}    $(git remote get-url origin 2>/dev/null || echo 'no configurado')"
    echo ""

    # Git status resumido
    local ahead behind
    ahead=$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "0")
    behind=$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "0")
    echo -e "  ${CYAN}⬆ Por subir:${NC}  ${ahead} commits"
    echo -e "  ${CYAN}⬇ Por bajar:${NC}  ${behind} commits"
    echo ""

    # Engram sync status
    engram sync --status 2>&1 | tail -5
    echo ""

    # Chunks
    local chunk_count=0
    if [ -d ".engram/chunks" ]; then
        chunk_count=$(find .engram/chunks -type f 2>/dev/null | wc -l)
    fi
    echo -e "  ${CYAN}📦 Chunks:${NC}     ${chunk_count} archivos de sync"
    echo ""
}

# ============================================================================
# AUTO: Pull + Push (para usar al final del día)
# ============================================================================
cmd_auto() {
    info "🔄 Smart Sync → AUTO (pull + push completo)"
    echo ""
    cmd_pull
    echo ""
    cmd_push
    echo ""
    success "✅ AUTO completado — memorias sincronizadas"
}

# ============================================================================
# Ayuda
# ============================================================================
show_help() {
    cat <<EOF
📡 Engram Smart Sync — Sincronización inteligente de memoria

USO:
  engram-smart-sync push     Subir tus cambios a git
  engram-smart-sync pull     Bajar cambios de otras máquinas
  engram-smart-sync status   Ver estado del sync
  engram-smart-sync auto     Pull + push automático (para fin de sesión)

EJEMPLOS:
  # Antes de arrancar a trabajar (trae lo de la otra máquina):
  engram-smart-sync pull

  # Cuando terminás de trabajar (sube lo tuyo):
  engram-smart-sync push

  # Todo en uno:
  engram-smart-sync auto

REQUISITOS:
  - Engram CLI instalado
  - ~/.engram/ debe ser un repo git con remote configurado

Este script NO modifica cómo funciona Engram.
Solo usa 'engram sync' y 'engram sync --import' para coordinar con git.
EOF
}

# ============================================================================
# Main
# ============================================================================
main() {
    check_engram

    case "${1:-help}" in
        pull)   check_git_repo; cmd_pull ;;
        push)   check_git_repo; cmd_push ;;
        status) check_git_repo; cmd_status ;;
        auto)   check_git_repo; cmd_auto ;;
        help|--help|-h) show_help ;;
        *)
            error "Comando desconocido: $1"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
