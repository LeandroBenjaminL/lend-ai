# Git/GitHub — Workflow

## Decision tree

```
What do you need to do?
│
├── Commit changes
│   └── → Load skill commits-real
│
├── Create a PR
│   └── → Load skill branch-pr
│
├── PR too large (>400 lines)
│   └── → Load skill chained-pr
│
├── Report a bug or request a feature
│   └── → Load skill issue-creation
│
├── Design branching strategy or releases
│   └── → Load skill gitops-engineer
│
├── Git for data science (DVC, datasets)
│   └── → Load skill shared-git-data
│
└── Not sure / multiple areas
    └── → I'll handle it (git-github)
```

## Enterprise flow

```
1. ISSUE → create issue describing the problem/feature
2. BRANCH → git checkout -b type/issue-number-description
3. CODE → implement changes
4. COMMIT → conventional commits in English US
5. PR → open PR with description, screenshots, testing
6. REVIEW → assign reviewer, wait for approval
7. MERGE → reviewer merges to main
8. DOCS → update documentation if needed
9. ENGRAM → save decisions and changes
```

## Rules

1. English US for all commits, PRs, issues
2. Conventional commits always
3. PR < 400 lines or chained-pr
4. Issues with measurable acceptance criteria
5. Always link issues to PRs
6. Engram after every significant operation
