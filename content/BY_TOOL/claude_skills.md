# Claude Skills & Workflow Patterns

Patterns learned from building and debugging Claude Skills and multi-agent workflows.

---

## Portability

### Never Use Symlinks in Git
**Problem:** Symlinks store absolute paths. When cloned elsewhere, they break.
```
# Bad: symlink to /Users/dp/Projects/multi-agent-workflow/scripts
# In Claude Code web: "No such file or directory"
```
**Solution:** Use copy mode for anything that needs to work across environments.

### .skill Files Are Zips
**Problem:** Claude.ai skills are zip files. Claude Code can't read inside them.
**Solution:** Extract skill content to plain markdown files alongside the .skill files.

### Always Test in Claude Code Web
**Problem:** Works locally ≠ works in Claude Code web container.
**Solution:** After any workflow change, test in Claude Code web before assuming it works.

---

## Context Management

### Fresh Context Per Phase
**Problem:** One chat accumulates context until overflow.
**Solution:** Each workflow phase starts a fresh chat. State persists in files, not context.

### State Files Over Memory
**Problem:** Claude can't remember across sessions.
**Solution:** `WORKFLOW_STATE.json` tracks progress. Any Claude instance can pick up where another left off.

### Explicit Instructions Beat Implicit Knowledge
**Problem:** Claude improvises when instructions are vague.
**Solution:** Phase guides should be explicit: "Create AGENT_PROMPTS/ directory with files named 1_role.md"

---

## Multi-Agent Coordination

### 3-4 Agents, Not 5
**Problem:** 5 agents = more coordination overhead, diminishing returns.
**Solution:** 3-4 agents is the sweet spot for most projects.

### Clear Boundaries Prevent Conflicts
**Problem:** Agents modify same files = merge conflicts.
**Solution:** Agent prompts must specify exact files. COORDINATION.md documents who touches what.

### Dependencies Dictate Merge Order
**Problem:** Merging in wrong order breaks things.
**Solution:** COORDINATION.md includes dependency graph. Merge foundations first.

### Sprint Check-ins Over Fire-and-Forget
**Problem:** Agent goes off track for 2 hours before you notice.
**Solution:** 30-60 min sprints with progress reports. Adjust prompts between sprints.

---

## File Organization

### Namespace Workflow Files
**Problem:** Workflow files mixed with project files = confusion.
**Solution:** All workflow files under `workflow/` directory in each project.

### Copy Learnings, Don't Link
**Problem:** Symlinked learnings break in Claude Code.
**Solution:** `init-project --copy` copies learnings snapshot. Aggregate back periodically.

### Phase Guides as Plain Markdown
**Problem:** Instructions buried in zip files or scattered docs.
**Solution:** `workflow/phases/phase1-planning.md` through `phase6-iteration.md`. Claude reads directly.

---

## Common Mistakes

### Don't Trust Claude to Follow Structure
If you want `AGENT_PROMPTS/1_backend.md`, say exactly that. Don't say "create agent prompts" and hope for the right structure.

### Don't Skip the Phase Guide
Tell Claude: "Read workflow/phases/phase3-codex-review.md and follow the instructions"
Not: "Do a codex review" (Claude will improvise)

### Don't Mix Portable and Local Paths
Either everything is portable (copy mode) or everything is local (link mode). Mixing causes subtle breaks.

---

## CLAUDE.md Placement

### Different Contexts Need Different Locations
**Date:** 2025-12-12
**Project:** professional-development
**Context:** Setting up consistent Claude behavior across environments

**Problem:**
CLAUDE.md with user preferences (SSH config, code style, commit conventions) only works in one context. New Claude Code sessions keep forgetting SSH preference.

**Solution:**
Place CLAUDE.md in different locations for each context:

| Environment | Location | How It Works |
|-------------|----------|--------------|
| Claude Code CLI (local) | `~/.claude/CLAUDE.md` | Auto-loaded every session |
| Claude Code Web | Repo root `/CLAUDE.md` | Agent clones repo, reads it |
| claude.ai Projects | Project Knowledge files | Uploaded as project context |
| claude.ai (no project) | User Preferences in Settings | Limited, not full CLAUDE.md |

**Prevention:**
- Full CLAUDE.md at `~/.claude/CLAUDE.md` for local CLI
- Trimmed agent-focused CLAUDE.md in every repo root
- Critical env notes (like SSH) at top of file so Claude sees them early

---

## Quick Reference

```bash
# Initialize project (portable)
/path/to/multi-agent-workflow/bin/init-project --copy /path/to/project

# Check workflow state
python workflow/core/workflow_state.py . status

# Start phase 3
# Tell Claude: "Read workflow/phases/phase3-codex-review.md and follow the instructions"

# After changes to central learnings, re-init projects
/path/to/multi-agent-workflow/bin/init-project --copy .
```

---

## Claude Code Hooks

### Hooks May Not Fire in v2.0.76
**Date:** 2026-01-01
**Problem:**
Configured hooks in `~/.claude/settings.json` for SessionStart and UserPromptSubmit. Tried multiple formats:
```json
// Format 1: matcher as object (error: expected string)
{"matcher": {}, "hooks": [...]}

// Format 2: no matcher (no error, but didn't fire)
{"hooks": [...]}
```
Hooks never fired - tested with `touch /tmp/hook-fired` command.

**Solution:**
Use CLAUDE.md as fallback. Add "Session Rituals" section at top of `~/.claude/CLAUDE.md`:
```markdown
## Session Rituals (IMPORTANT)

### On Session Start
Proactively run `/capability-sync` (keep output brief)

### On Session End
When I say "wrap up" / "session end", run `/session-end`
```
Claude reads CLAUDE.md every session, so instructions are followed even when hooks don't work.

**Prevention:**
- Always have CLAUDE.md fallback for critical automation
- Hybrid approach: hooks for when they work + CLAUDE.md + manual skills
- Test hooks with simple commands (`touch file`) before complex logic

---

## Cross-Platform Skills

### Skills Work in Desktop If Properly Set Up
**Date:** 2026-01-01
**Problem:**
Skills defined for Claude Code (`/capability-sync`, `/session-end`) needed to work in Claude Desktop app too.

**Solution:**
1. Skills live in `/Users/dp/Projects/skills/` with SKILL.md files
2. Symlinked to `~/.claude/skills/` for Claude Code
3. For Desktop: add skills to Desktop app's MCP or project knowledge
4. Create platform-specific preferences file for Desktop settings

**Key Insight:**
The Skill tool invokes skills by name. As long as the skill definition is accessible, it works. Desktop needs skill content in its context (project knowledge or MCP).

---

*Last updated: 2026-01-01*
*Source: Session automation debugging, capability sync refactor*
