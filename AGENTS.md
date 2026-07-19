# AGENTS.md

# Photo Picker AI Development Guide

> **Read this document completely before making any changes to the project.**
>
> This file defines how AI agents should understand, navigate, and contribute to this repository.

---

# Project Overview

Photo Picker is a desktop application for rapidly selecting photos from large collections using a **keyboard-first workflow**.

Project goals:

- Fast
- Stable
- Offline
- Safe
- Minimal UI
- Zero data loss

This project intentionally favors **simplicity over complexity**.

---

# Mandatory Rules

Before writing, modifying, or deleting any code, ALWAYS follow this order:

1. Read `AGENTS.md`.
2. Identify the requested task.
3. Read every required document listed in **Task Routing**.
4. Understand the existing architecture.
5. Implement the smallest possible change.
6. Verify the implementation.
7. Update documentation if necessary.
8. Update `CHANGELOG.md` for every meaningful change.

Never skip documentation.

Never assume undocumented behavior.

---

# Documentation Loading Rules

All project documentation is located in:

```text
/docs
```

Before implementation, AI **MUST** load the documentation relevant to the task.

| Task                | Required Documents             |
| ------------------- | ------------------------------ |
| Product behavior    | `docs/PRD.md`                  |
| Architecture        | `docs/SYSTEM_ARCHITECTURE.md`  |
| Components          | `docs/COMPONENT_SPEC.md`       |
| Class relationships | `docs/CLASS_DIAGRAM.md`        |
| UI                  | `docs/UI_SPEC.md`              |
| User Flow           | `docs/USERFLOW.md`             |
| Keyboard Shortcuts  | `docs/SHORTCUT_SPEC.md`        |
| State Management    | `docs/STATE_MACHINE.md`        |
| Storage             | `docs/STORAGE_ARCHITECTURE.md` |
| Configuration       | `docs/CONFIGURATION.md`        |
| Error Handling      | `docs/ERROR_HANDLING.md`       |
| Development Tasks   | `docs/TASK_BREAKDOWN.md`       |
| Testing             | `docs/TEST_PLAN.md`            |
| Release History     | `CHANGELOG.md`                 |

---

# Task Routing

## If implementing UI

Read:

- `docs/UI_SPEC.md`
- `docs/USERFLOW.md`

---

## If implementing Startup Window

Read:

- `docs/UI_SPEC.md`
- `docs/CONFIGURATION.md`
- `docs/USERFLOW.md`

---

## If implementing Viewer

Read:

- `docs/UI_SPEC.md`
- `docs/SHORTCUT_SPEC.md`
- `docs/STATE_MACHINE.md`

---

## If implementing ViewerController

Read:

- `docs/COMPONENT_SPEC.md`
- `docs/CLASS_DIAGRAM.md`
- `docs/STATE_MACHINE.md`

---

## If implementing Workspace

Read:

- `docs/STORAGE_ARCHITECTURE.md`
- `docs/CONFIGURATION.md`
- `docs/ERROR_HANDLING.md`

---

## If implementing Repository

Read:

- `docs/STORAGE_ARCHITECTURE.md`
- `docs/COMPONENT_SPEC.md`

---

## If implementing Service

Read:

- `docs/COMPONENT_SPEC.md`
- `docs/ERROR_HANDLING.md`

---

## If implementing Keyboard Navigation

Read:

- `docs/SHORTCUT_SPEC.md`
- `docs/UI_SPEC.md`

---

## If fixing bugs

Read:

- `docs/ERROR_HANDLING.md`
- `docs/TEST_PLAN.md`

---

## If refactoring

Read:

- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/CLASS_DIAGRAM.md`
- `docs/COMPONENT_SPEC.md`

Refactoring must not change application behavior unless explicitly requested.

---

## If adding new features

Read:

- `docs/PRD.md`
- `docs/TASK_BREAKDOWN.md`

Then read any additional documents related to that feature.

---

# Documentation Priority

If documentation appears to conflict, follow this priority:

1. `docs/PRD.md`
2. `docs/SYSTEM_ARCHITECTURE.md`
3. `docs/COMPONENT_SPEC.md`
4. `docs/CLASS_DIAGRAM.md`
5. `docs/UI_SPEC.md`
6. `docs/USERFLOW.md`
7. `docs/STATE_MACHINE.md`
8. `docs/STORAGE_ARCHITECTURE.md`
9. `docs/CONFIGURATION.md`
10. `docs/SHORTCUT_SPEC.md`
11. `docs/ERROR_HANDLING.md`
12. `docs/TASK_BREAKDOWN.md`
13. `docs/TEST_PLAN.md`
14. `CHANGELOG.md`

Documentation is the source of truth.

---

# Architecture

The application uses a layered architecture.

```text
Presentation
    │
