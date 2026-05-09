#!/usr/bin/env bash
# ============================================================================
# Lend.Ai — Install Script
# Ecosistema unificado de agentes AI: Data Analysis + Frontend Development
#
# Usage:
#   curl -sL https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh | bash
#
# Or download and run:
#   curl -sLO https://raw.githubusercontent.com/LeandroBenjaminL/lend-ai/main/install.sh
#   chmod +x install.sh
#   ./install.sh [OPTIONS]
# ============================================================================

set -euo pipefail

# ============================================================================
# Configuración
# ============================================================================

GITHUB_OWNER="LeandroBenjaminL"
GITHUB_REPO="lend-ai"
GITHUB_BRANCH="main"
INSTALL_DIR="${LEND_AI_HOME:-${HOME}/.lend-ai}"
INSTALL_METHOD="auto"
INSTALL_VERSION="latest"
DEFAULT_ENGRAM_PORT="7437"

# ============================================================================
# Colores
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

# ============================================================================
# Logging
# ============================================================================

info()    { echo -e "${BLUE}[info]${NC}    $*"; }
success() { echo -e "${GREEN}[ok]${NC}      $*"; }
warn()    { echo -e "${YELLOW}[warn]${NC}    $*"; }
error()   { echo -e "${RED}[error]${NC}   $*" >&2; }

fatal() {
    error "$@"
    if [ "${GENTLEMAN_MODE:-true}" = "true" ]; then
        echo ""
        read -p "  ¿Querés salir del instalador? (s/N): " confirm
        if [ "$confirm" = "s" ] || [ "$confirm" = "S" ]; then
            exit 1
        else
            warn "Continuando de todos modos (modo Gentleman)..."
            return 1
        fi
    else
        exit 1
    fi
}

step()    { echo -e "\n${CYAN}${BOLD}==>${NC} ${BOLD}$*${NC}"; }
substep() { echo -e "  ${CYAN}>${NC} $*"; }

# ============================================================================
# Help
# ============================================================================

show_help() {
    cat <<EOF
${BOLD}Lend.Ai — Installer${NC}

Uso: install.sh [OPCIONES]

Opciones:
  --method M    Método: auto (default), git
  --dir DIR     Directorio de instalación (default: ~/.lend-ai)
  --branch BR   Rama de GitHub (default: main)
  -h, --help    Mostrar esta ayuda

Ejemplos:
  curl -sL https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/main/install.sh | bash
  ./install.sh
  ./install.sh --dir ~/mis-agentes
  ./install.sh --branch develop

EOF
}

# ============================================================================
# Banner
# ============================================================================

print_banner() {
    echo ""
    echo -e "${CYAN}${BOLD}"
    echo "   ╔═══════════════════════════════════════════════╗"
    echo "   ║                                               ║"
    echo "   ║   _      _        _        _    ___   ___     ║"
    echo "   ║  | |    | |      | |      / \  |_ _| |_ _|    ║"
    echo "   ║  | |    | |      | |     / _ \  | |   | |     ║"
    echo "   ║  | |___ | |___   | |___ / ___ \ | |   | |     ║"
    echo "   ║  |_____||_____|  |_____/_/   \_\___| |___|    ║"
    echo "   ║                                               ║"
    echo "   ║   Data Analysis  +  Frontend Development      ║"
    echo "   ╚═══════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo -e "  ${DIM}Lend.Ai — Ecosistema unificado de agentes AI${NC}"
    echo -e "  ${DIM}${GITHUB_OWNER}/${GITHUB_REPO}${NC}"
    echo ""
}

# ============================================================================
# Plataforma
# ============================================================================

