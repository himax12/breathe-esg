# Templates for Deep Codebase Explanation

This file contains reusable templates for explaining code concepts.

---

## Template 1: Explaining a Module

```markdown
## [Module Name]

### What It Is
A "department" that handles [specific responsibility].

### Real-World Analogy
It's like a [real department] because [reason].

### The Problem It Solves
Before this existed, developers had to [old way], which caused [problem].

### How It Works
```
┌─────────────────────────────────────────────────────┐
│  Module: [Name]                                      │
│                                                     │
│  Input: [what comes in]                            │
│       │                                             │
│       ▼                                             │
│  ┌─────────────────┐                                │
│  │ Validation      │ ← "The security checkpoint"   │
│  └─────────────────┘                                │
│       │                                             │
│       ▼                                             │
│  ┌─────────────────┐                                │
│  │ Processing      │ ← "Where work happens"        │
│  └─────────────────┘                                │
│       │                                             │
│       ▼                                             │
│  Output: [what comes out]                          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Directory Structure
```
module/
├── subpackage1/      ← "handles X"
│   ├── ClassA.java   ← "does Y"
│   └── ClassB.java   ← "does Z"
└── subpackage2/
    └── ...
```

### Key Classes

| Class | Responsibility | Key Method |
|-------|---------------|------------|
| ClassName | What it does | methodName() |

### How It Works (with code)

```java
// Step 1: [what happens] - like [analogy]
// Step 2: [what happens] - like [analogy]
// Step 3: [what happens] - like [analogy]
```

### Interactions with Other Modules

```
This module → [relationship] → That module
```

### Edge Cases
- If [condition], it [does this]
- If [condition], it [does this]
```

---

## Template 2: Explaining a Function/Method

```markdown
## Function: [Name]

### Signature
```java
returnType methodName(Type1 param1, Type2 param2)
```

### What It Does
A "worker" that takes [input] and produces [output].

### The Purpose
"Given [input], we need [result] so that [benefit]."

### Step-by-Step Breakdown

```
1. First, it [does this] — like [analogy]
2. Then, it [does this] — like [analogy]
3. Finally, it [returns this] — which is [explanation]
```

### Code Walkthrough

```java
// "Take the ingredient"
InputType input = getInput();

// "Prepare it - like chopping vegetables"
processed = transform(input);

// "Check it's good quality"
validate(processed);

// "Cook it into the final dish"
return cook(processed);
```

### Edge Cases
- If input is [null/empty/error], it [handles this way]
- If [race condition], it [prevents this]
```

---

## Template 3: Explaining an Architecture Pattern

```markdown
## Pattern: [Name]

### The Core Idea
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   PROBLEM: [What issue does this solve?]              │
│                                                         │
│   BEFORE:                                              │
│   A does B does C does D — if D breaks, everything     │
│   breaks, and changes to A might break D               │
│                                                         │
│   AFTER:                                              │
│   A → B → C → D                                        │
│   But with [special mechanism] so changes don't ripple │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### The Metaphor
"This is like [metaphor] because [how they relate]."

### Implementation Skeleton
```java
// The pattern in action:

class [Concept] {
  private dependency: Dependency;

  constructor(dep: Dependency) {
    this.dependency = dep; // "Give me the tools I need"
  }

  doWork() {
    // "Here's where [pattern] magic happens"
    return this.dependency.provide();
  }
}
```

### When to Use This Pattern
- Use when: [condition]
- Don't use when: [condition]
```

---

## Template 4: Explaining a Data Structure

```markdown
## Data Structure: [Name]

### Simple Definition
"A [container type] that stores [what] and provides [what operations]."

### Real-World Analogy
"Like a [real-world container] because [how they work similarly]."

### Visual Representation

```
┌────────────────────────────────────────┐
│                                        │
│   [visual diagram of the structure]    │
│                                        │
│   • Item 1 → points to Item 2           │
│   • Item 2 → points to Item 3           │
│   • Item 3 → null (end)                │
│                                        │
└────────────────────────────────────────┘
```

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert   | O(?) | O(?)  |
| Delete   | O(?) | O(?)  |
| Search   | O(?) | O(?)  |
| Get      | O(?) | O(?)  |

