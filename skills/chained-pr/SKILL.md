---
name: chained-pr
description: >
  Chained PRs for large changes — split a 1000-line PR into smaller,
  sequential, reviewable PRs under 400 lines each.
  Trigger: When a PR exceeds 400 lines changed, or when planning chained PRs.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: chained-pr

Chained PRs. Large changes broken into reviewable chunks.

## Trigger

- A PR has more than 400 lines
- A large change can be split into logical steps
- Multiple PRs need to be coordinated with dependencies

## Workflow LEND

1. ANALYZE
   ├── Total changes: how many lines? how many files?
   ├── Dependencies: can changes be isolated or do they depend on each other?
   ├── Logical order: which PR needs to be merged first?
   └── Base: all against main

2. OFFER (Senior Menu)
   ├── A) 2 PRs — PR1: refactor/cleanup, PR2: the new feature
   ├── B) 3 PRs — PR1: preparation, PR2: core logic, PR3: integration
   └── C) N PRs — sequence of small PRs, each < 400 lines

3. CHOOSE → user confirms

4. EXECUTE
   ├── PR1 base → main, PR2 base → PR1 (target branch = PR1)
   ├── Each PR: < 400 lines, focused on one logical change
   ├── Description: link to previous and next PR in the chain
   ├── Merge in order: PR1 → main, then PR2 → main (after PR1)
   └── If PR1 changes → PR2 needs rebase

5. VERIFY
   ├── Each PR is < 400 lines
   ├── The chain has a logical order
   └── No conflicts between PRs in the chain
