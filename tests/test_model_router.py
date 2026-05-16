"""
Tests de validación del model-router.py.

Verifica que el router:
- Exista y sea Python válido
- Responda correctamente a los comandos CLI
- Resuelva agentes, skills y tasks
- Gestione tiers correctamente
- Sea consistente con models.json
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

# ── Helpers ──────────────────────────────────────────────────────────────────


def _run_router(script: Path, *args: str) -> subprocess.CompletedProcess:
    """Ejecuta model-router.py con los argumentos dados y devuelve el resultado."""
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def _router_json(script: Path, *args: str) -> dict[str, Any]:
    """Ejecuta model-router.py y parsea su salida como JSON."""
    result = _run_router(script, *args)
    assert result.returncode == 0, (
        f"Error ejecutando: python3 model-router.py {' '.join(args)}\nstderr: {result.stderr}"
    )
    return json.loads(result.stdout)


# ── Tests ────────────────────────────────────────────────────────────────────


class TestRouterBasics:
    """Pruebas básicas de existencia y parseo."""

    def test_router_script_exists(self, model_router_script: Path) -> None:
        """model-router.py existe en disco."""
        assert model_router_script.exists(), (
            f"No se encuentra model-router.py en {model_router_script}"
        )

    def test_router_is_valid_python(self, model_router_script: Path) -> None:
        """model-router.py es Python sintácticamente válido."""
        source = model_router_script.read_text(encoding="utf-8")
        try:
            compile(source, str(model_router_script), "exec")
        except SyntaxError as e:
            pytest.fail(f"Error de sintaxis en model-router.py:\n{e}")


class TestRouterList:
    """Tests del comando 'list'."""

    @pytest.mark.slow
    def test_router_list_returns_valid_json(self, model_router_script: Path) -> None:
        """`python3 model-router.py list` devuelve JSON válido."""
        data = _router_json(model_router_script, "list")

        assert "tiers" in data, "La respuesta 'list' no contiene 'tiers'"
        assert "skills" in data, "La respuesta 'list' no contiene 'skills'"
        assert "agents" in data, "La respuesta 'list' no contiene 'agents'"
        assert "active_tier" in data, "La respuesta 'list' no contiene 'active_tier'"

    @pytest.mark.slow
    def test_list_tiers_match_models_json(
        self, model_router_script: Path, models_data: dict[str, Any]
    ) -> None:
        """Los tiers listados coinciden con los definidos en models.json."""
        data = _router_json(model_router_script, "list")
        expected_tiers = models_data.get("llm_models", {}).get("_tiers", {})

        for tier_key in expected_tiers:
            assert tier_key in data["tiers"], (
                f"Tier '{tier_key}' de models.json no aparece en la respuesta 'list'"
            )

    @pytest.mark.slow
    def test_list_agents_not_empty(self, model_router_script: Path) -> None:
        """La lista de agentes no está vacía."""
        data = _router_json(model_router_script, "list")
        assert len(data["agents"]) > 0, "La lista de agentes está vacía"


class TestRouterResolve:
    """Tests del comando 'resolve'."""

    @pytest.mark.slow
    def test_router_resolve_agent(self, model_router_script: Path) -> None:
        """`resolve --agent data-analysis` devuelve un tier válido."""
        result = _router_json(model_router_script, "resolve", "--agent", "data-analysis")

        assert result.get("agent") == "data-analysis", (
            f"Se esperaba agent='data-analysis', got '{result.get('agent')}'"
        )
        assert "tier" in result, "Respuesta no contiene 'tier'"
        assert result["tier"], f"Tier está vacío: {result}"

    @pytest.mark.slow
    def test_router_resolve_skill(self, model_router_script: Path) -> None:
        """`resolve --skill data-cleaning` devuelve un resultado con skill y tier."""
        result = _router_json(model_router_script, "resolve", "--skill", "data-cleaning")

        assert result.get("skill") == "data-cleaning", (
            f"Se esperaba skill='data-cleaning', got '{result.get('skill')}'"
        )
        assert "tier" in result, "Respuesta no contiene 'tier'"
        assert "model" in result, "Respuesta no contiene 'model'"

    @pytest.mark.slow
    def test_router_resolve_nonexistent(self, model_router_script: Path) -> None:
        """Resolver un agente que no existe debe devolver el tier default."""
        result = _router_json(
            model_router_script, "resolve", "--agent", "this-agent-does-not-exist-xyz"
        )

        assert "tier" in result, "Respuesta no contiene 'tier'"
        # El default es T3-balanced según model-router.py
        assert result["tier"] is not None, "Tier es None"

    @pytest.mark.slow
    def test_router_resolve_task(self, model_router_script: Path) -> None:
        """`resolve --task classification` devuelve un resultado.

        Nota: el router resuelve tasks a skills, y la respuesta incluye
        'skill' y 'tier' (no 'task' cuando el resolve es exitoso).
        """
        result = _router_json(model_router_script, "resolve", "--task", "classification")

        assert "skill" in result, f"Respuesta no contiene 'skill': {result}"
        assert "tier" in result, "Respuesta no contiene 'tier'"
        assert result["tier"] is not None, "El tier no debería ser None"


class TestRouterTierManagement:
    """Tests de gestión de tiers (set-tier, get-tier)."""

    @pytest.mark.slow
    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="model-router writes to /tmp, not available on Windows",
    )
    def test_router_set_and_get_tier(self, model_router_script: Path) -> None:
        """`set-tier T4` y después `get-tier` devuelve T4-reasoning."""
        # Setear
        set_result = _run_router(model_router_script, "set-tier", "T4")
        assert set_result.returncode == 0, f"Error al setear tier: {set_result.stderr}"
        set_data = json.loads(set_result.stdout)
        assert "tier" in set_data, f"Respuesta de set-tier no contiene 'tier': {set_data}"

        # Obtener
        get_result = _router_json(model_router_script, "get-tier")
        assert get_result.get("tier") == set_data["tier"], (
            f"get-tier devolvió '{get_result.get('tier')}', pero se seteó '{set_data['tier']}'"
        )

        # Restaurar default
        _run_router(model_router_script, "set-tier", "T3")

    @pytest.mark.slow
    def test_router_set_invalid_tier(self, model_router_script: Path) -> None:
        """Setear un tier inválido debe devolver un error."""
        result = _run_router(model_router_script, "set-tier", "T99-INVALID")
        # Debe fallar o devolver error
        data = json.loads(result.stdout)
        assert "error" in data, f"Set tier inválido debería devolver error: {data}"

    @pytest.mark.slow
    def test_router_get_tier_after_set(self, model_router_script: Path) -> None:
        """get-tier siempre devuelve un tier válido."""
        result = _router_json(model_router_script, "get-tier")
        assert "tier" in result, "Respuesta de get-tier no contiene 'tier'"
        assert result["tier"], "El tier no debería estar vacío"

        # Restaurar default
        _run_router(model_router_script, "set-tier", "T3")


class TestRouterConsistency:
    """Tests de consistencia entre el router y models.json."""

    @pytest.mark.slow
    def test_all_tiers_exist_in_models(
        self, model_router_script: Path, models_data: dict[str, Any]
    ) -> None:
        """Todos los tiers mencionados por el router existen en models.json _tiers."""
        data = _router_json(model_router_script, "list")
        expected_tiers = set(models_data.get("llm_models", {}).get("_tiers", {}).keys())

        for agent_entry in data["agents"]:
            tier = agent_entry.get("tier", "")
            assert tier in expected_tiers, (
                f"Agente '{agent_entry.get('agent')}' usa tier '{tier}' "
                f"que no existe en models.json _tiers ({expected_tiers})"
            )

        for skill_entry in data["skills"]:
            tier = skill_entry.get("tier", "")
            assert tier in expected_tiers, (
                f"Skill '{skill_entry.get('skill')}' usa tier '{tier}' "
                f"que no existe en models.json _tiers"
            )

    @pytest.mark.slow
    def test_no_agent_without_tier(self, model_router_script: Path) -> None:
        """Cada agente en el router tiene un tier asignado."""
        data = _router_json(model_router_script, "list")

        for agent_entry in data["agents"]:
            tier = agent_entry.get("tier")
            assert tier, f"Agente '{agent_entry.get('agent')}' no tiene tier asignado"
