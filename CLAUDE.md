# Claude Code Rules - Todo App Phase II

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to transform the existing console-based Todo app into a full-stack web application.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- Successfully upgrading the Todo app from Phase I (Console) to Phase II (Full-Stack Web)
- Building a secure, multi-user, production-grade web application
- Implementing JWT authentication with user-isolated data
- Creating a modern luxury UI/UX experience
- Following the spec-driven development workflow

## Core Objectives (Product Promise)

- Transform console app to full-stack web application with Next.js frontend and FastAPI backend
- Implement secure JWT authentication using Better Auth with user data isolation
- Set up persistent database using SQLModel and Neon PostgreSQL
- Create modern luxury UI with Tailwind CSS and Framer Motion animations
- Follow agentic workflow: Read specs → Generate architecture & plan → Break into tasks → Implement incrementally

## Technology Stack

### Frontend:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Framer Motion (for animations)

### Backend:
- FastAPI (Python)
- SQLModel ORM
- Neon Serverless PostgreSQL

### Authentication:
- Better Auth (Frontend)
- JWT tokens
- Shared secret via BETTER_AUTH_SECRET

## UI/UX Design Requirements

### Design Theme (Luxury & Modern)
Style:
- Minimal
- Premium SaaS dashboard look
- Apple / Linear / Vercel inspired

Color Palette:
- Primary: Deep Charcoal / Jet Black (#0B0B0E)
- Secondary: Soft Graphite / Dark Gray (#1A1A1F)
- Accent: Royal Gold / Champagne (#C9A24D)
- Success: Emerald Green
- Danger: Soft Crimson
- Text: Off-white (#F5F5F7)

### UI Behavior & Interactions
Hover Effects:
- Buttons: Smooth scale (scale-105), soft glow or shadow, color transition (300ms)
- Cards: Lift effect, border highlight on hover

Micro-Interactions:
- Checkbox toggle animation
- Task completion strike-through animation
- Loading skeletons
- Button ripple or glow

Animations:
- Page transitions (fade/slide)
- Modal open/close animation
- Smooth routing transitions
- Scroll animations with Framer Motion

## Feature Requirements

### Core Todo Features
- Create task
- View all tasks
- View single task
- Update task
- Delete task
- Toggle completion

### Multi-User Support
- Each user has isolated data
- No cross-user access
- Ownership enforced at API level

## Authentication Flow

### Frontend (Better Auth):
- Enable JWT plugin
- Signup & Signin pages
- Issue JWT token on login
- Store token securely
- Attach token to ALL API requests

### Backend (FastAPI):
- JWT verification middleware
- Decode token using shared secret
- Extract user_id from JWT
- Validate user_id matches route
- Reject unauthorized requests with 401

## REST API Contract

ALL endpoints:
- Require JWT
- Authorization: Bearer <token>
- Filter data by authenticated user

Endpoints:
- GET    /api/{user_id}/tasks
- POST   /api/{user_id}/tasks
- GET    /api/{user_id}/tasks/{id}
- PUT    /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH  /api/{user_id}/tasks/{id}/complete

## Development Workflow

1. Read all specs:
   - @specs/overview.md
   - @specs/features/task-crud.md
   - @specs/features/authentication.md
   - @specs/api/rest-endpoints.md
   - @specs/database/schema.md
   - @specs/ui/components.md
   - @specs/ui/pages.md

2. Generate Phase II architecture & plan

3. Break plan into tasks:
   - Backend setup
   - Auth middleware
   - Database integration
   - API routes
   - Frontend pages
   - UI animations
   - API client
   - JWT wiring

4. Implement step-by-step:
   - Backend first
   - Frontend second
   - Integration last

## Monorepo Structure
```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   │   ├── task-crud.md
│   │   └── authentication.md
│   ├── api/
│   │   └── rest-endpoints.md
│   ├── database/
│   │   └── schema.md
│   └── ui/
│       ├── components.md
│       └── pages.md
├── CLAUDE.md
├── frontend/
│   └── CLAUDE.md
├── backend/
│   └── CLAUDE.md
```

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps.

## Default policies (must follow)
- Follow the agentic workflow: Read specs → Generate architecture & plan → Break into tasks → Implement incrementally
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
