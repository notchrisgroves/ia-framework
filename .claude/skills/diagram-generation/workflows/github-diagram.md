# GitHub Diagram Workflow

Using Mermaid diagrams in GitHub documentation (README, docs, issues, PRs).

---

## GitHub Native Rendering

GitHub automatically renders Mermaid diagrams in markdown. No export needed.

### Basic Usage

````markdown
```mermaid
flowchart LR
    A[Start] --> B[Process] --> C[End]
```
````

Renders directly in:
- README.md
- Documentation files
- Issues and Pull Requests
- Wiki pages

---

## Common Diagram Types

### Flowchart

````markdown
```mermaid
flowchart TB
    subgraph Input
        A[User Request]
    end

    subgraph Processing
        B{Decision}
        C[Action 1]
        D[Action 2]
    end

    A --> B
    B -->|Yes| C
    B -->|No| D
```
````

### Sequence Diagram

````markdown
```mermaid
sequenceDiagram
    participant U as User
    participant C as Claude
    participant S as Skill

    U->>C: /command
    C->>S: Load skill
    S-->>C: Context
    C-->>U: Response
```
````

### Class Diagram

````markdown
```mermaid
classDiagram
    class Agent {
        +name: string
        +skills: Skill[]
        +execute()
    }

    class Skill {
        +name: string
        +workflows: Workflow[]
    }

    Agent --> Skill
```
````

### State Diagram

````markdown
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Request
    Processing --> Complete: Success
    Processing --> Error: Failure
    Complete --> [*]
    Error --> Idle: Retry
```
````

### Entity Relationship

````markdown
```mermaid
erDiagram
    USER ||--o{ POST : creates
    POST ||--|{ COMMENT : has
    USER ||--o{ COMMENT : writes
```
````

---

## Best Practices

### 1. Keep Diagrams Focused

```mermaid
%% Good: Clear, focused diagram
flowchart LR
    A --> B --> C
```

Avoid cramming too much into one diagram.

### 2. Use Subgraphs for Organization

```mermaid
flowchart TB
    subgraph Frontend
        A[React]
        B[Components]
    end

    subgraph Backend
        C[API]
        D[Database]
    end

    Frontend --> Backend
```

### 3. Add Labels to Edges

```mermaid
flowchart LR
    A -->|"HTTP GET"| B
    B -->|"JSON"| C
```

### 4. Use Appropriate Direction

- `TB` (top-bottom) - Hierarchies, processes
- `LR` (left-right) - Sequences, flows
- `BT` (bottom-top) - Rare, specific uses
- `RL` (right-left) - Rare

---

## Styling

### Node Shapes

```
[Rectangle]
(Rounded)
{Diamond}
([Stadium])
[[Subroutine]]
[(Database)]
((Circle))
```

### Colors (via style)

````markdown
```mermaid
flowchart LR
    A[Error] --> B[Warning] --> C[Success]

    style A fill:#ff6b6b,stroke:#333
    style B fill:#ffd93d,stroke:#333
    style C fill:#6bcb77,stroke:#333
```
````

---

## When to Export Instead

Export to PNG/SVG when:
- Sharing outside GitHub
- Including in presentations
- Adding to Ghost blog
- Creating PDFs

Use:
```bash
python skills/diagram-generation/scripts/export-diagram.py \
    docs/architecture.mmd -o docs/images/architecture.png
```

---

## Diagram Source Files

For complex diagrams, maintain `.mmd` source files:

```
docs/
├── architecture.md      # References diagram
├── diagrams/
│   └── architecture.mmd # Source (for exports)
```

In markdown:
````markdown
<!-- For GitHub: inline rendering -->
```mermaid
flowchart TB
    ...
```

<!-- For other uses: exported image -->
![Architecture](images/architecture.png)
````

---

**Workflow:** github-diagram
**Skill:** diagram-generation