Controller
    │
Domain
    │
Services
    │
Repositories
    │
Storage
```

Never bypass architecture.

Forbidden:

- Presentation → Repository
- Presentation → Storage
- Service → UI
- Repository → UI

---

# Project Structure

```text
photo-picker/

docs/
src/
storage/
assets/
tests/
```

Follow `docs/FILE_STRUCTURE.md`.

---

# Development Principles

## Keep It Simple

Prefer the simplest implementation that satisfies the requirements.

Avoid unnecessary abstractions.

---

## Single Responsibility

Each class should have exactly one responsibility.

Avoid "God Classes".

---

## Thin Controllers

Controllers coordinate.

Business logic belongs in Domain or Services.

---

## Workspace First

Workspace is the Aggregate Root.

Never duplicate Workspace state.

Update Workspace before updating UI.

---

## Repository Pattern

Repositories only:

- Read data
- Write data

Repositories must never contain business logic.

---

## Services

Services perform operations.

Examples:

- Image loading
- File copy
- Cache creation
- Overlay rendering

Services never manipulate UI directly.

---

# Coding Standards

Follow:

- Python 3.12+
- PEP 8
- Type hints
- Small classes
- Small methods
- Meaningful names

Avoid:

- Global mutable state
- Long methods
- Deep nesting
- Magic numbers
- Duplicate code

---

# GUI Framework

Use:

```text
PySide6
```

Do not introduce another GUI framework.

---

# State Management

Application state is managed by:

- Workspace
- ViewerController

Follow:

`docs/STATE_MACHINE.md`

Never introduce hidden state.

---

# File Safety

Original files are immutable.

Allowed:

- Read originals
- Copy originals

Forbidden:

- Rename originals
- Delete originals
- Move originals
- Compress originals
- Modify metadata
- Overwrite originals

Data loss is unacceptable.

---

# Configuration

Global configuration:

```text
storage/settings.json
```

Workspace data:

```text
storage/workspaces/
```

Do not mix application settings with Workspace data.

Follow:

`docs/CONFIGURATION.md`

---

# Error Handling

Always follow:

`docs/ERROR_HANDLING.md`

Rules:

- Never crash unexpectedly.
- Continue whenever possible.
- Log every important error.
- Display clear messages.
- Preserve Workspace whenever possible.

---

# Performance Goals

Navigation should feel instant.

Optimize:

- Background preloading
- Memory cache
- Lazy loading

Avoid unnecessary disk access.

---

# Keyboard First

Everything must be usable without a mouse.

Keyboard behavior is defined in:

`docs/SHORTCUT_SPEC.md`

Never change shortcuts without updating the documentation.

---

# UI Principles

The interface should be:

- Minimal
- Fast
- Responsive
- Clean
- Distraction-free

Avoid:

- Excessive dialogs
- Decorative animations
- Complex layouts

---

# Documentation Update Rules

Whenever project behavior changes, update the relevant documentation.

Possible updates include:

- `docs/PRD.md`
- `docs/UI_SPEC.md`
- `docs/USERFLOW.md`
- `docs/COMPONENT_SPEC.md`
- `docs/SYSTEM_ARCHITECTURE.md`
- `docs/CLASS_DIAGRAM.md`
- `docs/STATE_MACHINE.md`
- `docs/STORAGE_ARCHITECTURE.md`
- `docs/CONFIGURATION.md`
- `docs/SHORTCUT_SPEC.md`
- `docs/ERROR_HANDLING.md`
- `CHANGELOG.md`

Documentation must always reflect the implementation.

---

# Testing

Every implemented feature should satisfy:

`docs/TEST_PLAN.md`

Do not consider a task complete until its relevant test cases pass.

---

# Definition of Done

A task is complete only if:

- Code builds successfully.
- No obvious lint issues.
- Type checking passes.
- Manual tests pass.
- Architecture remains consistent.
- Documentation is updated when required.
- `CHANGELOG.md` is updated when applicable.

---

# AI Agent Responsibilities

AI agents should:

- Read documentation before coding.
- Preserve architecture.
- Reuse existing components.
- Avoid unnecessary dependencies.
- Keep implementations minimal.
- Explain significant design decisions.
- Produce maintainable code.

---

# AI Agent Restrictions

Never:

- Rewrite the architecture without explicit request.
- Introduce another GUI framework.
- Ignore documented behavior.
- Create duplicate components.
- Refactor unrelated code.
- Remove existing functionality unless instructed.
- Invent features not described in the documentation.

---

# Final Principle

When multiple valid implementations exist:

Choose the solution that is:

1. Easiest to understand.
2. Consistent with the existing architecture.
3. Easiest to maintain.
4. Least surprising to future contributors.

Clarity is always preferred over cleverness.
