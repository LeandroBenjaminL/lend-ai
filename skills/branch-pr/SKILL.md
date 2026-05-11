---
name: branch-pr
description: >
  Enterprise PR workflow — issue-first, branch naming, conventional commits,
  PR description, and review cycle. PRs under 400 lines.
  Trigger: When creating a PR, preparing changes for review, or opening a branch.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: branch-pr

Enterprise PR workflow. Small PRs, clear descriptions, review before merge.

## Trigger

- You're creating a new branch to work on an issue
- Changes are ready and you need to open a PR
- Someone requested a review on your PR
- A PR is too large and needs splitting (> 400 lines)

## Workflow LEND

1. ANALYZE
   ├── Issue: is there an associated issue? what does it solve?
   ├── Scope: how many files? how many lines? (> 400 → chained-pr)
   ├── Base branch: main, develop, or feature branch?
   └── Dependencies: does this PR block or depend on others?

2. OFFER (Senior Menu)
   ├── A) Simple branch + PR — direct branch + PR with minimal template
   ├── B) PR with description — context, changes, testing, screenshots
   └── C) Structured PR — issue link, description, checklist, breaking changes

3. CHOOSE → user confirms

4. EXECUTE
   ├── Branch name: `type/issue-number-description` (feat/123-login, fix/45-crash)
   ├── Format types: feat/, fix/, chore/, docs/, refactor/, test/
   ├── Commits: conventional commits in English, atomic
   ├── PR description: what, why, how, testing evidence, screenshots
   ├── Template: context, changes, testing, checklist for reviewer
   ├── Small PR: < 400 lines. If larger → chained-pr
   ├── Labels: feat, fix, chore, breaking, needs-review
   └── REVIEW CYCLE: author opens → reviewer approves/requests changes → author updates → merge

5. VERIFY
   ├── The PR has a clear description
   ├── Tests pass in CI
   ├── No conflicts with the base branch
   └── Reviewer is assigned

## Patterns

- **Issue-first**: every branch/PR comes from an issue
- **Small PRs**: < 400 lines, one logical change
- **Branch naming**: `type/issue-number-description`
- **PR description**: what, why, how, screenshots, testing
- **Review cycle**: author opens → reviewer feedback → author updates → merge

## Anti-patterns

- ❌ PRs without an associated issue
- ❌ PRs with 1000+ lines — split them with chained-pr
- ❌ PR descriptions without context — "fixes stuff" is not a description
- ❌ Merging without review
- ❌ Branch names like "fix-stuff" or "asd123"
