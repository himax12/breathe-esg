# Skill: Deep Codebase Explanation

## Purpose

Transform complex codebase explanations into intuitive, ground-up understanding using layered concepts, real-world analogies, and actual code references. This skill builds understanding from foundation to implementation.

## Philosophy

**Understanding = "Why" → "How" → "What"**

Real understanding comes from:
1. **Why** - What problem does this solve? Why does it exist?
2. **How** - How does it work internally? (with analogies)
3. **What** - What does the code actually do? (with code references)

We build understanding **bottom-up**: fundamental concepts → intermediate ideas → full implementation → your first contribution

---

## The Analogy Framework

### The House Metaphor

```
Codebase = A House You're Moving Into

├── Blueprints (Architecture)     → How rooms connect, where pipes go
├── Rooms (Modules/Packages)      → Functional areas
├── Walls (Interfaces/APIs)       → What separates things
├── Doors (Function calls)         → How you move between rooms
├── Furniture (Classes/Functions)  → What fills each space
└── Foundation (Data models)      → What everything rests on
```

### The Restaurant Metaphor

```
Codebase = A Restaurant

├── Kitchen (Core Business Logic)      → Where work actually happens
├── Waiter (API Layer)                 → Receives orders, delivers food
├── Menu (Interface/Contracts)        → What you can order
├── Recipes (Schemas/Types)            → How dishes are structured
├── Tables (Data structures)          → Where orders are placed
└── Delivery (Response handling)      → How results get back to you
```

### The City Metaphor

```
Codebase = A City

├── Zoning (Module boundaries)
├── Roads (Internal APIs)
├── Public Transit (External APIs)
├── City Planning (Architecture patterns)
├── Utilities (Shared services)
└── Infrastructure (Core libraries)
```

---

## Layered Understanding Stack

Build understanding in layers, never jumping straight to code:

```
Layer 1: Mental Model (The "What is this?" layer)
    ↓ "This is a graph database - like a smart contact list"

Layer 2: Problem It Solves (The "Why does this exist?" layer)
    ↓ "Before this, finding friends-of-friends required 5 table JOINs"

Layer 3: Component Interactions (The "How does it work?" layer)
    ↓ "Vertices are like spreadsheet rows, edges are like hyperlinks"

Layer 4: Implementation Details (The "How is it built?" layer)
    → Now we can look at actual code and understand WHERE things happen
```

---

## Deep Dive Structure

For every concept, follow this structure:

```markdown
## ANALOGY FIRST

"Imagine [real-world thing]..."

## THE PROBLEM IT SOLVES

"Before this existed, developers had to [old way], which caused [problem]."

## THE CORE MECHANISM

"It works like [real thing] because [reason]."

## CODE WALKTHROUGH

```java
// Actual code with inline comments
// Think of it like: [analogy for this line]
```

## DATA FLOW DIAGRAM

```
Input → Process → Output
```

## KEY FILES TO REFERENCE

| File | Purpose | Lines |
|------|---------|-------|
| path/to/file.java | What it does | ~N |
```

---

## Explanation Templates

### Template 1: Explaining a Module/Package

```markdown
## [Module Name]

### What It Is
A "department" that handles [specific responsibility].

### Real-World Analogy
It's like a [real department] because [reason].

### The Problem It Solves
Before this existed, developers had to [old way], which caused [problem].

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

### Template 2: Explaining a Function/Method

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

### Template 3: Explaining an Architecture Pattern

```markdown
## Pattern: [Name]

### The Core Problem

