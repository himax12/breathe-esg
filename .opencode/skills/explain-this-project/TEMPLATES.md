# Explanation Templates

Reusable templates for consistent, structured explanations.

---

## 1. Explaining a Variable

```markdown
## Variable: [Name]

### Type
`[Type]` - e.g., `string`, `User[]`, `Map<string, number>`

### Purpose
"A box that holds [description]"

### Analogy
"Imagine a labeled jar - [analogy]"

### What's Inside
- If `const`: "Once set, never changes - like a carved-in-stone measurement"
- If `let`: "Can be updated - like a car's odometer"
- If it's an array: "A numbered list, like seats in a theater"
- If it's an object: "A properties sheet, like a character sheet in a game"

### Example Value
```typescript
const [name] = [actual value];
// Would look like: [what it looks like printed out]
```

### Related Operations
- Reading: "To see what's inside, we [how]"
- Writing: "To change it, we [how]"
- Common bugs: "People often mess up by [common mistake]"
```

---

## 2. Explaining a Function

```markdown
## Function: [Name]

### What It Does
"One sentence: Takes [input] and returns [output]"

### Signature
```typescript
function [name]([params]): [ReturnType]
```

### The Transformation
```
INPUT                              OUTPUT
──────                             ──────
[what comes in]    ──────►    [what comes out]

Before: [raw/unstructured]
After:  [processed/structured]
```

### Step-by-Step Walkthrough

```
Step 1: [Name this step]
        "First we [what happens]"
        Code: `// [actual line]`
        Like: [analogy]

Step 2: [Name this step]
        "Then we [what happens]"
        Code: `// [actual line]`
        Like: [analogy]

Step 3: [Name this step]
        "Finally we [what happens]"
        Code: `// [actual line]`
        Like: [analogy]
```

### Edge Cases
| Input | Behavior |
|-------|----------|
| `null` | [what happens] |
| `[]` (empty) | [what happens] |
| `undefined` | [what happens] |
| Large input | [what happens] |

### Real-World Parallel
"When you [action], that's like calling this function with [input]."

### Code Example
```typescript
// Input
const input = [example];

// Call
const result = [name](input);

// Output
console.log(result); // [what prints]
```

---

## 3. Explaining a Class

```markdown
## Class: [Name]

### What It Is
"A blueprint for [what it creates]"

### Analogy
"Like a [real-world thing] because [reason]"

### The Schema
```typescript
class [Name] {
  // Properties - "Characteristics"
  [prop1]: [Type]  // "[description]"
  [prop2]: [Type]  // "[description]"

  // Methods - "Actions it can do"
  [method1](): [ReturnType]  // "[what it does]"
  [method2]([params]): [ReturnType]  // "[what it does]"
}
```

### Instantiation
```typescript
const instance = new [Name]([constructor args]);
// "Creating a new [class] is like [real world equivalent]"
```

### Properties Explained
| Property | Type | Purpose |
|----------|------|---------|
| `[prop]` | `Type` | "[why it exists]" |

### Methods Explained
| Method | Input | Output | What It Does |
|--------|-------|--------|--------------|
| `[method]` | `params` | `ReturnType` | "[description]" |

### State Machine (if applicable)
```
[State A]  ──event1──►  [State B]
    ▲                       │
    │                       ▼
    └──event2────  [State C]
```

### Usage Example
```typescript
const my[name] = new [Name]();

// "To [achieve X], we call..."
my[name].[method]();

// "This modifies the [property], which [effect]"
```

---

## 4. Explaining an Interface/Type

```markdown
## Interface: [Name]

### What It Defines
"A contract that says 'anything using this must have...'"

### The Contract
```typescript
interface [Name] {
  [field1]: [Type];  // "Must have [description]"
  [field2]: [Type];  // "Must have [description]"
}
```

### Visual Contract
```
┌─────────────────────────────────┐
│      [Name] Interface           │
├─────────────────────────────────┤
│  field1: Type    ✓ REQUIRED     │
│  field2: Type    ✓ REQUIRED     │
│  [field3]: Type  ○ OPTIONAL     │
└─────────────────────────────────┘
```

### Real-World Parallel
"Like a job application form - it specifies what information must be provided."

### Usage Pattern
```typescript
function processItem(item: [Name]) {
  // "We can trust that item has [fields] because of the interface"
  item.[field1]; // TypeScript knows this exists
}
```

### Relationship to Classes
```
Interface [Name]
       ▲
       │ implements
       │
    [Class] ──── "I promise to provide everything in the contract"
```

---

## 5. Explaining a Module/File

```markdown
## Module: [File Name]

### Location
```
src/
└── [path]
    └── [filename]
```

### What It Contains
"[Purpose of this file]"

### Key Exports
```typescript
export [item]     // "[description]"
export [item]     // "[description]"
```

### Internal Dependencies
```
┌────────────────────────────────────────────┐
│           [Filename]                        │
├────────────────────────────────────────────┤
│  Imports from:                             │
│    ├── [module1]  →  uses [what]          │
│    └── [module2]  →  uses [what]          │
│                                            │
│  Exports to:                               │
│    ├── [consumer1]  →  provides [what]    │
│    └── [consumer2]  →  provides [what]    │
└────────────────────────────────────────────┘
```

### The Single Responsibility
"This module does ONE thing: [what]"

If it does more, it's a red flag.

---

## 6. Explaining an API Endpoint

```markdown
## Endpoint: [Method] [Path]

### What It Does
"[One sentence description]"

### The Request
```
[METHOD] [path]

Headers:
  Content-Type: application/json
  Authorization: Bearer [token]

