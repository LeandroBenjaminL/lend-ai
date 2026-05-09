#!/usr/bin/env python3
"""
model-router.py — Router activo de modelos LLM como MCP Server.

Lee models.json y expone tools MCP para resolver qué modelo usar
según skill, agente o tarea. Persiste el tier activo.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("❌ mcp package not installed. Run: pip install mcp")
    sys.exit(1)

logging.basicConfig(level=logging.WARNING, format="%(levelname)s — %(message)s")
log = logging.getLogger("model-router")

# ── Rutas ────────────────────────────────────────────────────────────────────

_BASE_DIR_DEFAULT = Path(__file__).resolve().parent.parent
BASE_DIR = Path(os.environ.get("DATA_ANALYST_HOME", str(_BASE_DIR_DEFAULT)))
MODELS_JSON = BASE_DIR / "models.json"
ACTIVE_TIER_FILE = Path(
    os.environ.get("DATA_ANALYST_TIER_FILE", "/tmp/opencode-active-tier.json")
)
DEFAULT_TIER = "T3-balanced"
CONFIG_JSON = BASE_DIR / "model-routing.config.json"

# ── Carga de datos ───────────────────────────────────────────────────────────


def cargar_models() -> dict[str, Any]:
    if not MODELS_JSON.exists():
        log.error("No se encuentra %s", MODELS_JSON)
        return {}
    try:
        with open(MODELS_JSON, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.error("Error al leer %s: %s", MODELS_JSON, e)
        return {}


_models_data: dict[str, Any] = {}


def _extraer_tiers(data: dict) -> dict[str, dict]:
    return data.get("llm_models", {}).get("_tiers", {})


def _extraer_agentes(data: dict) -> dict[str, str]:
    mapping: dict[str, str] = {}
    llm = data.get("llm_models", {})
    for entry in llm.get("primary_agents", []):
        nombre, tier = entry.get("agent"), entry.get("tier")
        if nombre and tier:
            mapping[nombre] = tier
    for entry in llm.get("sub_agents", []):
        nombre, tier = entry.get("agent"), entry.get("tier")
        if nombre and tier:
            mapping[nombre] = tier
    sdd = llm.get("_sdd_subagents", {}).get("agents", [])
    for entry in sdd:
        nombre, tier = entry.get("agent"), entry.get("tier")
        if nombre and tier:
            mapping[nombre] = tier
    return mapping


_SKILL_TO_AGENT_MAP: dict[str, str] = {
    "ml-modeling": "data-modeler",
    "time-series-analysis": "data-modeler",
    "data-analysis": "data-explorer",
    "data-profiling": "data-explorer",
    "data-visualization": "data-reporter",
    "reporting": "data-reporter",
    "etl-pipelines": "data-etl",
    "sql-analysis": "data-etl",
    "api-integration": "data-etl",
    "web-scraping": "data-etl",
    "database-connections": "data-etl",
    "data-validation": "data-validation",
    "notebook-integration": "data-explorer",
    "file-formats": "data-etl",
    "python-environment": "data-archive",
    "git-data": "data-archive",
    "regex-data": "data-cleaning",
    "streamlit": "data-reporter",
    "statistical-testing": "data-modeler",
    "data-cleaning": "data-cleaning",
    "data-verify": "data-verify",
    "data-archive": "data-archive",
    "data-design": "data-design",
    "data-question": "data-question",
    "cognitive-doc-design": "sdd-design",
    "comment-writer": "data-reporter",
    "work-unit-commits": "data-etl",
    "go-testing": "data-verify",
    "branch-pr": "data-etl",
    "chained-pr": "data-etl",
    "issue-creation": "data-archive",
    "judgment-day": "data-verify",
    "skill-creator": "data-design",
    "skill-registry": "data-archive",
}


def _construir_skill_agent_map(agentes: dict[str, str]) -> dict[str, str]:
    skills_en_models = set()
    for entry in _models_data.get("ml_models", []):
        nombre = entry.get("skill")
        if nombre:
            skills_en_models.add(nombre)
    skills_en_models.update(_SKILL_TO_AGENT_MAP.keys())
    mapping: dict[str, str] = {}
    for skill in sorted(skills_en_models):
        agent_ref = _SKILL_TO_AGENT_MAP.get(skill)
        if agent_ref and agent_ref in agentes:
            mapping[skill] = agentes[agent_ref]
        else:
            mapping[skill] = DEFAULT_TIER
    return mapping


def _construir_task_skill_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for entry in _models_data.get("ml_models", []):
        skill = entry.get("skill", "")
        for tarea in entry.get("tasks", []):
            task_name = tarea.get("task")
            if task_name:
                mapping[task_name] = skill
    return mapping


def obtener_modelo_para_tier(tier: str) -> str:
    tiers = _extraer_tiers(_models_data)
    entry = tiers.get(tier)
    return entry.get("modelo", "") if entry else ""


def leer_tier_activo() -> str:
    if not ACTIVE_TIER_FILE.exists():
        return DEFAULT_TIER
    try:
        with open(ACTIVE_TIER_FILE, encoding="utf-8") as f:
            data = json.load(f)
        tier = data.get("tier", DEFAULT_TIER)
        tiers = _extraer_tiers(_models_data)
        if tier not in tiers:
            return DEFAULT_TIER
        return tier
    except (json.JSONDecodeError, OSError):
        return DEFAULT_TIER


def guardar_tier_activo(tier: str) -> dict:
    tiers = _extraer_tiers(_models_data)
    if tier not in tiers:
        return {"error": f"Tier '{tier}' no existe. Válidos: {list(tiers.keys())}"}
    data = {
        "tier": tier,
        "modelo": tiers[tier].get("modelo", ""),
        "tipo_tarea": tiers[tier].get("tipo_tarea", ""),
    }
    try:
        with open(ACTIVE_TIER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data
    except OSError as e:
        return {"error": str(e)}


# ── Override helpers ─────────────────────────────────────────────────────────


def _cargar_overrides() -> dict:
    """Carga la config completa desde model-routing.config.json (con overrides)."""
    if not CONFIG_JSON.exists():
        return {"overrides": {"skills": {}, "agents": {}}}
    try:
        with open(CONFIG_JSON, encoding="utf-8") as f:
            data = json.load(f)
        if "overrides" not in data:
            data["overrides"] = {}
        data["overrides"].setdefault("skills", {})
        data["overrides"].setdefault("agents", {})
        return data
    except (json.JSONDecodeError, OSError) as e:
        log.error("Error al leer %s: %s", CONFIG_JSON, e)
        return {"overrides": {"skills": {}, "agents": {}}}


def _guardar_overrides(data: dict) -> dict:
    """Persiste la config completa en model-routing.config.json."""
    try:
        with open(CONFIG_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return {"status": "ok"}
    except OSError as e:
        return {"error": str(e)}


# ── Inicializar datos ────────────────────────────────────────────────────────


def _init_data() -> tuple[
    dict[str, dict], dict[str, str], dict[str, str], dict[str, str]
]:
    data = cargar_models()
    _models_data.update(data)
    tiers = _extraer_tiers(data)
    agentes = _extraer_agentes(data)
    skill_map = _construir_skill_agent_map(agentes)
    task_map = _construir_task_skill_map()
    return tiers, agentes, skill_map, task_map


tiers, agentes, skill_map, task_map = _init_data()

# ── MCP Server ───────────────────────────────────────────────────────────────

mcp = FastMCP(
    "model-router",
    instructions="""MCP server que resuelve qué modelo LLM usar según skill, agente o tarea.

