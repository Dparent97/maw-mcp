"""
Multi-Agent Workflow MCP Server

Provides tools to coordinate parallel AI agent development workflows.
Works with Cursor, Claude Code, and Claude.ai.
"""
import json
import re
from pathlib import Path
from typing import Optional

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import AnyUrl

from .state import (
    WorkflowState, AgentInfo, WaveInfo,
    load_state, save_state, format_status, suggest_next_step
)

# Server setup
server = Server("maw-mcp")
CONTENT_DIR = Path(__file__).parent.parent / "content"


def slugify(text: str) -> str:
    """Convert text to URL-safe slug"""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:30]


# =============================================================================
# TOOL: maw_status
# =============================================================================
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="maw_status",
            description="Show current workflow state and recommended next action",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Path to project (default: current directory)",
                        "default": "."
                    }
                }
            }
        ),
        Tool(
            name="maw_review",
            description="Phase 3: Analyze codebase, identify improvements, generate agent prompts. PAUSES for your review before agents can be launched.",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."},
                    "focus": {
                        "type": "string",
                        "description": "Optional focus area: security, performance, testing, docs, all"
                    },
                    "wave_name": {
                        "type": "string",
                        "description": "Name for this wave of improvements (e.g., 'Foundation & Security')"
                    }
                }
            }
        ),
        Tool(
            name="maw_launch",
            description="Phase 4: Get agent prompts with branch names and launch sequence",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."},
                    "agent_id": {
                        "type": "integer",
                        "description": "Get prompt for specific agent only"
                    }
                }
            }
        ),
        Tool(
            name="maw_checkin",
            description="Phase 4: Evaluate agent progress reports and get updated guidance",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."},
                    "reports": {
                        "type": "string",
                        "description": "Paste agent progress reports here"
                    }
                },
                "required": ["reports"]
            }
        ),
        Tool(
            name="maw_integrate",
            description="Phase 5: Get merge order, conflict detection, and integration checklist",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."}
                }
            }
        ),
        Tool(
            name="maw_decide",
            description="Phase 6: Get recommendation to deploy, iterate, or add features",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."}
                }
            }
        ),
        Tool(
            name="maw_learn",
            description="Capture learnings from current session to PROJECT_LEARNINGS.md",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "."},
                    "learning": {
                        "type": "string",
                        "description": "What you learned (or leave blank for guided capture)"
                    },
                    "promote": {
                        "type": "boolean",
                        "description": "Also add to central UNIVERSAL_PATTERNS.md",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="maw_patterns",
            description="Search or browse accumulated patterns from UNIVERSAL_PATTERNS.md",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (leave blank to list all)"
                    }
                }
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Route tool calls to handlers"""
    handlers = {
        "maw_status": handle_status,
        "maw_review": handle_review,
        "maw_launch": handle_launch,
        "maw_checkin": handle_checkin,
        "maw_integrate": handle_integrate,
        "maw_decide": handle_decide,
        "maw_learn": handle_learn,
        "maw_patterns": handle_patterns,
    }
    
    handler = handlers.get(name)
    if not handler:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    result = await handler(arguments)
    return [TextContent(type="text", text=result)]


# =============================================================================
# HANDLERS
# =============================================================================

async def handle_status(args: dict) -> str:
    """Show current workflow state"""
    project_path = args.get("project_path", ".")
    state = load_state(project_path)
    
    status = format_status(state)
    next_step = suggest_next_step(state)
    
    return f"{status}\n\n{next_step}"


async def handle_review(args: dict) -> str:
    """Phase 3: Analyze and generate agent prompts"""
    project_path = args.get("project_path", ".")
    focus = args.get("focus", "all")
    wave_name = args.get("wave_name", "")
    
    state = load_state(project_path)
    path = Path(project_path).resolve()
    
    # Create AGENT_PROMPTS directory
    prompts_dir = path / "AGENT_PROMPTS"
    prompts_dir.mkdir(exist_ok=True)
    
    # This is where the actual analysis would happen
    # For now, return instructions for the LLM to do the analysis
    
    analysis_prompt = f"""
