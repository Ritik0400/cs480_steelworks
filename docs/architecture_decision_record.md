# Architecture Decision Record

## Status
Accepted

## Context
SteelWorks, LLC needs an internal web application to import multiple Excel files into a database and provide a GUI for users (e.g., quality engineers) to query and compare data across lots and defects over time.

The development team is small (student team), delivery time is limited (course project), and maintainability and testability are important. In an AI-assisted development workflow, architectural boundaries help prevent mixing UI, business logic, and database access in uncontrolled ways.

We need an architecture that is:
- Easy to understand for undergraduate students
- Easy to deploy and demo
- Compatible with automated testing and CI/CD
- Representative of common industry practices for small-to-medium internal systems

## Decision
We will build the system as a **client–server** web application, using a **monolithic** codebase with **layered architecture**, backed by a **single relational database**, and using **synchronous** request/response interactions.

Specifically:

- **Client–Server:** Browser-based UI acts as client; application process acts as server.
- **Monolith:** One deployable application containing UI, business logic, and data access.
- **Layered Architecture:**
  - Presentation / UI Layer
  - Service / Business Logic Layer
  - Data Access Layer (Repository / DAO)
  - Database
- **Single Database:** One relational database.
- **Synchronous Architecture:** Each user action sends a request to the server and receives a response within the same request cycle (no message queues or event-driven infrastructure required).

## Alternatives Considered
None

## Consequences

### Positive

- Faster development and iteration
- Simpler deployment (single service + single database)
- Clear separation of concerns improves maintainability
- Easier to unit test service and data layers independently
- Lower operational complexity
- Aligns with common enterprise patterns for internal tools

### Negative

- Limited horizontal scalability compared to microservices
- Long-running tasks (e.g., large Excel imports) may block requests
- Tight coupling to a single database schema
- Refactoring required if migrating to distributed or event-driven architecture in the future
