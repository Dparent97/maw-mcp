# Agent Coordination

## Wave [N]: [Wave Name]

**Started:** [Date]
**Target:** [Date]

## Launch Sequence

### Phase 1: Foundation (run first)
| Agent | Role | Branch | Est. Time |
|-------|------|--------|-----------|
| 1 | [Role] | `agent/1-slug` | 2h |

**Wait for Agent 1 to create base PR before launching Phase 2**

### Phase 2: Parallel Work
| Agent | Role | Branch | Est. Time |
|-------|------|--------|-----------|
| 2 | [Role] | `agent/2-slug` | 2h |
| 3 | [Role] | `agent/3-slug` | 2h |
| 4 | [Role] | `agent/4-slug` | 1.5h |

## Dependencies

```
Agent 1 ──► Agent 2
        └─► Agent 3
        └─► Agent 4
```

## Integration Points

| From | To | Interface |
|------|----|-----------|
| Agent 1 | Agent 2 | [API/file/contract] |
| Agent 1 | Agent 3 | [API/file/contract] |

## Merge Order

1. Agent 1 PR (foundation)
2. Agent 4 PR (docs/tests - low risk)
3. Agent 2 PR
4. Agent 3 PR

## Communication

If blocked or need clarification:
1. Check if another agent's work answers your question
2. Document blocker in your PR description
3. Continue with next task if possible
4. Flag for coordinator attention

## Success Criteria

- [ ] All PRs pass CI
- [ ] No merge conflicts
- [ ] Integration tests pass
- [ ] Manual verification complete
