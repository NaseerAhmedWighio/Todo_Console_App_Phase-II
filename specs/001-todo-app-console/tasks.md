---
description: "Task list for In-Memory Python Console App Todo Application"
---

# Tasks: In-Memory Python Console App Todo Application

**Input**: Design documents from `/specs/001-todo-app-console/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python 3.9+ project with FastAPI, uvicorn, Pydantic, pytest dependencies in pyproject.toml
- [X] T003 [P] Configure linting and formatting tools (flake8, black, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task model in src/models/task.py with Pydantic validation
- [X] T005 [P] Create in-memory storage implementation in src/storage/in_memory.py
- [X] T006 Create TodoService with atomic operations in src/services/todo_service.py
- [X] T007 Configure error handling and logging infrastructure
- [X] T008 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items and view their existing tasks with descriptions and completion status

**Independent Test**: Can be fully tested by adding multiple tasks through the console and viewing the complete list, delivering core value of task management.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T009 [P] [US1] Contract test for GET /tasks endpoint in tests/contract/test_api_endpoints.py
- [ ] T010 [P] [US1] Contract test for POST /tasks endpoint in tests/contract/test_api_endpoints.py
- [ ] T011 [P] [US1] Unit test for Task model validation in tests/unit/test_models/test_task.py
- [ ] T012 [P] [US1] Unit test for TodoService add_task functionality in tests/unit/test_services/test_todo_service.py
- [ ] T013 [P] [US1] Unit test for TodoService get_all_tasks functionality in tests/unit/test_services/test_todo_service.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Task model in src/models/task.py with all required fields and validation
- [X] T015 [P] [US1] Create TaskResponse model for API responses in src/models/task.py
- [X] T016 [US1] Implement add_task functionality in src/services/todo_service.py
- [X] T017 [US1] Implement get_all_tasks functionality in src/services/todo_service.py
- [X] T018 [US1] Implement get_task_by_id functionality in src/services/todo_service.py
- [X] T019 [US1] Create GET /tasks endpoint in src/api/main.py
- [X] T020 [US1] Create POST /tasks endpoint in src/api/main.py
- [X] T021 [US1] Create CLI add_task command in src/cli/cli_app.py
- [X] T022 [US1] Create CLI view_tasks command in src/cli/cli_app.py
- [X] T023 [US1] Add validation and error handling for empty descriptions
- [X] T024 [US1] Add logging for user story 1 operations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Allow users to modify existing task details or remove tasks they no longer need

**Independent Test**: Can be fully tested by modifying and deleting tasks through the console, delivering enhanced task management capabilities.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Contract test for PUT /tasks/{id} endpoint in tests/contract/test_api_endpoints.py
- [ ] T026 [P] [US2] Contract test for DELETE /tasks/{id} endpoint in tests/contract/test_api_endpoints.py
- [ ] T027 [P] [US2] Unit test for TodoService update_task functionality in tests/unit/test_services/test_todo_service.py
- [ ] T028 [P] [US2] Unit test for TodoService delete_task functionality in tests/unit/test_services/test_todo_service.py

### Implementation for User Story 2

- [X] T029 [P] [US2] Create TaskUpdate model for API updates in src/models/task.py
- [X] T030 [US2] Implement update_task functionality in src/services/todo_service.py
- [X] T031 [US2] Implement delete_task functionality in src/services/todo_service.py
- [X] T032 [US2] Create PUT /tasks/{id} endpoint in src/api/main.py
- [X] T033 [US2] Create DELETE /tasks/{id} endpoint in src/api/main.py
- [X] T034 [US2] Create CLI update_task command in src/cli/cli_app.py
- [X] T035 [US2] Create CLI delete_task command in src/cli/cli_app.py
- [X] T036 [US2] Add validation and error handling for non-existent tasks
- [X] T037 [US2] Add logging for user story 2 operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P3)

**Goal**: Provide progress tracking functionality by allowing users to toggle task completion status

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete through the console, delivering progress tracking value.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T038 [P] [US3] Contract test for PUT /tasks/{id}/complete endpoint in tests/contract/test_api_endpoints.py
- [ ] T039 [P] [US3] Contract test for PUT /tasks/{id}/incomplete endpoint in tests/contract/test_api_endpoints.py
- [ ] T040 [P] [US3] Unit test for TodoService mark_task_complete functionality in tests/unit/test_services/test_todo_service.py
- [ ] T041 [P] [US3] Unit test for TodoService mark_task_incomplete functionality in tests/unit/test_services/test_todo_service.py

### Implementation for User Story 3

- [X] T042 [P] [US3] Create TaskStatusUpdate model for status changes in src/models/task.py
- [X] T043 [US3] Implement mark_task_complete functionality in src/services/todo_service.py
- [X] T044 [US3] Implement mark_task_incomplete functionality in src/services/todo_service.py
- [X] T045 [US3] Create PUT /tasks/{id}/complete endpoint in src/api/main.py
- [X] T046 [US3] Create PUT /tasks/{id}/incomplete endpoint in src/api/main.py
- [X] T047 [US3] Create CLI mark_task_complete command in src/cli/cli_app.py
- [X] T048 [US3] Create CLI mark_task_incomplete command in src/cli/cli_app.py
- [X] T049 [US3] Add validation and error handling for status operations
- [X] T050 [US3] Add logging for user story 3 operations

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T051 [P] Documentation updates in README.md
- [X] T052 Code cleanup and refactoring
- [X] T053 Performance optimization across all stories
- [X] T054 [P] Additional unit tests to achieve 80%+ coverage in tests/
- [X] T055 Security hardening
- [X] T056 Run quickstart validation
- [X] T057 Create main application entry point in src/main.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for GET /tasks endpoint in tests/contract/test_api_endpoints.py"
Task: "Unit test for Task model validation in tests/unit/test_models/test_task.py"

# Launch all models for User Story 1 together:
Task: "Create Task model in src/models/task.py with all required fields and validation"
Task: "Create TaskResponse model for API responses in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence