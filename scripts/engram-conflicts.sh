#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# engram-conflicts.sh
# Wrapper para Conflict Surfacing de Engram
#
# Uso:
#   engram-conflicts.sh scan [--semantic] [--project <name>]   → Escanear conflictos
#   engram-conflicts.sh list [--project <name>]                 → Listar conflictos
#   engram-conflicts.sh stats [--project <name>]                → Estadísticas
#   engram-conflicts.sh show <relation_id>                      → Detalle de un conflicto
#   engram-conflicts.sh judge <conflict_id> <verdict>           → Juzgar un conflicto
#   engram-conflicts.sh deferred [--status <s>] [--limit <n>]   → Conflictos diferidos
#   engram-conflicts.sh check                                    → Verificar soporte de Engram
#   engram-conflicts.sh help                                     → Mostrar ayuda
# ─────────────────────────────────────────────────────────────
set -euo pipefail

# ─── Colores ───
VERDE=$'\033[0;32m'
AMARILLO=$'\033[1;33m'
ROJO=$'\033[0;31m'
CYAN=$'\033[0;36m'
GRIS=$'\033[0;90m'
BOLD=$'\033[1m'
NC=$'\033[0m'

# ─── Constantes ───
SCRIPT_NAME="$(basename "$0")"
PROJECT_DEFAULT="data-analyst-ecosystem"

# ─── Help ───
ayuda() {
    cat <<EOF
${BOLD}engram-conflicts.sh${NC} — Conflict Surfacing para Engram

${BOLD}Uso:${NC}
  ${SCRIPT_NAME} scan [--semantic] [--project <name>]   Escanear conflictos
  ${SCRIPT_NAME} list [--project <name>]                 Listar conflictos
  ${SCRIPT_NAME} stats [--project <name>]                Estadísticas de conflictos
  ${SCRIPT_NAME} show <relation_id>                      Mostrar detalle de un conflicto
  ${SCRIPT_NAME} judge <conflict_id> <verdict>           Juzgar un conflicto
  ${SCRIPT_NAME} deferred [--status <s>] [--limit <n>]   Conflictos diferidos / pendientes
  ${SCRIPT_NAME} check                                    Verificar instalación de Engram
  ${SCRIPT_NAME} help                                     Mostrar esta ayuda

${BOLD}Verdictos disponibles:${NC}
  related, compatible, scoped, conflicts_with, supersedes, not_conflict

${BOLD}Ejemplos:${NC}
  ${SCRIPT_NAME} scan
  ${SCRIPT_NAME} scan --semantic --project data-analyst-ecosystem
  ${SCRIPT_NAME} list --project data-analyst-ecosystem
  ${SCRIPT_NAME} stats
  ${SCRIPT_NAME} show rel-abc123
  ${SCRIPT_NAME} judge rel-abc123 compatible

${BOLD}Documentación:${NC}
  docs/conflict-surfacing.md
EOF
}

# ─── Logging ───
log_info()  { echo -e "${VERDE}✔${NC} $*"; }
log_warn()  { echo -e "${AMARILLO}⚠${NC} $*"; }
log_error() { echo -e "${ROJO}✘${NC} $*"; }
log_step()  { echo -e "${CYAN}→${NC} $*"; }
log_raw()   { echo -e "$*"; }

# ─── Detectar proyecto ───
detectar_proyecto() {
    local proyecto

    # 1. Si se pasó --project, usar ese
    if [[ -n "${PROJECT_OVERRIDE:-}" ]]; then
        echo "$PROJECT_OVERRIDE"
        return
    fi

    # 2. Detectar desde git remote
    if git rev-parse --show-toplevel &>/dev/null 2>&1; then
        local remote_url
        remote_url="$(git remote get-url origin 2>/dev/null || true)"
        if [[ -n "$remote_url" ]]; then
            proyecto="$(basename -s .git "$remote_url" 2>/dev/null || true)"
            if [[ -n "$proyecto" ]]; then
                echo "$proyecto"
                return
            fi
        fi

        # Fallback: nombre del directorio raíz del repo
        proyecto="$(basename "$(git rev-parse --show-toplevel 2>/dev/null)")"
        if [[ -n "$proyecto" ]]; then
            echo "$proyecto"
            return
        fi
    fi

    # 3. Fallback: nombre del directorio actual
    proyecto="$(basename "$(pwd)")"
    echo "$proyecto"
}

