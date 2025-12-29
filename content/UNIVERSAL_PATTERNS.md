# Universal Patterns

**Purpose:** Cross-project rules and patterns that apply to ALL work in the multi-agent workflow.
**Scope:** Language-agnostic, role-agnostic best practices.

---

## Core Principles

### 1. Explicit Over Implicit
**Rule:** Always make assumptions, dependencies, and contracts explicit.

**Why:** Prevents misunderstandings between agents and reduces integration issues.

**Examples:**
- Document function contracts in docstrings
- List PR dependencies explicitly
- State assumptions in design documents
- Declare interfaces before implementation

**Anti-Pattern:**
```python
# Bad: Implicit assumption
def process(data):
    return data[0]  # Assumes data is non-empty list
```

**Correct Pattern:**
```python
# Good: Explicit validation
def process(data):
    """Process data. Requires non-empty list."""
    if not data:
        raise ValueError("data must be non-empty list")
    return data[0]
```

---

### 2. Fail Fast, Fail Clearly
**Rule:** Detect errors early and provide actionable error messages.

**Why:** Reduces debugging time and prevents cascading failures.

**Examples:**
- Validate inputs at function entry
- Use type hints/checks
- Provide context in error messages
- Fail during initialization, not at runtime

**Anti-Pattern:**
```javascript
// Bad: Silent failure
function loadConfig(path) {
    try {
        return JSON.parse(fs.readFileSync(path));
    } catch (e) {
        return {};  // Silently returns empty config
    }
}
```

**Correct Pattern:**
```javascript
// Good: Clear failure
function loadConfig(path) {
    if (!fs.existsSync(path)) {
        throw new Error(`Config file not found: ${path}`);
    }
    try {
        return JSON.parse(fs.readFileSync(path));
    } catch (e) {
        throw new Error(`Invalid JSON in config ${path}: ${e.message}`);
    }
}
```

---

### 3. Single Source of Truth
**Rule:** Each piece of information should have exactly one authoritative source.

**Why:** Prevents inconsistencies and reduces maintenance burden.

**Examples:**
- Configuration in one file, not scattered
- State managed in workflow_state.py, not duplicated
- Documentation in code, not separate docs
- Constants defined once, imported everywhere

**Violations to Watch:**
- Hardcoded values duplicated across files
- Configuration in multiple places
- Documentation that contradicts code
- Derived values stored instead of calculated

---

### 4. Idempotency
**Rule:** Operations should produce the same result when run multiple times.

**Why:** Enables safe retries and simplifies debugging.

**Examples:**
- Scripts that can be re-run safely
- Database migrations that check before applying
- File operations that don't fail if already done
- API calls that handle "already exists" gracefully

**Anti-Pattern:**
```python
# Bad: Fails on re-run
def initialize():
    os.mkdir("output")  # Fails if directory exists
```

**Correct Pattern:**
```python
# Good: Safe to re-run
def initialize():
    os.makedirs("output", exist_ok=True)
```

---

### 5. Separation of Concerns
**Rule:** Each module/function should have one clear responsibility.

**Why:** Improves testability, reusability, and maintainability.

**Examples:**
- Separate data fetching from processing
- UI logic separate from business logic
- Configuration separate from implementation
- Testing separate from production code

**Violations to Watch:**
- Functions that do multiple unrelated things
- Modules with mixed responsibilities
- UI components with business logic
- Test code in production modules

---

## Workflow-Specific Patterns

### 6. Phase Handoff Protocol
**Rule:** Each phase must produce complete, documented outputs before next phase starts.

**Why:** Prevents rework and ensures quality gates are met.

**Checklist:**
- [ ] All deliverables completed
- [ ] Documentation updated
- [ ] State transitioned in workflow_state.py
- [ ] Learnings captured
- [ ] Next phase notified with context

---

### 7. Stub Before Implement
**Rule:** When parallel work is needed, create stubs first.

**Why:** Unblocks dependent agents without forcing sequential work.

**Process:**
1. Identify interfaces needed by other agents
2. Create stub using template
3. Document expected behavior
4. Share stub with dependent agents
5. Implement later without breaking contracts

---

### 8. Review Before Merge
**Rule:** All code must pass Phase 3 review before integration.

**Why:** Catches issues early when they're cheap to fix.

**Non-Negotiables:**
- No direct commits to main
- All changes via PR
- PR template fully filled out
- Review checklist completed

---

### 9. Test Before Push
**Rule:** All tests must pass locally before creating PR.

