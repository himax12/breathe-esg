---
name: explain-this-project
description: Explain a codebase from first principles using diagrams, analogies, and building concepts from the ground up. Makes complex code accessible to newcomers by connecting abstract ideas to concrete, everyday experiences. Uses interactive questioning to understand the user's background and tailor explanations.
version: 1.0.0
author: opencode
type: skill
category: education
tags:
  - explanation
  - first-principles
  - education
  - diagrams
  - analogies
  - onboarding
---

# Explain This Project

## Purpose

Transform complex codebase explanations into intuitive, ground-up understanding. This skill exists because reading raw code without context is like trying to understand a city by looking at individual bricks.

## Philosophy

**Knowledge，建筑一块砖不足以理解房子 structure**

Real understanding comes from:
1. **Why** - What problem does this solve? Why does it exist?
2. **How** - How does it work internally?
3. **What** - What does the code actually do?

We build understanding **bottom-up**: from fundamental concepts → intermediate ideas → full implementation.

---

## The Analogy Framework

### For Newcomers: The House Metaphor

```
Codebase = A House You're Moving Into

├── Blueprints (Architecture)     → How rooms connect, where pipes go
├── Rooms (Modules/Packages)      → Functional areas
├── Walls (Interfaces/APIs)       → What separates things
├── Doors (Function calls)         → How you move between rooms
├── Furniture (Classes/Functions)  → What fills each space
└── Foundation (Data models)      → What everything rests on
```

### For Advanced: The City Metaphor

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

## Core Technique: Concept Stacking

Build understanding in layers:

```
Layer 1: Mental Model (The "What is this?" layer)
    ↓ "This is a web server - like a waiter in a restaurant"

Layer 2: Component Interactions (The "How does it work?" layer)
    ↓ "The waiter takes orders (requests) and brings food (responses)"

Layer 3: Implementation Details (The "How is it built?" layer)
    → Now we can look at actual code and understand WHERE things happen
```

---

## How to Use This Skill

### Step 1: Understanding Your Background

Before explaining, I will ask you questions to calibrate:

```markdown
## Questions I'll Ask:

1. **Technical Background**
   - "How comfortable are you with programming?"
   - "Have you worked with [relevant languages] before?"
   - "Do you know what a [concept] is?"

2. **Project Context**
   - "Have you seen similar projects before?"
   - "What's your goal - just understand, or be able to modify?"

3. **Learning Style**
   - "Do you prefer analogies or technical precision?"
   - "How much detail do you want?"

4. **Current Level**
   - "On a scale of 1-10, how lost do you feel right now?"
```

### Step 2: Building the Explanation

For each concept, I will structure explanations as:

```
┌─────────────────────────────────────────────────────────┐
│  CONCEPT: [Name]                                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  THE ANALOGY:                                           │
│  "Imagine [everyday thing]..."                         │
│                                                         │
│  THE PROBLEM IT SOLVES:                                 │
│  "Before this existed, developers had to..."           │
│                                                         │
│  THE MECHANISM:                                         │
│  "It works like [real thing] because..."              │
│                                                         │
│  CODE EXAMPLE:                                          │
│  ```                                                    │
│  // This does X                                        │
│  // Think of it like Y                                 │
│  ```                                                   │
│                                                         │
│  ANALOGY BACK TO REAL WORLD:                            │
│  "So next time you [action], that's similar to..."    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Diagram Conventions

When I generate diagrams, I use these conventions:

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

## Interactive Mode

### The Question Protocol

During explanation, I'll ask:

```markdown
### Before Moving to Next Concept:

☑️ "Did that make sense? (yes/no/partially)"
☑️ "Want me to go deeper on this part?"
☑️ "Shall I show you the actual code now?"

### During Code Walkthrough:

☑️ "What does THIS line do? [let them guess]"
☑️ "Why do you think we check THIS condition first?"
☑️ "If this function was a person, what would their job be?"
```

### Socratic Method Triggers

```
┌──────────────────────────────────────────────────────────┐
│  When you see a concept, try to:                         │
│                                                          │
│  1. EXTRACT PRINCIPLE                                    │
│     "What's the ONE thing this teaches us?"            │
│                                                          │
│  2. FIND ANALOGY                                         │
│     "What's this similar to in real life?"              │
│                                                          │
│  3. DRAW IT OUT                                          │
│     "If you had to draw this, what would it look like?" │
│                                                          │
│  4. TEACH IT BACK                                        │
│     "How would you explain this to a 5-year-old?"       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Explanation Templates

### Template 1: Explaining a Module

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

### Template 2: Explaining a Function

```markdown
## Function: [Name]

### Signature
```typescript
function doSomething(input: Type): Output
```

### What It Does
A "worker" that takes [input] and produces [output].

### The Purpose
"Given [input], we need [result] so that [benefit]."

### Step-by-Step
1. First, it [does this] — like [analogy]
2. Then, it [does this] — like [analogy]
3. Finally, it [returns this] — which is [explanation]

### Edge Cases
- If input is [condition], it [does this]
- If input is [condition], it [does this]

### Code Walkthrough
```typescript
const result = input // "Take the ingredient"
  .transform()       // "Prepare it - like chopping vegetables"
  .validate()        // "Check it's good quality"
  .process();        // "Cook it into the final dish"
