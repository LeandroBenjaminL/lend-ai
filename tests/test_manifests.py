"""
Tests de validación de manifests YAML de agentes.

Verifica que cada .yaml en manifests/:
- Sea YAML válido
- Tenga los campos obligatorios
- Cumpla con las reglas del ecosistema
"""

from pathlib import Path
from typing import Any

import yaml

# ── Helper local (también definido en conftest.py para las fixtures) ────────


def _get_agent_field(data: dict, field: str):
    """Busca field en top-level del dict o dentro de la clave 'agent'."""
    if field in data:
        return data[field]
    agent = data.get("agent", {})
    if isinstance(agent, dict) and field in agent:
        return agent[field]
    return None


# ── Campos obligatorios en la raíz ──────────────────────────────────────────

REQUIRED_TOP_LEVEL = {"agent", "instructions"}

# mcp_bindings y sub_agents se buscan en top-level O dentro de `agent:`
REQUIRED_AGNOSTIC = {"mcp_bindings"}

REQUIRED_AGENT_FIELDS = {"name", "layer", "trigger", "description"}
REQUIRED_INSTRUCTION_FIELDS = {"persona", "workflow"}


def _get_agent_name(yaml_data: dict[str, Any]) -> str:
    """Extrae el nombre del agente del YAML, o 'unknown' si falta."""
    agent = yaml_data.get("agent", {})
    if isinstance(agent, dict):
        return agent.get("name", "unknown")
    return "unknown"


