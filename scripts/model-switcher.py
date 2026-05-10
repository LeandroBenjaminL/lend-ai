#!/usr/bin/env python3
"""
model-switcher.py ── TUI interactivo para cambiar modelos por agente/skill.

Abrilo con Ctrl+P en OpenCode y elegí visualmente qué modelo usar
en cada skill o sub-agente. Cambia en caliente, persiste a config.

Usage:
    python3 scripts/model-switcher.py
    /model-switch  (desde OpenCode)

Requiere: Python 3.10+, model-router.py, model-routing.config.json
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# ── ANSI Colors ────────────────────────────────────────────────────────────

C = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bg_black": "\033[40m",
}


def c(color: str, text: str) -> str:
    return f"{C.get(color, '')}{text}{C['reset']}"


# ── Paths ──────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTER = BASE_DIR / "mcp-servers" / "model-router.py"
CONFIG = BASE_DIR / "model-routing.config.json"

TIER_COLORS = {
    "T1-ultra-fast": "green",
    "T2-fast": "blue",
    "T3-balanced": "yellow",
    "T4-reasoning": "magenta",
    "T5-deep": "red",
}

TIER_SHORT = {
    "T1-ultra-fast": "T1",
    "T2-fast": "T2",
    "T3-balanced": "T3",
    "T4-reasoning": "T4",
    "T5-deep": "T5",
}


# ── Data loading ────────────────────────────────────────────────────────────


def load_config() -> dict:
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def run_router(*args: str) -> dict:
    """Ejecuta model-router.py en modo CLI y devuelve JSON parseado."""
    try:
        result = subprocess.run(
            ["python3", str(ROUTER), *args],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.stdout.strip():
            return json.loads(result.stdout.strip())
        return {"error": result.stderr.strip()}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        return {"error": str(e)}


def clear():
    os.system("clear 2>/dev/null || cls 2>/dev/null")


# ── Display helpers ─────────────────────────────────────────────────────────


def print_header():
    print()
    print(c("bold", c("cyan", "╔══════════════════════════════════════════════════════╗")))
    title = "  🎯 MODEL SWITCHER — Orquestador de Modelos TUI  "
    print(c("bold", c("cyan", "║")), c("bold", c("yellow", title)), c("bold", c("cyan", "║")))
    print(c("bold", c("cyan", "╚══════════════════════════════════════════════════════╝")))
    print()
    print(c("dim", "  Elegí qué modelo usar para cada skill o sub-agente."))
    print(c("dim", "  Los cambios persisten en model-routing.config.json"))
    print()


def tier_tag(tier_name: str) -> str:
    """Devuelve T3 🔵 DeepSeek Medium estilizado."""
    short = TIER_SHORT.get(tier_name, tier_name)
    color = TIER_COLORS.get(tier_name, "white")
    return f"{c(color, '●')} {c('bold', short)}"


def model_name(tier_entry: dict) -> str:
    """Nombre humano del modelo para un tier."""
    name = tier_entry.get("model", "?")
    # Friendly names
    mapping = {
        "minimax-free": "Minimax Free",
        "minimax": "Minimax",
        "deepseek-medium": "DeepSeek Medium",
        "deepseek-pro": "DeepSeek Pro",
        "deepseek-pro-max": "DeepSeek Pro Max",
    }
    return mapping.get(name, name)


def tier_row(name: str, tier_info: dict) -> str:
    return (
        f"  {tier_tag(name)}  {c('dim', '→')}  "
        f"{c('bold', model_name(tier_info))}  "
        f"{c('dim', '(' + tier_info.get('description', '') + ')')}"
    )


# ── Main views ──────────────────────────────────────────────────────────────


def show_main_menu(config: dict, overrides: dict):
    """Pantalla principal: resumen de skills + agentes + tiers disponibles."""
    print_header()

    tiers = config.get("tiers", {})

    # Tiers disponibles
    print(c("bold", "═══ TIERS DISPONIBLES ═══"))
    print()
    for tname, tdata in tiers.items():
        print(tier_row(tname, tdata))
    print()

    # Overrides activos
    skill_overrides = overrides.get("skills", {})
    agent_overrides = overrides.get("agents", {})
    total_overrides = len(skill_overrides) + len(agent_overrides)

    print(c("bold", f"═══ OVERRIDES ACTIVOS ({total_overrides}) ═══"))
    print()
    if skill_overrides:
        print(c("cyan", "  Skills:"))
        for skill, tier in sorted(skill_overrides.items()):
            color = TIER_COLORS.get(tier, "white")
            short = TIER_SHORT.get(tier, tier)
            model = model_name(tiers.get(tier, {}))
            print(f"    {c('yellow', skill)} → {c(color, short)} {c('dim', model)}")
    if agent_overrides:
        print(c("cyan", "  Agentes:"))
        for agent, tier in sorted(agent_overrides.items()):
            color = TIER_COLORS.get(tier, "white")
            short = TIER_SHORT.get(tier, tier)
            model = model_name(tiers.get(tier, {}))
            print(f"    {c('blue', agent)} → {c(color, short)} {c('dim', model)}")
    if not skill_overrides and not agent_overrides:
        print(c("dim", "  (ninguno — todo en default según models.json)"))
    print()

    # Default skills
    skills_config = config.get("skills", {})
    if skills_config:
        print(c("bold", "═══ SKILLS (defaults) ═══"))
        print()
        for skill, tier in sorted(skills_config.items()):
            color = TIER_COLORS.get(tier, "white")
            short = TIER_SHORT.get(tier, tier)
            overridden = " ⚡" if skill in skill_overrides else ""
            model = model_name(tiers.get(tier, {}))
            tag = f"{c(color, short):<6}"
            extra = f"{c('dim', model)}{c('magenta', overridden)}"
            print(f"  {c('yellow', skill):<30} {tag} {extra}")
        print()

    print(c("bold", "═══ ACCIONES ═══"))
    print()
    print(f"  [{c('yellow', 's')}]  Cambiar modelo de una {c('yellow', 'skill')}")
    print(f"  [{c('blue', 'a')}]  Cambiar modelo de un {c('blue', 'agente')}")
    print(f"  [{c('green', 'l')}]  Listar todas las skills y agentes con su modelo")
    print(f"  [{c('magenta', 'r')}]  Resetear un override")
    print(f"  [{c('red', 'q')}]  Salir")
    print()


def pick_skill(config: dict):
    """Seleccionar skill y cambiarle el tier."""
    clear()
    print_header()
    skills_config = config.get("skills", {})
    overrides = config.get("overrides", {}).get("skills", {})
    tiers = config.get("tiers", {})

    skills_list = sorted(skills_config.keys())
    print(c("bold", "Seleccioná la skill:"))
    print()
    for i, skill in enumerate(skills_list, 1):
        default_tier = skills_config[skill]
        current_tier = overrides.get(skill, default_tier)
        color = TIER_COLORS.get(current_tier, "white")
        short = TIER_SHORT.get(current_tier, current_tier)
        marker = c("magenta", " ⚡") if skill in overrides else ""
        model = model_name(tiers.get(current_tier, {}))
        rest = f"{c(color, short)} {c('dim', model)}{marker}"
        print(f"  [{c('yellow', str(i))}] {c('yellow', skill):<30} → {rest}")
    print()
    print(f"  [{c('red', '0')}] Volver")
    print()

    try:
        choice = input(f"{c('cyan', '►')} ").strip()
        if choice == "0" or choice == "":
            return
        idx = int(choice) - 1
        if 0 <= idx < len(skills_list):
            skill = skills_list[idx]
            pick_tier(config, "skill", skill)
    except (ValueError, IndexError):
        pass


def pick_agent(config: dict):
    """Seleccionar agente desde manifests y cambiarle el tier."""
    clear()
    print_header()

    # Obtener agentes desde model-router
    result = run_router("list")
    agents_list = sorted(result.get("agents", []))
    if not agents_list:
        print(c("red", "  No se encontraron agentes."))
        input(c("dim", "\n  Enter para volver..."))
        return

    overrides = config.get("overrides", {}).get("agents", {})
    tiers = config.get("tiers", {})

    print(c("bold", "Seleccioná el agente:"))
    print()
    for i, a in enumerate(agents_list, 1):
        name = a.get("agent", "?")
        current_tier = overrides.get(name, a.get("tier", "T3-balanced"))
        color = TIER_COLORS.get(current_tier, "white")
        short = TIER_SHORT.get(current_tier, current_tier)
        marker = c("magenta", " ⚡") if name in overrides else ""
        model = model_name(tiers.get(current_tier, {}))
        rest = f"{c(color, short)} {c('dim', model)}{marker}"
        print(f"  [{c('blue', str(i))}] {c('blue', name):<30} → {rest}")
    print()
    print(f"  [{c('red', '0')}] Volver")
    print()

    try:
        choice = input(f"{c('cyan', '►')} ").strip()
        if choice == "0" or choice == "":
            return
        idx = int(choice) - 1
        if 0 <= idx < len(agents_list):
            agent = agents_list[idx].get("agent", "")
            if agent:
                pick_tier(config, "agent", agent)
    except (ValueError, IndexError):
        pass


def pick_tier(config: dict, entity_type: str, entity_name: str):
    """Mostrar tiers disponibles y seleccionar uno."""
    clear()
    print_header()

    tiers = config.get("tiers", {})
    overrides = config.get("overrides", {}).get(
        "skills" if entity_type == "skill" else "agents", {}
    )
    current = overrides.get(
        entity_name,
        config.get("skills", {}).get(entity_name, "T3-balanced"),
    )

    label = c("yellow", entity_name) if entity_type == "skill" else c("blue", entity_name)
    print(c("bold", f"Asignar modelo a {entity_type}: {label}"))
    print(c("dim", f"  Actual: {tier_tag(current)} {model_name(tiers.get(current, {}))}"))
    print()

    tier_keys = list(tiers.keys())
    for i, tname in enumerate(tier_keys, 1):
        tdata = tiers[tname]
        print(f"  [{c('cyan', str(i))}] {tier_row(tname, tdata)}")
    print()
    print(f"  [{c('red', '0')}] Cancelar")
    print()

    try:
        choice = input(f"{c('cyan', '►')} ").strip()
        if choice == "0" or choice == "":
            return
        idx = int(choice) - 1
        if 0 <= idx < len(tier_keys):
            selected_tier = tier_keys[idx]

            # Persistir
            if entity_type == "skill":
                result = run_router("set-skill-tier", entity_name, selected_tier)
            else:
                result = run_router("set-agent-tier", entity_name, selected_tier)

            if "error" in result:
                print()
                print(c("red", f"  ❌ Error: {result['error']}"))
                input(c("dim", "\n  Enter para continuar..."))
                return

            print()
            new_model = model_name(tiers.get(selected_tier, {}))
            msg = f"  ✅ {entity_type} '{entity_name}' → {tier_tag(selected_tier)} {new_model}"
            print(c("green", msg))
            print(c("dim", "  Guardado en model-routing.config.json"))
            input(c("dim", "\n  Enter para continuar..."))
    except (ValueError, IndexError):
        pass


def reset_override(config: dict):
    """Resetear un override individual."""
    clear()
    print_header()

    skill_ov = config.get("overrides", {}).get("skills", {})
    agent_ov = config.get("overrides", {}).get("agents", {})
    tiers: dict = config.get("tiers", {})  # noqa: F841

    items = []
    for skill, tier in sorted(skill_ov.items()):
        items.append(("skill", skill, tier))
    for agent, tier in sorted(agent_ov.items()):
        items.append(("agent", agent, tier))

    if not items:
        print(c("dim", "  No hay overrides activos para resetear."))
        input(c("dim", "\n  Enter para volver..."))
        return

    print(c("bold", "Seleccioná el override a resetear:"))
    print()
    for i, (etype, ename, tier) in enumerate(items, 1):
        color = TIER_COLORS.get(tier, "white")
        short = TIER_SHORT.get(tier, tier)
        icon = c("yellow", "⬢") if etype == "skill" else c("blue", "⬡")
        print(
            f"  [{c('magenta', str(i))}] {icon} {c('bold', ename):<30} {c(color, short)} → default"
        )  # noqa: E501
    print()
    print(f"  [{c('red', '0')}] Cancelar")
    print()

    try:
        choice = input(f"{c('cyan', '►')} ").strip()
        if choice == "0" or choice == "":
            return
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            etype, ename, _ = items[idx]
            if etype == "skill":
                result = run_router("reset-skill-tier", ename)
            else:
                result = run_router("reset-agent-tier", ename)

            if "error" in result:
                print()
                print(c("red", f"  ❌ Error: {result['error']}"))
            else:
                print()
                print(c("green", f"  ✅ {etype} '{ename}' vuelve al tier default"))
            input(c("dim", "\n  Enter para continuar..."))
    except (ValueError, IndexError):
        pass


def list_all_view(config: dict):
    """Vista completa de skills + agentes con modelos."""
    clear()
    print_header()

    tiers = config.get("tiers", {})
    skill_overrides = config.get("overrides", {}).get("skills", {})
    agent_overrides = config.get("overrides", {}).get("agents", {})

    # Skills
    skills_config = config.get("skills", {})
    print(c("bold", "═══ SKILLS ═══"))
    print()
    print(f"  {'SKILL':<30} {'TIER':<8} {'MODELO':<20} {'ESTADO'}")
    print(f"  {'─' * 30} {'─' * 8} {'─' * 20} {'─' * 10}")
    for skill, tier in sorted(skills_config.items()):
        actual = skill_overrides.get(skill, tier)
        color = TIER_COLORS.get(actual, "white")
        short = TIER_SHORT.get(actual, actual)
        status = c("magenta", "⚡ overridden") if skill in skill_overrides else c("dim", "default")
        model = model_name(tiers.get(actual, {}))
        print(f"  {c('yellow', skill):<30} {c(color, short):<8} {model:<20} {status}")

    # Agents from router
    result = run_router("list")
    agents_list = sorted(result.get("agents", []), key=lambda x: x.get("agent", ""))
    if agents_list:
        print()
        print(c("bold", "═══ AGENTES ═══"))
        print()
        print(f"  {'AGENTE':<30} {'TIER':<8} {'MODELO':<20} {'ESTADO'}")
        print(f"  {'─' * 30} {'─' * 8} {'─' * 20} {'─' * 10}")
        for a in agents_list:
            name = a.get("agent", "?")
            default_tier = a.get("tier", "T3-balanced")
            actual = agent_overrides.get(name, default_tier)
            color = TIER_COLORS.get(actual, "white")
            short = TIER_SHORT.get(actual, actual)
            status = (
                c("magenta", "⚡ overridden") if name in agent_overrides else c("dim", "default")
            )  # noqa: E501
            model = model_name(tiers.get(actual, {}))
            print(f"  {c('blue', name):<30} {c(color, short):<8} {model:<20} {status}")

    print()
    input(c("dim", "  Enter para volver..."))


# ── Main loop ───────────────────────────────────────────────────────────────


def main():
    if not CONFIG.exists():
        print(c("red", f"❌ No se encuentra {CONFIG}"))
        sys.exit(1)

    config = load_config()

    while True:
        clear()
        overrides = config.get("overrides", {"skills": {}, "agents": {}})
        show_main_menu(config, overrides)

        try:
            choice = input(f"{c('cyan', '►')} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice in ("q", "quit", "exit"):
            print()
            print(c("green", "Hasta luego. 🚀"))
            break
        elif choice == "s":
            pick_skill(config)
            config = load_config()  # recargar después de cambios
        elif choice == "a":
            pick_agent(config)
            config = load_config()
        elif choice == "l":
            list_all_view(config)
        elif choice == "r":
            reset_override(config)
            config = load_config()
        elif choice == "":
            continue


if __name__ == "__main__":
    main()