### Code Example

```java
// Creating: like [analogy]
DataStructure ds = new DataStructure();

// Adding: like [analogy]
ds.add(item);

// Finding: like [analogy]
ds.find(predicate);
```
```

---

## Template 5: Request-Response Flow

```markdown
## [Request Type] Flow

When you [action], here's what happens:

```
┌──────────────────────────────────────────────────────────────────┐
│  STEP 1: [Description]                                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ [Code snippet or description of what happens]              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  STEP 2: [Description]                                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ [Code snippet or description of what happens]              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  STEP N: [Description]                                           │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ [Code snippet or description of what happens]              │  │
│  └────────────────────────────────────────────────────────────┘  │
│                           │                                      │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │ Response: [what gets returned]                             │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Key Files Involved

| File | Role |
|------|------|
| path/to/file1.java | [what it does] |
| path/to/file2.java | [what it does] |
```

---

## Template 6: API Endpoint

```markdown
## API Endpoint: [Method] [Path]

### What It Does
[Brief description of what this endpoint accomplishes].

### Real-World Analogy
"It's like a [analogy] at a [place]."

### Request

```http
[METHOD] [PATH]
Content-Type: application/json

{
    "field1": "value1",
    "field2": "value2"
}
```

### Response

```json
{
    "status": "success",
    "data": {
        // response fields
    }
}
```

### How It Works

1. [First step] - like [analogy]
2. [Second step] - like [analogy]
3. [Third step] - like [analogy]

### Error Cases

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | [bad input] | `{"error": "..."}` |
| 404 | [not found] | `{"error": "..."}` |
| 500 | [server error] | `{"error": "..."}` |

### Code Location
- API Handler: `path/to/Handler.java`
- Service: `path/to/Service.java`
- Repository: `path/to/Repository.java`
```

---

## Template 7: First Contribution Guide

```markdown
## Contributing to [Project Name]

### Your First Contribution

Welcome! Here's how to make your first contribution.

### 1. Setup Development Environment

```bash
# Install prerequisites
- [tool1] version X+
- [tool2] version Y+

# Clone the repository
git clone [repo-url]
cd [project-name]

# Build
mvn clean install -DskipTests

# Run tests
mvn test
```

### 2. Find a Good First Issue

Look for issues labeled:
- `good first issue`
- `beginner`
- `documentation`

### 3. Understand the Code

1. Find the relevant module: [description]
2. Read key files:
   - `path/to/file1.java` - [what it does]
   - `path/to/file2.java` - [what it does]
3. Trace the flow: [description]

### 4. Make Your Change

```bash
# Create a branch
git checkout -b fix/my-first-fix

# Make your changes...
# Don't forget tests!

# Run tests
mvn test -pl module -am

# Commit
git commit -m "Fix: [description]"
```

### 5. Submit Your PR

1. Push: `git push origin fix/my-first-fix`
2. Create PR on GitHub
3. Describe what you changed and why
4. Reference any related issues

### Code Style

- Follow existing patterns in the codebase
- Run linting: `[lint command]`
- Format code: `[format command]`
```

---

## Template 8: Troubleshooting Guide

```markdown
## Troubleshooting [Component]

### Common Issues

#### Issue: [Problem Description]

**Symptoms:**
- [What user sees]

**Cause:**
[Why this happens]

**Solution:**
```bash
# Steps to fix
command1
command2
```

---

#### Issue: [Problem Description]

**Symptoms:**
- [What user sees]

**Cause:**
[Why this happens]

**Solution:**
```bash
# Steps to fix
command1
command2
```

### Debugging Tips

1. Enable verbose logging:
```bash
# Set log level to DEBUG
export LOG_LEVEL=DEBUG
```

2. Check configuration:
```bash
# Validate config
[command] --validate-config
```

3. Common commands:
```bash
# Check status
[command] status

# View logs
[command] logs --tail 100

# Restart
[command] restart
```
```
