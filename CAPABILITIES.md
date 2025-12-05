# My Claude Code Capabilities

Last updated: 2025-12-03

## MCP Servers (Always Active)
- browser - Chrome automation (screenshots, click, fill, console logs)
- shadcn - UI component registry (search, examples, CLI commands)

## Docker MCP Gateway
`docker-mcp` provides access to 200+ on-demand servers.

**Check session-enabled servers:** `docker.exe mcp server list`
**Search catalog:** `mcp-find query="database" limit=10`

Categories: databases, git/cloud, web/browser, apis, ai

Add with `mcp-add`, configure with `mcp-config-set`. Session-scoped.

## Skills
- ai-multimodal - Gemini API for audio/video/image processing
- bubbletea - Go TUI development
- canvas-design - Visual art and poster creation
- claude-code - Claude Code usage guidance
- debugging - Debugging strategies
- docker-mcp - Docker MCP Toolkit guide
- docs-seeker - Documentation search via llms.txt
- problem-solving - Structured problem solving
- skill-creator - Create new skills
- ui-styling - shadcn/ui + Tailwind styling
- web-frameworks - Next.js, Turborepo, RemixIcon
- xterm-js - Terminal UI implementations

## Custom Agents
- mcp-manager - MCP server discovery/setup (Sonnet)

## Custom Slash Commands
- /codex - Query OpenAI Codex
- /gemini - Query Google Gemini
- /handoff - Generate handoff summary for new session
- /pmux - Prompt engineer with tmux send-keys
- /pmux2 - Prompt engineer v2
- /prompt-engineer - Interactive prompt refinement

## Built-in Subagent Types
- Explore (Haiku) - Fast codebase exploration
- Plan (Sonnet) - Implementation planning
- general-purpose - Multi-step autonomous tasks
