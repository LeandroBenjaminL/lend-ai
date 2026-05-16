"""
Tests de consistencia entre opencode.json y agents/manifests.

Regla fundamental: si un agente existe en opencode.json debe tener
su manifest YAML, y viceversa (excepto skills sin agente propio).
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENCODE_JSON = REPO_ROOT / "opencode.json"
MANIFESTS_DIR = REPO_ROOT / "agents" / "manifests"

SKILLS_WITHOUT_MANIFEST = {
    "lend-ai-mentor",
    "frontend-react-development",
    "frontend-css-styling",
    "frontend-type-script",
    "frontend-api-integration",
    "frontend-state-management",
    "frontend-testing",
    "frontend-responsive-design",
    "frontend-web-performance",
    "shared-api-integration",
    "shared-git-data",
}


def _get_opencode_agents() -> set[str]:
    with open(OPENCODE_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("agent", {}).keys())


def _get_manifest_names() -> set[str]:
    return {f.stem for f in MANIFESTS_DIR.glob("*.yaml")}


class TestOpencodeManifestConsistency:
    def test_all_opencode_agents_have_manifests(self):
        """Cada agente en opencode.json tiene su manifest YAML."""
        opencode_agents = _get_opencode_agents()
        manifest_names = _get_manifest_names()

        agents_expected = opencode_agents - SKILLS_WITHOUT_MANIFEST
        missing = agents_expected - manifest_names
        assert not missing, f"Agentes en opencode.json sin manifest YAML: {sorted(missing)}"

    def test_all_manifests_have_opencode_agents(self):
        """Cada manifest YAML tiene su agente en opencode.json."""
        opencode_agents = _get_opencode_agents()
        manifest_names = _get_manifest_names()

        manifest_expected = manifest_names - SKILLS_WITHOUT_MANIFEST
        missing = manifest_expected - opencode_agents
        assert not missing, f"Manifests sin agente en opencode.json (huerfanos): {sorted(missing)}"

    def test_opencode_json_is_valid(self):
        """opencode.json es JSON valido."""
        with open(OPENCODE_JSON, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, dict)
        assert "agent" in data
        assert len(data["agent"]) > 0

    def test_opencode_has_required_mcps(self):
        """opencode.json tiene los MCPs core configurados."""
        with open(OPENCODE_JSON, encoding="utf-8") as f:
            data = json.load(f)
        mcps = data.get("mcp", {})

        required = {"engram", "filesystem", "github", "agent-router", "model-router"}
        for mcp in required:
            assert mcp in mcps, f"MCP '{mcp}' no encontrado en opencode.json"
