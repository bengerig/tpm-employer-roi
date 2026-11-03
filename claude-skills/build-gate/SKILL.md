---
name: build-gate
description: "Pre-flight gate for Ben's technical build work. Fires automatically on build, automate, wire up, set up, script, deploy, connect, or fix requests whose output is something that runs, including standing up monitoring, verification or trial routines for a build. Also fires on a second acceptance test failure, and holds a stall comparison he invokes by name."
---

# Build Gate

Ben's builds fail in a predictable way. Not from bad code. From a build that quietly outgrows the problem, and from a session that keeps grinding because each individual next step looked reasonable. This skill makes both visible while they are still cheap.

Two parts with two different entry points.

**Part 1, pre-flight.** Fires on its own the moment a build request lands. Establishes five items and writes them to a gate file.

**Part 2, stall comparison.** Runs only when Ben asks for it by name, or when he opens a fresh session with an acceptance test and a failure summary pasted in. You cannot see a stall from inside the session that is having one, so do not try to declare one. What Part 1 does instead is print a count that lets Ben see it himself and make the call.

If the incoming request is a build, go to Part 1. If Ben is asking for the stall comparison, or has pasted a failure summary, go to Part 2. Read only the part in play.

---

# Part 1. Pre-flight

## Scope

Applies to delivery mode. Building, automating, wiring up, scripting, deploying, standing up an agent, configuring a connector, writing a migration, fixing a broken pipeline.

Does not apply when the output is something people read. Writing, strategy, research, labor market analysis, a deck or memo, an agenda, a governance model. Building the machinery that produces those documents is still a build and does apply. If Ben is still deciding whether to build a thing, this is not live yet. It goes live the moment he says build it.

Ambiguous cases resolve toward running pre-flight. On a ten minute script it costs one exchange. Skipping it on a three day build costs three days.

## The five items

These go on the record before the first line of code.

