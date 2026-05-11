---
name: commits-real
description: >
  Professional commits with Conventional Commits in English US.
  Semantic versioning, changelog generation, and commit hygiene.
  Trigger: When writing commits, creating PRs, filing issues, or writing documentation.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T3-balanced
---

# Skill: commits-real

Professional commits. Every message tells a story.

## Trigger

- You finished a change and need to commit
- You're creating a PR or issue
- You need to update a CHANGELOG
- Setting up semantic versioning for a project

## Workflow LEND

1. ANALYZE
   ├── What changed? files, functionality, bug fix, refactor?
   ├── Scope: which module? (api, ui, data, infra, docs)
   ├── Breaking: does it break backward compatibility?
   └── Issues: are there related issues or PRs?

2. OFFER (Senior Menu)
   ├── A) Simple conventional commit — feat/fix/chore + short message in English
   ├── B) Commit with body — conventional commit + description + issue reference
   └── C) Full structure — conventional commit + breaking change + changelog update

3. CHOOSE → user confirms

4. EXECUTE
   ├── Format: `type(scope): message` (feat, fix, chore, docs, refactor, test, style)
   ├── Message: imperative, present tense, < 50 chars title, < 72 chars body
   ├── Breaking: `feat(api): remove deprecated endpoint\n\nBREAKING CHANGE: ...`
   ├── Atomic commits: one change per commit, not "multiple fixes"
   ├── Issues: `Closes #123` or `Refs #456` in the body
   ├── Language: English US, technical, clear
   └── Versioning: semver (major.minor.patch) based on conventional commits

5. VERIFY
   ├── The message follows conventional commit format
   ├── No unrelated files in the commit
   └── Breaking changes are documented

## Patterns

- **Imperative mood**: "Add login endpoint" not "Added login endpoint" or "Adding login endpoint"
- **Atomic commits**: one logical change per commit
- **Issue linking**: `Closes #123` in the body, not the title
- **Scope**: lowercase, single word: (api), (ui), (data), (deps)
- **Types**: feat, fix, chore, docs, refactor, test, style, perf, ci

## Anti-patterns

- ❌ Vague messages: "update", "fix", "changes"
- ❌ Commits in Spanish — English US only
- ❌ Multiple features in one commit
- ❌ Breaking changes without BREAKING CHANGE note
- ❌ Unrelated files in the same commit
