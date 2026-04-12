---
name: minimalist-javascript-coding
description: 'Write or refactor JavaScript code with a minimal, readable, well-documented style. Use when coding in JavaScript, choosing dependencies, designing small features, or reviewing code for simplicity and clarity.'
argument-hint: 'javascript feature or refactor'
user-invocable: true
disable-model-invocation: false
---

# Minimalist JavaScript Coding

## When to Use
- Writing new JavaScript code
- Refactoring JavaScript code for clarity
- Choosing between built-in APIs and dependencies
- Reviewing JavaScript code for simplicity, readability, and documentation

## Philosophy
- Prefer the smallest solution that is correct.
- Use built-in JavaScript and platform APIs first.
- Add dependencies only if they remove meaningful complexity.
- Optimize for understanding, not for cleverness.
- Keep the codebase easy to extend without becoming a large system.

## Procedure
1. Clarify the real goal before coding.
2. Choose the simplest data model and control flow that solves the problem.
3. Prefer small functions, explicit names, and direct logic over abstraction.
4. Document exported functions, important modules, and non-obvious decisions.
5. Add comments only when they explain intent or tradeoffs that code alone cannot show.
6. Avoid premature generalization, background workers, queues, and layered architecture unless they are clearly needed.
7. Validate the result with a small example, test, or manual check.

## Code Style Rules
- Keep functions short and focused.
- Use descriptive names instead of extra explanation in code.
- Prefer `const` by default and `let` only when mutation is required.
- Prefer early returns over deeply nested conditionals.
- Avoid framework-heavy solutions when a direct function or module is enough.
- Keep I/O, business logic, and persistence separate only when that separation stays simple.

## Documentation Rules
- Document the purpose of a module or function when it is not obvious.
- Explain constraints, assumptions, and expected inputs or outputs.
- Keep docs close to the code they describe.
- Prefer concise comments or JSDoc over long prose.

## Completion Check
- The code is easy to read without tracing many layers.
- The implementation uses the fewest moving parts that still make sense.
- Any new dependency is justified.
- The main behavior is documented.
- The result is understandable by someone new to the project.