detect_platform() {
    local uname_os uname_arch

    uname_os="$(uname -s)"
    uname_arch="$(uname -m)"

    case "$uname_os" in
        Darwin) OS="macos"; OS_LABEL="macOS" ;;
        Linux)  OS="linux"; OS_LABEL="Linux" ;;
        *)      fatal "OS no soportado: $uname_os. Solo macOS y Linux." ;;
    esac

    if [ -f /proc/version ] && grep -qi microsoft /proc/version 2>/dev/null; then
        OS="wsl"
        OS_LABEL="WSL (Windows Subsystem for Linux)"
    fi

    case "$uname_arch" in
        x86_64|amd64)  ARCH="x86_64"; ARCH_LABEL="x86_64 (amd64)" ;;
        aarch64|arm64) ARCH="arm64";  ARCH_LABEL="arm64" ;;
        *)             ARCH="$uname_arch"; ARCH_LABEL="$uname_arch" ;;
    esac

    success "Plataforma: ${OS_LABEL} | Arquitectura: ${ARCH_LABEL}"
}

# ============================================================================
# Prerequisitos
# ============================================================================

check_prerequisites() {
    step "Verificando prerequisitos (Modo Gentleman)"

    local missing=()
    local warnings=0

    if ! command -v git &>/dev/null; then
        missing+=("git")
    fi

    if ! command -v curl &>/dev/null; then
        missing+=("curl")
    fi

    if ! command -v python3 &>/dev/null; then
        warn "python3 no encontrado — algunas funciones no estarán disponibles"
        warnings=$((warnings + 1))
    fi

    if ! command -v pip3 &>/dev/null; then
        if python3 -m pip --version &>/dev/null 2>&1; then
            alias pip3="python3 -m pip"
            success "pip3 disponible via python3 -m pip"
        else
            warn "pip3 no encontrado — no se instalarán dependencias Python"
            warnings=$((warnings + 1))
        fi
    else
        success "pip3 disponible"
    fi

    if ! command -v node &>/dev/null; then
        warn "Node.js no encontrado — MCPs via npx no funcionarán"
        warnings=$((warnings + 1))
    else
        success "Node.js $(node --version) disponible"
    fi

    if ! command -v npx &>/dev/null; then
        warn "npx no encontrado — MCPs via npx no funcionarán"
        warnings=$((warnings + 1))
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        fatal "Faltan herramientas críticas: ${missing[*]}. Instalalas y reintentá."
    fi

    if command -v sha256sum &>/dev/null; then
        SHASUM_CMD="sha256sum"
    elif command -v shasum &>/dev/null; then
        SHASUM_CMD="shasum -a 256"
    else
        warn "sha256sum/shasum no encontrado — no se verificarán checksums"
        SHASUM_CMD=""
    fi

    if [ "$warnings" -gt 0 ]; then
        warn "$warnings advertencias. El sistema funcionará con capacidad reducida."
    fi

    success "Verificación completa"
}

# ============================================================================
# Backup
# ============================================================================

run_backup() {
    step "Backup snapshot (pre-instalación)"

    local backup_dir="${INSTALL_DIR}.backup.$(date +%Y%m%d-%H%M%S)"

    if [ -d "${INSTALL_DIR}" ]; then
        info "Respaldando instalación existente..."
        cp -a "${INSTALL_DIR}" "${backup_dir}" 2>/dev/null && {
            BACKUP_PATH="$backup_dir"
            success "Backup creado en: ${backup_dir}"
        } || {
            warn "No se pudo crear backup. Continuando..."
            BACKUP_PATH=""
        }
    else
        info "No hay instalación previa para backupear"
        BACKUP_PATH=""
    fi
}

# ============================================================================
# Instalar vía git clone
# ============================================================================

install_git() {
    step "Instalando via git clone"

    if [ -d "${INSTALL_DIR}/.git" ]; then
        info "Lend.Ai ya instalado. Actualizando..."
        git -C "${INSTALL_DIR}" fetch origin "${GITHUB_BRANCH}" 2>/dev/null || warn "No se pudo actualizar (sin conexión?)"
        git -C "${INSTALL_DIR}" reset --hard "origin/${GITHUB_BRANCH}" 2>/dev/null || true
        success "Actualizado a la última versión (rama ${GITHUB_BRANCH})"
    else
        info "Clonando repositorio..."
        mkdir -p "$(dirname "${INSTALL_DIR}")"
        git clone --branch "${GITHUB_BRANCH}" --depth 1 \
            "https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}.git" \
            "${INSTALL_DIR}" || {
            fatal "No se pudo clonar el repositorio. Verificá conexión a Internet."
        }
        success "Repositorio clonado en ${INSTALL_DIR} (rama ${GITHUB_BRANCH})"
    fi

    cd "${INSTALL_DIR}"
    success "Instalación completada en ${INSTALL_DIR}"
}

