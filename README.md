# Intelligence Adjacent (IA) Framework

**Intelligence Adjacent (IA)** is a framework for building AI systems that work alongside human intelligence rather than attempting to replace it.

We believe that orchestration and scaffolding are more important than model intelligence. The goal is upgrading human capabilities, not automation.

---

## What You Get

```
AGENTS          SKILLS              COMMANDS
  |               |                    |
  v               v                    v
security      code-review         /pentest
writer        threat-intel        /blog-post
advisor       career              /job-analysis
legal         architecture-review /risk-assessment
              ...and more         ...and more
```

**Agents** - Specialized identities for security, writing, advisory, and legal work
**Skills** - Domain expertise with progressive context loading
**Commands** - Guided workflows triggered by `/command`

---

## Prerequisites

- **Claude Code** - Anthropic's official CLI ([installation guide](https://docs.anthropic.com/en/docs/claude-code))
- **Git** - [git-scm.com/downloads](https://git-scm.com/downloads)
- **Python 3.10+** - For validation tools

### Install Claude Code

```bash
# Install via npm
npm install -g @anthropic-ai/claude-code

# Verify
claude --version
```

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone anywhere you like
git clone https://github.com/notchrisgroves/ia-framework.git
cd ia-framework
```

### Step 2: Run the Installer

**macOS / Linux:**
```bash
./setup/install.sh
```

**Windows (PowerShell as Administrator or with Developer Mode):**
```powershell
.\setup\install.ps1
```

The installer:
1. Creates a symlink: `~/.claude` → `<your-clone>/.claude`
2. Copies `.env.example` → `~/.env` for your API keys
3. Creates user directories (sessions, plans, output)

### Step 3: Configure API Keys

Edit `~/.env` with your keys:

```bash
# OpenRouter - Multi-model access (recommended)
OPENROUTER_API_KEY=sk-or-your-key

# GitHub - For repository operations
GITHUB_TOKEN=ghp_your-token
```

### Step 4: Authenticate Claude Code

**Option A: Claude Pro/Team Subscription (Recommended)**
```bash
claude
# Follow login prompts - credentials stored in ~/.claude/.credentials.json
```

**Option B: API Key**
```bash
# Add to shell profile (~/.bashrc, ~/.zshrc, etc.)
export ANTHROPIC_API_KEY=sk-ant-your-key
```

### Step 5: Start Using

```bash
# Launch Claude Code from any directory
claude

# Try a command
/pentest
/code-review
/job-analysis
```

---

## How It Works

```
~/.claude/                    <-- Symlinked to your clone
├── CLAUDE.md                 # Framework navigation (auto-loaded)
├── agents/                   # Specialized agents
├── skills/                   # Domain expertise
├── commands/                 # Slash commands
├── docs/                     # Architecture docs
├── library/                  # Templates & patterns
├── tools/                    # Validation scripts
└── hooks/                    # Pre-commit automation
```

When you run `claude`, it automatically reads `~/.claude/CLAUDE.md` which provides the framework context. The symlink means updates to your clone are immediately available.

---

## Updating

```bash
cd /path/to/ia-framework
git pull origin main
```

Your customizations in `agents/`, `commands/`, `skills/` are preserved. Framework updates apply immediately via the symlink.

---

## Creating Your Own Components

### New Skill
```bash
# In Claude Code
"Create a new skill for [your domain]"

# Or manually
mkdir -p ~/.claude/skills/my-skill
# Create SKILL.md following library/templates/
```

### New Agent
```bash
cp ~/.claude/agents/example-agent.md ~/.claude/agents/my-agent.md
# Edit to define identity and routing
```

### New Command
```bash
cp ~/.claude/commands/example-command.md ~/.claude/commands/my-command.md
# Edit to define workflow
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [Hierarchical Context Loading](.claude/docs/hierarchical-context-loading.md) | How context is progressively loaded |
| [Agent Format Standards](.claude/docs/AGENT-FORMAT-STANDARDS.md) | How to create agents |
| [File Location Standards](.claude/docs/FILE-LOCATION-STANDARDS.md) | Where files belong |
| [Credential Handling](.claude/docs/CREDENTIAL-HANDLING-ENFORCEMENT.md) | Security best practices |

---

## VPS Deployment (Optional)

For hands-on security testing, deploy tools to a VPS. See the [Setup Guide](https://notchrisgroves.com/ia-setup-guide/) for VPS configuration with SSH keys, Docker containers, and Twingate zero-trust access.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Framework:** Intelligence Adjacent (IA) | **Version:** 1.0.0
