# CI/CD Pilot — Patterns

### GitHub Actions reusable workflow
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    uses: ./.github/workflows/lint.yml
  test:
    uses: ./.github/workflows/test.yml
  deploy:
    needs: [lint, test]
    if: github.ref == 'refs/heads/main'
    uses: ./.github/workflows/deploy.yml
```

### Caching strategy
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```