# ─── Verificar Engram ───
check_engram() {
    log_step "Verificando Engram..."

    if ! command -v engram &>/dev/null; then
        log_error "Engram no está instalado."
        echo ""
        echo "   Instalalo con:"
        echo "     brew install gentleman-programming/tap/engram"
        echo "     go install github.com/Gentleman-Programming/engram/cmd/engram@latest"
        echo ""
        echo "   Más info: https://github.com/Gentleman-Programming/engram"
        return 1
    fi

    local version
    version="$(engram --version 2>/dev/null | head -1)"
    log_info "Engram detectado: ${CYAN}${version}${NC}"

    # Verificar que soporte conflicts
    if ! engram conflicts list --help &>/dev/null; then
        log_warn "Esta versión de Engram no soporta 'conflicts'."
        echo "   Actualizá con: brew update && brew upgrade engram"
        return 1
    fi
    log_info "Conflict Surfacing disponible"

    # Verificar DB
    if [[ ! -f ~/.engram/engram.db ]]; then
        log_warn "No se encuentra ~/.engram/engram.db"
        echo "   Puede que no haya memorias todavía o que Engram no se haya inicializado."
    else
        local db_size
        db_size="$(du -h ~/.engram/engram.db 2>/dev/null | cut -f1)"
        log_info "Base de datos: ${CYAN}~/.engram/engram.db${NC} (${db_size})"
    fi

    # Verificar ENGRAM_AGENT_CLI si se necesita --semantic
    if [[ -z "${ENGRAM_AGENT_CLI:-}" ]]; then
        log_warn "ENGRAM_AGENT_CLI no está seteado."
        echo "   Necesario para escaneo semántico. Ejemplo:"
        echo "     export ENGRAM_AGENT_CLI=opencode"
        echo "     export ENGRAM_AGENT_CLI=claude"
    else
        local cli_path
        cli_path="$(command -v "$ENGRAM_AGENT_CLI" 2>/dev/null || echo "no encontrado")"
        log_info "ENGRAM_AGENT_CLI=${CYAN}${ENGRAM_AGENT_CLI}${NC} (${cli_path})"
    fi

    return 0
}

# ─── Scan ───
cmd_scan() {
    local extra_args=()
    local proyecto

    proyecto="$(detectar_proyecto)"
    log_step "Escaneando conflictos en proyecto: ${CYAN}${proyecto}${NC}"

    if [[ -n "${SEMANTIC:-}" ]]; then
        log_info "Modo semántico activado (usa ${CYAN}ENGRAM_AGENT_CLI${NC})"
        extra_args+=(--semantic)
    fi

    # Dry-run primero para ver cuántos candidatos hay
    log_step "Dry-run: calculando candidatos..."
    engram conflicts scan --project "$proyecto" --dry-run "${extra_args[@]}" 2>&1

    echo ""
    log_warn "¿Aplicar los cambios? (y/N)"
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        log_info "Escaneo cancelado."
        return 0
    fi

    log_step "Aplicando escaneo..."
    engram conflicts scan --project "$proyecto" --apply "${extra_args[@]}" 2>&1
    log_info "Escaneo completado."
}

# ─── List ───
cmd_list() {
    local extra_args=()
    local proyecto

    proyecto="$(detectar_proyecto)"

    if [[ -n "${STATUS_FILTER:-}" ]]; then
        extra_args+=(--status "$STATUS_FILTER")
    fi
    if [[ -n "${LIMIT:-}" ]]; then
        extra_args+=(--limit "$LIMIT")
    fi

    log_step "Conflictos en proyecto: ${CYAN}${proyecto}${NC}"
    if [[ -n "${STATUS_FILTER:-}" ]]; then
        log_info "Filtro por estado: ${CYAN}${STATUS_FILTER}${NC}"
    fi
    echo ""

    engram conflicts list --project "$proyecto" "${extra_args[@]}" 2>&1
}

# ─── Stats ───
cmd_stats() {
    local proyecto
    proyecto="$(detectar_proyecto)"

    log_step "Estadísticas de conflictos: ${CYAN}${proyecto}${NC}"
    echo ""

    engram conflicts stats --project "$proyecto" 2>&1
}

# ─── Show ───
cmd_show() {
    local relation_id="$1"

    if [[ -z "$relation_id" ]]; then
        log_error "Falta el relation_id. Uso: ${SCRIPT_NAME} show <relation_id>"
        return 1
    fi

    log_step "Mostrando conflicto: ${CYAN}${relation_id}${NC}"
    echo ""

    engram conflicts show "$relation_id" 2>&1
}