```
BEFORE: [how things were done]
    A → B → C → D
    If D breaks, everything breaks.

AFTER: [how it works now]
    With [pattern name], changes don't ripple because [reason].
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

### Template 4: Explaining a Data Structure

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

## First Principles Breakdown

For any concept, always start here:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WHY DOES THIS EXIST?                                       │
│  ─────────────────────                                      │
│  What human problem motivated creating this?                │
│  Before this: developers had to [workaround]               │
│  That caused: [pain point]                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IS IT AT ITS CORE?                                    │
│  ───────────────────────                                     │
│  Strip away all implementation details                      │
│  This is fundamentally a [simple concept]:                  │
│  "A mechanism for [doing X] in [context Y]"                │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  HOW DOES IT WORK?                                          │
│  ────────────────────                                       │
│  Step 1: [What happens first]                               │
│  Step 2: [What happens second]                               │
│  Step 3: [What happens third]                               │
│  ...                                                        │
│                                                             │
│  Think of it like: [physical analogy]                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT ARE THE PIECES?                                       │
│  ──────────────────────                                     │
│  Part A: Does [X] — like a [real thing]                   │
│  Part B: Does [Y] — like a [real thing]                   │
│  Part C: Does [Z] — like a [real thing]                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Teaching Sequence

When explaining a complex project, use this sequence:

### 1. The One-Line Summary
Start with the absolute simplest description.

### 2. The Problem It Solves
Why would someone use this? What's the pain point it solves?

### 3. The Core Abstraction
What is the fundamental mental model? (Graph, REST API, Event bus, etc.)

### 4. The Architecture Overview
Show the high-level components and how they interact.

### 5. Deep Dives (User Chooses)
- A: Core Data Structures (What it stores)
- B: Query/Request Flow (How requests process)
- C: Distributed/Scale (How it scales)
- D: Your First Change (How to contribute)

---

## Interactive Checkpoints

After each major section, verify understanding:

```
✓ "Did that make sense? (yes/no/partially)"
✓ "Want me to go deeper on this part?"
✓ "Shall I show you the actual code now?"
✓ "Ready to move to the next section?"
```

### Socratic Questions

After showing code, ask:
- "What does THIS line do? [let them guess]"
- "Why do you think we check THIS condition first?"
- "If this function was a person, what would their job be?"

### Principle Extraction

Help them distill what they've learned:
```
┌────────────────────────────────────────────────────────────┐
│  THE ONE THING THIS TEACHES US:                           │
│  "..."                                                    │
│                                                            │
│  ANALOGY FOR REAL LIFE:                                   │
│  "Next time you [action], that's similar to..."           │
└────────────────────────────────────────────────────────────┘
```

---

## For Contributing: Path to First Contribution

When the user wants to contribute:

```
1. DEV ENVIRONMENT SETUP
   - Prerequisites check (Java, Maven, etc.)
   - Build commands
   - Test commands

2. FIND A BEGINNER ISSUE
   - Documentation fixes
   - Test coverage additions
   - Small bug fixes

3. UNDERSTAND THE CODE
   - Find the relevant module
   - Read the key classes
   - Trace the data flow

4. MAKE THE CHANGE
   - Follow coding conventions
   - Add/update tests
   - Run tests locally

5. SUBMIT
   - Create PR with clear description
   - Reference any issues
```

---

## Diagram Conventions

### System Diagram

```
                    ┌─────────────────────────────────────┐
                    │         SYSTEM OVERVIEW             │
                    └─────────────────────────────────────┘

    Input          Process              Output
    ─────          ───────              ──────

    ┌───┐         ┌─────────┐         ┌───┐
    │ A │ ──────▶ │ Module  │ ──────▶ │ B │
    └───┘         │   1     │         └───┘
                  └─────────┘
                       │
                       ▼
                  ┌─────────┐
                  │ Module  │
                  │   2     │ ──────▶ ┌───┐
                  └─────────┘         │ C │
                                        └───┘
```

### Data Flow

```
    Request                                      Response
    ───────                                      ────────

    User ──▶ [Controller] ──▶ [Service] ──▶ [Database]
                   │              │
                   │              ▼
                   │         [Transform]
                   │              │
                   ▼              ▼
              [Validate]     [Response]
```

### Sequence Diagram

```
    User        Server       Database       Cache
      │           │             │            │
      │──req──────▶│             │            │
      │           │──query──────▶│            │
      │           │              │            │
      │           │◀──result─────│            │
      │           │              │            │
      │◀──resp────│             │            │
```

### Component Hierarchy

```
    Project Root
    │
    ├── 📁 src/
    │   ├── 📁 modules/          ← "Neighborhoods"
    │   │   ├── 📁 users/        ← "User district"
    │   │   │   ├── user.entity.ts      "Blueprint for a user"
    │   │   │   ├── user.service.ts     "User operations"
    │   │   │   └── user.controller.ts  "User entrance desk"
    │   │   └── 📁 orders/
    │   └── 📁 shared/
    │       └── 📁 utils/       ← "Public works"
    └── 📁 tests/
