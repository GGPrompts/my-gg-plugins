# Tool Catalog

Complete reference of available tools for agent configuration.

## File Operations

### Read

**Purpose**: Read file contents

**Use When**: Agent needs to view file contents, understand code, analyze documents

**Capabilities**:
- Read any file type (code, text, images, PDFs, notebooks)
- Specify line ranges for large files
- View images visually (multimodal)

**Example Use Cases**:
- Understanding existing code before editing
- Analyzing configuration files
- Reading documentation

---

### Write

**Purpose**: Create or overwrite files

**Use When**: Agent needs to create new files or replace entire file contents

**Capabilities**:
- Create new files
- Overwrite existing files completely
- Any file type

**Note**: Requires reading the file first if it exists.

---

### Edit

**Purpose**: Make targeted changes to existing files

**Use When**: Agent needs to modify specific parts of a file

**Capabilities**:
- Find and replace strings
- Precise edits without rewriting whole file
- Replace all occurrences option

**Note**: More efficient than Write for partial changes.

---

### Glob

**Purpose**: Find files by pattern

**Use When**: Agent needs to locate files by name or extension

**Capabilities**:
- Glob patterns (`**/*.ts`, `src/**/*.tsx`)
- Returns paths sorted by modification time

**Example Patterns**:
- `**/*.md` - All markdown files
- `src/components/**/*.tsx` - React components
- `**/test*.py` - Test files

---

### Grep

**Purpose**: Search file contents

**Use When**: Agent needs to find code patterns, definitions, or text

**Capabilities**:
- Regex pattern matching
- Filter by file type or glob
- Context lines before/after
- Count matches
- Multiline matching

**Example Searches**:
- Function definitions: `function\s+\w+`
- Imports: `import.*from`
- TODO comments: `TODO|FIXME`

---

## System Operations

### Bash

**Purpose**: Execute shell commands

**Use When**: Agent needs to run commands, scripts, git operations, or system tools

**Capabilities**:
- Any shell command
- Background execution
- Timeout control

**Common Uses**:
- `git status`, `git diff`, `git commit`
- `npm install`, `npm run build`
- `python script.py`
- Running tests

**Note**: Avoid using for file operations (use Read/Write/Edit instead).

---

### BashOutput

**Purpose**: Get output from background shell

**Use When**: Agent started a background process and needs to check output

---

### KillShell

**Purpose**: Terminate background shell

**Use When**: Agent needs to stop a running background process

---

## Web Operations

### WebSearch

**Purpose**: Search the web

**Use When**: Agent needs current information, documentation, or external resources

**Capabilities**:
- Web search with domain filtering
- Returns search results with links

**Example Uses**:
- "React 19 new features"
- "TypeScript 5.4 documentation"
- Latest library versions

---

### WebFetch

**Purpose**: Fetch and analyze web page content

**Use When**: Agent needs to read specific web pages

**Capabilities**:
- Fetches URL content
- Converts HTML to markdown
- Processes with AI for extraction

**Note**: Prefer MCP web tools if available (fewer restrictions).

---

## Agent Operations

### Task

**Purpose**: Spawn sub-agents for complex tasks

**Use When**: Agent needs to delegate work to specialists

**Capabilities**:
- Launch specialized sub-agents
- Parallel execution
- Various agent types (Explore, Plan, general-purpose, etc.)

**Agent Types**:
- `Explore` - Codebase exploration
- `Plan` - Implementation planning
- `general-purpose` - Multi-step tasks
- Custom agents from `.claude/agents/`

---

### TodoWrite

**Purpose**: Track tasks and progress

**Use When**: Agent is working on multi-step tasks

**Capabilities**:
- Create task lists
- Track status (pending, in_progress, completed)
- Visible to user for progress tracking

**Best Practice**: Use for any task with 3+ steps.

---

## User Interaction

### AskUserQuestion

**Purpose**: Ask user for input or clarification

**Use When**: Agent needs user decision or missing information

**Capabilities**:
- Present options with descriptions
- Multi-select support
- 1-4 questions at once

---

## Notebook Operations

### NotebookEdit

**Purpose**: Edit Jupyter notebook cells

**Use When**: Agent is working with .ipynb files

**Capabilities**:
- Replace cell contents
- Insert new cells
- Delete cells
- Change cell type (code/markdown)

---

## MCP Tools

MCP (Model Context Protocol) tools are dynamically loaded from configured servers. Common categories:

### Database Tools
- Query databases
- Schema inspection
- Data manipulation

### API Tools
- External service integration
- Authentication helpers
- Data fetching

### Specialized Tools
- Image generation
- PDF manipulation
- Browser automation

**Note**: MCP tools are prefixed with `mcp__` and configured separately. Reference specific MCP tools in the agent's system prompt if needed.

---

## Tool Groupings by Agent Type

### Read-Only Agent
```yaml
tools:
  - Read
  - Grep
  - Glob
```

### Researcher Agent
```yaml
tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
```

### Code Reviewer
```yaml
tools:
  - Read
  - Grep
  - Glob
  - Bash  # For running tests, linting
```

### Builder/Editor
```yaml
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
```

### Full Access (Default)
Omit `tools` field entirely to grant all available tools.

### Orchestrator
```yaml
tools:
  - Read
  - Grep
  - Glob
  - Task
  - TodoWrite
```

### Quick/Minimal
```yaml
tools:
  - Read
  - Grep
  - Glob
model: haiku
```

---

## Tool Selection Principles

1. **Minimum Viable Set**: Only include tools the agent actually needs
2. **Read Before Write**: Agents that write should also read
3. **Match the Role**: Reviewers don't need Write, Builders do
4. **Consider MCP**: If agent needs external capabilities, note them in system prompt
5. **Task for Delegation**: Include Task only if agent should spawn sub-agents