# ─── Judge ───
cmd_judge() {
    local conflict_id="$1"
    local verdict="$2"

    if [[ -z "$conflict_id" ]]; then
        log_error "Falta el conflict_id. Uso: ${SCRIPT_NAME} judge <conflict_id> <verdict>"
        echo ""
        echo "   Verdictos válidos: related, compatible, scoped, conflicts_with, supersedes, not_conflict"
        return 1
    fi

    if [[ -z "$verdict" ]]; then
        log_error "Falta el veredicto. Uso: ${SCRIPT_NAME} judge <conflict_id> <verdict>"
        echo ""
        echo "   Verdictos válidos: related, compatible, scoped, conflicts_with, supersedes, not_conflict"
        return 1
    fi

    # Validar veredicto
    case "$verdict" in
        related|compatible|scoped|conflicts_with|supersedes|not_conflict)
            ;;
        *)
            log_error "Veredicto inválido: ${CYAN}${verdict}${NC}"
            echo "   Válidos: related, compatible, scoped, conflicts_with, supersedes, not_conflict"
            return 1
            ;;
    esac

    # Si el conflict_id no tiene prefijo "rel-", asumir que es un ID numérico
    if [[ "$conflict_id" =~ ^[0-9]+$ ]]; then
        log_step "Resolviendo conflict_id numérico ${conflict_id}... (usar rel-<sync_id> es más confiable)"
    fi

    log_step "Juzgando conflicto ${CYAN}${conflict_id}${NC} como ${BOLD}${verdict}${NC}"

    # Engram no tiene un "judge" directo en CLI; usamos mem_judge vía el MCP
    # pero mostramos el comando y las instrucciones al usuario/agente
    echo ""
    log_info "Para juzgar desde un agente, usá esta llamada MCP:"
    echo ""
    echo -e "   ${GRIS}mem_judge(judgment_id=\"${conflict_id}\", relation=\"${verdict}\")${NC}"
    echo ""
    log_warn "¿Estás corriendo desde un agente con acceso a mem_judge? (s/N)"
    read -r desde_agente
    if [[ "$desde_agente" == "s" || "$desde_agente" == "S" ]]; then
        log_info "Delegando el juicio al agente. Usá el comando MCP de arriba."
        return 0
    fi

    log_info "Como alternativa, también podés ignorar/confirmar desde Engram CLI:"
    echo ""
    echo "   Para ignorar este candidato (not_conflict):"
    echo "     engram conflicts deferred --replay --status pending"
    echo ""
    echo "   NOTA: el juicio directo se hace vía el MCP mem_judge,"
    echo "   no desde la CLI. Usá este wrapper desde un agente AI."
}

# ─── Deferred ───
cmd_deferred() {
    local extra_args=()
    local proyecto

    proyecto="$(detectar_proyecto)"

    if [[ -n "${STATUS_FILTER:-}" ]]; then
        extra_args+=(--status "$STATUS_FILTER")
    fi
    if [[ -n "${LIMIT:-}" ]]; then
        extra_args+=(--limit "$LIMIT")
    fi

    log_step "Conflictos diferidos en proyecto: ${CYAN}${proyecto}${NC}"
    echo ""

    engram conflicts deferred "${extra_args[@]}" 2>&1
}

# ═════════════════════════════════════════════════════════════
# Parseo de argumentos
# ═════════════════════════════════════════════════════════════

COMMAND=""
PROJECT_OVERRIDE=""
SEMANTIC=""
STATUS_FILTER=""
LIMIT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        scan|list|stats|show|judge|deferred|check|help)
            COMMAND="$1"
            shift
            ;;
        --project)
            PROJECT_OVERRIDE="$2"
            shift 2
            ;;
        --project=*)
            PROJECT_OVERRIDE="${1#*=}"
            shift
            ;;
        --semantic)
            SEMANTIC=1
            shift
            ;;
        --status)
            STATUS_FILTER="$2"
            shift 2
            ;;
        --status=*)
            STATUS_FILTER="${1#*=}"
            shift
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --limit=*)
            LIMIT="${1#*=}"
            shift
            ;;
        -*)
            log_error "Opción desconocida: $1"
            echo "   Usá '${SCRIPT_NAME} help' para ver las opciones disponibles."
            exit 1
            ;;
        *)
            # Argumentos posicionales se acumulan
            POSITIONAL_ARGS+=("$1")
            shift
            ;;
    esac
done

# ═════════════════════════════════════════════════════════════
# Ejecución
# ═════════════════════════════════════════════════════════════

case "$COMMAND" in
    scan)
        cmd_scan
        ;;
    list)
        cmd_list
        ;;
    stats)
        cmd_stats
        ;;
    show)
        cmd_show "${POSITIONAL_ARGS[0]:-}"
        ;;
    judge)
        cmd_judge "${POSITIONAL_ARGS[0]:-}" "${POSITIONAL_ARGS[1]:-}"
        ;;
    deferred)
        cmd_deferred
        ;;
    check)
        check_engram
        ;;
    help|"")
        ayuda
        ;;
    *)
        log_error "Comando desconocido: ${COMMAND}"
        echo "   Usá '${SCRIPT_NAME} help' para ver los comandos disponibles."
        exit 1
        ;;
esac
