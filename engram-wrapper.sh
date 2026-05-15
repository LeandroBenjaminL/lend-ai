#!/bin/bash
# Wrapper para ejecutar engram en SSH no-interactivo
# Homebrew no está en PATH por defecto en sesiones SSH non-login
export PATH="$HOME/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"
ENGRAM=$(command -v engram 2>/dev/null || echo "/home/linuxbrew/.linuxbrew/bin/engram")
exec "$ENGRAM" "$@"