## Phase 3: Codex Review

Analyze this codebase and identify 3-5 high-impact improvements.

**Focus:** {focus}
**Wave:** {wave_name or "Wave 1"}

### Analysis Areas
1. **Performance** - Slow queries, memory issues, N+1 problems
2. **Security** - Auth, validation, injection risks
3. **Code Quality** - Duplication, complexity, error handling
4. **Testing** - Coverage gaps, missing integration tests
5. **Documentation** - README, API docs, setup guides

### Output Required

For each improvement, create a file in `AGENT_PROMPTS/`:

```
AGENT_PROMPTS/
├── 1_Backend_Engineer.md
├── 2_Security_Hardening.md
├── 3_Testing_Infrastructure.md
├── COORDINATION.md
└── README.md
```

### Agent Prompt Template

Each agent file must include:

```markdown
# Agent N: [Role Name]

## Mission
[One sentence goal]

## Branch
`agent/N-[slug]`

## Files to Modify
- path/to/file1.py
- path/to/file2.py

## Tasks
1. [Specific task]
2. [Specific task]

## Definition of Done
- [ ] [Deliverable]
- [ ] Tests pass
- [ ] PR created

## Time Estimate
[X] hours
```

### Launch Sequence

Specify in COORDINATION.md:
- Which agent(s) run first
- Which can run in parallel
- Dependencies between agents

### After Creating Prompts

Update WORKFLOW_STATE.json:
- Set phase: 3
- Set review_complete: true
- Add agents array with id, role, slug, branch for each

Then tell the user: "Review AGENT_PROMPTS/ before running maw_launch"
"""
    
    # Update state
    state.phase = 3
    state.status = "reviewing"
    if wave_name:
        state.wave = WaveInfo(number=state.iteration + 1, name=wave_name)
    save_state(state, project_path)
    
    return analysis_prompt


async def handle_launch(args: dict) -> str:
    """Phase 4: Get agent launch prompts with sequencing"""
    project_path = args.get("project_path", ".")
    agent_id = args.get("agent_id")
    
    state = load_state(project_path)
    path = Path(project_path).resolve()
    prompts_dir = path / "AGENT_PROMPTS"
    
    if not state.review_complete:
        return """⚠️ Review not complete.

Run maw_review first to:
1. Analyze the codebase
2. Generate agent prompts in AGENT_PROMPTS/
3. Set review_complete in state

Then you can run maw_launch."""
    
    if not prompts_dir.exists():
        return f"⚠️ AGENT_PROMPTS/ not found at {prompts_dir}"
    
    # Read agent prompts
    prompt_files = sorted(prompts_dir.glob("[0-9]_*.md"))
    if not prompt_files:
        return "⚠️ No agent prompt files found (expected: 1_Role.md, 2_Role.md, etc.)"
    
    # Build launch output
    lines = ["## 🚀 Agent Launch Sequence\n"]
    
    # Read COORDINATION.md for sequence info
    coord_file = prompts_dir / "COORDINATION.md"
    if coord_file.exists():
        lines.append("### Launch Order")
        lines.append(coord_file.read_text())
        lines.append("")
    else:
        lines.append("### Launch Order")
        lines.append("1. Agent 1 - Run first (~20 min)")
        lines.append("2. Agents 2+ - Run in parallel after Agent 1 creates base\n")
    
    lines.append("---\n")
    lines.append("### Agent Prompts\n")
    lines.append("Copy each prompt to a separate Cursor/Claude Code session:\n")
    
    for pf in prompt_files:
        agent_num = int(pf.name.split("_")[0])
        
        if agent_id and agent_num != agent_id:
            continue
        
        content = pf.read_text()
        role = pf.stem.split("_", 1)[1].replace("_", " ")
        
        # Extract branch from content or generate
        branch_match = re.search(r'`(agent/\d+-[^`]+)`', content)
        branch = branch_match.group(1) if branch_match else f"agent/{agent_num}-{slugify(role)}"
        
        lines.append(f"#### Agent {agent_num}: {role}")
        lines.append(f"**Branch:** `{branch}`")
        lines.append("")
        lines.append("```")
        lines.append(f"You are Agent {agent_num}: {role}")
        lines.append(f"Branch: {branch}")
        lines.append(f"Read and implement: AGENT_PROMPTS/{pf.name}")
        lines.append("Create PR when done.")
        lines.append("START NOW")
        lines.append("```")
        lines.append("")
    
    # Update state
    state.phase = 4
    state.status = "launching"
    save_state(state, project_path)
    
    return "\n".join(lines)


async def handle_checkin(args: dict) -> str:
    """Phase 4: Evaluate progress and provide guidance"""
    project_path = args.get("project_path", ".")
    reports = args.get("reports", "")
    
    if not reports:
        return """## Agent Check-in

