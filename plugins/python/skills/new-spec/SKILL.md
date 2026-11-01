---
name: new-spec
description: Interviews the engineer and writes a feature specification in docs/specs for approval before coding. Use when asked to plan, specify or design a new feature, or when a new feature is requested and no approved spec exists yet.
---

# New spec

Every new feature needs an approved spec before code. Bug fixes, refactors and small changes need only a ticket.

## 1. Get the ticket

Ask for the ticket ID if you don't have it. Its format is in `AGENTS.md`. Don't continue without one.

## 2. Understand the context

Read `AGENTS.md`, the related `docs/domains/*.md`, and the code in the affected domains. Don't ask what the code already answers.

## 3. Interview the engineer

Ask until you could implement the feature without guessing. Ask a few focused questions per round, and offer a recommendation with each. Cover:

- the problem and who has it
- behavior and edge cases
- what's out of scope
- which domains it touches, and whether it needs a new domain or a combined domain
- new ports, adapters, config, secrets or services
- failure handling

## 4. Write the spec

Copy `assets/spec_template.md` from this skill to `docs/specs/<ticket>-<domain>-<slug>.md`, for example `docs/specs/TED-123-car-add-scd2-ingest.md`. Use lowercase hyphens in the slug. Remove any section that doesn't apply.

- Acceptance criteria describe observable behavior, and each can be checked by the engineer.
- List exact files using `python:architecture` and `python:naming`.
- Don't plan tests. See `python:testing-policy`.

## 5. Get approval

Keep the status as `Draft`, and ask the engineer to review it. Set it to `Approved` only after they say so. Then, and only then, start coding.

## 6. Keep it current

If the design changes while coding, update the spec in the same change. Set `Implemented` when the work is finished.
