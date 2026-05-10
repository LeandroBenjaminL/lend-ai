#!/usr/bin/env python3
"""
Model Picker - Selector interactivo de modelos para OpenCode.

Muestra una lista de modelos organizados por precio y te deja elegir.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = BASE_DIR / "model-routing.config.json"


def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config()
    tiers = config.get("tiers", {})
    skills = config.get("skills", {})

    if len(sys.argv) < 2:
        print("=" * 60)
        print("🎯 SELECCIONAR MODELO PARA SKILL")
        print("=" * 60)
        print("\n📋 Uso: python model-picker.py <skill>")
        print("\n📌 Skills disponibles:")
        for skill in sorted(skills.keys()):
            tier = skills[skill]
            model = tiers.get(tier, {}).get("model", "N/A")
            cost = tiers.get(tier, {}).get("cost", "")
            print(f"   {skill:30} → {model} ({cost})")
        return

    skill = sys.argv[1]
    if skill not in skills:
        print(f"❌ Skill '{skill}' no encontrada")
        print(f"📌 Disponibles: {', '.join(sorted(skills.keys()))}")
        return

    current_tier = skills[skill]
    current_model = tiers.get(current_tier, {}).get("model", "N/A")

    print(f"\n🎯 Skill: {skill}")
    print(f"   Modelo actual: {current_model} ({current_tier})")
    print("\n" + "=" * 60)
    print("📦 MODELOS DISPONIBLES")
    print("=" * 60)

    free_tiers = []
    low_tiers = []
    medium_tiers = []
    high_tiers = []

    for tier_name, tier_info in tiers.items():
        cost = tier_info.get("cost", "")
        if cost == "free":
            free_tiers.append((tier_name, tier_info))
        elif cost == "low":
            low_tiers.append((tier_name, tier_info))
        elif cost == "medium":
            medium_tiers.append((tier_name, tier_info))
        elif cost == "high":
            high_tiers.append((tier_name, tier_info))

    opciones = []
    idx = 1

    if free_tiers:
        print("\n🆓 FREE (0 tokens)")
        for tier_name, tier_info in free_tiers:
            model = tier_info.get("model", "")
            desc = tier_info.get("description", "")[:50]
            marker = "← ACTUAL" if tier_name == current_tier else ""
            print(f"   {idx}. {model} {marker}")
            print(f"      {desc}")
            opciones.append(tier_name)
            idx += 1

    if low_tiers:
        print("\n💵 LOW ($0.05-$0.30)")
        for tier_name, tier_info in low_tiers:
            model = tier_info.get("model", "")
            desc = tier_info.get("description", "")[:50]
            marker = "← ACTUAL" if tier_name == current_tier else ""
            print(f"   {idx}. {model} {marker}")
            print(f"      {desc}")
            opciones.append(tier_name)
            idx += 1

    if medium_tiers:
        print("\n💰 MEDIUM ($0.20-$0.60)")
        for tier_name, tier_info in medium_tiers:
            model = tier_info.get("model", "")
            desc = tier_info.get("description", "")[:50]
            marker = "← ACTUAL" if tier_name == current_tier else ""
            print(f"   {idx}. {model} {marker}")
            print(f"      {desc}")
            opciones.append(tier_name)
            idx += 1

    if high_tiers:
        print("\n💎 HIGH ($0.50+)")
        for tier_name, tier_info in high_tiers:
            model = tier_info.get("model", "")
            desc = tier_info.get("description", "")[:50]
            marker = "← ACTUAL" if tier_name == current_tier else ""
            print(f"   {idx}. {model} {marker}")
            print(f"      {desc}")
            opciones.append(tier_name)
            idx += 1

    print("\n" + "=" * 60)
    choice = input("👉 Elegí un número (o Enter para cancelar): ").strip()

    if not choice:
        print("❌ Cancelado")
        return

    try:
        num = int(choice)
        if num < 1 or num > len(opciones):
            print(f"❌ Número inválido. Elegí entre 1 y {len(opciones)}")
            return

        nuevo_tier = opciones[num - 1]
        nuevo_model = tiers[nuevo_tier].get("model", "")

        skills[skill] = nuevo_tier
        config["skills"] = skills

        with open(CONFIG, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Cambiado: {skill} → {nuevo_model}")

    except ValueError:
        print("❌输入 inválido")


if __name__ == "__main__":
    main()
