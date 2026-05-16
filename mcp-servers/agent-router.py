#!/usr/bin/env python3
"""
Agent Router — MCP Server para el ecosistema Lend.Ai.

Enruta tareas al agente correcto según manifests YAML, resuelve tiers
y modelos vía model-router, y expone herramientas de consulta e inventario.

Usage:
  python3 agent-router.py

Requires: mcp, pyyaml
"""

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
)
log = logging.getLogger("agent-router")

# ── Dependencias ─────────────────────────────────────────────────────────────

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("❌ mcp package not installed. Run: pip install mcp")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("❌ PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ── Constantes ───────────────────────────────────────────────────────────────

_MANIFESTS_DIR_DEFAULT = Path(__file__).resolve().parent.parent / "agents" / "manifests"
MANIFESTS_DIR = Path(
    os.environ.get(
        "LEND_AI_MANIFESTS_DIR",
        os.environ.get("DATA_ANALYST_MANIFESTS_DIR", str(_MANIFESTS_DIR_DEFAULT)),
    )
)

_BASE_DIR = Path(__file__).resolve().parent
MODEL_ROUTER = _BASE_DIR / "model-router.py"
DEFAULT_TIER = "T3-balanced"

REQUIRED_FIELDS = [
    "agent.name",
    "agent.layer",
    "instructions.persona",
    "instructions.workflow",
]

# ── Helpers ──────────────────────────────────────────────────────────────────


def _list_yaml_files(directory: Path | None = None) -> list[Path]:
    """Return all .yaml files in the manifests directory."""
    target = directory or MANIFESTS_DIR
    return sorted(target.glob("*.yaml"))


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load a single YAML file safely."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _get_agent_name(data: dict[str, Any]) -> str:
    """Extract agent name from parsed YAML data."""
    agent = data.get("agent", {})
    if isinstance(agent, dict):
        return agent.get("name", "")
    return ""


def _resolve_model_router(agent_name: str) -> dict[str, str]:
    """
    Ejecuta model-router.py resolve --agent <name> y devuelve tier + modelo.

    Si falla (archivo no encontrado, timeout, error de parseo), devuelve
    DEFAULT_TIER sin modelo.
    """
    if not MODEL_ROUTER.exists():
        log.warning("model-router.py no encontrado en %s", MODEL_ROUTER)
        return {"tier": DEFAULT_TIER, "model": ""}

    try:
        result = subprocess.run(
            ["python3", str(MODEL_ROUTER), "resolve", "--agent", agent_name],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            return {
                "tier": data.get("tier", DEFAULT_TIER),
                "model": data.get("model", ""),
            }
        else:
            log.warning(
                "model-router falló para '%s' (exit %d): %s",
                agent_name,
                result.returncode,
                result.stderr.strip(),
            )
    except subprocess.TimeoutExpired:
        log.warning("model-router timeout para '%s'", agent_name)
    except FileNotFoundError:
        log.warning("python3 no encontrado al ejecutar model-router")
    except json.JSONDecodeError as e:
        log.warning("model-router devolvió JSON inválido para '%s': %s", agent_name, e)
    except OSError as e:
        log.warning("Error ejecutando model-router para '%s': %s", agent_name, e)

    return {"tier": DEFAULT_TIER, "model": ""}


def _build_agent_map() -> dict[str, dict[str, Any]]:
    """Construye {agent_name: parsed_yaml_data} desde todos los manifests."""
    agents: dict[str, dict[str, Any]] = {}
    for yaml_path in _list_yaml_files():
        try:
            data = _load_yaml(yaml_path)
            name = _get_agent_name(data)
            if name:
                agents[name] = data
            else:
                log.warning("YAML sin agent.name: %s", yaml_path.name)
        except yaml.YAMLError as e:
            log.warning("Error parseando %s: %s", yaml_path.name, e)
        except OSError as e:
            log.warning("Error leyendo %s: %s", yaml_path.name, e)
    return agents


def _format_agent_summary(name: str, data: dict[str, Any]) -> dict[str, Any]:
    """Arma un resumen legible para un agente."""
    agent_info = data.get("agent", {})
    return {
        "name": name,
        "layer": agent_info.get("layer", "?"),
        "description": agent_info.get("description", ""),
        "trigger": agent_info.get("trigger", ""),
        "mcp_bindings": data.get("mcp_bindings", []),
        "sub_agents": data.get("sub_agents", []),
    }


def _tokenize(text: str) -> set[str]:
    """Tokeniza un texto: lowercase, split por espacios y comas."""
    import re

    tokens = re.split(r"[\s,;.]+", text.lower())
    return {t for t in tokens if t}


# ── Carga inicial ───────────────────────────────────────────────────────────

ALL_AGENTS = _build_agent_map()
log.info("Agent Router iniciado — %d agentes cargados", len(ALL_AGENTS))

# ── MCP Server ──────────────────────────────────────────────────────────────

mcp = FastMCP("Agent Router")


@mcp.tool()
def list_agents(layer: str | None = None) -> str:
    """
    Lista todos los agentes registrados en el ecosistema.

    Args:
        layer: Filtrar por capa ("0", "0.5", "1"). Si se omite, lista todos.

    Returns:
        Lista formateada con nombre, capa y descripción de cada agente.
    """
    valid_layers = {"0", "0.5", "1"}
    if layer is not None and layer not in valid_layers:
        return f"❌ Layer inválida: '{layer}'. Válidas: {', '.join(sorted(valid_layers))}"

    results: list[dict[str, Any]] = []
    for name, data in sorted(ALL_AGENTS.items()):
        info = _format_agent_summary(name, data)
        if layer is None or str(info["layer"]) == layer:
            results.append(info)

    if not results:
        msg = (
            f"No se encontraron agentes para layer '{layer}'."
            if layer
            else "No hay agentes registrados."
        )
        return msg

    lines = [f"## Agentes ({len(results)} total)"]
    for r in results:
        mcp_list = ", ".join(r["mcp_bindings"]) if r["mcp_bindings"] else "(ninguno)"
        sub = ", ".join(r["sub_agents"]) if r["sub_agents"] else "(ninguno)"
        lines.append(f"\n### {r['name']}  (layer {r['layer']})")
        lines.append(f"  {r['description']}")
        lines.append(f"  Trigger: {r['trigger']}")
        lines.append(f"  MCPs: {mcp_list}")
        lines.append(f"  Sub-agentes: {sub}")

    return "\n".join(lines)


@mcp.tool()
def resolve_agent(name: str) -> str:
    """
    Resuelve la información completa de un agente, incluyendo tier y modelo
    obtenidos del model-router.

    Args:
        name: Nombre del agente (ej: "data-analysis").

    Returns:
        JSON con datos del YAML + tier + modelo del LLM asignado.
    """
    data = ALL_AGENTS.get(name)
    if data is None:
        return json.dumps(
            {"error": f"Agente '{name}' no encontrado."},
            ensure_ascii=False,
            indent=2,
        )

    info = _format_agent_summary(name, data)
    routing = _resolve_model_router(name)

    result = {
        **info,
        "tier": routing["tier"],
        "model": routing["model"],
        "instructions": {
            "persona": data.get("instructions", {}).get("persona", ""),
            "workflow": data.get("instructions", {}).get("workflow", ""),
            "patterns": data.get("instructions", {}).get("patterns", ""),
        },
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_agent_mcp_bindings(name: str) -> str:
    """
    Devuelve los MCPs vinculados a un agente específico.

    Args:
        name: Nombre del agente.

    Returns:
        Lista de nombres de MCP tools que el agente puede usar.
    """
    data = ALL_AGENTS.get(name)
    if data is None:
        return json.dumps(
            {"error": f"Agente '{name}' no encontrado."},
            ensure_ascii=False,
            indent=2,
        )

    bindings = data.get("mcp_bindings", [])
    return json.dumps(
        {
            "agent": name,
            "mcp_bindings": bindings,
            "count": len(bindings),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def get_sub_agents(name: str) -> str:
    """
    Devuelve los sub-agentes que un agente puede spawnear.

    Args:
        name: Nombre del agente.

    Returns:
        Lista de nombres de sub-agentes.
    """
    data = ALL_AGENTS.get(name)
    if data is None:
        return json.dumps(
            {"error": f"Agente '{name}' no encontrado."},
            ensure_ascii=False,
            indent=2,
        )

    subs = data.get("sub_agents", [])
    # Resolver tier para cada sub-agente
    resolved = []
    for s in subs:
        routing = _resolve_model_router(s)
        resolved.append(
            {
                "name": s,
                "tier": routing["tier"],
                "model": routing["model"],
            }
        )

    return json.dumps(
        {
            "agent": name,
            "sub_agents": resolved,
            "count": len(resolved),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def resolve_task(task_description: str, agents_yaml_path: str = "") -> str:
    """
    Encuentra el mejor agente para una descripción de tarea usando
    fuzzy matching de keywords contra los campos 'trigger' de los YAML.

    Args:
        task_description: Descripción en lenguaje natural de la tarea.
        agents_yaml_path: Ruta al directorio de manifests YAML.
                          Si se omite, usa la ruta por defecto.

    Returns:
        Top-3 agentes con score de confianza.
    """
    # Determinar directorio de manifests
    if agents_yaml_path and agents_yaml_path.strip():
        target_dir = Path(agents_yaml_path)
        if not target_dir.is_dir():
            return json.dumps(
                {
                    "error": f"El directorio '{agents_yaml_path}' no existe o no es un directorio.",
                },
                ensure_ascii=False,
                indent=2,
            )
    else:
        target_dir = MANIFESTS_DIR

    # Cargar agents desde el directorio indicado
    agents: dict[str, dict[str, Any]] = {}
    for yaml_path in _list_yaml_files(target_dir):
        try:
            data = _load_yaml(yaml_path)
            name = _get_agent_name(data)
            if name:
                agents[name] = data
        except Exception as e:
            log.warning("Error cargando %s: %s", yaml_path.name, e)

    if not agents:
        return json.dumps(
            {
                "error": "No se encontraron agentes en el directorio especificado.",
            },
            ensure_ascii=False,
            indent=2,
        )

    # Tokenizar la tarea
    task_tokens = _tokenize(task_description)

    # Scoring: cuantos tokens del trigger aparecen en la tarea
    scored: list[tuple[str, float, dict[str, Any]]] = []
    for name, data in agents.items():
        trigger = data.get("agent", {}).get("trigger", "")
        trigger_tokens = _tokenize(trigger)

        if not trigger_tokens:
            scored.append((name, 0.0, data))
            continue

        # Cantidad de tokens del trigger que están presentes en la tarea
        matches = len(task_tokens & trigger_tokens)
        score = matches / len(trigger_tokens) if trigger_tokens else 0.0

        # Bonus por match exacto (trigger es substring de task_description)
        if trigger.lower() in task_description.lower():
            score = max(score, 0.9)

        # Bonus extra si la tarea menciona el nombre del agente
        if name.lower() in task_description.lower():
            score = min(score + 0.3, 1.0)

        scored.append((name, score, data))

    # Ordenar por score descendente
    scored.sort(key=lambda x: (-x[1], x[0]))

    top3 = scored[:3]
    results = []
    for name, score, data in top3:
        info = _format_agent_summary(name, data)
        info["match_score"] = round(score, 4)
        results.append(info)

    return json.dumps(
        {
            "task": task_description,
            "results": results,
            "total_agents_evaluated": len(agents),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def resolve_task_deep(
    task_description: str,
    max_depth: int = 3,
    agents_yaml_path: str = "",
) -> str:
    """
    Encuentra el mejor agente para una tarea y resuelve recursivamente
    toda su cadena de sub-agentes (árbol de delegación profundo).

    Cada agente en el árbol incluye: nombre, layer, tier, modelo,
    descripción, trigger, y sus sub-agentes resueltos recursivamente
    hasta max_depth niveles de profundidad.

    Args:
        task_description: Descripción en lenguaje natural de la tarea.
        max_depth: Profundidad máxima de resolución recursiva (default: 3).
                   Depth=1 resuelve solo el agente principal.
                   Depth=2 incluye sub-agentes directos.
                   Depth=3 incluye sub-sub-agentes (default).
        agents_yaml_path: Ruta al directorio de manifests YAML.
                          Si se omite, usa la ruta por defecto.

    Returns:
        JSON con el árbol de delegación completo.
    """

    def _resolve_recursive(agent_name: str, depth: int, visited: set[str]) -> dict[str, Any] | None:
        """Resuelve un agente y sus sub-agentes recursivamente."""
        if agent_name in visited:
            return None
        visited.add(agent_name)

        data = ALL_AGENTS.get(agent_name)
        if data is None:
            return None

        agent_info = data.get("agent", {})
        routing = _resolve_model_router(agent_name)

        node = {
            "name": agent_name,
            "layer": agent_info.get("layer", "?"),
            "tier": routing["tier"],
            "model": routing["model"],
            "description": agent_info.get("description", ""),
            "trigger": agent_info.get("trigger", ""),
            "mcp_bindings": data.get("mcp_bindings", []),
            "sub_agents": [],
        }

        if depth < max_depth:
            subs = data.get("sub_agents", [])
            if isinstance(subs, list):
                for sub_name in subs:
                    sub_node = _resolve_recursive(sub_name, depth + 1, visited)
                    if sub_node:
                        node["sub_agents"].append(sub_node)

        return node

    # Determinar directorio de manifests
    if agents_yaml_path and agents_yaml_path.strip():
        target_dir = Path(agents_yaml_path)
        if not target_dir.is_dir():
            return json.dumps(
                {"error": f"El directorio '{agents_yaml_path}' no existe."},
                ensure_ascii=False,
                indent=2,
            )
    else:
        target_dir = MANIFESTS_DIR

    # Cargar agents
    agents: dict[str, dict[str, Any]] = {}
    for yaml_path in _list_yaml_files(target_dir):
        try:
            data = _load_yaml(yaml_path)
            name = _get_agent_name(data)
            if name:
                agents[name] = data
        except Exception as e:
            log.warning("Error cargando %s: %s", yaml_path.name, e)

    if not agents:
        return json.dumps(
            {"error": "No se encontraron agentes."},
            ensure_ascii=False,
            indent=2,
        )

    # Score: mismo algoritmo que resolve_task
    task_tokens = _tokenize(task_description)
    scored: list[tuple[str, float]] = []
    for name, data in agents.items():
        trigger = data.get("agent", {}).get("trigger", "")
        trigger_tokens = _tokenize(trigger)
        if not trigger_tokens:
            scored.append((name, 0.0))
            continue
        matches = len(task_tokens & trigger_tokens)
        score = matches / len(trigger_tokens)
        if trigger.lower() in task_description.lower():
            score = max(score, 0.9)
        if name.lower() in task_description.lower():
            score = min(score + 0.3, 1.0)
        scored.append((name, score))

    scored.sort(key=lambda x: (-x[1], x[0]))
    if not scored or scored[0][1] == 0.0:
        return json.dumps(
            {
                "task": task_description,
                "error": "No se encontró agente para esta tarea.",
                "results": [],
                "depth": max_depth,
            },
            ensure_ascii=False,
            indent=2,
        )

    top_name = scored[0][0]
    tree = _resolve_recursive(top_name, 1, set())

    return json.dumps(
        {
            "task": task_description,
            "depth": max_depth,
            "tree": tree,
            "total_agents_evaluated": len(agents),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def get_agents_by_mcp(mcp_name: str) -> str:
    """
    Devuelve todos los agentes que tienen un MCP específico en sus bindings.

    Args:
        mcp_name: Nombre del MCP (ej: "filesystem", "sqlite", "context7").

    Returns:
        Lista de agentes vinculados a ese MCP.
    """
    if not mcp_name or not mcp_name.strip():
        return json.dumps(
            {"error": "Debe especificar un nombre de MCP."},
            ensure_ascii=False,
            indent=2,
        )

    mcp_name = mcp_name.strip().lower()
    matched: list[dict[str, Any]] = []

    for name, data in sorted(ALL_AGENTS.items()):
        bindings = [b.lower() for b in data.get("mcp_bindings", [])]
        if mcp_name in bindings:
            info = _format_agent_summary(name, data)
            matched.append(info)

    return json.dumps(
        {
            "mcp": mcp_name,
            "agents": matched,
            "count": len(matched),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def agent_health_check() -> str:
    """
    Ejecuta un chequeo de salud completo sobre TODOS los manifests de agente.

    Verifica:
    - Cada .yaml es parseable
    - Campos obligatorios presentes (agent.name, agent.layer, instructions.*)
    - Sub-agentes referenciados existen como .yaml
    - Archivos de instructions existen (persona.md, workflow.md, patterns.md)
    - MCP bindings no están vacíos (solo warning)

    Returns:
        Reporte de salud con total_agents, valid, warnings, errors.
    """
    report: dict[str, Any] = {
        "total_agents": 0,
        "valid": 0,
        "warnings": [],
        "errors": [],
        "details": [],
    }

    yaml_files = _list_yaml_files()

    for yaml_path in yaml_files:
        agent_name = yaml_path.stem  # filename without .yaml
        report["total_agents"] += 1
        detail: dict[str, Any] = {
            "file": yaml_path.name,
            "agent_name": agent_name,
            "status": "valid",
            "issues": [],
        }

        # 1. Parseable?
        try:
            data = _load_yaml(yaml_path)
        except yaml.YAMLError as e:
            detail["status"] = "error"
            detail["issues"].append(f"YAML parse error: {e}")
            report["errors"].append(f"{yaml_path.name}: YAML parse error — {e}")
            report["details"].append(detail)
            continue

        if data is None:
            detail["status"] = "error"
            detail["issues"].append("Archivo YAML vacío")
            report["errors"].append(f"{yaml_path.name}: archivo YAML vacío")
            report["details"].append(detail)
            continue

        # 2. Campos obligatorios
        agent = data.get("agent", {})
        if not isinstance(agent, dict):
            detail["issues"].append("'agent' no es un diccionario")
        else:
            if not agent.get("name"):
                detail["issues"].append("Falta 'agent.name'")
            if agent.get("layer") is None:
                detail["issues"].append("Falta 'agent.layer'")

        instructions = data.get("instructions", {})
        if not isinstance(instructions, dict):
            detail["issues"].append("'instructions' no es un diccionario")
        else:
            for field in ["persona", "workflow"]:
                if field not in instructions:
                    detail["issues"].append(f"Falta 'instructions.{field}'")

        # 3. Instrucciones apuntan a archivos existentes
        actual_name = _get_agent_name(data)
        agent_dir = yaml_path.parent / actual_name if actual_name else yaml_path.parent / agent_name

        if isinstance(instructions, dict):
            for field in ["persona", "workflow"]:
                filename = instructions.get(field)
                if filename:
                    instr_path = agent_dir / filename
                    if not instr_path.exists():
                        detail["issues"].append(
                            f"Archivo 'instructions.{field}' no encontrado: {instr_path}"
                        )

        # 4. Sub-agentes referenciados existen como .yaml
        sub_agents = data.get("sub_agents", [])
        if isinstance(sub_agents, list):
            for sub_name in sub_agents:
                sub_yaml = yaml_path.parent / f"{sub_name}.yaml"
                if not sub_yaml.exists():
                    warn_msg = (
                        f"Sub-agente '{sub_name}' referenciado pero no existe como {sub_yaml.name}"
                    )
                    detail["issues"].append(warn_msg)

        # 5. MCP bindings (warning si está vacío, pero no error)
        mcp_bindings = data.get("mcp_bindings", [])
        if not mcp_bindings:
            warn_msg = "No tiene MCP bindings (puede ser intencional)"
            detail["issues"].append(warn_msg)
            report["warnings"].append(f"{yaml_path.name}: {warn_msg}")

        # Clasificar
        if detail["issues"]:
            # Separar en errores y warnings
            has_error = any(
                "Falta" in i
                or "no encontrado" in i
                or "parse error" in i
                or "vacío" in i
                or "diccionario" in i
                for i in detail["issues"]
            )
            if has_error:
                detail["status"] = "error"
                for issue in detail["issues"]:
                    report["errors"].append(f"{yaml_path.name}: {issue}")
            else:
                detail["status"] = "warning"
                for issue in detail["issues"]:
                    report["warnings"].append(f"{yaml_path.name}: {issue}")
        else:
            detail["status"] = "valid"
            report["valid"] += 1

        report["details"].append(detail)

    # Summary
    report["summary"] = (
        f"{report['valid']}/{report['total_agents']} válidos, "
        f"{len(report['warnings'])} warnings, "
        f"{len(report['errors'])} errores"
    )

    return json.dumps(report, ensure_ascii=False, indent=2)


# ── Entrypoint ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Iniciando Agent Router MCP Server...")
    mcp.run(transport="stdio")
