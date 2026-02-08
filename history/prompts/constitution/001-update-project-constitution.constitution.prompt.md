---
id: 001
title: Update Project Constitution
stage: constitution
date: 2026-01-23
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude Code
command: sp.constitution
labels: [constitution, todo-app, phase-ii, upgrade]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - specs/overview.md
  - specs/architecture.md
  - specs/features/task-crud.md
  - specs/features/authentication.md
  - specs/api/rest-endpoints.md
  - specs/database/schema.md
  - specs/ui/components.md
  - specs/ui/pages.md
  - frontend/CLAUDE.md
  - backend/CLAUDE.md
  - CLAUDE.md
tests:
  -
---

## Prompt

```text
You are Claude Code running with GitHub Spec-Kit Plus.
Operate strictly using a Spec-Driven, Agentic Dev Stack workflow.

Your task is to UPGRADE my Todo App from:
Phase I (Console Application)
→ Phase II (Full-Stack Web Application)

This upgrade MUST include:
- Full backend + frontend implementation
- Secure JWT authentication
- Persistent database
- Modern, premium, luxury UI/UX design
- Smooth animations and interactions

⚠️ ABSOLUTE RULES
- Follow Agentic Workflow ONLY:
  1. Read specs
  2. Generate architecture & plan
  3. Break into tasks
  4. Implement incrementally
- NO manual coding by the user
- Reference specs using @specs/*
- Respect ALL CLAUDE.md instructions
- Frontend and backend must be fully integrated

---

## 🎯 PHASE II OBJECTIVE

Transform the existing console-based Todo app into a:
- Secure
- Multi-user
- Full-stack
- Production-grade web application

With:
- RESTful API
- JWT authentication
- User-isolated data
- Modern luxury UI experience

---

## 🧱 TECHNOLOGY STACK (MANDATORY)

Frontend:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (JWT enabled)
- Framer Motion (for animations)

Backend:
- FastAPI (Python)
- SQLModel ORM
- Neon Serverless PostgreSQL

Authentication:
- Better Auth (Frontend)
- JWT tokens
- Shared secret via BETTER_AUTH_SECRET

Spec System:
- GitHub Spec-Kit Plus
- Claude Code

---

## ✨ UI / UX DESIGN REQUIREMENTS (VERY IMPORTANT)

### 🎨 DESIGN THEME (Luxury & Modern)

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

Typography:
- Clean modern fonts
- Clear hierarchy
- Large headings, subtle body text

---

### 🧠 UI BEHAVIOR & INTERACTIONS

Hover Effects:
- Buttons:
  - Smooth scale (scale-105)
  - Soft glow or shadow
  - Color transition (300ms)
- Cards:
  - Lift effect
  - Border highlight on hover

Micro-Interactions:
- Checkbox toggle animation
- Task completion strike-through animation
- Loading skeletons
- Button ripple or glow

Scroll Animations (if scroll = true):
- Fade-in on scroll
- Slide-up animations for task cards
- Section reveal using Framer Motion
- Sticky header with blur background

Transitions:
- Page transitions (fade/slide)
- Modal open/close animation
- Smooth routing transitions

Responsiveness:
- Fully responsive (mobile, tablet, desktop)
- Mobile-first layout
- Touch-friendly buttons

---

## 🧩 FEATURE REQUIREMENTS

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

---

## 🔐 AUTHENTICATION FLOW (CRITICAL)

Frontend (Better Auth):
- Enable JWT plugin
- Signup & Signin pages
- Issue JWT token on login
- Store token securely
- Attach token to ALL API requests

Backend (FastAPI):
- JWT verification middleware
- Decode token using shared secret
- Extract user_id from JWT
- Validate user_id matches route
- Reject unauthorized requests with 401

Environment Variable:
- BETTER_AUTH_SECRET (shared by frontend & backend)

---

## 🔌 REST API CONTRACT (STRICT)

ALL endpoints:
- Require JWT
- Authorization: Bearer <token>
- Filter data by authenticated user

Endpoints:

GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete

Behavior:
- 401 if no token
- 403 if user mismatch
- Only return user's own tasks

---

## 🗄 DATABASE REQUIREMENTS

Use SQLModel + Neon PostgreSQL.

Schema:
- users (managed by Better Auth)
- tasks:
  - id
  - user_id
  - title
  - description
  - completed
  - created_at
  - updated_at

Indexes:
- user_id
- completed

---

## 🏗 MONOREPO STRUCTURE (MANDATORY)

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

---

## 🧠 WORKFLOW YOU MUST FOLLOW

1️⃣ Read all specs:
- @specs/overview.md
- @specs/features/task-crud.md
- @specs/features/authentication.md
- @specs/api/rest-endpoints.md
- @specs/database/schema.md
- @specs/ui/components.md
- @specs/ui/pages.md

2️⃣ Generate Phase II architecture & plan

3️⃣ Break plan into tasks:
- Backend setup
- Auth middleware
- Database integration
- API routes
- Frontend pages
- UI animations
- API client
- JWT wiring

4️⃣ Implement step-by-step:
- Backend first
- F
```

## Response snapshot

The project constitution has been successfully updated from version 1.1.0 to 2.0.0 to reflect the transformation from a console-based Todo app to a full-stack web application with authentication, database, and modern UI. The update included:

1. Completely redesigned core principles for full-stack architecture
2. Added new principles for JWT Authentication & Authorization, Multi-User Data Isolation, Modern UI/UX, Next.js Frontend, and SQLModel + Neon PostgreSQL
3. Removed the Console-Centric Interface principle as it's no longer applicable
4. Updated technical requirements to reflect the new technology stack
5. Created all required spec files:
   - specs/overview.md
   - specs/architecture.md
   - specs/features/task-crud.md
   - specs/features/authentication.md
   - specs/api/rest-endpoints.md
   - specs/database/schema.md
   - specs/ui/components.md
   - specs/ui/pages.md
6. Created frontend and backend CLAUDE.md files with specific guidelines
7. Updated the root CLAUDE.md to reflect the Todo App Phase II objectives

## Outcome

- ✅ Impact: Major overhaul of project constitution for Phase II upgrade from console to full-stack web application
- 🧪 Tests: No tests required for documentation changes
- 📁 Files: 13 files created/updated including constitution, specs, and guidelines
- 🔁 Next prompts: Generate architecture & plan for Phase II implementation
- 🧠 Reflection: Successfully transformed the project constitution to align with the new full-stack architecture requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing the backend components