0. **Existing coverage.** Name what already delivers this outcome today: a Claude routine, a skill, a connector, or Ben doing it by hand and how often. If something already covers it, the build must beat it on one named measure (minutes of Ben's time, accuracy, cost) and that measure goes into the acceptance test. If nothing beats the existing path on a measure, recommend not building and stop. This check exists because the Hermes ETC brief duplicated a working Claude morning brief and digest while costing more to run and watch.

1. **Business outcome.** What changes for Ben, a collaborative, an employer, or a funder once this runs. Not the technical result. "Grant deliverable status is current without me reading five docs" is an outcome. "A sync script" is not.
2. **Minimum acceptance test.** One concrete observable that decides pass or fail. Runnable, checkable, and small enough to run repeatedly. "Running `x` against last month's file emits 14 rows and no errors" is an acceptance test. "It works reliably" is not.
3. **Complexity ceiling.** Three maximum counts. Platforms, orchestration layers, integrations. A platform is a distinct runtime or service the build depends on. An orchestration layer is anything that schedules, chains, or supervises other steps. An integration is a distinct external API or data source. Monitoring counts. Every scheduled check, inspection, recheck chain or verification routine set up to watch the build is an orchestration layer against the ceiling, and it uses the run-verifier skill rather than a hand-written prompt.
4. **Kill criteria.** Stated in elapsed hours, or in repeated failures of the acceptance test, or both.

If Ben supplied all five, restate them and start.

If he did not, propose concrete defaults for the missing items and get one confirmation. Propose, do not interrogate. One compact block he can approve or amend in a single reply. Never walk the items across several turns, and never write code while any item is open.

Starting defaults when he gives you nothing to work from.

| Item | Default |
|------|---------|
| Complexity ceiling | 2 platforms, 1 orchestration layer, 2 integrations |
| Kill criteria | 3 hours elapsed, or 3 failed acceptance test runs on the same component, or $15 compute spent with no green |

Size the ceiling to the actual build rather than reaching for the default. A local rename script is 1/0/0. The default is a ceiling for a real integration, not a floor for everything.

Business outcome and acceptance test have no generic default. Infer both from what he asked for, state your inference plainly, and let him correct it.

When the session is unattended and no confirmation is possible, write the gate file with the assumed items, say so at the top of the work, and proceed only if the build is reversible. If it is not reversible, do the preparatory work and stop.

## The gate file

Once confirmed, write the items to `build-gate.md` beside the build, before writing code. Add a short suffix to the filename when more than one build lives in the same folder.

```markdown
# Build gate

Existing coverage: <what does this today> | measure to beat:
Outcome:
Acceptance test:
Ceiling: N platforms / N orchestration / N integrations (monitoring included)
Kill criteria:
Started: <date -Iseconds>
Spend at start: <cost_usd from get_session, or unknown>

## Log
- <timestamp> gate confirmed
- <timestamp> acceptance test PASS or FAIL, one line on what changed
```

The file exists so the gate outlives the session. Ben can reopen a build a week later, or hand it to a fresh session, without reconstructing what he agreed to. Append a log line at every acceptance test run. Do not rewrite history in it.

## The status line

Run `date` at gate close to record wall clock start. Then open every build turn with one line.

```
BUILD | green: turn 6 (3 ago) | fails 1 | elapsed 1h12m | spend $4.10 | ceiling 2/1/2 of 2/1/2 | kill 3h or 3 fails or $15
```

- **green** is the turn number of the last passing acceptance test run and how many turns ago that was. If it has never passed, write `green: none (7 since gate)`.
- **elapsed** comes from an actual `date` call each turn, not estimation.
- **ceiling** is platforms/orchestration/integrations currently in the build against the maximums.
- **fails** is the count of acceptance test failures since the last green, counted across sessions and unattended runs from the gate file log, not only this thread.
- **spend** is `usage.cost_usd` from `get_session` (session_id omitted) minus the spend at start. Laptop-bridge sessions report no cost. Write `spend unknown` there and never guess.
- **kill** repeats the criteria verbatim.

A turn is one response from you. Count every response in the build, including ones that only ran a command.

The reason to print this is that it hands Ben a count he can verify without your cooperation. He counts your responses since the last one that reported a green test. He reads a clock. If the line stops appearing, or its numbers do not match what he can see in the thread, that is itself the signal.

## When the count crosses a line

Say so plainly and recommend that Ben run the stall comparison in a fresh session. Do not run it yourself from inside the build, and do not reason past the count because the current attempt feels close. Feeling close is what the count exists to overrule.

Surface it when any of these is true.

- A second acceptance test failure with the same failure signature, in this session or in any scheduled run or trial logged in the gate file. Provider errors, timeouts, OVER_CAP and an unreachable machine all count as failures of the build. They are not outside the build's control.
- Half the spend criterion is used with no green.
- 8 turns since the last passing acceptance test run.
- The acceptance test has never passed and 8 turns have elapsed since gate close.
- Half the kill criteria hours have elapsed with no green.
- A step would exceed any of the three ceiling counts. This one stops and goes back to Ben regardless of the count, because it changes the architecture he approved.
- The kill criteria are reached. This one stops the build.

When you surface it, produce the handoff block below and stop writing code.

```
BUILD HANDOFF

Existing coverage:
Outcome:
Acceptance test:
Ceiling:
Kill criteria:

What was tried:
Observable failure:
Ruled out:
```

Carry the gate items, the failure summary, and nothing else. Not the code from the failed approach, not the debugging narrative, not any reasoning about work already done. Tell Ben to paste this into a fresh session. Continuation is the failure mode, not the recovery, because this thread already holds the failed approach in context and will keep proposing variants of it.

## What not to do

- No scoring rubrics, weighted matrices, confidence percentages, or risk ratings.
- No effort or duration estimates for remaining work. Kill criteria are a budget Ben set, not a forecast you produce.
- No enhancements, hardening, or refactoring proposals until the acceptance test passes.
- No new dependency, agent, or orchestration layer without first stating why the simpler path fails.
- No monitoring of a build that has not passed its acceptance test once by hand. Watching a red build on a schedule produces reports, not progress.
- No treating a passing unit test or a clean run as a green unless it is the acceptance test as written.

---

# Part 2. Stall comparison

Run this only when Ben asks for it, or when he opens with an acceptance test and a failure summary. Never launch it on your own from inside a running build.

## Inputs

Work from what Ben pasted. Usually the gate items and a failure summary, from `build-gate.md` or a handoff block. If the acceptance test or the observable failure is missing, ask for that one thing and nothing else. Do not ask for the code, the transcript, or the history of attempts. Their absence is deliberate. Reading the failed approach in detail is how you end up recommending a variant of it.

## The four paths

Present all four. For each one, state what it keeps, what it discards, and what it costs from where the build now stands. No scores, no percentages, no hour estimates for the work ahead. Those are false precision and Ben has rejected them.

| Path | Meaning |
|------|---------|
| Continue | Same approach, same architecture. Justify it against the observed failure, not against sunk effort. If the only argument for continuing is how much is already built, that is not an argument. |
| Simplify | Cut scope, a platform, a layer, or an integration and pass a narrower acceptance test. Name exactly what gets cut and what the narrower test becomes. |
| Replace | Same acceptance test, different mechanism. Name the specific alternative, not a category. |
| Abandon | The outcome does not justify the build. Say what Ben does instead, including doing it by hand and how often that costs him. Name the existing coverage from item 0 if it already does the job. |

Weigh each path against the business outcome from the gate, not against the build. State the spend to date and the monitoring the build has needed. Both are costs of the path, not sunk effort. The question is whether the outcome still justifies what it now takes to get there.

## The recommendation

Close with one named path and the reason. Sunk effort is not a reason. Then stop and wait for Ben to choose.

If he picks continue, simplify, or replace, restate the gate with any items the choice changed, write a fresh `build-gate.md`, and start the build clean in this session. A path chosen after a stall gets a new gate, not an inherited one.