Paste progress reports from each agent using this format:

```
Agent 1:
✅ Done: [completed tasks]
🔄 Working on: [current task]
⚠️ Blocked by: [issues or "None"]
⏭️ Next: [planned next]
📎 PR: [link if created]

Agent 2:
...
```

Then run maw_checkin again with the reports."""
    
    # Return re-evaluation guidance
    return f"""## Progress Analysis

Based on the reports:

{reports}

### Re-evaluation Guide

| Status | Action |
|--------|--------|
| ✅ Ahead of schedule | Add stretch goal or help blocked agent |
| ⚠️ Blocked | Provide workaround or redirect to different task |
| 🔄 On track | Continue current path |
| ❌ Behind | Simplify scope or extend time |

### Updated Prompts

If any agent needs redirection, provide an updated prompt:

```
Agent N (UPDATED):
Previous: [what they were doing]
New Focus: [what to do instead]
Reason: [why the change]
Files: [updated file list]
Time: [remaining estimate]
```

### Next Check-in

Schedule another check-in in 30-60 minutes, or when agents report completion."""


async def handle_integrate(args: dict) -> str:
    """Phase 5: Integration guidance"""
    project_path = args.get("project_path", ".")
    state = load_state(project_path)
    
    # Build merge order guidance
    return """## Phase 5: Integration

### Pre-Merge Checklist
- [ ] All agents report complete
- [ ] All PRs created and passing CI
- [ ] No merge conflicts detected

### Recommended Merge Order

1. **Documentation/Tests** (lowest risk)
   - Docs-only PRs first
   - Test additions second
   
2. **Backend/Infrastructure**
   - Core changes before dependent changes
   - Database migrations before code using them
   
3. **Frontend/UI**
   - After backend APIs stable
   
4. **Integration/Cross-cutting**
   - Last, after components stable

### Merge Commands

```bash
# For each PR in order:
gh pr view <number>           # Review changes
gh pr checks <number>         # Verify CI passes
gh pr merge <number> --squash # Merge
git pull                      # Update local
pytest                        # Run tests
```

### Conflict Resolution

If conflicts detected:
1. Identify which files conflict
2. Merge the simpler PR first
3. Rebase the complex PR on updated main
4. Re-run tests after each merge

### After All Merges

Run maw_decide to determine: deploy, iterate, or add features."""


async def handle_decide(args: dict) -> str:
    """Phase 6: Deploy/iterate/add decision"""
    project_path = args.get("project_path", ".")
    state = load_state(project_path)
    
    return f"""## Phase 6: Decision Time

### Current State
- Project: {state.project}
- Iteration: {state.iteration}
- Agents completed: {len([a for a in state.agents if a.status == 'complete'])}

### Decision Framework

| Condition | Recommendation |
|-----------|----------------|
| All tests pass, no critical issues | ✅ **Deploy** |
| Minor issues found | ⚠️ **Fix then deploy** |
| Quality score < 7/10, major refactoring needed | 🔄 **Iterate** (run maw_review again) |
| Core solid, users request features | ➕ **Add features** (new iteration) |

### Questions to Answer

