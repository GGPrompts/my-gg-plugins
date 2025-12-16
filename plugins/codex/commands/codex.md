---
description: Query OpenAI Codex for root cause analysis (read-only, no edits)
---

# Codex Root Cause Investigation

You are Claude Code, and the user wants to consult OpenAI Codex (via codex CLI) for root cause analysis of a bug or technical issue.

## Your Task

1. **Understand the context** from the user's query and our conversation history
2. **Create a focused debug prompt** for codex that includes:
   - Clear description of the issue/bug
   - Relevant code locations (file:line)
   - What we've tried so far
   - Specific question for codex to answer
3. **Execute codex in read-only mode** (no file edits allowed)
4. **Present codex's analysis** back to the user

## Important: Codex Exec Command Format

Use this exact format:

```bash
codex exec -m gpt-5 -c model_reasoning_effort="high" --sandbox read-only "Your debug prompt here"
```

**Flags explanation:**
- `exec` - Non-interactive mode (one-shot query)
- `-m gpt-5` - Use GPT-5 model (can also use `gpt-5-codex`)
- `-c model_reasoning_effort="high"` - Maximum reasoning for complex debugging
  - Options: `low`, `medium`, `high` (default: medium)
  - Use `high` for tricky bugs that need deep analysis
- `--sandbox read-only` - **CRITICAL**: Prevents codex from editing any files
  This ensures codex can only analyze/suggest, not modify code

## Debug Prompt Template

Structure your prompt to codex like this:

```
# Bug Investigation Request

## Issue
[Brief description of the bug/problem]

## Context
- **File(s):** path/to/file.go:lineNumber
- **What's happening:** [observed behavior]
- **Expected behavior:** [what should happen]
- **What we've tried:** [any attempted fixes]

## Code Snippet
[Paste relevant code if helpful, but keep it concise]

## Question
What is the root cause of this issue? Please provide:
1. Root cause analysis
2. Why previous fixes didn't work (if applicable)
3. Suggested fix approach

Keep response focused and actionable.
```

## Execution Steps

1. **Create the prompt** based on conversation context and user query
2. **Execute codex:**
   ```bash
   codex exec -m gpt-5 -c model_reasoning_effort="high" --sandbox read-only "your prompt here"
   ```
   - **IMPORTANT:** Use Bash tool with `timeout: 600000` (10 minutes in milliseconds)
   - **Do NOT use `run_in_background` mode** - let it run synchronously
   - Wait for complete response before processing (saves context tokens)
3. **Parse the output** - codex will show:
   - Session info (model, workdir, etc.) - you can skip this
   - User prompt (echo of what you sent) - skip this
   - **codex's response** - this is what matters!
   - Token count - skip this
4. **Extract just codex's analysis** and present it clearly to the user
5. **Summarize key findings** in your own words
6. **Ask if user wants to implement** the suggested fix

## Output Format

Present codex's response like this:

```
## Codex Analysis:

[Codex's response here - clearly formatted]

---

**Summary:** [Your 2-3 sentence summary of codex's findings]

**Next steps:** [Ask if user wants to implement the fix or investigate further]
```

## Example Usage

**User types:** `/codex investigate the paste bug in update_keyboard.go`

**You do:**
1. Review recent conversation about the paste bug
2. Create focused prompt: "Bug in update_keyboard.go:476 - multi-line pastes rejected. We fixed whitespace validation but Tab navigation still fails. Why?"
3. Execute: `codex exec -m gpt-5 -c model_reasoning_effort="high" --sandbox read-only "..."`
4. Wait synchronously for response (use Bash timeout: 600000)
5. Present codex's findings with your summary

## Important Notes

- **Always use `--sandbox read-only`** - Never let codex edit files via this command
- **Run synchronously, not in background** - Prevents context token waste from polling
- **Use Bash tool timeout** - Set `timeout: 600000` (10 min) for high reasoning effort
- **Keep prompts focused** - Don't dump entire files, just relevant snippets
- **Extract signal from noise** - Skip session info, only show codex's actual analysis
- **Follow up intelligently** - If codex's answer is unclear, you can query again with clarification
- **Implement fixes yourself** - After getting codex's analysis, YOU write the code (not codex)

## Troubleshooting

If codex returns an error:
- Check if codex CLI is installed: `which codex`
- Verify authentication: `codex login`
- Increase Bash timeout if needed: `timeout: 900000` (15 minutes in ms)

If codex's answer is off-target:
- Refine your prompt with more specific context
- Include actual code snippets
- Ask more focused questions

If context usage is high:
- Ensure you're using synchronous execution (not background mode)
- Verify timeout is set on both codex command and Bash tool
- Check that you're not accidentally polling for output

---

**Remember:** This command is for **investigation only**. Codex analyzes, you implement.
