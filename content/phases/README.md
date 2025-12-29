# Multi-Agent Workflow Phases

This directory contains detailed instructions for each workflow phase.

## Phase Overview

| Phase | Name | When to Use |
|-------|------|-------------|
| **1** | [Planning](phase1-planning.md) | New projects - structure and tech stack |
| **2** | [Framework](phase2-framework.md) | New projects - skeleton code |
| **3** | [Codex Review](phase3-codex-review.md) | **Start here for existing projects** - analyze code, generate agent prompts |
| **4** | [Agent Launcher](phase4-agent-launcher.md) | Launch parallel agents, track progress |
| **5** | [Integration](phase5-integration.md) | Merge all agent PRs |
| **5.5** | [Quality Audit](phase5-quality-audit.md) | Post-merge review (optional) |
| **6** | [Iteration](phase6-iteration.md) | Decide: deploy, iterate, or add features |

## Quick Start

### For Existing Projects
```
Phase 3 → Phase 4 → Phase 5 → Phase 6
```

### For New Projects
```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6
```

## Typical Workflow

1. **Phase 3**: Analyze codebase, identify 3-5 improvements, generate agent prompts
2. **Phase 4**: Launch 3-4 Claude Code agents in parallel, monitor progress
3. **Phase 5**: Review and merge all PRs
4. **Phase 6**: Decide next step (deploy or iterate)

## Time Estimates

| Phase | Quick | Comprehensive |
|-------|-------|---------------|
| Phase 3 | 30 min | 1 hour |
| Phase 4 | 2-4 hours | 4-6 hours |
| Phase 5 | 15-20 min | 45-60 min |
| Phase 5.5 | 30-40 min | 2-3 hours |
| Phase 6 | 10 min | 30 min |

**Total iteration**: 3-6 hours depending on project complexity

## Usage in Claude Code

Reference these files directly:
```
Read workflow/phases/phase3-codex-review.md and follow the instructions
```

Or use workflow state:
```
python workflow/core/workflow_state.py . next-step
```