Body:
{
  "[field]": [type]  // "[description]"
}
```

### The Response
```
[Status Code] [Status Text]

{
  "[field]": [type]  // "[description]"
}
```

### The Flow
```
User ──► [Controller] ──► [Service] ──► [Database]
         │                    │
         │                    ▼
         │              [Transform]
         ▼                    │
   [Validate]                 ▼
         │              [Return]
         ▼                    │
   [Format Error] ◄───────────┘
```

### Error Cases
| Status | When |
|--------|------|
| 400 | "[what validation fails]" |
| 401 | "[what auth fails]" |
| 404 | "[what not found]" |
| 500 | "[what server fails]" |

### Try It
```bash
curl -X [METHOD] [url] \
  -H "Content-Type: application/json" \
  -d '{"[field]": [value]}'
```

---

## 7. Explaining a Design Pattern

```markdown
## Pattern: [Name]

### The Problem
"Before this pattern, when you had [scenario], you had to [old approach], which caused [pain]."

### The Solution
"This pattern says: 'What if we [key insight]?'"

### The Structure
```
┌─────────────────────────────────────────────────────────┐
│                   [Pattern Name]                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Participants:                                          │
│    • [Role A]  →  "Does [X]"                          │
│    • [Role B]  →  "Does [Y]"                          │
│                                                         │
│  Relationships:                                         │
│    [Role A] ──uses──► [Role B]                        │
│                                                         │
│  Flow:                                                  │
│    1. [First step]                                    │
│    2. [Second step]                                    │
│    3. [Third step]                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Real-World Analogy
"Like [real world scenario] because [similarity]"

### Code Template
```typescript
// The pattern in action:
class [Example] {
  private collaborator: [Interface];

  constructor(dep: [Interface]) {
    this.collaborator = dep; // "I need someone who can [X]"
  }

  doWork() {
    // "Here's where the pattern magic happens"
    return this.collaborator.performAction();
  }
}
```

### When To Use
- When you have [scenario A]
- When you need [benefit]
- When [alternative] is too rigid

### When Not To Use
- When [scenario B]
- When overhead exceeds benefit

---

## 8. Explaining an Error

```markdown
## Error: [Name/Type]

### The Signal
"When you see this error, it means [core message]"

### The Anatomy
```
[Error Type]: [What went wrong]
    at [Location] ([file:line])
    at [Location] ([file:line])
```

### Root Cause Analysis
```
Symptom: [what you see]
    │
    ▼
Cause: [what actually happened]
    │
    ▼
Source: [where it originated]
```

### The Fix Pattern
```typescript
// Before (causes error)
const result = dangerousOperation();

// After (handles properly)
try {
  const result = dangerousOperation();
} catch (error) {
  // Handle: [what to do]
  console.error("Recovery action");
}
```

### Prevention
"To avoid this error in the future: [guidelines]"

---

## 9. Explaining a Data Flow

```markdown
## Data Flow: [Description]

### The Journey
```
[Start]
   │
   ▼
[Step 1] ──transforms──► [Intermediate A]
   │
   ▼
[Step 2] ──validates──► [Intermediate B]
   │
   ▼
[Step 3] ──stores─────► [Destination]
```

### At Each Stage

**Stage 1: [Name]**
- Input: [what comes in]
- Transform: [what changes]
- Output: [what goes out]
- Location: [file/function]

**Stage 2: [Name]**
- Input: [what comes in]
- Transform: [what changes]
- Output: [what goes out]
- Location: [file/function]

### The Shape of Data
```
Input shape:    { id, email, name }
                    │
                    ▼ Removes password
Intermediate:    { id, email }
                    │
                    ▼ Adds computed field
Output shape:    { id, email, avatarUrl }
```

### Key Transformations
| From | To | Transform |
|------|----|----------|
| `raw string` | `parsed object` | `JSON.parse()` |
| `user object` | `database row` | `serialize()` |

---

## 10. Explaining Architecture

```markdown
## Architecture: [System Name]

### The Big Picture
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│              [System] Architecture                      │
│                                                         │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐           │
│   │ Client  │───►│   API   │───►│   Data  │           │
│   └─────────┘    │ Gateway │    │  Store  │           │
│                  └─────────┘    └─────────┘           │
│                       │                                │
│                       ▼                                │
│                  ┌─────────┐                          │
│                  │ Services│                          │
│                  └─────────┘                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

**Layer 1: [Name]**
- Responsibility: [what it does]
- Contains: [what files/modules]
- Talks to: [who]

**Layer 2: [Name]**
- Responsibility: [what it does]
- Contains: [what files/modules]
- Talks to: [who]

### Key Principles

```
1. [Principle Name]
   "We [do X] because [benefit]"
   Example: "We cache responses because [speed benefit]"

2. [Principle Name]
   "We [do Y] because [benefit]"
```

### Data Flow
```
Browser ──HTTPS──► Load Balancer ──► API Server
                                        │
                                        ▼
                                   [Cache]
                                        │
                                        ▼
                                   [Database]
```

### Where to Find Things
| If you need... | Look in... |
|----------------|------------|
| [something] | [location] |
| [something] | [location] |

---

## Template Cheat Sheet

Quick reference for common needs:

```
| To explain...          | Use template...              |
|------------------------|-------------------------------|
| A variable             | Template 1                    |
| A function             | Template 2                    |
| A class                | Template 3                    |
| An interface           | Template 4                    |
| A module               | Template 5                    |
| An API endpoint        | Template 6                    |
| A design pattern       | Template 7                    |
| An error               | Template 8                    |
| Data flow              | Template 9                    |
| Architecture           | Template 10                   |
```

---

**Templates** - Building blocks for consistent, clear explanations.