# ============================================================================
# Instalar dependencias Python
# ============================================================================

install_python_deps() {
    step "Instalando dependencias Python"

    if [ -f "${INSTALL_DIR}/requirements.txt" ]; then
        substep "Instalando desde requirements.txt..."
        pip3 install -r "${INSTALL_DIR}/requirements.txt" -q 2>&1 | tail -1 || \
            warn "Algunas dependencias Python no se instalaron"
        success "Dependencias Python instaladas"
    else
        info "No hay requirements.txt — instalando paquetes core"
        pip3 install mcp pyyaml pydantic pytest pandas numpy -q 2>&1 | tail -1 || true
        success "Paquetes core instalados"
    fi
}

# ============================================================================
# Cachear MCPs npm
# ============================================================================

cache_npm_mcps() {
    step "Cacheando MCPs npm"

    local packages=(
        "@modelcontextprotocol/server-sequential-thinking"
        "@modelcontextprotocol/server-filesystem"
        "@modelcontextprotocol/server-puppeteer"
        "@modelcontextprotocol/server-github"
        "duckduckgo-mcp-server"
        "mcp-sqlite"
        "@jtalk22/slack-mcp"
        "@piotr-agier/google-drive-mcp"
    )

    for pkg in "${packages[@]}"; do
        echo -ne "  ${BLUE}📦 ${pkg}...${NC}"
        npx -y "${pkg}" --help &>/dev/null || npx -y "${pkg}" --version &>/dev/null || true
        echo -e "\r  ${GREEN}✅ ${pkg}${NC}"
    done

    success "MCPs npm cacheados"
}

# ============================================================================
# Configurar OpenCode
# ============================================================================

setup_opencode_config() {
    step "Configurando OpenCode"

    local opencode_config_dir="${HOME}/.config/opencode"

    if ! command -v opencode &>/dev/null && [ ! -f "${HOME}/.opencode/bin/opencode" ]; then
        warn "OpenCode no detectado. Saltando configuración."
        info "Podés configurar manualmente después:"
        info "  cp ${INSTALL_DIR}/opencode.json ~/.config/opencode/opencode.json"
        return
    fi

    mkdir -p "${opencode_config_dir}"

    # Backup existente
    if [ -f "${opencode_config_dir}/opencode.json" ]; then
        cp "${opencode_config_dir}/opencode.json" "${opencode_config_dir}/opencode.json.backup.$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true
    fi

    # Copiar opencode.json reemplazando placeholder
    if [ -f "${INSTALL_DIR}/opencode.json" ]; then
        sed -e "s|{LEND_AI_HOME}|${INSTALL_DIR}|g" \
            "${INSTALL_DIR}/opencode.json" > "${opencode_config_dir}/opencode.json"
        success "opencode.json configurado en ${opencode_config_dir}"
    else
        warn "opencode.json no encontrado en ${INSTALL_DIR}"
    fi

    # tui.json con plugins
    if [ ! -f "${opencode_config_dir}/tui.json" ]; then
        cat > "${opencode_config_dir}/tui.json" <<- TUIEOF
{
  "plugin": [
    "opencode-sdd-engram-manage",
    "opencode-subagent-statusline"
  ]
}
TUIEOF
        success "tui.json creado con plugins SDD + Subagent Monitor"
    fi
}

# ============================================================================
# Verificar instalación
# ============================================================================

