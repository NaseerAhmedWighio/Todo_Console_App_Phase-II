<!-- SYNC IMPACT REPORT:
Version change: 2.0.0 → 2.1.0 (updated Better Auth API usage and corrected authentication implementation)
Modified principles: VII. JWT Authentication & Authorization (updated to reflect correct Better Auth v1.4.17 API)
Added sections: None
Removed sections: None
Templates requiring updates: ✅ updated (plan-template.md, spec-template.md, tasks-template.md)
Follow-up TODOs: None
-->

# Full-Stack Web Application Constitution (Todo App Phase II)

## Core Principles

### I. Full-Stack Architecture
The application must be implemented as a full-stack web application with separate backend and frontend components. The backend provides RESTful APIs, while the frontend consumes these APIs to deliver a rich user experience. Clear separation of concerns between client and server components must be maintained with well-defined API contracts.

### II. Python-First Backend Development
All backend services must be implemented in Python using FastAPI framework following PEP 8 style guidelines. Code must be clean, readable, and maintainable with proper documentation. Type hints are mandatory for all public interfaces to ensure code clarity and prevent runtime errors.

### III. Next.js Frontend with TypeScript
The frontend must be built using Next.js 16+ with TypeScript, following modern React patterns and best practices. Component-based architecture with proper state management and error boundaries. All user-facing logic must be encapsulated in reusable, testable components.

### IV. Test-First (NON-NEGOTIABLE)
TDD is mandatory: Unit tests must be written before implementation code. Tests must cover all core functionality including edge cases. Red-Green-Refactor cycle strictly enforced with 80%+ code coverage required before merging. Both backend and frontend must have comprehensive test suites.

### V. Tailwind CSS Styling with Premium Design
All styling must be implemented using Tailwind CSS following the luxury SaaS dashboard design system. The color palette must adhere to the specified theme: Primary: Deep Charcoal (#0B0B0E), Secondary: Soft Graphite (#1A1A1F), Accent: Royal Gold (#C9A24D), and appropriate success/error colors. Typography must follow clean, modern hierarchy principles.

### VI. Framer Motion Animations & Interactions
All user interactions must include smooth animations and micro-interactions using Framer Motion. This includes hover effects, checkbox toggle animations, task completion transitions, loading skeletons, and page transitions. Animation durations and easing must follow consistent patterns across the application.

### VII. JWT Authentication & Authorization
Secure JWT-based authentication must be implemented using Better Auth on the frontend and custom JWT middleware on the backend. Authentication must be enforced at the API level with proper token validation and error handling. The shared BETTER_AUTH_SECRET must be used consistently across both frontend and backend. Frontend must use the correct Better Auth client API: createAuthClient for initialization, authClient.signIn/signOut methods for authentication flows, and useAuthQuery for session management.

### VIII. Multi-User Data Isolation
Each user must have isolated data with strict enforcement at the API level. The backend must validate that all operations are performed on resources owned by the authenticated user. Cross-user data access must be prevented through proper authorization checks in all API endpoints.

### IX. SQLModel + Neon PostgreSQL Database
Data persistence must be implemented using SQLModel ORM with Neon Serverless PostgreSQL. The database schema must include proper indexes, foreign key relationships, and data integrity constraints. Connection pooling and proper error handling for database operations must be implemented.

### X. Dependency Management with uv and npm
Backend dependencies must be managed using uv package manager, while frontend dependencies use npm. Virtual environments must be properly isolated and reproducible. Dependencies must be pinned to specific versions to ensure consistent builds across environments.

## Core Application Features
<!-- Specific functional requirements for the todo application -->

The application must support these essential operations: Add Task (create new todo items), Delete Task (remove tasks from the list), Update Task (modify existing task details), View Task List (display all tasks for the authenticated user), Mark as Complete (toggle task completion status). All operations must maintain data integrity, provide appropriate user feedback, and enforce user isolation.

## Technical Requirements
<!-- Technology stack, performance, and operational constraints -->

Technology Stack: Next.js 16+, TypeScript, Tailwind CSS, Better Auth, Framer Motion (frontend); Python 3.9+, FastAPI, SQLModel, Neon PostgreSQL (backend). Performance: API endpoints must respond within 500ms, frontend interactions must be smooth with <60fps. Memory Usage: Backend must not exceed 200MB RAM under normal operation. Error Handling: All operations must gracefully handle invalid inputs, network errors, and system failures with appropriate user feedback. Authentication: JWT tokens must be validated on all API requests with proper 401/403 error responses.

## Development Workflow
<!-- Code review, testing, and quality standards -->

All code changes require peer review before merging. Automated tests must pass before merge. Commits must follow conventional commit format with clear, descriptive messages. Branch naming follows feature/{story-id}-{short-description} convention. Code must pass linting checks (flake8, mypy for backend; eslint, prettier for frontend) before merging. API contracts must be documented and versioned appropriately.

## Governance
All development activities must comply with these principles. Changes to this constitution require team consensus and documented approval. Code reviews must verify compliance with all principles. New features must align with core application functionality and not violate established architectural constraints. Security considerations must be evaluated for all changes affecting authentication, authorization, or data handling.

**Version**: 2.1.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-24