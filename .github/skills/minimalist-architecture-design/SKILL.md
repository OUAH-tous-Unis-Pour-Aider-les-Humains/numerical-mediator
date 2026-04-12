---
name: minimalist-architecture-design
description: 'Design small, readable software architectures with a minimal approach. Use when planning APIs, database schemas, backend/frontend boundaries, project structure, technology choices, or other cross-language tasks that should stay simple and understandable.'
argument-hint: 'architecture, API, schema, or project design'
user-invocable: true
disable-model-invocation: false
---

# Minimalist Architecture Design

## When to Use
- Designing an application architecture
- Planning APIs or data contracts
- Choosing a database schema
- Defining backend and frontend boundaries
- Scoping a prototype or proof of concept
- Reviewing a design for unnecessary complexity

## Philosophy
- Prefer the smallest architecture that can prove the idea.
- Keep the system understandable before keeping it scalable.
- Use the fewest moving parts that still cover the real need.
- Avoid distributed systems, queues, and layered abstractions unless they solve a known problem.
- Choose explicit contracts over implicit coupling.
- Favor simple integration paths over flexible but hard-to-read frameworks.

## Procedure
1. Define the exact goal of the system or feature.
2. List the non-negotiable constraints, including scope, data, users, and runtime environment.
3. Identify the smallest vertical slice that demonstrates the concept end to end.
4. Separate the system into only the parts that need to be separate.
5. Define the data model and the API or interface contract with the fewest fields and relations needed.
6. Choose technologies that reduce complexity rather than increase optionality.
7. Note the tradeoffs you are accepting by keeping the design small.
8. Validate the design with a simple execution path, example payloads, or a minimal schema.

## Design Rules
- Keep boundaries clear: UI, API, persistence, and domain logic should be separated only when it stays simple.
- Prefer direct data flow over event-driven complexity.
- Keep schemas normalized enough to be safe, but not so abstract that they become hard to use.
- Make API shapes obvious and stable.
- Write down the assumptions that justify each important choice.
- Avoid designing for scale before the first working version exists.

## Documentation Rules
- Document the purpose of each major component.
- Record the main data entities and their relationships.
- Describe the request/response shape of important APIs.
- Explain why a choice was made when the alternative would also have worked.
- Keep the documentation short enough that it is actually read.

## Completion Check
- The architecture solves the current problem without obvious excess.
- The main data flow can be explained in a few steps.
- The API or interface contract is clear.
- The schema or component split is easy to justify.
- A new contributor can understand the system without reading a large design document.
