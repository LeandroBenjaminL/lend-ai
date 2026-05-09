"""Configuración compartida de tests para Frontend Ecosystem."""

from pathlib import Path

# Raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Rutas importantes
MANIFESTS_DIR = PROJECT_ROOT / "agents" / "manifests"
SKILLS_DIR = PROJECT_ROOT / "skills"
MCP_SERVERS_DIR = PROJECT_ROOT / "mcp-servers"
