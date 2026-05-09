#!/bin/bash
# ─────────────────────────────────────────────────────────────
# engram-git-sync.sh
# Sincroniza Engram entre PCs vía git
#
# Uso:
#   ./scripts/engram-git-sync.sh           → muestra estado
#   ./scripts/engram-git-sync.sh push       → sube cambios
#   ./scripts/engram-git-sync.sh pull       → baja cambios
#   ./scripts/engram-git-sync.sh status     → estado detallado
#   ./scripts/engram-git-sync.sh setup      → configura desde cero
# ─────────────────────────────────────────────────────────────

set -euo pipefail

ENGRAM_DIR="$HOME/.engram"
GIT_REMOTE="origin"
GIT_BRANCH="main"
GITHUB_USER="LeandroBenjaminL"
GITHUB_REPO="engram-data"

# Colores
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${CYAN}[info]${NC}    $*"; }
ok()      { echo -e "${VERDE}[ok]${NC}      $*"; }
warn()    { echo -e "${AMARILLO}[warn]${NC}    $*"; }
error()   { echo -e "${ROJO}[error]${NC}   $*"; }

show_status() {
    echo -e "\n${CYAN}📡 Engram Sync — Estado${NC}"
    echo "═══════════════════════════"

    if [ ! -d "$ENGRAM_DIR" ]; then
        echo -e "❌ ${ROJO}~/.engram/ no existe${NC}"
        echo "   Ejecutá: ./scripts/engram-git-sync.sh setup"
        return
    fi

    if [ -L "$ENGRAM_DIR" ]; then
        TARGET=$(readlink "$ENGRAM_DIR")
        echo -e "📍 Modo:       Symlink → ${CYAN}$TARGET${NC}"
        echo -e "⚠️  No es un repo git. Corré setup para migrar."
        return
    fi

    echo -e "📍 Ubicación:  ${CYAN}$ENGRAM_DIR${NC}"

    if [ -d "$ENGRAM_DIR/.git" ]; then
        echo -e "🔗 Modo:       ${VERDE}Git sync${NC}"
        REMOTE=$(cd "$ENGRAM_DIR" && git remote get-url origin 2>/dev/null || echo "no configurado")
        echo -e "🌐 Remote:     ${CYAN}$REMOTE${NC}"

        cd "$ENGRAM_DIR"
        # Por subir
        UNSTAGED=$(git status --short 2>/dev/null | wc -l)
        [ "$UNSTAGED" -gt 0 ] && echo -e "📤 Por subir:  ${AMARILLO}$UNSTAGED archivo(s) sin commit${NC}" \
                              || echo -e "📤 Por subir:  ${VERDE}nada${NC}"

        # Por bajar
        git fetch --quiet 2>/dev/null || true
        BEHIND=$(git rev-list --count HEAD.."$GIT_REMOTE/$GIT_BRANCH" 2>/dev/null || echo 0)
        [ "$BEHIND" -gt 0 ] && echo -e "📥 Por bajar:  ${AMARILLO}$BEHIND commit(s)${NC}" \
                            || echo -e "📥 Por bajar:  ${VERDE}nada${NC}"
    else
        echo -e "🔗 Modo:       ${AMARILLO}Local (sin git)${NC}"
    fi

    # Tamaño
    if [ -f "$ENGRAM_DIR/engram.db" ]; then
        SIZE=$(du -h "$ENGRAM_DIR/engram.db" | cut -f1)
        echo -e "💾 Tamaño:     ${CYAN}$SIZE${NC}"
    fi
}

do_push() {
    cd "$ENGRAM_DIR"
    echo -e "${CYAN}⬆️  Pusheando cambios...${NC}"
    git add .
    if git diff --cached --quiet; then
        echo -e "${VERDE}Nada nuevo para subir.${NC}"
    else
        git commit -m "sync $(date '+%Y-%m-%d %H:%M')"
        git push "$GIT_REMOTE" "$GIT_BRANCH"
        echo -e "${VERDE}✅ Push completado.${NC}"
    fi
}

do_pull() {
    cd "$ENGRAM_DIR"
    echo -e "${CYAN}⬇️  Bajando cambios...${NC}"
    if git pull --ff-only "$GIT_REMOTE" "$GIT_BRANCH" 2>/dev/null; then
        echo -e "${VERDE}✅ Pull completado.${NC}"
    else
        echo -e "${ROJO}❌ Pull falló. Podés tener conflictos o no hay conexión.${NC}"
    fi
}

do_setup() {
    echo -e "${CYAN}🔧 Configurando Engram sync vía git...${NC}"

    if [ -L "$ENGRAM_DIR" ]; then
        OLD_TARGET=$(readlink "$ENGRAM_DIR")
        echo -e "⚠️  ~/.engram es un symlink → ${AMARILLO}$OLD_TARGET${NC}"
        echo "   Haciendo backup de datos..."
        cp -a "$OLD_TARGET/." /tmp/engram-migrate/
        rm "$ENGRAM_DIR"
        mkdir -p "$ENGRAM_DIR"
        cp -a /tmp/engram-migrate/. "$ENGRAM_DIR/"
        rm -rf /tmp/engram-migrate/
        echo -e "   ${VERDE}✅ Datos migrados${NC}"
    elif [ ! -d "$ENGRAM_DIR" ]; then
        mkdir -p "$ENGRAM_DIR"
        echo -e "   ${VERDE}✅ Directorio creado${NC}"
    fi

    cd "$ENGRAM_DIR"

    if [ ! -d ".git" ]; then
        git init
        git branch -m main
        cat > .gitignore << 'GITIGNORE'
*.db-shm
*.db-wal
GITIGNORE
        git add -A
        git commit -m "init: engram memoria" 2>/dev/null || echo "   (primer commit)"
        echo -e "   ${VERDE}✅ Git init${NC}"
    fi

    # Configurar remote
    if ! git remote get-url origin &>/dev/null; then
        git remote add origin "https://github.com/$GITHUB_USER/$GITHUB_REPO.git"
        echo -e "   ${VERDE}✅ Remote configurado${NC}"
    fi

    # Push inicial
    echo ""
    echo -e "${CYAN}⬆️  Pusheando a GitHub...${NC}"
    git push -u origin main 2>&1 || echo -e "${AMARILLO}⚠️  Push falló. Revisá conexión o autenticación.${NC}"

    echo ""
    echo -e "${VERDE}✅ Setup completado.${NC}"
    echo ""
    echo -e "   📝 Recordá agregar al ${CYAN}~/.bashrc${NC}:"
    echo -e "   if [ -d \"\$HOME/.engram/.git\" ]; then"
    echo -e "       cd \"\$HOME/.engram\" && git pull --ff-only 2>/dev/null && cd - >/dev/null"
    echo -e "   fi"
}

# ─── Main ───
case "${1:-status}" in
    push)   do_push ;;
    pull)   do_pull ;;
    status) show_status ;;
    setup)  do_setup ;;
    *)
        echo -e "Uso: $0 {status|push|pull|setup}"
        echo ""
        show_status
        ;;
esac
