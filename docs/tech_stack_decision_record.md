# Tech Stack Decision Record

## Status
Accepted

## Context
The stack must:

- Have strong AI support (Copilot, ChatGPT, etc.)
- Be widely used and well-documented
- Support clean separation between UI, service, and data layers
- Be easy to set up on student laptops

## Decision
We will use the following tech stack:

- **Python** as the primary programming language
- **Poetry** for dependency and environment management
- **Pytest** for automated testing
- **Streamlit** for the web-based UI layer
- **SQLAlchemy** as the ORM and data access layer
- **PostgreSQL** as the production database

The architecture remains:

- Layered (UI → Service → Repository → DB)
- Monolithic
- Synchronous
- Single relational database

## Alternatives Considered

1. **Java + Spring Boot + JPA + Thymeleaf**
   - Strong enterprise relevance
   - Higher complexity and steeper learning curve

2. **Node.js + Express + PostgreSQL**
   - Popular full-stack ecosystem
   - Less structured backend patterns for beginners

## Consequences

### Positive

- Excellent AI support and large training data coverage
- Massive community and documentation
- Python lowers barrier for students
- Pytest enables TDD and CI-friendly workflow
- SQLAlchemy enforces separation of concerns
- PostgreSQL is widely used in industry
- Poetry ensures reproducible environments
- Streamlit enables rapid UI prototyping

### Negative

- Streamlit is less common in traditional enterprise production systems
- ORM abstraction may hide SQL performance issues
- Monolithic Python apps are not as performant as JVM-based stacks at scale
- Students may not learn REST API design deeply (since Streamlit abstracts it)
- Migration to microservices later would require architectural changes
