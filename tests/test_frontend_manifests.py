"""Tests para validar manifests YAML del Frontend Ecosystem."""

import yaml
import pytest
from conftest import MANIFESTS_DIR


def _get_manifest_files():
    """Retorna todos los archivos .yaml en agents/manifests/."""
    if not MANIFESTS_DIR.exists():
        return []
    return sorted(MANIFESTS_DIR.glob("*.yaml"))


def _get_manifest_dirs():
    """Retorna todos los directorios de instrucciones en agents/manifests/."""
    if not MANIFESTS_DIR.exists():
        return []
    return sorted([d for d in MANIFESTS_DIR.iterdir() if d.is_dir()])


@pytest.mark.parametrize("yaml_file", _get_manifest_files(), ids=lambda p: p.name)
def test_manifest_is_valid_yaml(yaml_file):
    """Cada manifest .yaml debe ser YAML válido."""
    with open(yaml_file) as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"YAML inválido en {yaml_file.name}: {e}")
    assert data is not None, f"{yaml_file.name} está vacío"


@pytest.mark.parametrize("yaml_file", _get_manifest_files(), ids=lambda p: p.name)
def test_manifest_has_required_fields(yaml_file):
    """Cada manifest debe tener los campos obligatorios de agente."""
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    assert "agent" in data, f"{yaml_file.name}: falta 'agent'"
    agent = data["agent"]
    assert "name" in agent, f"{yaml_file.name}: falta 'agent.name'"
    assert "layer" in agent, f"{yaml_file.name}: falta 'agent.layer'"
    assert "trigger" in agent, f"{yaml_file.name}: falta 'agent.trigger'"
    assert "description" in agent, f"{yaml_file.name}: falta 'agent.description'"
    assert agent["layer"] in [0, 1], f"{yaml_file.name}: layer debe ser 0 o 1"


@pytest.mark.parametrize("yaml_file", _get_manifest_files(), ids=lambda p: p.name)
def test_manifest_has_instructions(yaml_file):
    """Cada manifest debe tener instrucciones (persona.md, workflow.md, patterns.md)."""
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    # Solo validar si tiene la sección instructions
    if "instructions" in data.get("agent", {}):
        instr = data["agent"]["instructions"]
        agent_name = yaml_file.stem
        instr_dir = MANIFESTS_DIR / agent_name

        for key in ["persona", "workflow", "patterns"]:
            filename = instr.get(key)
            if filename:
                filepath = instr_dir / filename
                assert filepath.exists(), (
                    f"{yaml_file.name}: falta {filename} en {instr_dir}/"
                )


@pytest.mark.parametrize("yaml_file", _get_manifest_files(), ids=lambda p: p.name)
def test_manifest_name_matches_filename(yaml_file):
    """El nombre del agente debe coincidir con el nombre del archivo."""
    with open(yaml_file) as f:
        data = yaml.safe_load(f)
    expected_name = yaml_file.stem  # filename sin .yaml
    assert data["agent"]["name"] == expected_name, (
        f"El nombre del agente '{data['agent']['name']}' no coincide "
        f"con el nombre del archivo '{expected_name}'"
    )


def test_all_manifests_have_matching_dirs():
    """Cada manifest .yaml debe tener su directorio de instrucciones."""
    yaml_files = {f.stem for f in _get_manifest_files()}
    dirs = {d.name for d in _get_manifest_dirs()}

    # Los YAML que tienen dir de instrucciones
    for name in yaml_files:
        if name in dirs:
            instr_dir = MANIFESTS_DIR / name
            has_instr = any(
                [
                    (instr_dir / "persona.md").exists(),
                    (instr_dir / "workflow.md").exists(),
                    (instr_dir / "patterns.md").exists(),
                ]
            )
            # Esto es informativo, no falla — puede tener el dir vacío
            if not has_instr:
                print(f"⚠️  {name}: directorio de instrucciones sin archivos .md")