```

---

## Customization Questions

Before deep diving, calibrate with:

### User's Experience Level
```
How familiar are you with:
- [Language/Stack]? (none/basic/intermediate/expert)
- [Pattern type]? (none/seen it/used it/taught it)
- Building [type of application]? (none/some/much)
```

### User's Learning Goals
```
What do you want from this explanation?
□ Just understand the big picture
□ Understand enough to make small changes
□ Understand enough to add major features
□ Be able to debug anything in this codebase
□ Be able to explain it to others
```

### User's Preferences
```
How do you prefer explanations?
- Analogies first, then code (Recommended for beginners)
- Code first, then analogies (Good for experienced devs)
- Side-by-side comparison
- Lots of diagrams
- Minimal diagrams, more text
```

### User's Current Confusion Level
```
"On a scale of 1-10, how lost do you feel right now?"
(10 = completely lost, 1 = just need specifics)
```

---

## Example Session Flow

```
USER: Explain this project to me

ASSISTANT:
Let me calibrate first!

Q1: "On a scale of 1-10, how lost do you feel?"
Q2: "What's your programming experience?"
Q3: "Do you prefer analogies or technical?"
Q4: "Your goal: understand / contribute / debug?"

USER: "I'm experienced with Python but not Java.
      I like analogies. I feel about a 7/10.
      I want to contribute."

ASSISTANT:
Great! I'll be your translator from Java/Python land.

Let's start with the FOUNDATION...

"First principles: This is a graph database.
 Think of it like a REALLY SMART contact list..."

[Builds understanding layer by layer]

Every few steps, I check:
✓ "Makes sense so far?"
✓ "Want to see code for this part?"
✓ "Need me to dig deeper on this?"

USER: "Actually, I'm confused about how vertices get IDs."

ASSISTANT:
No problem! Let's pause on the project tour
and go deep on ID strategies...

"Imagine you're assigning license plates...
 Each car (vertex) needs a unique identifier.
 We have 5 strategies for this..."

[Explains with new analogy, reconnects to codebase]

ASSISTANT:
"Back to our project tour - ready to continue?"
```

---

## Quick Start Prompts

To get the best explanation, you can say:

```
"Explain this project to me:
 - I know [Python/JS] but not [Java/TypeScript]
 - I understand basic programming but not [advanced patterns]
 - I prefer [analogy-heavy/code-heavy/visual]
 - My goal is to [understand/contribute/debug]
 - I feel like a [1-10] right now"
```

Or just say: **"Explain this project to me like I'm a complete beginner"**

Or: **"I want to contribute - show me the dev setup and a first issue"**

---

## Tips for Effective Learning

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. ASK "WHY" EARLY                                       │
│     Don't accept "what" without understanding "why"        │
│                                                            │
│  2. DRAW THINGS OUT                                       │
│     If you can't visualize it, ask for a diagram           │
│                                                            │
│  3. CONNECT TO WHAT YOU KNOW                               │
│     "This is like [something I understand] because..."    │
│                                                            │
│  4. TEACH IT BACK                                         │
│     Try explaining it to someone else - reveals gaps       │
│                                                            │
│  5. DON'T FAKE UNDERSTANDING                              │
│     Say "I don't get X" - better than nodding along       │
│                                                            │
│  6. ASK SILLY QUESTIONS                                   │
│     "But WHY would anyone name it that?" reveals context  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## HTML Template Integration

This skill includes an interactive HTML template with the full explanation UI. Use it to create rich, interactive explanations.

### Template File

```
.skill/
├── SKILL.md                    ← This file
├── TEMPLATES.md                ← Explanation templates
├── DIAGRAMS.md                 ← Diagram syntax reference
├── ANALOGIES.md                ← Common analogies for concepts
└── template.html              ← Interactive HTML explanation UI
```

### Using the HTML Template

When explaining a project using the HTML approach:

1. **Open** `template.html` in a browser or render it as markdown preview
2. **Fill in** the sections with project-specific content
3. **Customize** the HTML with actual file paths, function names, and code

The template includes:
- Progress indicator
- Question calibration box
- First principles (problem/solution)
- Analogy + diagram
- Component flow
- Code walkthrough
- File structure
- Interactive check

---

## Skill Metadata

**Base directory**: The directory containing this SKILL.md file
**Templates**: TEMPLATES.md, ANALOGIES.md, DIAGRAMS.md
**Interactive UI**: template.html

**When to use this skill**:
- User asks to understand a codebase
- User wants to contribute but needs orientation
- User is confused about architecture or design patterns
- User wants a ground-up explanation, not just code

**When NOT to use this skill**:
- User just wants a quick answer to a specific question
- User already understands the codebase
- User just wants code snippets, not explanations
