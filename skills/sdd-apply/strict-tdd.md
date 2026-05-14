# Strict TDD Module — Apply Phase

> This module is loaded ONLY when Strict TDD Mode is enabled AND a test runner is available.
> If you are reading this, the orchestrator already verified both conditions.

## TDD Philosophy

TDD is not testing. TDD is **software design driven by tests**. You write a test that describes what the code SHOULD do, then write the minimum code to make it real. The tests design the API, the contracts, the behavior. Code is a side effect of tests.

### The Three Laws

1. Do NOT write production code until you have a failing test
2. Do NOT write more test than is necessary to fail
3. Do NOT write more code than is necessary to pass the test

## TDD Implementation Cycle

```
FOR EACH TASK:
├── 0. SAFETY NET (only if modifying existing files)
│   ├── Run existing tests → capture baseline: "N tests passing"
│   └── If any FAIL → STOP, report as "pre-existing failure"
│
├── 1. UNDERSTAND the task, spec, design, and existing patterns
│
├── 2. RED — Write a failing test FIRST
│   ├── Test describes expected behavior from the spec
│   ├── Production code referenced does NOT exist yet
│   └── GATE: Do NOT proceed until test is written
│
├── 3. GREEN — Write the MINIMUM code to pass
│   ├── Implement ONLY what the failing test needs
│   ├── Fake It is valid here (hardcoded returns are OK)
│   ├── Execute tests → must PASS
│   └── GATE: Do NOT proceed until GREEN is confirmed
│
├── 4. TRIANGULATE
│   ├── Add a second test with DIFFERENT inputs
│   ├── If Fake It breaks → generalize to real logic
│   ├── Cover ALL spec scenarios for this task
│   ├── Minimum: 2 test cases (happy path + edge case)
│   └── Watch for trivial GREENs (test passes because code didn't run)
│
├── 5. REFACTOR — Improve without changing behavior
│   ├── Extract constants, functions, improve naming
│   ├── Execute tests after EACH refactoring → must STILL PASS
│   └── Boy Scout Rule: leave code cleaner than you found it
│
├── 6. Mark task complete [x]
└── 7. Save TDD cycle evidence
```

## TDD Cycle Evidence Table (MANDATORY)

For EVERY task, produce this table in your apply-progress:

```markdown
| Task | RED (test written) | GREEN (test passes) | REFACTOR | Status |
|------|-------------------|---------------------|----------|--------|
| 1.1  | test_auth_valid: 3 assertions | ✅ 3/3 passed | Extracted validateEmail() | ✅ |
| 1.2  | test_auth_invalid: 2 assertions | ✅ 2/2 passed | — (no refactor needed) | ✅ |
```

## Choosing Test Layer

| Task type | Test layer |
|-----------|-----------|
| Pure logic, utility, calculation | Unit test |
| Component rendering, interaction | Integration test (or unit with mocks) |
| API endpoint, data flow | Integration test |
| Full user workflow | E2E test |

## Anti-patterns

- ❌ Writing implementation before test (violates Law 1)
- ❌ Writing more code than the test requires (violates Law 3)
- ❌ Skipping triangulation without explicit reason
- ❌ Silent fallback to Standard Mode
- ❌ Missing TDD Evidence table
