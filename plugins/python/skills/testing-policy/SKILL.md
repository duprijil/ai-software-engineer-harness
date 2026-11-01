---
name: testing-policy
description: States the current testing policy, which is that agents do not write or run tests because the engineer does all testing. Use whenever a task involves tests, pytest, coverage, TDD, verification or a definition of done, and at the end of any code change.
---

# Testing policy

We don't do tests now. The testing is done by the real engineer.

## The agent never

- creates, edits, deletes or runs tests
- adds pytest, coverage tools, test folders or `test` Makefile targets
- adds test jobs or coverage settings to CI or Sonar
- plans test work in specs or task lists

Don't suggest adding tests, or describe missing tests as a problem. This holds even when the repo already has tests. If the engineer explicitly asks for a test in a task, do that one thing.

## The agent still

- runs `make format` and `make check`
- may run the code it wrote, when that's safe, to confirm it works
- reports honestly what it did and did not verify

## Handoff

End every code change with a short list for the engineer:

```markdown
**What to test**
- `make ingest-cars` with an empty provider response: exits cleanly and saves nothing
- Saving a car with a duplicate ID: raises `CarAlreadyExistsError`
```

Each item names the scenario to try and the expected outcome. Focus on the risky behavior this change touched, and keep the list short.
