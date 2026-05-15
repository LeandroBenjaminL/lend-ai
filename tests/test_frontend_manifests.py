"""Tests adaptados para manifests del ecosistema Lend.Ai."""

from pathlib import Path

import pytest
import yaml

MANIFESTS_DIR = Path("agents/manifests")


def test_lend_ai_manifest_exists():
    """El manifest del orquestador Lend.Ai debe existir."""
    manifest = MANIFESTS_DIR / "lend-ai.yaml"
    assert manifest.exists(), "❌ lend-ai.yaml no encontrado"

    with open(manifest) as f:
        data = yaml.safe_load(f)

    assert data["agent"]["name"] == "lend-ai"
    assert "data-analyst" in data.get("sub_agents", [])
    assert "frontend-senior" in data.get("sub_agents", [])


def test_frontend_senior_manifest_exists():
    """El manifest de frontend-senior debe existir."""
    manifest = MANIFESTS_DIR / "frontend-senior.yaml"
    assert manifest.exists()


def test_data_analyst_manifest_exists():
    """El manifest de data-analyst debe existir."""
    manifest = MANIFESTS_DIR / "data-analyst.yaml"
    assert manifest.exists()


@pytest.mark.parametrize(
    "required_dir",
    [
        "lend-ai",
        "data-analyst",
        "frontend-senior",
        "data-explorer",
        "data-modeler",
        "data-reporter",
        "framework-architect",
        "ui-crafter",
        "styling-engineer",
    ],
)
def test_required_manifest_dirs(required_dir):
    """Verificar que los directorios de manifiestos requeridos existen."""
    dir_path = MANIFESTS_DIR / required_dir
    assert dir_path.is_dir(), f"❌ Directorio {required_dir}/ no encontrado"
    assert (dir_path / "persona.md").exists()
    assert (dir_path / "workflow.md").exists()
    assert (dir_path / "patterns.md").exists()
