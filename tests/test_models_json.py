"""
Tests de validación del archivo models.json.

Verifica la estructura, secciones obligatorias, tiers, agentes
y consistencia interna del catálogo de modelos.
"""

from typing import Any

# ── Tests ────────────────────────────────────────────────────────────────────


class TestModelsJsonStructure:
    """Pruebas de estructura general de models.json."""

    def test_models_json_is_valid_json(self, models_data: dict[str, Any]) -> None:
        """models.json se puede parsear correctamente (ya se cargó en la fixture)."""
        assert models_data is not None, "models.json no se pudo cargar"

    def test_models_json_has_required_sections(
        self, models_data: dict[str, Any]
    ) -> None:
        """models.json tiene las secciones obligatorias: ml_models, llm_models."""
        assert "ml_models" in models_data, "Falta la sección 'ml_models'"
        assert "llm_models" in models_data, "Falta la sección 'llm_models'"
        assert isinstance(models_data["ml_models"], list), (
            "'ml_models' debe ser una lista"
        )
        assert isinstance(models_data["llm_models"], dict), (
            "'llm_models' debe ser un dict"
        )

    def test_models_json_has_tiers(self, models_data: dict[str, Any]) -> None:
        """llm_models tiene la sección _tiers."""
        tiers = models_data.get("llm_models", {}).get("_tiers", {})
        assert len(tiers) > 0, "_tiers está vacío o no existe"
        # Verificar que hay al menos 5 tiers
        assert len(tiers) >= 5, (
            f"Se esperaban al menos 5 tiers, se encontraron {len(tiers)}"
        )


class TestTiers:
    """Pruebas de la sección _tiers."""

    def test_tiers_have_model_and_type(self, models_data: dict[str, Any]) -> None:
        """Cada tier tiene 'modelo' y 'tipo_tarea'."""
        tiers = models_data.get("llm_models", {}).get("_tiers", {})
        errors: list[str] = []

        for tier_key, tier_data in tiers.items():
            if "modelo" not in tier_data:
                errors.append(f"Tier '{tier_key}': falta 'modelo'")
            if "tipo_tarea" not in tier_data:
                errors.append(f"Tier '{tier_key}': falta 'tipo_tarea'")

        assert not errors, "\n".join(errors)

    def test_tier_names_are_consistent(self, models_data: dict[str, Any]) -> None:
        """Los nombres de tier siguen el patrón T<N>-<desc> o similar."""
        tiers = models_data.get("llm_models", {}).get("_tiers", {})
        errors: list[str] = []

        for tier_key in tiers:
            if not tier_key.startswith("T"):
                errors.append(f"Tier '{tier_key}' no empieza con 'T'")

        assert not errors, "\n".join(errors)

    def test_tier_ranges_are_valid(self, models_data: dict[str, Any]) -> None:
        """tier_range en cada agente solo contiene tiers que existen en _tiers."""
        llm = models_data.get("llm_models", {})
        tiers = set(llm.get("_tiers", {}).keys())
        errors: list[str] = []

        sections = [
            ("primary_agents", "agent"),
            ("sub_agents", "agent"),
        ]

        for section_key, name_field in sections:
            for entry in llm.get(section_key, []):
                name = entry.get(name_field, "unknown")
                tier_range = entry.get("tier_range", [])
                for t in tier_range:
                    if t not in tiers:
                        errors.append(
                            f"{section_key}/{name}: tier_range contiene '{t}' "
                            f"que no existe en _tiers ({tiers})"
                        )

        assert not errors, "\n".join(errors)


class TestPrimaryAgents:
    """Pruebas de primary_agents en models.json."""

    def test_primary_agents_have_tier(self, models_data: dict[str, Any]) -> None:
        """Todos los primary_agents tienen tier definido."""
        agents = models_data.get("llm_models", {}).get("primary_agents", [])
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            if not entry.get("tier"):
                errors.append(f"primary_agent '{name}': falta 'tier'")

        assert not errors, "\n".join(errors)

    def test_primary_agents_have_required_fields(
        self, models_data: dict[str, Any]
    ) -> None:
        """Todos los primary_agents tienen agent, role, recommended, tier."""
        agents = models_data.get("llm_models", {}).get("primary_agents", [])
        required = {"agent", "role", "recommended", "tier"}
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            missing = required - set(entry.keys())
            if missing:
                errors.append(f"primary_agent '{name}': faltan campos {missing}")

        assert not errors, "\n".join(errors)


