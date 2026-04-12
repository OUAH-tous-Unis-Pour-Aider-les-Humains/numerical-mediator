# numerical-mediator
An open source application to connect people’s arguments and assemble the solution.

# Context
This branch is a lightweight proof of concept.

Its goal is to understand how the system works, not to build a production-ready or scalable architecture.

So we intentionally avoid heavy infrastructure and "big system" tools (for example Celery, distributed task queues, microservice orchestration, etc.).

For this branch, keep the stack minimal:

- a simple SQL database
- a Python backend to read/write data
- a JavaScript frontend using React Flow to build and visualize schemas

This branch is not intended to grow into a large system. It is only here to validate the core concepts with a simple and understandable implementation.