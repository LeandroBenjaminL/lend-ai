# Git/GitHub — Patterns

## Commit pattern
```
type(scope): short imperative description (< 50 chars)

Optional body with details (< 72 chars per line)

Closes #123
```

## Branch pattern
```
type/issue-number-description
feat/42-add-login
fix/17-fix-null-crash
docs/3-update-readme
```

## PR pattern
- Description: what, why, how, screenshots
- Labels: feat, fix, chore, breaking
- Reviewer: assign someone
- CI: must pass before merge

## Issue labels
- P0: Critical — blocks release
- P1: High — should be done this sprint
- P2: Medium — nice to have
- P3: Low — backlog

## Language
- All commits, PRs, issues → English US
- Technical, clear, imperative mood
- No emoji without permission
