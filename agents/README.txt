# Claude Code Sub-Agents

This directory contains user-level sub-agents that are available across all projects.

## Available Agents

- **orchestrator**: AI orchestration and multi-agent coordination
- **docker-expert**: Docker and containerization specialist
- **frontend-dev**: Frontend development (React, Vue, etc.)

## Usage

These agents can be invoked by:
1. Claude Code automatically delegating to them
2. Explicitly mentioning them in your request
3. Using the Task tool with appropriate subagent_type

## Creating New Agents

See the Claude Code documentation for sub-agent format:
https://docs.anthropic.com/en/docs/claude-code/sub-agents