Tiers disponibles:
- T1-ultra-fast: Minimax Free (tareas mecánicas)
- T2-fast: Minimax (tareas simples)
- T3-balanced: DeepSeek Medium (default)
- T4-reasoning: DeepSeek Pro (razonamiento estructurado)
- T5-deep: DeepSeek Pro Max (máxima complejidad)
""",
)


@mcp.tool()
def resolve_skill(nombre: str) -> str:
    """Resuelve el tier y modelo para una skill (ej: data-analysis, ml-modeling, reporting)."""
    # Priorizar override manual sobre el mapping por defecto
    overrides = _cargar_overrides()
    override_tier = overrides.get("overrides", {}).get("skills", {}).get(nombre)
    if override_tier and override_tier in tiers:
        tier = override_tier
    else:
        tier = skill_map.get(nombre, DEFAULT_TIER)
    modelo = obtener_modelo_para_tier(tier)
    return json.dumps(
        {"skill": nombre, "tier": tier, "model": modelo}, indent=2, ensure_ascii=False
    )


@mcp.tool()
def resolve_agent(nombre: str) -> str:
    """Resuelve el tier y modelo para un agente (ej: data-explorer, data-modeler)."""
    # Priorizar override manual sobre el mapping por defecto
    overrides = _cargar_overrides()
    override_tier = overrides.get("overrides", {}).get("agents", {}).get(nombre)
    if override_tier and override_tier in tiers:
        tier = override_tier
    else:
        tier = agentes.get(nombre, DEFAULT_TIER)
    modelo = obtener_modelo_para_tier(tier)
    return json.dumps(
        {"agent": nombre, "tier": tier, "model": modelo}, indent=2, ensure_ascii=False
    )


@mcp.tool()
def resolve_task(task_name: str) -> str:
    """Resuelve el tier y modelo para una tarea por nombre."""
    skill = task_map.get(task_name)
    if not skill:
        return json.dumps(
            {
                "task": task_name,
                "error": f"No se encontró ninguna skill con la tarea '{task_name}'",
                "tier": DEFAULT_TIER,
                "model": obtener_modelo_para_tier(DEFAULT_TIER),
            },
            indent=2,
            ensure_ascii=False,
        )
    return resolve_skill(skill)


@mcp.tool()
def set_tier(tier: str) -> str:
    """Guarda el tier activo (T1, T2, T3, T4, T5 o nombre completo como T3-balanced)."""
    tier_input = tier.strip()
    if tier_input in tiers:
        tier_key = tier_input
    else:
        matched = [k for k in tiers if k.startswith(tier_input.upper())]
        if len(matched) == 1:
            tier_key = matched[0]
        elif len(matched) > 1:
            return json.dumps(
                {"error": f"'{tier_input}' es ambiguo. Coincide con: {matched}"},
                ensure_ascii=False,
            )
        else:
            return json.dumps(
                {
                    "error": f"Tier '{tier_input}' no encontrado. Válidos: {list(tiers.keys())}"
                },
                ensure_ascii=False,
            )
    result = guardar_tier_activo(tier_key)
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def get_active_tier() -> str:
    """Lee el tier activo actual y su modelo correspondiente."""
    tier = leer_tier_activo()
    modelo = obtener_modelo_para_tier(tier)
    return json.dumps({"tier": tier, "model": modelo}, indent=2, ensure_ascii=False)


@mcp.tool()
def list_all() -> str:
    """Lista todos los tiers, skills y agentes con sus modelos asignados."""
    result = {
        "tiers": {
            k: {"modelo": v.get("modelo", ""), "tipo_tarea": v.get("tipo_tarea", "")}
            for k, v in tiers.items()
        },
        "skills": [
            {
                "skill": s,
                "tier": skill_map.get(s, DEFAULT_TIER),
                "model": obtener_modelo_para_tier(skill_map.get(s, DEFAULT_TIER)),
            }
            for s in sorted(skill_map)
        ],
        "agents": [
            {
                "agent": a,
                "tier": agentes.get(a, DEFAULT_TIER),
                "model": obtener_modelo_para_tier(agentes.get(a, DEFAULT_TIER)),
            }
            for a in sorted(agentes)
        ],
        "active_tier": leer_tier_activo(),
    }
    return json.dumps(result, indent=2, ensure_ascii=False)


@mcp.tool()
def set_skill_tier(skill: str, tier: str) -> str:
    """Asigna un tier específico a una skill. Persiste en model-routing.config.json."""
    if skill not in skill_map:
        return json.dumps(
            {
                "error": f"Skill '{skill}' no encontrada. Válidas: {sorted(skill_map.keys())}"
            },
            ensure_ascii=False,
        )
    if tier not in tiers:
        return json.dumps(
            {"error": f"Tier '{tier}' no existe. Válidos: {list(tiers.keys())}"},
            ensure_ascii=False,
        )
    config = _cargar_overrides()
    config.setdefault("overrides", {})
    config["overrides"].setdefault("skills", {})
    config["overrides"]["skills"][skill] = tier
    result = _guardar_overrides(config)
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    return json.dumps(
        {
            "status": "ok",
            "action": "set_skill_tier",
            "skill": skill,
            "tier": tier,
            "model": obtener_modelo_para_tier(tier),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def set_agent_tier(agent: str, tier: str) -> str:
    """Asigna un tier específico a un agente. Persiste en model-routing.config.json."""
    if agent not in agentes:
        return json.dumps(
            {
                "error": f"Agente '{agent}' no encontrado. Válidos: {sorted(agentes.keys())}"
            },
            ensure_ascii=False,
        )
    if tier not in tiers:
        return json.dumps(
            {"error": f"Tier '{tier}' no existe. Válidos: {list(tiers.keys())}"},
            ensure_ascii=False,
        )
    config = _cargar_overrides()
    config.setdefault("overrides", {})
    config["overrides"].setdefault("agents", {})
    config["overrides"]["agents"][agent] = tier
    result = _guardar_overrides(config)
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    return json.dumps(
        {
            "status": "ok",
            "action": "set_agent_tier",
            "agent": agent,
            "tier": tier,
            "model": obtener_modelo_para_tier(tier),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def reset_skill_tier(skill: str) -> str:
    """Elimina el override de una skill, vuelve al default."""
    if skill not in skill_map:
        return json.dumps(
            {
                "error": f"Skill '{skill}' no encontrada. Válidas: {sorted(skill_map.keys())}"
            },
            ensure_ascii=False,
        )
    config = _cargar_overrides()
    overrides_skills = config.get("overrides", {}).get("skills", {})
    if skill not in overrides_skills:
        return json.dumps(
            {"status": "noop", "message": f"Skill '{skill}' no tiene override activo."},
            indent=2,
            ensure_ascii=False,
        )
    del overrides_skills[skill]
    result = _guardar_overrides(config)
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    default_tier = skill_map.get(skill, DEFAULT_TIER)
    return json.dumps(
        {
            "status": "ok",
            "action": "reset_skill_tier",
            "skill": skill,
            "reverted_to_tier": default_tier,
            "model": obtener_modelo_para_tier(default_tier),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def reset_agent_tier(agent: str) -> str:
    """Elimina el override de un agente, vuelve al default."""
    if agent not in agentes:
        return json.dumps(
            {
                "error": f"Agente '{agent}' no encontrado. Válidos: {sorted(agentes.keys())}"
            },
            ensure_ascii=False,
        )
    config = _cargar_overrides()
    overrides_agents = config.get("overrides", {}).get("agents", {})
    if agent not in overrides_agents:
        return json.dumps(
            {
                "status": "noop",
                "message": f"Agente '{agent}' no tiene override activo.",
            },
            indent=2,
            ensure_ascii=False,
        )
    del overrides_agents[agent]
    result = _guardar_overrides(config)
    if "error" in result:
        return json.dumps(result, ensure_ascii=False)
    default_tier = agentes.get(agent, DEFAULT_TIER)
    return json.dumps(
        {
            "status": "ok",
            "action": "reset_agent_tier",
            "agent": agent,
            "reverted_to_tier": default_tier,
            "model": obtener_modelo_para_tier(default_tier),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def list_overrides() -> str:
    """Lista todos los overrides activos (skills + agents)."""
    config = _cargar_overrides()
    overrides = config.get("overrides", {"skills": {}, "agents": {}})
    skills = {}
    for skill, tier in overrides.get("skills", {}).items():
        skills[skill] = {"tier": tier, "model": obtener_modelo_para_tier(tier)}
    agents = {}
    for agent, tier in overrides.get("agents", {}).items():
        agents[agent] = {"tier": tier, "model": obtener_modelo_para_tier(tier)}
    return json.dumps(
        {
            "overrides": {"skills": skills, "agents": agents},
            "count": len(skills) + len(agents),
        },
        indent=2,
        ensure_ascii=False,
    )


# ── CLI (para tests y uso directo desde terminal) ────────────────────────────


def _run_cli() -> None:
    """Punto de entrada CLI: python3 model-router.py <comando> [args]."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Model Router — resuelve qué modelo LLM usar"
    )
    sub = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # list
    sub.add_parser("list", help="Lista todos los tiers, skills y agentes")

    # resolve
    resolve_p = sub.add_parser("resolve", help="Resuelve tier para agente/skill/task")
    resolve_p.add_argument("--agent", type=str, help="Nombre del agente")
    resolve_p.add_argument("--skill", type=str, help="Nombre de la skill")
    resolve_p.add_argument("--task", type=str, help="Nombre de la tarea")

    # set-tier
    set_tier_p = sub.add_parser("set-tier", help="Guarda el tier activo")
    set_tier_p.add_argument("tier", type=str, help="Tier (ej: T4, T3-balanced)")

    # get-tier
    sub.add_parser("get-tier", help="Lee el tier activo actual")

    # set-skill-tier
    set_sk_p = sub.add_parser(
        "set-skill-tier", help="Asigna un tier específico a una skill"
    )
    set_sk_p.add_argument("skill", type=str)
    set_sk_p.add_argument("tier", type=str)

    # set-agent-tier
    set_ag_p = sub.add_parser(
        "set-agent-tier", help="Asigna un tier específico a un agente"
    )
    set_ag_p.add_argument("agent", type=str)
    set_ag_p.add_argument("tier", type=str)

    # reset-skill-tier
    reset_sk_p = sub.add_parser("reset-skill-tier", help="Elimina override de skill")
    reset_sk_p.add_argument("skill", type=str)

    # reset-agent-tier
    reset_ag_p = sub.add_parser("reset-agent-tier", help="Elimina override de agente")
    reset_ag_p.add_argument("agent", type=str)

    # list-overrides
    sub.add_parser("list-overrides", help="Lista overrides activos")

    args = parser.parse_args()

    if args.command == "list":
        print(list_all())
    elif args.command == "resolve":
        if args.agent:
            print(resolve_agent(args.agent))
        elif args.skill:
            print(resolve_skill(args.skill))
        elif args.task:
            print(resolve_task(args.task))
        else:
            parser.error("resolve requiere --agent, --skill o --task")
    elif args.command == "set-tier":
        print(set_tier(args.tier))
    elif args.command == "get-tier":
        print(get_active_tier())
    elif args.command == "set-skill-tier":
        print(set_skill_tier(args.skill, args.tier))
    elif args.command == "set-agent-tier":
        print(set_agent_tier(args.agent, args.tier))
    elif args.command == "reset-skill-tier":
        print(reset_skill_tier(args.skill))
    elif args.command == "reset-agent-tier":
        print(reset_agent_tier(args.agent))
    elif args.command == "list-overrides":
        print(list_overrides())
    else:
        parser.print_help()


if __name__ == "__main__":
    # Si hay argumentos CLI, corremos como CLI
    # Si no, corremos como MCP server (lo llama el agente vía stdio)
    if len(sys.argv) > 1:
        _run_cli()
    else:
        mcp.run(transport="stdio")
