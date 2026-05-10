#!/usr/bin/env python3
"""
model-commands.py — Ejecutor de comandos /model para OpenCode.

Usage:
    python3 scripts/model-commands.py <comando> [args]

Comandos:
    set agent <nombre> <tier>
    set skill <nombre> <tier>
    list [skills|agents]
    reset agent <nombre>
    reset skill <nombre>
    tiers
    help
"""

import argparse
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTER = BASE_DIR / "mcp-servers" / "model-router.py"
CONFIG = BASE_DIR / "model-routing.config.json"

TIER_COLORS = {
    "T1-ultra-fast": "\033[32m",
    "T2-fast": "\033[34m",
    "T3-balanced": "\033[33m",
    "T4-reasoning": "\033[35m",
    "T5-deep": "\033[31m",
}
RESET = "\033[0m"
BOLD = "\033[1m"


def c(color: str, text: str) -> str:
    return f"{color}{text}{RESET}"


def load_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def save_config(data: dict) -> dict:
    try:
        with open(CONFIG, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return {"status": "ok"}
    except OSError as e:
        return {"error": str(e)}


def run_router(*args: str) -> dict:
    return {"error": "Not used - direct write"}


def cmd_set_agent(agent: str, tier: str) -> str:
    config = load_config()
    config.setdefault("overrides", {})
    config["overrides"].setdefault("agents", {})
    config["overrides"]["agents"][agent] = tier
    result = save_config(config)
    if "error" in result:
        return c("red", f"❌ Error: {result['error']}")
    return c("green", f"✅ Agente '{agent}' → {tier}")


def cmd_set_skill(skill: str, tier: str) -> str:
    config = load_config()
    config.setdefault("overrides", {})
    config["overrides"].setdefault("skills", {})
    config["overrides"]["skills"][skill] = tier
    result = save_config(config)
    if "error" in result:
        return c("red", f"❌ Error: {result['error']}")
    return c("green", f"✅ Skill '{skill}' → {tier}")


def cmd_list(which: str = "all") -> str:
    config = load_config()
    tiers = config.get("tiers", {})
    skills_default = config.get("skills", {})
    overrides = config.get("overrides", {})
    skill_overrides = overrides.get("skills", {})
    agent_overrides = overrides.get("agents", {})

    agent_tier_map = {
        "data-analyst": "T1-ultra-fast",
        "data-explorer": "T1-ultra-fast",
        "data-cleaner": "T1-ultra-fast",
        "data-modeler": "T4-reasoning",
        "data-reporter": "T1-ultra-fast",
        "data-design": "T4-reasoning",
        "data-etl": "T1-ultra-fast",
        "data-validator": "T1-ultra-fast",
        "data-verify": "T4-reasoning",
        "data-archive": "T1-ultra-fast",
        "data-orchestrator": "T1-ultra-fast",
        "gentle-orchestrator": "T4-reasoning",
    }

    output = []
    output.append(f"{c(BOLD, '═══ CONFIGURACIÓN DE MODELOS ═══')}\n")

    if which in ("all", "skills"):
        output.append(c(BOLD, "SKILLS:"))
        output.append(f"  {'Skill':<30} {'Tier':<10} {'Estado'}")
        output.append(f"  {'─' * 30} {'─' * 10} {'─' * 10}")
        for skill, default_tier in sorted(skills_default.items()):
            tier = skill_overrides.get(skill, default_tier)
            tier_key = tier if tier in tiers else "T3-balanced"
            is_ov = c("magenta", "⚡ override") if skill in skill_overrides else c("dim", "default")
            color = TIER_COLORS.get(tier_key, "")
            output.append(f"  {c('yellow', skill):<30} {c(color, tier_key):<10} {is_ov}")
        output.append("")

    if which in ("all", "agents"):
        output.append(c(BOLD, "AGENTES:"))
        output.append(f"  {'Agente':<30} {'Tier':<10} {'Estado'}")
        output.append(f"  {'─' * 30} {'─' * 10} {'─' * 10}")
        for agent, default_tier in sorted(agent_tier_map.items()):
            tier = agent_overrides.get(agent, default_tier)
            is_ov = c("magenta", "⚡ override") if agent in agent_overrides else c("dim", "default")
            color = TIER_COLORS.get(tier, "")
            output.append(f"  {c('blue', agent):<30} {c(color, tier):<10} {is_ov}")

    return "\n".join(output)


def cmd_reset(entity: str, name: str) -> str:
    config = load_config()
    overrides = config.get("overrides", {})
    target = overrides.get(entity + "s", {})

    if name not in target:
        return c("yellow", f"⚠ {entity.capitalize()} '{name}' no tiene override")

    del target[name]
    save_config(config)
    return c("green", f"✅ {entity.capitalize()} '{name}' volvió al default")


def cmd_tiers() -> str:
    config = load_config()
    tiers = config.get("tiers", {})

    output = [c(BOLD, "═══ TIERS DISPONIBLES ═══"), ""]
    for name, data in tiers.items():
        color = TIER_COLORS.get(name, "")
        model = data.get("model", "?")
        desc = data.get("description", "")
        output.append(f"{c(color, '●')} {c(BOLD, name)} — {model}")
        if desc:
            output.append(f"   {c('dim', desc)}")
        output.append("")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Comandos /model para OpenCode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # /model set agent <agent> <tier>
    set_agent = sub.add_parser("set-agent", help="Asignar tier a un agente")
    set_agent.add_argument("agent", help="Nombre del agente")
    set_agent.add_argument("tier", help="Tier (T1-T5)")

    # /model set skill <skill> <tier>
    set_skill = sub.add_parser("set-skill", help="Asignar tier a una skill")
    set_skill.add_argument("skill", help="Nombre de la skill")
    set_skill.add_argument("tier", help="Tier (T1-T5)")

    # /model list [skills|agents]
    lst = sub.add_parser("list", help="Listar configuración")
    lst.add_argument("which", nargs="?", default="all", choices=["all", "skills", "agents"])

    # /model reset agent <name>
    reset_a = sub.add_parser("reset-agent", help="Resetear agente al default")
    reset_a.add_argument("agent", help="Nombre del agente")

    # /model reset skill <name>
    reset_s = sub.add_parser("reset-skill", help="Resetear skill al default")
    reset_s.add_argument("skill", help="Nombre de la skill")

    # /model tiers
    sub.add_parser("tiers", help="Ver tiers disponibles")

    args = parser.parse_args()

    if args.command == "set-agent":
        print(cmd_set_agent(args.agent, args.tier))
    elif args.command == "set-skill":
        print(cmd_set_skill(args.skill, args.tier))
    elif args.command == "list":
        print(cmd_list(args.which))
    elif args.command == "reset-agent":
        print(cmd_reset("agent", args.agent))
    elif args.command == "reset-skill":
        print(cmd_reset("skill", args.skill))
    elif args.command == "tiers":
        print(cmd_tiers())
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
