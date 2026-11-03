# Claude skills

Six skills from the Nov 3, 2026 time review. Each folder holds a SKILL.md. Each zip in `zips/` is ready to upload.

| Skill | Status | Replaces |
|---|---|---|
| run-verifier | new | Hand-written ETC package checks and ten-minute recheck chains |
| build-gate | update | Adds existing coverage check, monitoring counted against the ceiling, spend tally, second-failure stop |
| system-audit | new | Separate inventory and registry audits, Brain Upkeep Part C |
| session-handoff | new | Hand-drafted next-session prompts |
| routine-author | new | Boundary rules retyped into each routine prompt |
| daily-briefing | update (cs plugin) | Separate heartbeat and midday nudge prompts |

## Install

- New skills and build-gate. Go to claude.ai, Settings, Capabilities, Skills. Upload the zip. Replace the existing build-gate.
- daily-briefing lives in the cs plugin. Replace `skills/daily-briefing/SKILL.md` in the plugin source and resync it.
