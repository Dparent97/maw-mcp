# MAW Quickstart Guide

Get multiple AI agents working on your code at the same time.

---

## What Does This Do?

Instead of Claude doing one thing at a time, MAW lets you have multiple Claudes working in parallel:

| Without MAW | With MAW |
|-------------|----------|
| Fix bug → wait → write tests → wait → update docs | Fix bug + write tests + update docs (all at once) |
| 3 hours | 1 hour |

Each agent works on its own copy of the code (a "branch"), then you combine them when done.

---

## The Workflow

```
You: "Review my code"
        ↓
   Claude analyzes, creates task list
        ↓
You: "Launch the agents"  
        ↓
   You copy prompts to separate Claude windows
   Each one works independently
        ↓
You: "Check in" (paste their reports)
        ↓
   Dashboard shows who's done
        ↓
You: "Integrate"
        ↓
   Merge order + test checklist
        ↓
You: "What's next?"
        ↓
   Deploy, or do another round
```

---

## Step 1: Setup (One Time)

Tell Claude Desktop where to find MAW. 

Open this file (create if it doesn't exist):
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

Paste this:
```json
{
  "mcpServers": {
    "maw": {
      "command": "python3",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/maw-mcp"
    }
  }
}
```

Change `/path/to/maw-mcp` to wherever you put this folder.

Restart Claude Desktop.

---

## Step 2: Review

Open a chat and say:

> "Review this codebase for improvements. Focus on security. Call it Wave 1."

Claude will:
1. Look at your code
2. Identify 3-5 things to fix
3. Create a folder called `AGENT_PROMPTS/` with one file per task

**Stop here and read the prompts.** Make sure they make sense before continuing.

---

## Step 3: Launch

Say:

> "Show me the launch sequence"

Claude gives you:
- Which agent to start first
- Which can run in parallel
- Copy-paste prompts for each

**Open separate Claude windows** (or Cursor sessions) and paste each prompt. Each agent works on its own branch.

---

## Step 4: Check In

When agents finish, they create PRs on GitHub. Just say:

> "Check on the agents"

Claude auto-fetches from GitHub and shows:
```
📊 Agent Status Dashboard (from GitHub)

| PRs Found | Files Changed | Conflicts |
|-----------|---------------|-----------|
| 4         | 23            | 0         |

### Agent PRs
| Agent | PR | Branch | +/- | Status |
|-------|----|---------|----|--------|
| 1 | #4 | agent/1-logging | +628/-3 | ✅ Open |
| 2 | #1 | agent/2-deployment | +198/-5 | ✅ Open |
| 3 | #2 | agent/3-offline | +312/-8 | ✅ Open |
| 4 | #3 | agent/4-testing | +1387/-0 | ✅ Open |

### ✅ No Conflicts Detected
```

No more copy-pasting reports!

---

## Step 5: Integrate

When all agents are done:

> "How do I integrate these?"

Claude fetches PR info and gives you:
```
## Integrate

### Pre-Merge Checklist
- [ ] All PRs passing CI
- [ ] No merge conflicts detected

### Recommended Merge Order

**1. Tests** (low risk)
   - Agent 4: Integration Testing → PR #3

**2. Backend/Infrastructure**  
   - Agent 1: Logging Infrastructure → PR #4
   - Agent 2: Deployment Ready → PR #1

**3. Frontend/UI**
   - Agent 3: Offline Error Recovery → PR #2

### Merge Commands

```bash
# Merge in this order:
gh pr merge 3 --squash && git pull && pytest
gh pr merge 4 --squash && git pull && pytest
gh pr merge 1 --squash && git pull && pytest
gh pr merge 2 --squash && git pull && pytest
```
```

Copy-paste the merge commands and you're done.

---

## Step 6: Decide

After integration:

> "What should I do next?"

Claude recommends:
- **Deploy** if everything works
- **Iterate** if more fixes needed
- **Add features** if the foundation is solid

---

## Commands Reference

| You Say | What Happens |
|---------|--------------|
| "Check workflow status" | Shows current phase and next step |
| "Review this codebase" | Analyzes code, creates agent tasks |
| "Show launch sequence" | Gives copy-paste prompts for agents |
| "Check on the agents" | Auto-fetches PRs from GitHub, shows dashboard |
| "How do I integrate?" | Merge order + actual PR commands |
| "What's next?" | Deploy/iterate/add features recommendation |
| "Save this learning..." | Captures notes for future reference |
| "Search patterns for X" | Finds relevant past learnings |

---

## Tips

**Start small.** Try it on a simple project first.

**Read the prompts.** The pause between review and launch exists so you can edit the tasks.

**One branch per agent.** Never let two agents work on the same branch.

**Check in regularly.** Don't wait until the end to see if agents are stuck.

---

## Files Created in Your Project

```
your-project/
├── WORKFLOW_STATE.json    ← Tracks progress
├── AGENT_PROMPTS/         ← Task files for each agent
│   ├── 1_Backend.md
│   ├── 2_Testing.md
│   ├── COORDINATION.md
│   └── README.md
└── PROJECT_LEARNINGS.md   ← Notes from this project
```

---

## Troubleshooting

**"maw tools not found"**  
Restart Claude Desktop after editing the config file.

**"Review not complete"**  
Run the review step first before trying to launch.

**"Couldn't fetch from GitHub"**  
Make sure `gh` CLI is installed and authenticated:
```bash
brew install gh
gh auth login
```

**Agent stuck**  
Check their PR on GitHub for errors. Provide clarification and have them continue.

**Merge conflicts**  
Follow the merge order from integrate step. The tool detects which files overlap.

---

## Example Session

```
You: Review this Flask app for improvements, call it "Security Wave"

Claude: [analyzes code, creates AGENT_PROMPTS/]
        Done! Review the prompts in AGENT_PROMPTS/ then ask for launch sequence.

You: Show me the launch sequence

Claude: Launch Order:
        1. Agent 1 (Backend Security) - run first
        2. Agents 2, 3, 4 - run in parallel after
        
        [copy-paste prompts for each]

You: [opens 4 Claude windows, pastes prompts, agents work, create PRs]

You: Check on the agents

Claude: 📊 Agent Status Dashboard (from GitHub)
        
        | PRs Found | Conflicts |
        |-----------|-----------|
        | 4         | 0         |
        
        ✅ All PRs open, no conflicts!

You: How do I integrate?

Claude: ### Merge Commands
        
        ```bash
        gh pr merge 3 --squash && git pull && pytest
        gh pr merge 4 --squash && git pull && pytest
        gh pr merge 1 --squash && git pull && pytest  
        gh pr merge 2 --squash && git pull && pytest
        ```

You: [runs merge commands]
     What's next?

Claude: All tests passing, no critical issues.
        Recommendation: ✅ Deploy
```

---

## Need Help?

Check the full README.md for detailed tool documentation.
