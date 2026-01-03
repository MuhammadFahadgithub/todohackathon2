---
id: 001
title: Initial Constitution Creation
stage: constitution
date: 2026-01-02
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 001-todo-core-features
user: user
command: /sp.constitution
labels: ["constitution", "governance", "sdd", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

You are the Constitution Agent for this project.

Your role is to define the non-negotiable principles, rules, and quality bars that govern **all future specs, plans, tasks, and implementations** in this repository.

This project is a **Todo Application** built using **Spec-Driven Development (SDD)** with **SpecKit Plus**, executed via **Claude CLI**, and supported by multiple agents and skills.

---

## Project Purpose

Build a clean, reliable, and extensible Todo application using **spec-first thinking** where:
- Requirements are clarified before coding
- Decisions are documented
- Small, testable increments are preferred
- AI agents behave predictably and responsibly

---

## Core Principles (Non-Negotiable)

### 1. Spec Before Code
- No implementation is allowed without:
  - `/sp.specify`
  - `/sp.plan`
  - `/sp.tasks`
- Code must **trace back** to an approved spec or task.

### 2. Small & Verifiable Changes
- Every change must be:
  - Small
  - Testable
  - Reviewable
- Avoid large refactors unless explicitly planned.

### 3. Single Source of Truth
- Specs are the authority — **not assumptions**.
- If something is unclear, the agent must:
  - Ask clarifying questions
  - Or update the spec before proceeding.

### 4. Explicit Decisions
- Architecturally significant choices must:
  - Be detected
  - Be surfaced to the user
  - Suggest creating an ADR (`/sp.adr`)
- Never auto-create ADRs without consent.

---

## Agent Behavior Rules

### Agents MUST:
- Follow SpecKit Plus workflow strictly
- Use MCP / CLI tools when available
- Record Prompt History Records (PHRs) for:
  - Implementation work
  - Planning/architecture discussions
  - Debugging sessions
  - Spec/task/plan creation
  - Multi-step workflows

## Response snapshot

Created the initial Todo App Constitution v1.0.0 with:
- 4 Core Principles: Spec Before Code, Small & Verifiable Changes, Single Source of Truth, Explicit Decisions
- Agent Behavior Rules section with MUST/MUST NOT constraints
- Human as Tool Strategy for user invocation triggers
- Quality Standards covering code, testing, performance, and security
- Governance section with amendment procedure, versioning policy, and compliance review

All dependent templates verified compatible:
- plan-template.md: Constitution Check section aligns
- spec-template.md: User Stories + Requirements structure compatible
- tasks-template.md: Phase structure compatible

## Outcome

- Impact: Established foundational governance for all future Todo App development
- Tests: N/A (governance document)
- Files: .specify/memory/constitution.md (created v1.0.0)
- Next prompts: `/sp.specify` for first feature, consider `/sp.adr` for tech stack decisions
- Reflection: Constitution provides clear guardrails for spec-driven development workflow

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution principles during first `/sp.specify` run
