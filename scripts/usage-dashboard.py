#!/usr/bin/env python3
"""Lend.Ai Usage Dashboard - analyzes Engram SQLite DB for usage patterns."""

import sqlite3
import sys
from datetime import datetime, timedelta, timezone

ENGRAM_DB = r"C:\Users\leand\.engram\engram.db"

BOX_W = 60


HDR = "#" * BOX_W


def fmt_box(title: str) -> str:
    return f"\n{HDR}\n  {title}\n{HDR}\n"


def try_query(db, sql, params=()):
    try:
        c = db.cursor()
        c.execute(sql, params)
        return c.fetchall()
    except Exception as e:
        print(f"  [WARN] query failed: {e}")
        return []


def build_report(db):
    output = []

    def out(line=""):
        output.append(line)

    out(fmt_box("LEND.AI USAGE DASHBOARD"))

    # ── Sessions ──
    out("SESSIONES")
    total_sessions = try_query(db, "SELECT COUNT(*) FROM sessions")
    total_s = total_sessions[0][0] if total_sessions else 0
    out(f"  Total: {total_s}")

    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    recent = try_query(db, "SELECT COUNT(*) FROM sessions WHERE started_at >= ?", (week_ago,))
    recent_s = recent[0][0] if recent else 0
    out(f"  Ultimos 7 dias: {recent_s}")

    # Sessions per week approximation
    rows = try_query(
        db, "SELECT started_at FROM sessions WHERE started_at IS NOT NULL ORDER BY started_at"
    )
    if len(rows) >= 2:
        try:
            first = datetime.fromisoformat(rows[0][0])
            last = datetime.fromisoformat(rows[-1][0])
            weeks = max((last - first).days / 7, 1)
            avg = round(total_s / weeks, 1)
        except Exception:
            avg = "N/A"
    else:
        avg = "N/A"
    out(f"  Promedio por semana: {avg}")

    # ── Most Active Areas ──
    out("\nAREAS MAS ACTIVAS (por observaciones)")
    active = try_query(
        db,
        "SELECT topic_key, COUNT(*) as cnt FROM observations "
        "WHERE topic_key IS NOT NULL AND topic_key != '' "
        "GROUP BY topic_key ORDER BY cnt DESC LIMIT 10",
    )
    if active:
        for i, (key, cnt) in enumerate(active, 1):
            out(f"  {i}. {key} - {cnt} obs")
    else:
        out("  (sin topic_keys asignados aun)")

    # ── Least Active Areas ──
    out("\nAREAS MENOS ACTIVAS")
    least = try_query(
        db,
        "SELECT topic_key, COUNT(*) as cnt FROM observations "
        "WHERE topic_key IS NOT NULL AND topic_key != '' "
        "GROUP BY topic_key ORDER BY cnt ASC LIMIT 5",
    )
    if least:
        for key, cnt in least:
            label = " (dead weight)" if cnt == 0 else ""
            out(f"  {key} - {cnt} obs{label}")
    else:
        out("  (sin topic_keys asignados aun)")

    # ── Observation Types ──
    out("\nTIPOS DE OBSERVACION")
    types = try_query(
        db, "SELECT type, COUNT(*) as cnt FROM observations GROUP BY type ORDER BY cnt DESC"
    )
    if types:
        for t, cnt in types:
            out(f"  {t}: {cnt}")

    # ── Session timeline ──
    out("\nSESIONES EN EL TIEMPO")
    timeline = try_query(
        db,
        "SELECT DATE(started_at) as d, COUNT(*) as cnt FROM sessions "
        "WHERE started_at IS NOT NULL GROUP BY d ORDER BY d",
    )
    if timeline:
        for d, cnt in timeline:
            bar = "#" * cnt
            out(f"  {d} | {bar} {cnt}")
    else:
        out("  (sin datos)")

    # ── Recommendations ──
    out("\nRECOMENDACIONES")
    zero_areas = try_query(
        db,
        "SELECT topic_key FROM observations "
        "WHERE topic_key IS NOT NULL AND topic_key != '' "
        "GROUP BY topic_key HAVING COUNT(*) = 0",
    )
    zero_count = len(zero_areas)
    if active:
        top_key, top_cnt = active[0]
        out(f"  - {zero_count} areas tienen 0 observaciones - considerar eliminar o consolidar")
        out(f"  - Top area '{top_key}' ({top_cnt} obs) es la mas activa - enfocar aqui")
    else:
        out(f"  - {zero_count} areas tienen 0 observaciones - considerar eliminar o consolidar")
        out("  - No hay areas con observaciones aun")

    # Total obs count
    total_obs = try_query(db, "SELECT COUNT(*) FROM observations")
    out(f"\n  Total de observaciones: {total_obs[0][0] if total_obs else 0}")

    return "\n".join(output)


def main():
    try:
        db = sqlite3.connect(ENGRAM_DB)
        db.execute("PRAGMA journal_mode=WAL")
    except sqlite3.Error as e:
        print(f"  [ERROR] No se pudo conectar a la base de datos Engram: {e}")
        print(f"  Ruta: {ENGRAM_DB}")
        sys.exit(1)

    # Check if observations table exists
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='observations'")
    if not cursor.fetchone():
        print(fmt_box("LEND.AI USAGE DASHBOARD"))
        print("  Engram database structure unknown - run after some sessions")
        print(f"  Base de datos en: {ENGRAM_DB}")
        print("\n  Tablas disponibles:")
        for t in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
            print(f"    - {t[0]}")
        db.close()
        sys.exit(0)

    report = build_report(db)
    print(report)

    db.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
