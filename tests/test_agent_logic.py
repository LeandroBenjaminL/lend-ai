"""
Tests de LÓGICA del ecosistema de agentes — no solo validez YAML,
sino consistencia semántica: skills existen, permisos son válidos,
reglas de enseñanza/engram/docs están definidas en skills críticas.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENCODE_JSON = REPO_ROOT / "opencode.json"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


def _load_opencode() -> dict:
    with open(OPENCODE_JSON, encoding="utf-8-sig") as f:
        return json.load(f)


def _get_agent_names(opencode: dict) -> set[str]:
    return set(opencode.get("agent", {}).keys())


def _get_skill_folder_names(skills_dir: Path) -> set[str]:
    return {d.name for d in skills_dir.iterdir() if d.is_dir()}


def _read_skill_content(skills_dir: Path, skill_name: str) -> str:
    path = skills_dir / skill_name / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"{path} no existe")
    return path.read_text(encoding="utf-8")


class TestAgentSkills:
    """Skills referenciadas en agentes deben existir como carpetas en skills/."""

    def test_agents_have_skills(self, skills_dir: Path):
        opencode = _load_opencode()
        skill_folders = _get_skill_folder_names(skills_dir)
        errors = []

        for agent_name, config in opencode.get("agent", {}).items():
            for skill in config.get("skills", []):
                if skill not in skill_folders:
                    errors.append(
                        f"'{agent_name}' referencia skill '{skill}' "
                        f"que no existe como carpeta en skills/"
                    )

        assert not errors, "\n".join(errors)

    def test_skills_in_opencode_exist(self, skills_dir: Path):
        """Cada skill referenciada en opencode.json debe tener su SKILL.md."""
        opencode = _load_opencode()
        errors = []

        for agent_name, config in opencode.get("agent", {}).items():
            for skill in config.get("skills", []):
                skill_path = skills_dir / skill / "SKILL.md"
                if not skill_path.exists():
                    errors.append(
                        f"'{agent_name}' referencia skill '{skill}' "
                        f"que no tiene SKILL.md en skills/{skill}/"
                    )

        assert not errors, "\n".join(errors)


class TestAgentDefinitions:
    """Agentes en opencode.json deben estar bien definidos."""

    def test_no_empty_agents(self):
        opencode = _load_opencode()
        errors = []

        for agent_name, config in opencode.get("agent", {}).items():
            desc = config.get("description", "")
            if not desc or not desc.strip():
                errors.append(f"'{agent_name}': description está vacía")

            tools = config.get("tools", {}) or {}
            if not tools:
                errors.append(f"'{agent_name}': tools está vacío")

        assert not errors, "\n".join(errors)


class TestPermissionConsistency:
    """Permisos de tarea deben referenciar agentes existentes."""

    def test_agent_permission_consistency(self):
        opencode = _load_opencode()
        agent_names = _get_agent_names(opencode)
        errors = []

        for agent_name, config in opencode.get("agent", {}).items():
            tasks = config.get("permission", {}).get("task", {})
            for target in tasks:
                if target == "*":
                    continue
                if target not in agent_names:
                    errors.append(
                        f"'{agent_name}' tiene permission.task ref a "
                        f"'{target}' que no existe como agente en opencode.json"
                    )

        assert not errors, "\n".join(errors)


class TestN1SkillsCompleteness:
    """Los N1 skills listados en AGENTS.md deben estar en el array skills de lend-ai."""

    def test_n1_skills_complete(self):
        opencode = _load_opencode()
        lend_ai_skills = set(
            opencode.get("agent", {}).get("lend-ai", {}).get("skills", [])
        )
        n1_skills = self._extract_n1_skills()

        known_missing_allowed = {"lend-ai-workflow"}
        missing = n1_skills - lend_ai_skills - known_missing_allowed

        assert not missing, (
            f"N1 skills de AGENTS.md no están en lend-ai agent: {sorted(missing)}. "
            f"Nota: {known_missing_allowed} se carga desde profiles/, no desde skills array."
        )

    @staticmethod
    def _extract_n1_skills() -> set[str]:
        """Extrae nombres de skills de la tabla N1 en AGENTS.md."""
        skills = set()
        with open(AGENTS_MD, encoding="utf-8") as f:
            lines = f.readlines()

        in_n1 = False
        for line in lines:
            stripped = line.strip()
            if "### N1" in stripped and ("Skills de Sistema" in stripped):
                in_n1 = True
                continue
            if not in_n1:
                continue
            if "###" in stripped:
                break
            if "| `" in stripped or stripped.startswith("|`"):
                # Extract backtick-quoted skill names inside the table
                parts = stripped.split("`")
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        name = part.strip()
                        if name:
                            skills.add(name)

        return skills


class TestTeachingRules:
    """Skills de persona y mentor deben contener reglas de enseñanza."""

    TEACHING_PATTERNS = ["profesor", "gate", "ensen", "enseñ", "mentor"]
    TARGET_SKILLS = ["lend-ai-persona", "lend-ai-mentor"]

    def test_teaching_rules_defined(self, skills_dir: Path):
        errors = []
        for skill_name in self.TARGET_SKILLS:
            try:
                content = _read_skill_content(skills_dir, skill_name).lower()
            except FileNotFoundError as e:
                errors.append(str(e))
                continue

            found = [p for p in self.TEACHING_PATTERNS if p in content]
            if not found:
                errors.append(
                    f"{skill_name}/SKILL.md no contiene ningún patrón de enseñanza: "
                    f"{sorted(self.TEACHING_PATTERNS)}"
                )
        assert not errors, "\n".join(errors)


class TestEngramRules:
    """Skills críticas deben contener referencias a Engram."""

    ENGRAM_PATTERNS = ["mem_save", "engram", "topic_key", "mem_context", "mem_search"]
    TARGET_SKILLS = ["lend-ai-persona", "lend-ai-engram", "engram-memory-system"]

    def test_engram_rules_defined(self, skills_dir: Path):
        errors = []
        for skill_name in self.TARGET_SKILLS:
            try:
                content = _read_skill_content(skills_dir, skill_name).lower()
            except FileNotFoundError as e:
                errors.append(str(e))
                continue

            found = [p for p in self.ENGRAM_PATTERNS if p in content]
            if not found:
                errors.append(
                    f"{skill_name}/SKILL.md no contiene ningún patrón de Engram: "
                    f"{sorted(self.ENGRAM_PATTERNS)}"
                )
        assert not errors, "\n".join(errors)


class TestDocsRules:
    """Post-task docs review debe estar referenciado en skills críticas y workflow."""

    TARGET_FILES = [
        "skills/lend-ai-persona/SKILL.md",
        "skills/lend-ai-docs/SKILL.md",
        "profiles/lend-ai/workflow.md",
    ]

    def test_docs_rules_defined(self):
        errors = []
        for rel_path in self.TARGET_FILES:
            path = REPO_ROOT / rel_path
            if not path.exists():
                errors.append(f"{rel_path} no existe")
                continue

            content = path.read_text(encoding="utf-8").lower()

            if "docs review" not in content:
                errors.append(
                    f"{rel_path} no contiene 'docs review' (post-task docs check)"
                )

        assert not errors, "\n".join(errors)
