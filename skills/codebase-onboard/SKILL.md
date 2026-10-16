---
name: codebase-onboard
description: >
  Use this skill when entering a new project or folder for the first time — reads key files,
  maps the directory structure, identifies tech stack and patterns, then asks targeted questions
  to clarify goals, architecture, and current state. Trigger on: first message in a new directory,
  "what is this project", "help me understand this codebase", "onboard me", "what are we working with",
  "give me an overview", opening a project you haven't seen before, or any request to understand
  unfamiliar code. Also activates when the user drops into a folder with no prior context.
domain: analysis
composable: true
yields_to: [process, craft]
---

# Codebase Onboard

I am the first conversation in a new space. I read, I map, I ask — so every subsequent response starts from understanding, not assumption.

---

## When to Use

- **First message in a new directory** — no prior context exists for this project
- **User asks to understand unfamiliar code** — "what is this", "help me understand", "onboard me"
- **Dropped into a project mid-conversation** — user references files or folders not yet seen
- **Returning to a project after long absence** — context may have shifted
- **Ambiguous project state** — unclear if this is new, existing, or inherited code

---

## Core Instructions

### Phase 1: Map the Terrain (Do This First)

Read the directory listing and key metadata files to form an initial mental model. Order matters — start broad, then narrow.

```
1. List root directory          → see what exists
2. Read README.md (if present)  → project's self-description
3. Read package.json / pyproject.toml / Cargo.toml / go.mod / pom.xml
                                  → dependencies, scripts, entry points
4. Read .gitignore              → what's intentionally excluded
5. Scan src/ or equivalent      → code structure
6. Check for config files       → .env.example, docker-compose, CI configs
```

**Why this order**: The root directory tells you the project type. README tells you intent. Dependency files tell you the stack. Config files tell you the environment. Source structure tells you the architecture.

**If files are missing, note them** — a project without a README is a signal, not a failure.

### Phase 2: Build the Mental Model

After reading, synthesize these dimensions:

| Dimension | Source | Example |
|-----------|--------|---------|
| **Purpose** | README, top-level comments | "E-commerce API for a bookstore" |
| **Stack** | Dependency files, imports | "Node.js + Express + PostgreSQL" |
| **Architecture** | Directory structure, entry points | "MVC with service layer" |
| **State** | Git log, TODO files, test coverage | "Active development, 60% test coverage" |
| **Conventions** | Linting config, naming patterns | "ESLint strict, camelCase, functional components" |

Present this as a concise summary — 5-10 lines max. Not a dump, a lens.

### Phase 3: Ask to Clarify

The summary is a hypothesis. Questions confirm or correct it. Ask the **most impactful** questions first — the ones that change how you'd approach the work.

**Priority order for questions:**

1. **Goal** — "What are you trying to accomplish with this project?" (Changes everything downstream)
2. **Current state** — "Is this new code, existing code you're maintaining, or code you inherited?" (Determines risk tolerance)
3. **Your role** — "Are you the author, a contributor, or exploring this for the first time?" (Determines depth of explanation)
4. **Pain points** — "Anything specific that's confusing or broken?" (Focuses subsequent effort)
5. **Conventions** — "Any patterns or preferences I should follow?" (Prevents rework)

**Ask 2-3 questions max per round.** A wall of 8 questions gets ignored. Prioritize based on what the initial scan couldn't determine.

**Frame questions to invite specifics, not yes/no:**

```
Good: "What's the main goal for this project — building new features, fixing bugs, or understanding it for a code review?"
Weak: "Do you want me to help with this project?"
```

### Phase 4: Confirm and Hand Off

After the user answers, restate your understanding in 2-3 sentences. This is the transition from onboarding to execution:

```
"Got it — this is a Next.js e-commerce app you inherited, and you need to add
payment integration. The current Stripe setup in src/services/payments.ts is a
starting point. Where should we begin — reviewing the existing payment flow or
planning the new integration?"
```

---

## What to Read by Project Type

Not every project has the same entry points. Adapt your scan:

| Project Type | Key Files to Read |
|-------------|-------------------|
| **Node.js** | package.json, tsconfig.json, src/index.ts, .eslintrc |
| **Python** | pyproject.toml, requirements.txt, src/__init__.py, setup.cfg |
| **Rust** | Cargo.toml, src/main.rs, src/lib.rs, .clippy.toml |
| **Go** | go.mod, main.go, cmd/, internal/ |
| **Monorepo** | Root package.json, workspace config, packages/ listing |
| **Data/Research** | README, notebooks/, data/ structure, requirements.txt |
| **Mobile** | pubspec.yaml (Flutter), package.json (RN), Info.plist (iOS) |
| **Infrastructure** | docker-compose.yml, Terraform files, k8s manifests |

---

## Output Format

Present your findings as a structured but concise summary:

```markdown
## Project Overview

**Purpose**: [One sentence]
**Stack**: [Key technologies]
**Architecture**: [Pattern — MVC, microservices, monolith, etc.]
**State**: [Active/Stable/Legacy/Experimental + any notable signals]

### Structure
[Tree of key directories with 1-line descriptions]

### Notable Patterns
[2-3 things that stood out — conventions, interesting choices, potential concerns]
```

Then follow with questions.

---

## Boundaries

- Does not modify any files during onboarding — read-only until the user directs action
- Does not persist onboarding findings to memory — that's the memory skill's job
- Does not reorganize project structure — that's folder-organization's domain
- Does not run code or install dependencies during the scan phase
- Does not make assumptions about intent beyond what the files and user explicitly state

---

## Self-Verification

After completing the onboarding scan, verify:

- [ ] At least 3 key files were read (not just directory listing)
- [ ] The summary includes purpose, stack, and architecture
- [ ] Questions are prioritized, not exhaustive (2-3 max)
- [ ] No files were modified during the scan
- [ ] The hand-off invites specific next action, not a generic "what now?"

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: analysis
composable: true
yields_to: [process, craft]
```

Codebase-onboard owns **analysis** — the act of examining and understanding unfamiliar code. It does not own what happens after understanding is established.

### When Codebase-Onboard Leads

- First encounter with a new project or directory
- User explicitly asks to understand or explore unfamiliar code
- Transitioning between projects in a session
- Assessing inherited or legacy codebases

### When Codebase-Onboard Defers

| Other Skill's Domain | What Codebase-Onboard Does |
|---------------------|---------------------------|
| **Process** (e.g., memory, planner) | Onboard provides the understanding; process skills handle what to do with it — persisting context, planning work, structuring tasks |
| **Craft** (e.g., painter, harden) | Onboard identifies the tech stack and patterns; craft skills handle code quality, design, and visual implementation |
| **Content** (e.g., documenter, researcher) | Onboard reads existing docs; content skills create new ones |
| **Density** (e.g., caveman, compress) | Onboard's summary can be compressed if the user wants brevity, but the scan phase itself is not compressed — full reads are required for accurate understanding |

### Pipeline Behavior

- **Upstream**: Codebase-onboard runs first in any new-project context. Its output (understanding + questions) feeds into whatever skill the user needs next.
- **Downstream**: After onboarding, the conversation naturally transitions to planning (planner), implementation (build), documentation (documenter), or refactoring (refactor).

### Conflict Signal

If another analysis skill is active (e.g., data-analytics on a data project):

> `⚠️ Analysis conflict: codebase-onboard provides structural overview; [other skill] provides domain-specific analysis. Onboard defers to the specialized skill for domain questions, but retains ownership of "what is this project?" understanding.`
