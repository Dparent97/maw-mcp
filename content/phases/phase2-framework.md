# Phase 2: Framework Build

Builds working skeleton code based on Phase 1 planning.

## Prerequisites

- Phase 1 must be complete (project structure exists)
- WORKFLOW_STATE.json shows phase=1, status=complete

## What This Phase Does

1. Verifies Phase 1 completion
2. Creates core application files
3. Sets up dependencies
4. Creates initial commit
5. Optionally pushes to GitHub

## Workflow

```python
from workflow.core.workflow_state import WorkflowState

# Load and verify state
ws = WorkflowState("path/to/project")
state = ws.load()

if state['phase'] < 1:
    print("❌ Phase 1 not complete. Run phase1-planning first.")
    exit()

tech_stack = state['tech_stack']

# Create core files based on tech stack
# Example for Flask:
# - app/__init__.py
# - app/routes.py
# - app/models.py
# - run.py
# - requirements.txt

# Example for React:
# - src/App.jsx
# - src/index.jsx
# - package.json
# - vite.config.js

# Create working Hello World version

# Update state
ws.update_phase(2, "phase_2_complete")
ws.complete_phase(2)

print("\n✅ Phase 2 Complete!")
print("🏗️  Skeleton code created")
print("📦 Dependencies configured")
print("\n➡️  Next: Run phase3-codex-review to identify improvements")
```

## Core Files to Create

**Python/Flask:**
- Application factory pattern
- Basic routes
- Requirements file
- Development server

**React/Node:**
- Component structure
- Entry point
- Package.json with scripts
- Development server config

**Swift/iOS:**
- App structure
- Main views
- Project configuration

## Key Principles

1. **Keep it simple** - Just enough to run
2. **Follow conventions** - Use standard patterns
3. **Make it runnable** - User should be able to start app
4. **Document setup** - Update README with how to run

## Output

- Working skeleton application
- Can be run locally
- Dependencies listed
- Initial commit made
- State updated to Phase 2 complete