class TestYamlValidity:
    """Pruebas básicas de parseo y estructura YAML."""

    def test_all_yaml_are_valid_yaml(self, all_yaml_files: list[Path]) -> None:
        """Cada .yaml se puede parsear con yaml.safe_load() sin errores."""
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data is None:
                    errors.append(f"{yaml_file.name}: archivo vacío")
            except yaml.YAMLError as e:
                errors.append(f"{yaml_file.name}: {e}")

        assert not errors, f"Se encontraron {len(errors)} errores de parseo YAML:\n" + "\n".join(
            errors
        )

    def test_all_yaml_have_required_fields(self, all_yaml_files: list[Path]) -> None:
        """Cada YAML tiene los campos obligatorios: agent.*, mcp_bindings, instructions.*.

        Nota: mcp_bindings y sub_agents pueden estar en top-level o dentro de `agent:`.
        """
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            with open(yaml_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            name = _get_agent_name(data)

            # Top-level keys (agent, instructions)
            for key in REQUIRED_TOP_LEVEL:
                if key not in data:
                    errors.append(f"{yaml_file.name} ({name}): falta '{key}'")

            # Campos que pueden estar en top-level o dentro de agent
            for key in REQUIRED_AGNOSTIC:
                if _get_agent_field(data, key) is None:
                    errors.append(
                        f"{yaml_file.name} ({name}): falta '{key}' "
                        f"(ni en top-level ni dentro de agent)"
                    )

            # agent.*
            agent = data.get("agent", {})
            if isinstance(agent, dict):
                for field in REQUIRED_AGENT_FIELDS:
                    if field not in agent:
                        errors.append(f"{yaml_file.name} ({name}): falta 'agent.{field}'")

            # instructions.*
            instructions = data.get("instructions", {})
            if isinstance(instructions, dict):
                for field in REQUIRED_INSTRUCTION_FIELDS:
                    if field not in instructions:
                        errors.append(f"{yaml_file.name} ({name}): falta 'instructions.{field}'")

        assert not errors, f"Se encontraron {len(errors)} campos faltantes:\n" + "\n".join(errors)

    def test_all_yaml_have_valid_layer(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """Layer es '0', '0.5', o '1' según la arquitectura del ecosistema."""
        valid_layers = {"0", "0.5", "1"}  # noqa: N806
        errors: list[str] = []

        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            layer = data.get("agent", {}).get("layer")

            # Normalizar: el YAML puede tener int o string
            layer_str = str(layer) if layer is not None else None

            if layer_str not in valid_layers:
                errors.append(
                    f"{name}: layer='{layer_str}' no es válido. Se espera uno de {valid_layers}"
                )

        assert not errors, f"Se encontraron {len(errors)} layers inválidos:\n" + "\n".join(errors)


class TestManifestIntegrity:
    """Pruebas de integridad y consistencia entre manifests."""

    def test_sub_agents_exist(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """Cada sub_agent referenciado existe como otro .yaml en manifests/.

        Nota: sub_agents puede estar en top-level o dentro de `agent:`.
        """
        existing = {f.stem for f in all_yaml_files}
        errors: list[str] = []

        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            sub_agents = _get_agent_field(data, "sub_agents") or []
            for sub in sub_agents:
                if sub not in existing:
                    errors.append(f"{name}: sub_agent '{sub}' no tiene un .yaml en manifests/")

        assert not errors, f"Se encontraron {len(errors)} sub-agents sin manifest:\n" + "\n".join(
            errors
        )

    def test_instructions_files_exist(
        self, manifests_dir: Path, all_yaml_files: list[Path], profiles_dir: Path
    ) -> None:
        """Cada archivo referenciado en instructions (persona.md, workflow.md)
        existe en profiles/lend-ai/ (ubicacion centralizada)."""
        errors: list[str] = []

        for yaml_file in all_yaml_files:
            name = yaml_file.stem

            with open(yaml_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            instructions = data.get("instructions", {})
            for field in REQUIRED_INSTRUCTION_FIELDS:
                filename = instructions.get(field)
                if not filename:
                    continue

                instr_path = profiles_dir / "lend-ai" / filename
                if not instr_path.exists():
                    errors.append(f"{name}: falta archivo '{filename}' en {profiles_dir / 'lend-ai'}")

        assert not errors, (
            f"Se encontraron {len(errors)} problemas con archivos de instructions:\n"
            + "\n".join(errors)
        )

    def test_mcp_bindings_are_strings(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """mcp_bindings es una lista de strings.

        Nota: puede estar en top-level o dentro de `agent:`.
        """
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            bindings = _get_agent_field(data, "mcp_bindings") or []

            if not isinstance(bindings, list):
                errors.append(f"{name}: mcp_bindings no es una lista")
                continue

            for i, binding in enumerate(bindings):
                if not isinstance(binding, str):
                    errors.append(
                        f"{name}: mcp_bindings[{i}]='{binding}' no es string "
                        f"(tipo: {type(binding).__name__})"
                    )

        assert not errors, f"Se encontraron {len(errors)} bindings no-string:\n" + "\n".join(errors)

    def test_no_duplicate_names(self, all_manifest_names: list[str]) -> None:
        """No hay dos agentes con el mismo nombre."""
        seen: set[str] = set()
        duplicates: list[str] = []
        for name in all_manifest_names:
            if name in seen:
                duplicates.append(name)
            seen.add(name)

        assert not duplicates, f"Nombres duplicados encontrados: {duplicates}"

    def test_trigger_is_not_empty(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """Todos los agentes tienen trigger definido y no vacío."""
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            trigger = data.get("agent", {}).get("trigger", "")

            if not trigger or not trigger.strip():
                errors.append(f"{name}: trigger está vacío o ausente")

        assert not errors, f"Se encontraron {len(errors)} agentes sin trigger:\n" + "\n".join(
            errors
        )


class TestManifestConventions:
    """Convenciones de formato y estilo en manifests."""

    def test_agent_name_matches_filename(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """El agent.name dentro del YAML coincide con el nombre del archivo."""
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            expected = yaml_file.stem
            data = parse_yaml(expected)
            actual = data.get("agent", {}).get("name", "")
            if actual != expected:
                errors.append(
                    f"{yaml_file.name}: agent.name='{actual}' "
                    f"no coincide con el nombre del archivo '{expected}'"
                )
        assert not errors, "\n".join(errors)

    def test_description_is_not_empty(self, all_yaml_files: list[Path], parse_yaml: Any) -> None:
        """Todos los agentes tienen description definida."""
        errors: list[str] = []
        for yaml_file in all_yaml_files:
            name = yaml_file.stem
            data = parse_yaml(name)
            desc = data.get("agent", {}).get("description", "")
            if not desc or not desc.strip():
                errors.append(f"{name}: description está vacía o ausente")
        assert not errors, "\n".join(errors)
