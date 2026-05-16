"""Tests for agent-level contracts and skill registration."""

from pathlib import Path


def test_lend_ai_delegation_skill_exists():
    """Delegation skill must have a SKILL.md."""
    skill_path = Path("skills/lend-ai-delegation/SKILL.md")
    assert skill_path.exists(), "lend-ai-delegation SKILL.md not found"


def test_lend_ai_delegation_registered_in_agents_md():
    """Delegation skill must be referenced in AGENTS.md."""
    content = Path("AGENTS.md").read_text(encoding="utf-8")
    assert "lend-ai-delegation" in content, \
        "lend-ai-delegation not registered in AGENTS.md"


def test_engram_backup_in_update_sh():
    """update.sh must have Engram backup step."""
    content = Path("update.sh").read_text(encoding="utf-8")
    assert "engram.db.bak" in content, \
        "update.sh missing Engram backup"
    assert "Backup Engram" in content or "backup" in content.lower(), \
        "update.sh missing backup comment"
