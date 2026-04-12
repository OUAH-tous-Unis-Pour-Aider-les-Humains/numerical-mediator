---
name: minimalist-python-testing
description: 'Write and review Python tests with a minimal, readable style. Use when creating unit tests, test fixtures, test plans, or verifying Python behavior with pytest or the standard library.'
argument-hint: 'python tests or test plan'
user-invocable: true
disable-model-invocation: false
---

# Minimalist Python Testing

## When to Use
- Writing unit tests for Python code
- Reviewing or refactoring test suites
- Choosing a testing strategy for a small Python project
- Designing test fixtures, test data, and assertions
- Verifying behavior with `pytest` or the standard library test tools

## Philosophy
- Test behavior, not implementation details.
- Keep tests small, direct, and easy to read.
- Prefer a few clear tests over many fragile ones.
- Use the simplest test tools that solve the problem.
- Avoid heavy test infrastructure unless the codebase truly needs it.

## Procedure
1. Identify the behavior that matters most.
2. Separate normal cases, edge cases, and failure cases.
3. Write one test per meaningful behavior.
4. Use explicit test names that describe the expected result.
5. Keep setup minimal and local to the test when possible.
6. Prefer plain assertions and simple fixtures over complex abstractions.
7. Mock only external boundaries or slow dependencies.
8. Verify the tests are readable and fail with useful messages.

## Test Design Rules
- Focus on public behavior and observable outputs.
- Keep fixtures small and obvious.
- Use parametrization only when it makes the test clearer.
- Avoid over-mocking internal code.
- Prefer deterministic inputs and outputs.
- Keep test modules organized by feature or behavior.

## Review Checklist
- Does each test prove one clear behavior?
- Are the names descriptive enough to understand the intent quickly?
- Is the setup shorter than the test itself when possible?
- Are mocks limited to the boundaries that need them?
- Would a new developer understand the failure without extra context?

## Completion Check
- The tests cover the important behavior, not every line.
- The suite is easy to read and maintain.
- The test structure stays lightweight.
- Failures should point to the real problem quickly.