**Why:** Prevents broken builds and wasted CI resources.

**Minimum Requirements:**
- Unit tests pass
- Linting passes
- Type checks pass (if applicable)
- Manual testing completed

---

### 10. Learn and Document
**Rule:** After every significant task, update learnings.

**Why:** Builds institutional knowledge and prevents repeated mistakes.

**When to Document:**
- Bug fixed that was hard to diagnose
- Pattern discovered that worked well
- Mistake made that should be avoided
- Tool/technique that proved useful

**Where to Document:**
- PR template "Learnings" section
- Appropriate file in AGENT_LEARNINGS/
- MASTER_LEARNINGS.md for critical items
- This file for universal patterns

---

## Code Quality Patterns

### 11. Defensive Programming
**Rule:** Assume inputs are invalid until proven otherwise.

**Practices:**
- Validate all inputs
- Handle all error cases
- Use type hints/checks
- Add assertions for invariants

---

### 12. DRY (Don't Repeat Yourself)
**Rule:** Avoid duplicating logic or data.

**When to Apply:**
- Logic duplicated more than twice
- Data structures copied across files
- Configuration repeated in multiple places

**When NOT to Apply:**
- Premature abstraction
- Unrelated code that happens to look similar
- Test code (clarity > DRYness)

---

### 13. YAGNI (You Aren't Gonna Need It)
**Rule:** Don't add functionality until it's actually needed.

**Practices:**
- Build what's required now
- Avoid "future-proofing"
- Refactor when needs change
- Keep it simple

---

### 14. Boy Scout Rule
**Rule:** Leave code better than you found it.

**Practices:**
- Fix nearby issues while working
- Improve names if confusing
- Add missing tests
- Update outdated comments
- Don't create separate "cleanup" tasks

---

### 15. Model Paper Forms with Related Tables
**Date Added:** 2025-12-19
**Project:** oil_record_book_tool

**Rule:** When digitizing paper forms with repeating sections, create separate database tables for each repeating group rather than cramming everything into one model.

**Why:** Paper forms often have sections with variable rows (like "12 fuel tanks" or "line items on an invoice"). Modeling these as separate related tables is cleaner, more flexible, and matches the actual data structure.

**Anti-Pattern:**
```python
# Bad: All 12 tanks as individual columns
class HitchRecord(db.Model):
    tank_7p_feet: int
    tank_7p_inches: int
    tank_7p_gallons: float
    tank_7s_feet: int
    tank_7s_inches: int
    tank_7s_gallons: float
    tank_9p_feet: int
    # ... 30+ more columns for remaining tanks
```

**Correct Pattern:**
```python
# Good: Separate table for repeating section
class FuelTankSounding(db.Model):
    hitch_id: int = db.Column(db.ForeignKey("hitch_records.id"))
    tank_number: str  # "7", "9", "11", etc.
    side: str  # "port" or "stbd"
    sounding_feet: int
    sounding_inches: int
    gallons: float

class HitchRecord(db.Model):
    # Header fields only
    date: datetime
    vessel: str
    # Relationship to tanks
    fuel_tanks = db.relationship("FuelTankSounding", backref="hitch")
```

**Benefits:**
- Easier to add/remove tanks without schema changes
- Cleaner queries and serialization
- More obvious data structure
- Form validation can iterate over tanks uniformly

---

### 16. Hub-and-Spoke Agent Architecture
**Date Added:** 2025-12-20
**Project:** crew-shopping-list, multi-agent-workflow

**Rule:** Strategic planning stays in one hub session (Opus), tactical execution happens in parallel spoke agents (Sonnet/workers). Agents don't need framework context - just their specific prompt.

**Why:** Agents that know too much waste tokens and get confused. Clear separation prevents scope creep and token bloat.

**Architecture:**
```
Hub (Opus/claude.ai):
- Phase 3 codex review
- Generate agent prompts
- Capture learnings
- Cross-session synthesis

Coordinator (Cursor agent):
- Phase 4 launch/monitor
- Merge PRs, test, debug
- Reports back to hub

Workers (Cursor agents):
- Execute ONE specific prompt
- Create PR
- Don't need framework knowledge
```

**Anti-Pattern:**
```
# Bad: Giving agents full context
You are Agent 3. Here is the entire framework, all phase guides,
all learnings, the full project history...
```

**Correct Pattern:**
```
# Good: Minimal context
You are Agent 3: Stock Status UI
Branch: feat/stock-status-ui
Read AGENT_PROMPTS/3_Stock_Status_UI.md and implement.
Create PR when done.
```

