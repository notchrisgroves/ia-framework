# Mermaid Syntax Quick Reference

Quick reference for common Mermaid diagram syntax.

---

## Flowchart

```mermaid
flowchart TB
    %% Direction: TB (top-bottom), LR (left-right), BT, RL

    %% Nodes
    A[Rectangle]
    B(Rounded)
    C{Diamond}
    D([Stadium])
    E[(Database)]
    F((Circle))

    %% Connections
    A --> B           %% Arrow
    B --- C           %% Line
    C -.-> D          %% Dotted arrow
    D ==> E           %% Thick arrow
    E -->|label| F    %% Labeled

    %% Subgraphs
    subgraph Group["Group Title"]
        G[Node 1]
        H[Node 2]
    end
```

### Node Shapes

| Syntax | Shape |
|--------|-------|
| `[text]` | Rectangle |
| `(text)` | Rounded |
| `{text}` | Diamond |
| `([text])` | Stadium |
| `[(text)]` | Database |
| `((text))` | Circle |
| `[[text]]` | Subroutine |
| `>text]` | Flag |

### Connections

| Syntax | Type |
|--------|------|
| `-->` | Arrow |
| `---` | Line |
| `-.->` | Dotted arrow |
| `==>` | Thick arrow |
| `--text-->` | Labeled |
| `-->|text|` | Labeled (alt) |

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob

    A->>B: Request
    B-->>A: Response

    A->>+B: Activate
    B-->>-A: Deactivate

    Note over A,B: Note spanning both

    alt Success
        B->>A: OK
    else Failure
        B->>A: Error
    end

    loop Every minute
        A->>B: Heartbeat
    end
```

### Arrow Types

| Syntax | Type |
|--------|------|
| `->>` | Solid arrow |
| `-->>` | Dotted arrow |
| `-x` | Cross (async) |
| `--x` | Dotted cross |
| `-)` | Open arrow |
| `--)` | Dotted open |

### Activation

| Syntax | Effect |
|--------|--------|
| `->>+` | Activate target |
| `-->>-` | Deactivate target |
| `activate A` | Explicit activate |
| `deactivate A` | Explicit deactivate |

---

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }

    class Dog {
        +String breed
        +bark()
    }

    Animal <|-- Dog : extends

    class Owner {
        +String name
    }

    Owner "1" --> "*" Dog : owns
```

### Relationships

| Syntax | Type |
|--------|------|
| `<\|--` | Inheritance |
| `*--` | Composition |
| `o--` | Aggregation |
| `-->` | Association |
| `..>` | Dependency |
| `..\|>` | Realization |

### Visibility

| Symbol | Meaning |
|--------|---------|
| `+` | Public |
| `-` | Private |
| `#` | Protected |
| `~` | Package |

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> Processing : Start
    Processing --> Success : Complete
    Processing --> Error : Fail

    Success --> [*]
    Error --> Idle : Retry

    state Processing {
        [*] --> Step1
        Step1 --> Step2
        Step2 --> [*]
    }
```

---

## Entity Relationship

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"

    CUSTOMER {
        int id PK
        string name
        string email
    }

    ORDER {
        int id PK
        int customer_id FK
        date created
    }
```

### Cardinality

| Syntax | Meaning |
|--------|---------|
| `\|\|` | Exactly one |
| `o\|` | Zero or one |
| `}o` | Zero or more |
| `}\|` | One or more |

---

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Phase 1
    Task A :a1, 2025-01-01, 7d
    Task B :a2, after a1, 5d

    section Phase 2
    Task C :b1, after a2, 10d
    Milestone :milestone, m1, after b1, 0d
```

---

## Pie Chart

```mermaid
pie title Distribution
    "Category A" : 45
    "Category B" : 30
    "Category C" : 25
```

---

## Git Graph

```mermaid
gitGraph
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```

---

## Mind Map

```mermaid
mindmap
    root((Central Topic))
        Branch 1
            Leaf 1
            Leaf 2
        Branch 2
            Leaf 3
        Branch 3
```

---

## Styling

### Inline Styles

```mermaid
flowchart LR
    A --> B --> C

    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#bfb,stroke:#333
```

### Class-based Styles

```mermaid
flowchart LR
    A:::error --> B:::warning --> C:::success

    classDef error fill:#ff6b6b
    classDef warning fill:#ffd93d
    classDef success fill:#6bcb77
```

---

## Themes

Available themes:
- `default` - Standard colors
- `dark` - Dark background
- `forest` - Green tones
- `neutral` - Grayscale

Set via CLI: `mmdc -t dark ...`

---

**Reference:** mermaid-syntax
**Skill:** diagram-generation