```

### Back to Real Life
"So when you [real world action], that's the same as calling this function."
```

### Template 3: Explaining an Architecture Pattern

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
│   AFTER:                                               │
│   A → B → C → D                                        │
│   But with [special mechanism] so changes don't ripple │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### The Metaphor
"This is like [metaphor] because [how they relate]."

### Implementation Skeleton
```typescript
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

---

## First Principles Breakdown

### For Any Concept, Start Here:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  WHY DOES THIS EXIST?                                       │
│  ─────────────────────                                      │
│  What human problem motivated creating this?               │
│  Before this: developers had to [workaround]               │
│  That caused: [pain point]                                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IS IT AT ITS CORE?                                    │
│  ───────────────────────                                    │
│  Strip away all implementation details                     │
│  This is fundamentally a [simple concept]:                  │
│  "A mechanism for [doing X] in [context Y]"               │
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
│  Part A: Does [X] — like a [real thing]                    │
│  Part B: Does [Y] — like a [real thing]                    │
│  Part C: Does [Z] — like a [real thing]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Customization Questions

Before deep diving, I'll ask:

### Your Experience Level
```
How familiar are you with:
- [Language]? (none/basic/intermediate/expert)
- [Pattern type]? (none/seen it/used it/taught it)
- Building [type of application]? (none/some/much)
```

### Your Learning Goals
```
What do you want from this explanation?
□ Just understand the big picture
□ Understand enough to make small changes
□ Understand enough to add major features
□ Be able to debug anything in this codebase
□ Be able to explain it to others
```

### Your Preferences
```
How do you prefer explanations?
- Analogies first, then code
- Code first, then analogies
- Side-by-side comparison
- Lots of diagrams
- Minimal diagrams, more text
```

---

## Example Session Flow

```
YOU: Explain this project to me
     ↓
ME:  Let me calibrate first!
     ↓
Q1: "On a scale of 1-10, how lost do you feel?"
    "What's your programming experience?"
    "Do you prefer analogies or technical?"
     ↓
YOU: "I've done some Python, never TypeScript.
     I like analogies. I feel about a 3/10."
     ↓
ME:  Great! I'll be your translator.

     Let's start with the FOUNDATION...

     "First principles: A web server is like a RESTAURANT.
      You're the customer (browser), the menu is the API,
      and the kitchen is the server..."

     [Builds understanding layer by layer]

     Every few steps, I check:
     ✓ "Makes sense so far?"
     ✓ "Want to see code for this part?"
     ✓ "Need me to dig deeper on this?"

     ↓
YOU: "Actually, I'm confused about how the database
     connection pooling works."
     ↓
ME:  No problem! Let's pause on the project tour
     and go deep on connection pooling...

     "Imagine you're at a buffet with limited serving spoons..."
     [Explains with new analogy, reconnects to codebase]
     ↓
ME:  "Back to our project tour - ready to continue?"
     ✓
```

---

## When Explaining Doesn't Make Sense

Sometimes I can't explain because:

1. **Missing context** - I need to understand what THIS code does before explaining
2. **Unknown audience** - Who's this for? (new dev? product manager? non-technical?)
3. **Unknown goal** - Understand for debugging? Contributing? General knowledge?

In these cases, I'll ask a specific question before proceeding.

---

## Quick Start

To get the best explanation, you can:

```markdown
"Explain this project to me:
- I know [Python/JS] but not [TypeScript/Rust]
- I understand basic programming but not [advanced patterns]
- I prefer [analogy-heavy/code-heavy/visual]
- My goal is to [understand/change/debug/contribute]
- I feel like a [1-10] right now"
```

Or just say: **"Explain this project to me like I'm a complete beginner"**

---

## Tips for Effective Learning

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  1. ASK "WHY" EARLY                                       │
│     Don't accept "what" without understanding "why"       │
│                                                            │
│  2. DRAW THINGS OUT                                       │
│     If you can't visualize it, ask for a diagram          │
│                                                            │
│  3. CONNECT TO WHAT YOU KNOW                              │
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
.explain-this-project/
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

### Quick Template Sections

```html
<!-- 1. Progress -->
<div class="progress-fill" style="width: X%;"></div>

<!-- 2. Question Calibration -->
<section class="question-box">
  <!-- Ask about: experience level, learning style, goals -->
</section>

<!-- 3. First Principles -->
<div class="problem-box">The problem...</div>
<div class="solution-box">The solution...</div>

<!-- 4. Analogy + Diagram -->
<div class="analogy-box">Think of it like...</div>
<pre>ASCII diagram</pre>

<!-- 5. Code Example -->
<pre><code>actual code with analogies</code></pre>

<!-- 6. File Structure -->
<pre>Directory tree</pre>

<!-- 7. Interactive Check -->
<div class="options">
  <button>Yes, continue</button>
  <button>Need clarification</button>
  <button>Show more code</button>
</div>
```

---

**Explain This Project** - Building understanding from the ground up, one concept at a time.