# Phase 1: Project Planning

Plans the complete project structure, tech stack, and initial architecture for new projects.

## When to Use

- Starting brand new projects from scratch
- User requests "plan my project" or "Phase 1"
- **Skip this phase** for existing projects - go directly to phase3-codex-review

## What This Phase Does

1. Discusses project goals with user
2. Recommends tech stack based on requirements
3. Creates directory structure
4. Sets up initial files (.gitignore, README, etc.)
5. Initializes git repository
6. Creates WORKFLOW_STATE.json

## Workflow

```python
from workflow.core.workflow_state import WorkflowState

# Ask user about project
print("What type of project are you building?")
print("What's the main goal?")
print("Any tech preferences?")

# Based on answers, recommend tech stack
# Examples:
# - Web app → Flask/Python or React/Node
# - iOS app → Swift/SwiftUI
# - CLI tool → Python/Click
# - API → FastAPI/Python

# Create directory structure
# project/
# ├── src/
# ├── tests/
# ├── docs/
# ├── .gitignore
# ├── README.md
# └── requirements.txt (or package.json, etc.)

# Initialize state
ws = WorkflowState("path/to/project")
state = ws._empty_state()
state['tech_stack'] = "chosen_stack"
state['phase'] = 1
state['status'] = "phase_1_complete"
ws.save(state)

print("\n✅ Phase 1 Complete!")
print("📁 Project structure created")
print("🔧 Git initialized")
print("\n➡️  Next: Run phase2-framework to build initial code")
```

## Key Questions to Ask

1. **Purpose**: "What will this project do?"
2. **Users**: "Who will use it?"
3. **Platform**: "Web, mobile, desktop, CLI?"
4. **Data**: "What kind of data will it handle?"
5. **Deployment**: "Where will it run?"

## Tech Stack Recommendations

**Web Apps:**
- Frontend: React, Vue, or vanilla HTML/CSS/JS
- Backend: Flask, FastAPI, or Node/Express
- Database: PostgreSQL, SQLite

**Mobile:**
- iOS: Swift/SwiftUI
- Android: Kotlin
- Cross-platform: React Native

**CLI Tools:**
- Python with Click or Typer
- Node with Commander

## Output

- Scaffolded project directory
- Initial configuration files
- Git repository initialized
- WORKFLOW_STATE.json created
- Clear next step (Phase 2)
