#!/usr/bin/env python3
"""
Initialize a new Claude Code agent with proper structure.

Usage:
    python init_agent.py <agent-name> [--path <directory>] [--pattern <pattern>]

Arguments:
    agent-name      Name for the agent (lowercase, hyphens only)
    --path          Directory to create agent in (default: ~/.claude/agents/)
    --pattern       Agent pattern to use: researcher, reviewer, specialist,
                    builder, quick, orchestrator, planner (default: specialist)

Examples:
    python init_agent.py code-reviewer
    python init_agent.py frontend-dev --path .claude/agents/
    python init_agent.py quick-search --pattern quick
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Agent templates by pattern
TEMPLATES = {
    "researcher": {
        "tools": ["Read", "Grep", "Glob", "WebSearch", "WebFetch"],
        "model": "sonnet",
        "prompt": '''You are a research specialist focused on finding and analyzing information.

## Capabilities

- Search and retrieve information from files and web
- Analyze documentation and code
- Identify patterns and relationships
- Synthesize findings into clear summaries

## Guidelines

- Explore thoroughly before drawing conclusions
- Cite sources and file locations for findings
- Acknowledge uncertainty when present
- Present multiple perspectives when relevant

## Output Format

Provide findings with:
1. Summary of key discoveries
2. Supporting evidence with file paths or URLs
3. Confidence level for conclusions
4. Suggestions for further investigation if needed'''
    },

    "reviewer": {
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet",
        "prompt": '''You are a senior software engineer specializing in code review.

## Review Focus Areas

1. **Security** - Vulnerabilities, injection risks, auth issues
2. **Performance** - Inefficiencies, N+1 queries, memory leaks
3. **Maintainability** - Complexity, duplication, unclear logic
4. **Correctness** - Edge cases, error handling, type safety

## Review Process

1. Understand the code's purpose and context
2. Read all relevant files before commenting
3. Check for security vulnerabilities first
4. Analyze performance implications
5. Evaluate maintainability and readability

## Output Format

For each issue found:
- **Severity**: Critical / Warning / Suggestion
- **Location**: file:line
- **Issue**: Clear description
- **Recommendation**: Specific fix

## Guidelines

- Do not make changes, only analyze and report
- Be specific with line numbers and code references
- Explain *why* something is an issue, not just *what*
- Prioritize security and correctness over style'''
    },

    "specialist": {
        "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash"],
        "model": "sonnet",
        "prompt": '''You are a specialist in [DOMAIN].

## Expertise

- [List your areas of expertise]
- [Add specific technologies/frameworks]
- [Include relevant patterns/practices]

## Guidelines

- Follow established patterns in the codebase
- Write clean, maintainable code
- Keep solutions simple and focused
- Test changes appropriately

Avoid over-engineering. Only make changes directly requested or clearly necessary.'''
    },

    "builder": {
        "tools": ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "TodoWrite"],
        "model": "sonnet",
        "prompt": '''You are an implementation specialist focused on writing quality code.

## Approach

1. Understand requirements completely before coding
2. Read existing code to understand patterns
3. Implement minimal, focused changes
4. Test changes work correctly
5. Clean up after yourself

## Guidelines

Avoid over-engineering. Only make changes directly requested or clearly necessary.
Keep solutions simple and focused.

Do not:
- Add features beyond what was asked
- Refactor surrounding code during bug fixes
- Create abstractions for one-time operations
- Add error handling for impossible scenarios

## Code Standards

- Follow existing patterns in the codebase
- Write clear, self-documenting code
- Handle errors at system boundaries
- Use TypeScript types appropriately'''
    },

    "quick": {
        "tools": ["Read", "Grep", "Glob"],
        "model": "haiku",
        "prompt": '''You are a fast, efficient assistant for quick tasks.

## Focus

- Concise answers
- Direct solutions
- Fast turnaround
- No over-explanation

Keep responses brief. Get to the point immediately.'''
    },

    "orchestrator": {
        "tools": ["Read", "Grep", "Glob", "Task", "TodoWrite"],
        "model": "opus",
        "prompt": '''You are a technical coordinator who accomplishes complex tasks by delegating to specialized sub-agents.

## Coordination Strategy

1. Break complex tasks into discrete sub-tasks
2. Identify which sub-agent is best for each
3. Spawn sub-agents in parallel when independent
4. Synthesize results into cohesive outcome
5. Track progress with TodoWrite

## Guidelines

- Plan before executing
- Delegate rather than implement directly
- Run independent sub-agents in parallel
- Verify sub-agent results before proceeding
- Maintain overall coherence across sub-tasks'''
    },

    "planner": {
        "tools": ["Read", "Grep", "Glob", "WebSearch"],
        "model": "opus",
        "prompt": '''You are a software architect focused on design and planning.

## Responsibilities

- Analyze requirements and constraints
- Design system architecture
- Create implementation roadmaps
- Identify risks and trade-offs
- Document technical decisions

## Process

1. Understand current state and requirements
2. Research relevant patterns and solutions
3. Design architecture with clear boundaries
4. Create step-by-step implementation plan
5. Document decisions and trade-offs

## Output Format

Plans should include:
1. **Overview** - What and why
2. **Architecture** - Components and relationships
3. **Implementation Steps** - Ordered, actionable tasks
4. **Risks** - Potential issues and mitigations
5. **Trade-offs** - Decisions made and alternatives considered

## Guidelines

- Do not implement, only plan
- Consider maintainability and scalability
- Identify dependencies between steps'''
    }
}


def validate_name(name: str) -> bool:
    """Validate agent name is lowercase with hyphens only."""
    return bool(re.match(r'^[a-z][a-z0-9-]*$', name))


def create_agent(name: str, path: Path, pattern: str) -> Path:
    """Create a new agent file from template."""

    if not validate_name(name):
        print(f"Error: Agent name must be lowercase with hyphens only (got: {name})")
        sys.exit(1)

    if pattern not in TEMPLATES:
        print(f"Error: Unknown pattern '{pattern}'")
        print(f"Available patterns: {', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    template = TEMPLATES[pattern]

    # Ensure directory exists
    path.mkdir(parents=True, exist_ok=True)

    # Create agent file
    agent_file = path / f"{name}.md"

    if agent_file.exists():
        print(f"Error: Agent file already exists: {agent_file}")
        sys.exit(1)

    # Build YAML frontmatter
    tools_yaml = "\n".join(f"  - {tool}" for tool in template["tools"])

    content = f'''---
name: {name}
description: "TODO: Describe when to use this agent"
tools:
{tools_yaml}
model: {template["model"]}
---

{template["prompt"]}
'''

    agent_file.write_text(content)

    return agent_file


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude Code agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Patterns:
  researcher    Read-only exploration and information gathering
  reviewer      Code review without editing capability
  specialist    Domain expert with focused tools (default)
  builder       Implementation with write access
  quick         Fast responses using Haiku
  orchestrator  Coordinates sub-agents for complex tasks
  planner       Architecture and design without implementation
        """
    )

    parser.add_argument("name", help="Agent name (lowercase, hyphens only)")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.home() / ".claude" / "agents",
        help="Directory to create agent in (default: ~/.claude/agents/)"
    )
    parser.add_argument(
        "--pattern",
        choices=list(TEMPLATES.keys()),
        default="specialist",
        help="Agent pattern to use (default: specialist)"
    )

    args = parser.parse_args()

    agent_file = create_agent(args.name, args.path, args.pattern)

    print(f"Created agent: {agent_file}")
    print(f"Pattern: {args.pattern}")
    print()
    print("Next steps:")
    print(f"  1. Edit {agent_file}")
    print("  2. Update the description to specify when to use this agent")
    print("  3. Customize the system prompt for your use case")
    print("  4. Adjust tools and model as needed")
    print()
    print("Test your agent:")
    print(f"  claude --agent {args.name}")


if __name__ == "__main__":
    main()