verify_installation() {
    step "Verificando instalación"

    local warnings=0
    local required_dirs=(
        "agents" "skills" "mcp-servers" "profiles" "docs"
    )
    local required_files=(
        "opencode.json" "install.sh" "AGENTS.md"
        "profiles/lend-ai/persona.md"
        "profiles/lend-ai/workflow.md"
        "skills/data-analyst/SKILL.md"
        "skills/frontend-senior/SKILL.md"
        "skills/senior-orchestrator/SKILL.md"
    )

    echo -e "  ${BOLD}Estructura:${NC}"
    for dir in "${required_dirs[@]}"; do
        if [ -d "${INSTALL_DIR}/${dir}" ]; then
            echo -e "  ${GREEN}✅${NC} ${dir}/"
        else
            echo -e "  ${YELLOW}⚠️${NC} ${dir}/ — no encontrado"
            warnings=$((warnings + 1))
        fi
    done

    echo -e "  ${BOLD}Archivos esenciales:${NC}"
    for file in "${required_files[@]}"; do
        if [ -f "${INSTALL_DIR}/${file}" ]; then
            echo -e "  ${GREEN}✅${NC} ${file}"
        else
            echo -e "  ${YELLOW}⚠️${NC} ${file} — no encontrado"
            warnings=$((warnings + 1))
        fi
    done

    echo -e "  ${BOLD}Herramientas:${NC}"
    for cmd in git python3 node opencode; do
        if command -v "$cmd" &>/dev/null; then
            echo -e "  ${GREEN}✅${NC} ${cmd}"
        else
            echo -e "  ${YELLOW}⚠️${NC} ${cmd} — no encontrado"
            warnings=$((warnings + 1))
        fi
    done

    if [ "$warnings" -gt 0 ]; then
        warn "${warnings} advertencias. El sistema puede funcionar igual."
    else
        success "Instalación verificada — todo en orden"
    fi
}

# ============================================================================
# Verificar Engram
# ============================================================================

check_engram() {
    step "Verificando Engram (memoria persistente)"

    if command -v engram &>/dev/null; then
        local engram_version
        engram_version="$(engram --version 2>/dev/null || engram version 2>/dev/null || echo "desconocida")"
        success "Engram ${engram_version} disponible"

        if engram mcp --help &>/dev/null 2>&1; then
            success "Engram MCP listo para usar"
        else
            warn "Engram MCP no responde — podés necesitar actualizar"
        fi
    else
        warn "Engram no encontrado. Instalalo para memoria persistente:"
        warn "  brew install engram  o  https://engram.one"
    fi
}

# ============================================================================
# Próximos pasos
# ============================================================================

print_next_steps() {
    echo ""
    echo -e "${GREEN}${BOLD}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}${BOLD}║      ✅ Lend.Ai instalado con éxito        ║${NC}"
    echo -e "${GREEN}${BOLD}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  ${BOLD}📁 Instalado en:${NC}  ${INSTALL_DIR}"
    echo -e "  ${BOLD}🔧 Rama:${NC}          ${GITHUB_BRANCH}"

    if [ -n "${BACKUP_PATH:-}" ]; then
        echo -e "  ${BOLD}💾 Backup:${NC}         ${BACKUP_PATH}"
    fi

    echo ""
    echo -e "${BOLD}🚀 Próximos pasos:${NC}"
    echo ""
    echo -e "  ${CYAN}1.${NC} Abrí OpenCode y usá el agente Lend.Ai:"
    echo -e "     ${DIM}@lend-ai ¿qué podemos hacer hoy?${NC}"
    echo ""
    echo -e "  ${CYAN}2.${NC} Para data analysis:"
    echo -e "     ${DIM}@data-analyst analizá este dataset${NC}"
    echo ""
    echo -e "  ${CYAN}3.${NC} Para frontend:"
    echo -e "     ${DIM}@frontend-senior creá un componente React${NC}"
    echo ""
    echo -e "  ${CYAN}4.${NC} Atajos de teclado:"
    echo -e "     ${DIM}Alt+B   → Ver sub-agentes activos${NC}"
    echo -e "     ${DIM}Tab     → Cambiar entre agentes${NC}"
    echo ""
    echo -e "  ${CYAN}5.${NC} Si algo sale mal, restaurá desde backup:"
    if [ -n "${BACKUP_PATH:-}" ]; then
        echo -e "     ${DIM}cp -a ${BACKUP_PATH}/* ${INSTALL_DIR}/${NC}"
    fi
    echo ""
    echo -e "${BOLD}📚 Documentación:${NC}"
    echo -e "  ${DIM}https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}${NC}"
    echo ""
}