class TestSubAgents:
    """Pruebas de sub_agents en models.json."""

    def test_sub_agents_have_tier(self, models_data: dict[str, Any]) -> None:
        """Todos los sub_agents tienen tier definido."""
        agents = models_data.get("llm_models", {}).get("sub_agents", [])
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            if not entry.get("tier"):
                errors.append(f"sub_agent '{name}': falta 'tier'")

        assert not errors, "\n".join(errors)

    def test_sub_agents_have_required_fields(self, models_data: dict[str, Any]) -> None:
        """Todos los sub_agents tienen agent, role, recommended, tier."""
        agents = models_data.get("llm_models", {}).get("sub_agents", [])
        required = {"agent", "role", "recommended", "tier"}
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            missing = required - set(entry.keys())
            if missing:
                errors.append(f"sub_agent '{name}': faltan campos {missing}")

        assert not errors, "\n".join(errors)


class TestSddAgents:
    """Pruebas de _sdd_subagents en models.json."""

    def test_sdd_agents_have_tier(self, models_data: dict[str, Any]) -> None:
        """Todos los SDD agents tienen tier definido."""
        agents = (
            models_data.get("llm_models", {})
            .get("_sdd_subagents", {})
            .get("agents", [])
        )
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            if not entry.get("tier"):
                errors.append(f"sdd_agent '{name}': falta 'tier'")

        assert not errors, "\n".join(errors)

    def test_sdd_agents_have_required_fields(self, models_data: dict[str, Any]) -> None:
        """Todos los SDD agents tienen al menos agent, tier."""
        agents = (
            models_data.get("llm_models", {})
            .get("_sdd_subagents", {})
            .get("agents", [])
        )
        errors: list[str] = []

        for entry in agents:
            name = entry.get("agent", "unknown")
            if not entry.get("agent"):
                errors.append("SDD agent sin campo 'agent'")
            if not entry.get("tier"):
                errors.append(f"sdd_agent '{name}': falta 'tier'")

        assert not errors, "\n".join(errors)


class TestMlModels:
    """Pruebas de la sección ml_models."""

    def test_ml_models_have_skills(self, models_data: dict[str, Any]) -> None:
        """ml_models tiene al menos una skill definida."""
        skills = models_data.get("ml_models", [])
        assert len(skills) > 0, "ml_models está vacío"

    def test_ml_models_have_tasks(self, models_data: dict[str, Any]) -> None:
        """Cada skill en ml_models tiene al menos 1 task."""
        errors: list[str] = []
        for entry in models_data.get("ml_models", []):
            skill = entry.get("skill", "unknown")
            tasks = entry.get("tasks", [])
            if len(tasks) == 0:
                errors.append(f"Skill '{skill}': no tiene tasks definidas")

        assert not errors, "\n".join(errors)

    def test_ml_models_tasks_have_models(self, models_data: dict[str, Any]) -> None:
        """Cada task en ml_models tiene al menos 1 modelo."""
        errors: list[str] = []
        for entry in models_data.get("ml_models", []):
            skill = entry.get("skill", "unknown")
            for task_entry in entry.get("tasks", []):
                task_name = task_entry.get("task", "unknown")
                models = task_entry.get("models", [])
                if len(models) == 0:
                    errors.append(
                        f"Skill '{skill}', task '{task_name}': no tiene modelos"
                    )

        assert not errors, "\n".join(errors)

    def test_ml_models_skill_names_are_unique(
        self, models_data: dict[str, Any]
    ) -> None:
        """No hay skills duplicadas en ml_models."""
        seen: set[str] = set()
        duplicates: list[str] = []
        for entry in models_data.get("ml_models", []):
            skill = entry.get("skill", "")
            if skill in seen:
                duplicates.append(skill)
            seen.add(skill)

        assert not duplicates, f"Skills duplicadas en ml_models: {duplicates}"

    def test_ml_models_task_names_are_unique_per_skill(
        self, models_data: dict[str, Any]
    ) -> None:
        """Los nombres de task son únicos dentro de cada skill."""
        errors: list[str] = []
        for entry in models_data.get("ml_models", []):
            skill = entry.get("skill", "unknown")
            seen: set[str] = set()
            for task_entry in entry.get("tasks", []):
                task_name = task_entry.get("task", "")
                if task_name in seen:
                    errors.append(f"Skill '{skill}': task duplicada '{task_name}'")
                seen.add(task_name)

        assert not errors, "\n".join(errors)


class TestModelsMeta:
    """Pruebas de metadatos de models.json."""

    def test_models_json_has_meta(self, models_data: dict[str, Any]) -> None:
        """models.json tiene la sección _meta con title y version."""
        meta = models_data.get("_meta", {})
        assert "title" in meta, "Falta _meta.title"
        assert "version" in meta, "Falta _meta.version"
        assert meta["title"], "_meta.title no debería estar vacío"

    def test_models_json_has_schema(self, models_data: dict[str, Any]) -> None:
        """models.json referencia un $schema."""
        assert "$schema" in models_data, "Falta el campo $schema"
