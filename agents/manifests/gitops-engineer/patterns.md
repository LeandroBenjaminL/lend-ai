# GitOps Engineer — Patterns

### Branch strategy (trunk-based)
```
main ──────── feat1 ──────── feat2 ────────
      \         / \         /
       fix1 ────   fix2 ────
```

### Conventional Commits
```
feat: add dark mode toggle
fix: resolve N+1 query in user list
chore: bump dependencies
docs: update API reference
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

### Semantic versioning
```bash
# bump automatically from commits
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```
