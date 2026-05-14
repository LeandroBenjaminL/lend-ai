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

### Post-task (always)
1. Save this task to Engram with mem_save
2. Review if documentation needs updating (README, AGENTS.md, ARCHITECTURE.md)
3. If docs changed → include in the same PR/commit

## Patterns

- **Imperative mood**: "Add login endpoint" not "Added login endpoint" or "Adding login endpoint"
- **Atomic commits**: one logical change per commit, commit by work unit (not file type)
- **Issue linking**: `Closes #123` in the body, not the title
- **Scope**: lowercase, single word: (api), (ui), (data), (deps)
- **Types**: feat, fix, chore, docs, refactor, test, style, perf, ci
- **400-line PR budget**: default review budget is 400 changed lines. Split PRs that exceed this.

## Work-unit split examples

| Weak split | Better work-unit split |
|-----------|----------------------|
| Commit 1: "Add model" / Commit 2: "Add migration" | Commit 1: "Add User model + migration + test" |
| Commit 1: "Update styles" / Commit 2: "Fix styles" | Commit 1: "Update sign-in page styles" |
| Commit 1: "Refactor" / Commit 2: "More refactor" | Commit 1: "Extract AuthService from UserController" |

## Comment/Voice rules (for PRs, issues, reviews)

- **Be useful fast**: lead with what matters — the decision, the bug, the question
- **Warm and direct**: friendly but no fluff. "This is wrong because X" not "I think maybe we could consider..."
- **Short**: default to 1-2 sentences. Expand only when needed.
- **Explain why**: every request or observation includes the reasoning
- **Avoid pile-ons**: if someone already pointed it out, 👍 and move on
- **Match thread language**: reply in the same language as the thread
- **Rioplatense Spanish**: warm, voseo, direct. "Che, esto está mal porque..." not "Se sugiere considerar..."

## Comment formula

```
Direct observation/request → Why it matters → Concrete next action

"Este hook debería usar useCallback. Sin memoization se recrea
en cada render y rompe la comparación de dependencias del useEffect
de abajo. Metele useCallback con [] y validamos."
```

## PR/review doc guidelines

- State what to review FIRST (high-impact files)
- State what's OUT OF SCOPE (don't make reviewers guess)
- Link chain context if this is part of a PR chain
- Include test plan: what was tested manually and automatically

## Anti-patterns

- ❌ Vague messages: "update", "fix", "changes"
- ❌ Commits in Spanish — English US only
- ❌ Multiple features in one commit
- ❌ Breaking changes without BREAKING CHANGE note
- ❌ Unrelated files in the same commit
