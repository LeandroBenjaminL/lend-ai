"""
Tests de referencias cruzadas entre manifests, registry, skills y models.json.

Verifica que todos los componentes del ecosistema estén correctamente
interconectados y que no haya referencias rotas.
"""

from pathlib import Path
from typing import Any

# ── Helper local ─────────────────────────────────────────────────────────────


def _get_agent_field(data: dict, field: str):
    """Busca field en top-level del dict o dentro de la clave 'agent'."""
    if field in data:
        return data[field]
    agent = data.get("agent", {})
    if isinstance(agent, dict) and field in agent:
        return agent[field]
    return None


# ── Helpers ──────────────────────────────────────────────────────────────────


def _get_agents_from_registry(registry_path: Path) -> set[str]:
    """Extrae los nombres de agentes desde la tabla del AGENT_REGISTRY.md."""
    agents: set[str] = set()
    with open(registry_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Busca líneas con formato "| 00 | orchestrator |"
            # o "| 05 | data-analysis |"
            if line.startswith("|") and "|" in line[1:]:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 4 and parts[1].isdigit():
                    agent_name = parts[2].strip()
                    if agent_name and agent_name != "Agent":
                        agents.add(agent_name)
    return agents


def _get_agent_names_from_models(data: dict[str, Any]) -> set[str]:
    """Extrae nombres de agentes desde models.json (primary + sub + sdd)."""
    names: set[str] = set()
    llm = data.get("llm_models", {})

    for entry in llm.get("primary_agents", []):
        name = entry.get("agent")
        if name:
            names.add(name)

    for entry in llm.get("sub_agents", []):
        name = entry.get("agent")
        if name:
            names.add(name)

    for entry in llm.get("_sdd_subagents", {}).get("agents", []):
        name = entry.get("agent")
        if name:
            names.add(name)

    return names


# ── Tests ────────────────────────────────────────────────────────────────────


class TestRegistryConsistency:
    """Consistencia entre AGENT_REGISTRY.md y manifests."""

    def test_skills_in_registry_match_manifests(
        self, registry_path: Path, all_manifest_names: list[str]
    ) -> None:
        """Skills listadas en AGENT_REGISTRY.md existen como manifests."""
        registry_agents = _get_agents_from_registry(registry_path)
        manifest_set = set(all_manifest_names)

        missing: list[str] = []
        for agent in sorted(registry_agents):
            if agent not in manifest_set:
                missing.append(agent)

        # El orchestrator y gentle-orchestrator pueden no tener .yaml directo
        known_without_manifest = {"gentle-orchestrator", "orchestrator"}
        actual_missing = [m for m in missing if m not in known_without_manifest]

        assert not actual_missing, (
            f"Agentes en el registry sin manifest: {actual_missing}"
        )

    def test_all_manifests_are_in_registry(
        self, registry_path: Path, all_manifest_names: list[str]
    ) -> None:
        """Todos los manifests están mencionados en AGENT_REGISTRY.md."""
        registry_agents = _get_agents_from_registry(registry_path)

        missing: list[str] = []
        for name in all_manifest_names:
            if name not in registry_agents:
                missing.append(name)

        assert not missing, f"Manifests no mencionados en AGENT_REGISTRY.md: {missing}"


class TestSkillsConsistency:
    """Consistencia entre skills/ y manifests."""

    def test_skills_dir_matches_manifests(
        self, skills_dir: Path, all_manifest_names: list[str]
    ) -> None:
        """Skills en skills/ que son data-analysis tienen manifests correspondientes.
        Excluye _shared, sdd-*, bundle* y skills no-data-analysis."""
        manifest_set = set(all_manifest_names)
        skills_with_manifests: list[str] = []

        for child in skills_dir.iterdir():
            if not child.is_dir():
                continue
            skill_name = child.name

            # Excluir skills que no deberían tener manifest
            if skill_name.startswith("_") or skill_name.startswith("sdd-"):
                continue

            if skill_name not in manifest_set:
                skills_with_manifests.append(skill_name)

        assert not skills_with_manifests, (
            f"Skills en skills/ sin manifest correspondiente: {skills_with_manifests}"
        )

    def test_data_analysis_skills_have_skill_files(self, skills_dir: Path) -> None:
        """Cada skill de data-analysis tiene un SKILL.md."""
        missing: list[str] = []
        for child in skills_dir.iterdir():
            if not child.is_dir():
                continue
            skill_name = child.name
            if skill_name.startswith("_") or skill_name.startswith("sdd-"):
                continue
            skill_file = child / "SKILL.md"
            if not skill_file.exists():
                missing.append(skill_name)

        assert not missing, f"Skills sin SKILL.md: {missing}"


class TestModelsConsistency:
    """Consistencia entre models.json y manifests."""

    def test_models_json_agents_match_manifests(
        self, models_data: dict[str, Any], all_manifest_names: list[str]
    ) -> None:
        """Los agentes en models.json tienen manifiestos correspondientes
        (excepto los que se sabe que no tienen)."""
        model_agents = _get_agent_names_from_models(models_data)
        manifest_set = set(all_manifest_names)

        # Agentes en models.json que sabemos que no tienen manifest individual
        known_virtual = {
            "data-explorer",
            "data-cleaner",
            "data-modeler",
            "data-reporter",
            "data-etl",
            "data-validator",
            "gentle-orchestrator",
            "data-analyst",
            # SDD agents — viven en skills/ pero no tienen .yaml en manifests/
            "sdd-init",
            "sdd-propose",
            "sdd-spec",
            "sdd-design",
            "sdd-tasks",
            "sdd-apply",
            "sdd-verify",
            "sdd-archive",
            "sdd-explore",
            "sdd-onboard",
        }

        orphan_models = []
        for agent in sorted(model_agents):
            if agent not in manifest_set and agent not in known_virtual:
                orphan_models.append(agent)

        assert not orphan_models, (
            f"Agentes en models.json sin manifest y no listados como virtuales: "
            f"{orphan_models}"
        )

    def test_agent_layers_are_consistent(
        self, all_yaml_files: list[Path], parse_yaml: Any
    ) -> None:
        """Layer 0 solo tiene agentes estrategas, layer 1 tiene domain agents.
        Según el registry: layer 0.5 = strategists, layer 1 = domain agents.
        Pero los manifests usan layer 0 para los strategists."""
        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            layer = str(data.get("agent", {}).get("layer", ""))

            # Layer 0 agents
            if layer == "0":
                assert name.startswith("data-"), (
                    f"Layer 0 agent '{name}' no debería estar en layer 0"
                )


class TestMcpConsistency:
    """Verificación de bindings MCP."""

    def test_mcp_names_are_reasonable(
        self, all_yaml_files: list[Path], parse_yaml: Any
    ) -> None:
        """Los nombres de MCP bindings son razonables (no vacíos, sin espacios raros)."""
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            bindings = _get_agent_field(data, "mcp_bindings") or []
            for binding in bindings:
                if not binding.strip():
                    errors.append(f"{name}: binding vacío")
                if " " in binding.strip():
                    errors.append(f"{name}: binding '{binding}' contiene espacios")
        assert not errors, "\n".join(errors)