---

### 17. Use Existing Tooling (RTFM)
**Date Added:** 2025-12-20
**Project:** multi-agent-workflow

**Rule:** Before building new tooling, check if it already exists. `bin/init-project` existed for months before being rediscovered.

**Checklist before building:**
- [ ] Search repo for similar scripts
- [ ] Check `bin/` directory
- [ ] Read README and docs
- [ ] Ask "has this been solved?"

---

### 18. User Research > Feature Brainstorming
**Date Added:** 2025-12-20
**Project:** crew-shopping-list

**Rule:** Deep user context unlocks better product thinking than feature lists. "Juan shops from a frozen 2019 baseline" is more valuable than "add offline support."

**What to capture:**
- Who is the actual user? (Juan the cook, not "users")
- What's their real constraint? (Burned out, not tech savvy)
- What's competing with your app? (Yelling across the mess)
- What does failure look like? (Budget blown by week 2)

---

## Anti-Patterns to Avoid

### 1. Optimistic Assumptions
❌ Assuming file exists
❌ Assuming network is available
❌ Assuming data is valid
❌ Assuming user input is safe

✅ Always validate and handle failures

---

### 2. Silent Failures
❌ Catching exceptions without logging
❌ Returning empty/null on error
❌ Ignoring return codes
❌ Skipping validation

✅ Fail loudly with context

---

### 3. Magic Numbers/Strings
❌ Hardcoded values scattered in code
❌ Unclear constants without explanation
❌ Duplicate literal values
❌ Configuration embedded in logic

✅ Use named constants with clear meaning

---

### 4. God Objects/Functions
❌ Classes that do everything
❌ Functions with 100+ lines
❌ Modules with unrelated functionality
❌ Files with 1000+ lines

✅ Break into focused, single-purpose units

---

### 5. Premature Optimization
❌ Optimizing before measuring
❌ Complex code for hypothetical performance
❌ Trading clarity for speed without proof
❌ Over-engineering for scale not needed

✅ Make it work, make it right, then make it fast

---

### 6. Type Mismatch in JS/Python Boundary
**Date Added:** 2025-12-19
**Project:** oil_record_book_tool

❌ Using `parseInt()` in JS when backend expects Float
❌ Assuming JSON number types match DB column types
❌ Not validating types on API boundary

✅ Match JS parsing functions to backend types:
```javascript
// If backend is db.Float, use parseFloat
const gallons = parseFloat(document.getElementById('gallons').value);

// If backend is db.Integer, use parseInt
const feet = parseInt(document.getElementById('feet').value);
```

---

## Decision-Making Frameworks

### When to Refactor
**Refactor if:**
- Code is duplicated 3+ times
- Function is hard to understand
- Tests are difficult to write
- Adding features is painful

**Don't refactor if:**
- Current code works and is clear
- Change is purely aesthetic
- No tests exist to verify behavior
- Under time pressure (defer to next iteration)

---

### When to Add Abstraction
**Add abstraction if:**
- Pattern repeats 3+ times
- Multiple implementations of same concept
- Need to swap implementations
- Clear interface boundary exists

**Don't add abstraction if:**
- Only 1-2 uses
- Unclear how to generalize
- Would make code harder to understand
- YAGNI applies

---

### When to Write Tests
**Always test:**
- Public APIs
- Complex logic
- Error handling
- Security-critical code

**Optional testing:**
- Trivial getters/setters
- Framework boilerplate
- Generated code
- Prototype/experimental code

---

## Communication Patterns

### For PR Descriptions
- Start with "Why" before "What"
- Include context for reviewers
- List risks and mitigations
- Document learnings

### For Code Comments
- Explain "Why", not "What"
- Document non-obvious decisions
- Link to tickets/issues
- Keep comments up-to-date

### For Commit Messages
- Start with verb (Add, Fix, Update, Remove)
- Be specific about what changed
- Reference issues when applicable
- Keep under 72 characters for title

---

## Continuous Improvement

### Review This Document
- **Monthly:** Review and update patterns
- **After Major Issues:** Add new patterns learned
- **When Onboarding:** Use as training material
- **Before Starting:** Reference relevant sections

### Propose New Patterns
1. Document the pattern clearly
2. Provide examples and anti-patterns
3. Explain the "Why"
4. Submit as improvement proposal
5. Add to this file after approval

---

*These patterns are living rules. Challenge them if they don't serve the project, and update them when better patterns emerge.*
