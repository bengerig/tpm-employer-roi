---
name: session-handoff
description: "Writes and reads a fixed HANDOFF.md so work moves cleanly between Claude sessions, surfaces and machines. Use when Ben says wrap up, hand off, park this, write the next session prompt, pick up where we left off, resume, continue from the other session, or when a session cannot finish where it is (for example a tool only reachable from the CLI on his PC). Not for a stalled build. That goes to build-gate's BUILD HANDOFF."
---

# Session Handoff

Ben's work often spans several sessions, including CLI on his PC, cloud sessions and Cowork. Each one used to end with a fresh hand-written prompt for the next. This skill replaces that with one file in a fixed shape. It is written at the end and read first at the start.

Two modes. **Write** when a session ends with work left. **Resume** when a session starts on work that has a handoff file.

Use build-gate instead when the reason for stopping is a stall. That handoff deliberately carries no narrative. This one carries working state for a session that is healthy but has to stop.

## Where the file lives

`HANDOFF.md` in the root of the work: the repo, the build folder or the collaborative folder. If several workstreams share a folder, use `HANDOFF_<short-name>.md`. Never put it under a watched containment root such as Hermes-OS. Use the matching review or build folder outside it.

## Write mode

Overwrite the file with the current state. Keep the previous state as one line under History. Stay under 40 lines.

```markdown
# Handoff: <workstream>

Updated: <date -Iseconds> by <surface: CLI on ben-pc | cloud | Cowork>
Lane: CS | HTS | personal | system
Resume on: <surface the next step needs, and why>

## State
- Repo/folder: <path>, branch <name>, HEAD <short sha> (clean | uncommitted: <files>)
- Last verified: <acceptance test or check> PASS/FAIL at <time>
- Running or scheduled: <task names and IDs that touch this work>

## Next step
<one concrete action, with the command or file to start from>

## Open decisions for Ben
- <decision> (options, recommendation)

## Blockers
- <blocker> (what unblocks it)

## Do not
- <things the next session must not touch or redo>

## History
- <date> <one line on the previous state>
```

Rules for writing.

- Run `git rev-parse --short HEAD` and `git status --short`, or the folder equivalent, so State is observed and not remembered.
- Next step is one action. If there are several, the first one goes here and the rest go under Open decisions.
- No transcript, no debugging narrative, no code from failed attempts.
- Never put credential values, `.env` contents, personal contact details or mail text in the file.
- CS handoffs never mention HTS work. HTS handoffs never mention CS work.

After writing, give Ben a two-line message with the file path and the one-line prompt for the next session.

```
Load session-handoff and resume from <path>.
```

## Resume mode

1. Read the handoff file before anything else.
2. **Check for drift.** Compare State against what you observe now, including HEAD, uncommitted files, scheduled task status and the last verified result. List each difference in one line.
3. If you are on the wrong surface for `Resume on`, say so in one line, write nothing, and stop.
4. If the drift changes the next step, say how and propose the corrected step. Wait for one confirmation.
5. Otherwise start the Next step. Open decisions stay open until Ben answers them. Do not decide them by acting.
6. When the session ends with work left, switch to write mode.

## Style

Short declarative lines. No em dashes, no en dashes, no hyphens joining clauses, no colons delivering a point, no emojis.