1. Are all tests passing?
2. Any critical security issues?
3. Performance acceptable?
4. Documentation up to date?
5. Ready for real users?

### If Deploying

```bash
# Staging first
git checkout main
git pull
# Deploy to staging
# Run smoke tests
# Monitor for 24h

# Then production
# Deploy to production
# Monitor closely
```

### If Iterating

Run `maw_review` with focus on remaining issues.
This starts a new iteration with fresh agent prompts.

### Update State

After deciding, update WORKFLOW_STATE.json:
- If deployed: status = "deployed"
- If iterating: iteration += 1, run maw_review"""


async def handle_learn(args: dict) -> str:
    """Capture learnings"""
    project_path = args.get("project_path", ".")
    learning = args.get("learning", "")
    promote = args.get("promote", False)
    
    path = Path(project_path).resolve()
    learnings_file = path / "PROJECT_LEARNINGS.md"
    
    if not learning:
        return """## Capture Learnings

What did you learn this session? Consider:

- Bugs that took >10 minutes to solve
- Patterns that worked well
- Tools with non-obvious behavior
- Mistakes to avoid next time

Run maw_learn again with your learning:

```
maw_learn learning="[Your learning here]" promote=false
```

Set promote=true to also add to central UNIVERSAL_PATTERNS.md"""
    
    # Append to project learnings
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"\n### {timestamp}\n{learning}\n"
    
    if learnings_file.exists():
        content = learnings_file.read_text()
        learnings_file.write_text(content + entry)
    else:
        learnings_file.write_text(f"# Project Learnings\n{entry}")
    
    result = f"✅ Added to PROJECT_LEARNINGS.md"
    
    if promote:
        patterns_file = CONTENT_DIR / "UNIVERSAL_PATTERNS.md"
        if patterns_file.exists():
            content = patterns_file.read_text()
            patterns_file.write_text(content + f"\n---\n\n### From {path.name}\n**Date:** {timestamp}\n\n{learning}\n")
            result += "\n✅ Also added to UNIVERSAL_PATTERNS.md"
    
    return result


async def handle_patterns(args: dict) -> str:
    """Search or browse patterns"""
    query = args.get("query", "").lower()
    
    patterns_file = CONTENT_DIR / "UNIVERSAL_PATTERNS.md"
    if not patterns_file.exists():
        return "⚠️ UNIVERSAL_PATTERNS.md not found"
    
    content = patterns_file.read_text()
    
    if not query:
        # Return table of contents
        lines = ["## Universal Patterns\n"]
        for line in content.split("\n"):
            if line.startswith("### "):
                lines.append(f"- {line[4:]}")
        lines.append("\n\nRun `maw_patterns query=\"keyword\"` to search.")
        return "\n".join(lines)
    
    # Search for matching sections
    sections = content.split("### ")
    matches = []
    
    for section in sections[1:]:  # Skip header
        if query in section.lower():
            # Get just the title and first few lines
            lines = section.split("\n")
            title = lines[0]
            preview = "\n".join(lines[1:10])
            matches.append(f"### {title}\n{preview}...")
    
    if not matches:
        return f"No patterns found matching '{query}'"
    
    return f"## Patterns matching '{query}'\n\n" + "\n\n---\n\n".join(matches)


# =============================================================================
# RESOURCES
# =============================================================================

@server.list_resources()
async def list_resources():
    """List available phase guides"""
    from mcp.types import Resource
    
    resources = []
    phases_dir = CONTENT_DIR / "phases"
    
    if phases_dir.exists():
        for f in sorted(phases_dir.glob("*.md")):
            resources.append(Resource(
                uri=AnyUrl(f"file://{f}"),
                name=f.stem,
                description=f"Phase guide: {f.stem}",
                mimeType="text/markdown"
            ))
    
    return resources


@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read a phase guide"""
    path = Path(str(uri).replace("file://", ""))
    if path.exists():
        return path.read_text()
    return f"Resource not found: {uri}"


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run the MCP server"""
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
