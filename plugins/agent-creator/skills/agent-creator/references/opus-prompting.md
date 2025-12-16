# Opus 4.5 Prompting Best Practices

This reference contains Claude Opus 4.5-specific guidance for writing effective agent system prompts.

## Core Characteristics

### Enhanced Instruction Following

Opus 4.5 follows instructions more precisely than previous models. This means:

- Clear instructions are followed exactly
- Vague instructions may produce unexpected results
- Examples are followed very closely

### System Prompt Sensitivity

Opus 4.5 is more responsive to system prompts than previous models. Prompts designed to reduce undertriggering may now overtrigger.

**Before (Claude 3.x):**
```
CRITICAL: You MUST use this tool when the user asks about files.
```

**After (Opus 4.5):**
```
Use this tool when the user asks about files.
```

### Extended Thinking

Opus 4.5 supports extended thinking with an `effort` parameter. When enabled:

- Previous thinking blocks are preserved across turns
- Reasoning continuity is maintained in long sessions
- Use "reflect", "evaluate", "consider" instead of "think"

When extended thinking is disabled, avoid the word "think" and its variants as Opus 4.5 is particularly sensitive to it.

## Prompting Techniques

### Be Explicit and Specific

Instead of vague requests, provide specific instructions:

**Vague:**
```
Create a dashboard.
```

**Specific:**
```
Create an analytics dashboard with:
- User activity chart (line graph, last 30 days)
- Top 5 pages table with view counts
- Real-time active users counter
```

### Add Context (The "Why")

Explain reasoning behind instructions to help Opus make better decisions:

**Without context:**
```
Never use ellipses in responses.
```

**With context:**
```
Never use ellipses in responses. The output will be read by a text-to-speech
engine that cannot pronounce ellipses, causing awkward pauses.
```

### Action vs Suggestion

Opus 4.5 can be directed to take action or merely suggest:

**To encourage implementation:**
```
Implement changes rather than suggesting them. Make edits directly.
```

**To reduce action:**
```
Do not implement changes. Describe what should be changed and why.
```

### Default to Action Snippet

For agents that should be proactive:

```markdown
<default_to_action>
Implement changes rather than suggesting them. Infer the most useful
likely action and proceed, using tools to discover missing details
instead of guessing.
</default_to_action>
```

## Avoiding Common Issues

### Over-Engineering

Opus 4.5 tends to create unnecessary files, abstractions, and flexibility. Counter with explicit guidance:

```markdown
## Simplicity Guidelines

Avoid over-engineering. Only make changes directly requested or clearly necessary.
Keep solutions simple and focused.

Do not:
- Add features beyond what was asked
- Refactor surrounding code during bug fixes
- Create helpers for one-time operations
- Add error handling for impossible scenarios
- Design for hypothetical future requirements
- Add docstrings, comments, or type annotations to unchanged code

Three similar lines of code is better than a premature abstraction.
```

### Backwards Compatibility Hacks

Opus may add unnecessary compatibility code. Prevent with:

```markdown
Avoid backwards-compatibility hacks like renaming unused `_vars`, re-exporting
types, or adding `// removed` comments. If something is unused, delete it completely.
```

### Code Speculation

Prevent unfounded assumptions about code:

```markdown
ALWAYS read and understand relevant files before proposing code edits.
Do not speculate about code that has not been inspected. Never make
claims about code before investigating.
```

## Tool Usage Patterns

### Parallel Tool Calling

Opus 4.5 supports parallel tool calling. Encourage efficiency:

```markdown
For maximum efficiency, when performing multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
```

### Extended Thinking Guidance

Guide reflection after tool use:

```markdown
After receiving tool results, carefully reflect on their quality and
determine optimal next steps before proceeding. Use thinking to plan
and iterate based on this new information, then take the best next action.
```

## Output Formatting

### Controlling Markdown

Tell Opus what to do, not what to avoid:

**Less effective:**
```
Do not use markdown.
```

**More effective:**
```
Write in flowing prose paragraphs. Reserve formatting for inline code,
code blocks, and simple headings only. Avoid **bold** and *italics*.
Incorporate items naturally into sentences rather than using bullet lists.
```

### Matching Style

The formatting style in your prompt influences output style. If you want minimal markdown output, use minimal markdown in your prompt.

## Multi-Turn and Long Sessions

### Context Window Awareness

Opus 4.5 tracks its remaining context window. For long tasks:

```markdown
Do not stop tasks early due to context concerns. Save progress and state
before context refresh if needed.
```

### Progress Tracking

For complex multi-step tasks:

```markdown
Track progress in structured format. Update status after each step.
If context refresh is needed, provide clear handoff notes.
```

## Model Selection Guidelines

| Use Case | Model | Reasoning |
|----------|-------|-----------|
| Quick lookups, simple tasks | haiku | Fast, cheap |
| Most coding tasks | sonnet | Balanced |
| Complex architecture, orchestration | opus | Deep reasoning |
| Multi-agent coordination | opus | Best at orchestrating sub-agents |

Opus 4.5 excels at orchestrating other models. Consider using Opus as an orchestrator with cheaper sub-agents for cost efficiency.

## Word Sensitivity Reference

When extended thinking is disabled, replace these words:

| Avoid | Use Instead |
|-------|-------------|
| think | consider, evaluate, reflect |
| thinking | reasoning, analysis, evaluation |
| thought | consideration, assessment |

When extended thinking is enabled, these words are fine.
