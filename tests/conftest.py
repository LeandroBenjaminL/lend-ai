"""
Fixtures compartidas para la suite de tests del ecosistema Data Analyst.
"""

from pathlib import Path
from typing import Any

import pytest
import yaml


def get_agent_field(data: dict, field: str):
    """Obtiene un campo del YAML buscando primero en top-level y luego dentro de `agent:`.

    Algunos manifests tienen `mcp_bindings` y `sub_agents` como top-level keys,
    otros los tienen dentro del dict `agent:`. Esta función unifica la búsqueda.
    """
    if field in data:
        return data[field]
    agent = data.get("agent", {})
    if isinstance(agent, dict) and field in agent:
        return agent[field]
    return None


# ── Rutas base ───────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent  # tests/ -> data-analyst-ecosystem/


@pytest.fixture
def manifests_dir() -> Path:
    """Path al directorio de manifests de agentes.

    Usa agents/manifests directamente en vez del symlink raíz/manifests
    porque en GitHub Actions los symlinks no se resuelven correctamente.
    """
    direct = REPO_ROOT / "agents" / "manifests"
    if direct.exists():
        return direct
    return REPO_ROOT / "manifests"


@pytest.fixture
def model_router_script() -> Path:
    """Path al script model-router.py."""
    return REPO_ROOT / "mcp-servers" / "model-router.py"


@pytest.fixture
def models_json_path() -> Path:
    """Path al archivo models.json."""
    return REPO_ROOT / "models.json"


@pytest.fixture
def skills_dir() -> Path:
    """Path al directorio de skills."""
    return REPO_ROOT / "skills"


@pytest.fixture
def registry_path() -> Path:
    """Path al archivo AGENT_REGISTRY.md."""
    return REPO_ROOT / "registry" / "AGENT_REGISTRY.md"


@pytest.fixture
def all_yaml_files(manifests_dir: Path) -> list[Path]:
    """Lista de todos los archivos .yaml en manifests_dir."""
    return sorted(manifests_dir.glob("*.yaml"))


@pytest.fixture
def all_manifest_names(all_yaml_files: list[Path]) -> list[str]:
    """Lista de nombres de agentes (sin extensión .yaml)."""
    return sorted(f.stem for f in all_yaml_files)


@pytest.fixture
def parse_yaml(manifests_dir: Path):
    """Fixture-fábrica: dado un nombre de agente, parsea su YAML y devuelve un dict."""

    def _parse(name: str) -> dict[str, Any]:
        path = manifests_dir / f"{name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"No existe manifest para '{name}': {path}")
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ValueError(f"El archivo YAML '{path}' está vacío o es inválido")
        return data

    return _parse


@pytest.fixture
def models_data(models_json_path: Path) -> dict[str, Any]:
    """Carga y devuelve models.json como dict."""
    import json

    with open(models_json_path, encoding="utf-8") as f:
        return json.load(f)
