"""Validates .github/workflows/*.yml files are parseable and reference valid paths."""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"


def _collect_workflows():
    if not WORKFLOWS_DIR.exists():
        return []
    return sorted(WORKFLOWS_DIR.glob("*.yml")) + sorted(WORKFLOWS_DIR.glob("*.yaml"))


WORKFLOWS = _collect_workflows()

skip_windows = pytest.mark.skipif(
    not WORKFLOWS_DIR.exists(),
    reason="No .github/workflows directory found",
)


@skip_windows
class TestCIWorkflows:

    @pytest.mark.parametrize("wf_path", WORKFLOWS, ids=lambda p: p.name)
    def test_yaml_parseable(self, wf_path: Path):
        """Every workflow file must be valid YAML."""
        with open(wf_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data is not None, f"{wf_path.name} is empty"
        assert "name" in data, f"{wf_path.name} missing 'name'"
        assert "jobs" in data, f"{wf_path.name} missing 'jobs'"

    @pytest.mark.parametrize("wf_path", WORKFLOWS, ids=lambda p: p.name)
    def test_python_scripts_exist(self, wf_path: Path):
        """Every `python3` or `python ` or `pip install` in run steps
        references only scripts that exist on disk."""
        with open(wf_path, encoding="utf-8") as f:
            content = f.read()

        data = yaml.safe_load(content)
        for job_name, job in data.get("jobs", {}).items():
            steps = job.get("steps", [])
            for step in steps:
                run = step.get("run", "")
                if not isinstance(run, str):
                    continue
                for line in run.split("\n"):
                    line = line.strip()
                    for script_ref in ("python3 ", "python "):
                        if line.startswith(script_ref):
                            parts = line[len(script_ref):].split()
                            if parts and parts[0].startswith("scripts/") and not parts[0].startswith("scripts/model-commands"):
                                script_path = REPO_ROOT / parts[0]
                                assert script_path.exists(), (
                                    f"Script '{parts[0]}' referenced in {wf_path.name}"
                                    f" job '{job_name}' does not exist on disk"
                                )

    def test_all_workflows_have_required_sections(self):
        """Each workflow must have at least a test or validate job."""
        for wf_path in WORKFLOWS:
            with open(wf_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            job_names = list(data.get("jobs", {}).keys())
            has_validation = any(
                "lint" in n or "test" in n or "validate" in n
                for n in job_names
            )
            assert has_validation, (
                f"{wf_path.name} has no lint/test/validate job "
                f"(found: {job_names})"
            )