# ============================================================================
# Post-instalación
# ============================================================================

post_install_checks() {
    step "Post-instalación: verificaciones adicionales"

    if command -v python3 &>/dev/null; then
        if python3 -c "import yaml; print('YAML OK')" &>/dev/null 2>&1; then
            success "Python: YAML importable"
        else
            warn "Python: pyyaml no está instalado"
            substep "Corré: pip3 install pyyaml"
        fi
    fi

    if [ -f "${INSTALL_DIR}/opencode.json" ]; then
        if grep -q "{LEND_AI_HOME}" "${INSTALL_DIR}/opencode.json" 2>/dev/null; then
            warn "opencode.json tiene variables sin reemplazar"
            substep "Corré: sed -i 's|{LEND_AI_HOME}|${INSTALL_DIR}|g' ~/.config/opencode/opencode.json"
        fi
    fi

    if [ "$OS" = "wsl" ]; then
        info "Estás en WSL. Recordá que los MCPs corren en el entorno Linux."
    fi

    success "Post-instalación completada"
}

# ============================================================================
# .env setup
# ============================================================================

setup_env() {
    step "Configurando credenciales"

    if [ -f "${INSTALL_DIR}/.env.template" ] && [ ! -f "${INSTALL_DIR}/.env" ]; then
        cp "${INSTALL_DIR}/.env.template" "${INSTALL_DIR}/.env"
        info "Archivo .env creado desde template"
    fi

    if [ -f "${INSTALL_DIR}/.env" ]; then
        set +a
        source "${INSTALL_DIR}/.env" 2>/dev/null || true
        set -a

        if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${NOTION_TOKEN:-}" ]; then
            echo ""
            read -p "  ¿Querés configurar credenciales ahora? (s/N): " confirm_env
            if [ "$confirm_env" = "s" ] || [ "$confirm_env" = "S" ]; then
                setup_env_interactive
            fi
        else
            success "Credenciales ya configuradas"
        fi
    fi
}

setup_env_interactive() {
    echo ""
    info "Completá tus credenciales (dejá vacío para saltar):"
    echo ""

    read -p "  Token de GitHub (para PRs, issues): " input_gh
    read -p "  Token de Notion (para docs): " input_notion

    local sed_i=(-i)
    [[ "$(uname -s)" == "Darwin" ]] && sed_i=(-i "")

    [ -n "$input_gh" ]     && sed "${sed_i[@]}" "s|^# GITHUB_TOKEN=|GITHUB_TOKEN=${input_gh}|" "${INSTALL_DIR}/.env" 2>/dev/null || true
    [ -n "$input_notion" ] && sed "${sed_i[@]}" "s|^# NOTION_TOKEN=|NOTION_TOKEN=${input_notion}|" "${INSTALL_DIR}/.env" 2>/dev/null || true

    success "Credenciales configuradas"
}

# ============================================================================
# Main
# ============================================================================

main() {
    setup_colors

    while [ $# -gt 0 ]; do
        case "$1" in
            --method)
                [ $# -lt 2 ] && fatal "--method requiere un argumento (git|auto)"
                case "$2" in
                    git|auto) INSTALL_METHOD="$2"; shift 2 ;;
                    *) fatal "Método inválido: $2. Usá git o auto" ;;
                esac
                ;;
            --dir)
                [ $# -lt 2 ] && fatal "--dir requiere un argumento"
                INSTALL_DIR="$2"; shift 2
                ;;
            --branch)
                [ $# -lt 2 ] && fatal "--branch requiere un argumento"
                GITHUB_BRANCH="$2"; shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                fatal "Opción desconocida: $1. Usá --help para ayuda."
                ;;
        esac
    done

    print_banner

    step "Detectando plataforma"
    detect_platform

    step "Verificando prerequisitos"
    check_prerequisites

    step "Preparando backup"
    run_backup

    install_git

    setup_env
    install_python_deps
    cache_npm_mcps
    setup_opencode_config
    check_engram
    post_install_checks
    verify_installation

    print_next_steps
}

main "$@"
