"""Tests de existencia de manifests core del ecosistema Lend.Ai."""

from pathlib import Path

import yaml

MANIFESTS_DIR = Path("agents/manifests")
PROFILES_DIR = Path("profiles/lend-ai")


def _load_yaml(name: str) -> dict:
    path = MANIFESTS_DIR / f"{name}.yaml"
    assert path.exists(), f"{name}.yaml not found"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_lend_ai_manifest_exists():
    data = _load_yaml("lend-ai")
    assert data["agent"]["name"] == "lend-ai"
    assert "data-analyst" in data.get("sub_agents", [])
    assert "frontend-senior" in data.get("sub_agents", [])
    assert "devops" in data.get("sub_agents", [])
    assert "engram-keeper" in data.get("sub_agents", [])


def test_frontend_senior_manifest_exists():
    data = _load_yaml("frontend-senior")
    assert data["agent"]["name"] == "frontend-senior"


def test_data_analyst_manifest_exists():
    data = _load_yaml("data-analyst")
    assert data["agent"]["name"] == "data-analyst"


def test_devops_manifest_exists():
    data = _load_yaml("devops")
    assert data["agent"]["name"] == "devops"


def test_engram_keeper_manifest_exists():
    data = _load_yaml("engram-keeper")
    assert data["agent"]["name"] == "engram-keeper"


def test_profiles_exist():
    assert (PROFILES_DIR / "persona.md").exists()
    assert (PROFILES_DIR / "workflow.md").exists()
    assert (PROFILES_DIR / "output-style.md").exists()
