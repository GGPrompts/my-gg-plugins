---
description: Query Google Gemini for root cause analysis (read-only, no edits)
---

# Gemini Root Cause Investigation

You are Claude Code, and the user wants to consult Google Gemini (via gemini CLI) for root cause analysis of a bug or technical issue.

## Your Task

1. **Understand the context** from the user's query and our conversation history
2. **Create a focused debug prompt** for Gemini that includes:
   - Clear description of the issue/bug
   - Relevant code locations (file:line)
   - What we've tried so far
   - Specific question for Gemini to answer
3. **Execute Gemini in non-interactive mode** (no file edits allowed)
4. **Present Gemini's analysis** back to the user

## Important: Gemini CLI Command Format

Use this exact format:

```bash
gemini -p "Your debug prompt here"
```

**Flags explanation:**
- `-p` or `--prompt` - Non-interactive mode (one-shot query)
- **Important:** Non-interactive mode automatically prevents file writes
  Gemini cannot use WriteFile tool in this mode, ensuring read-only operation

## Debug Prompt Template

Structure your prompt to Gemini like this:

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
2. **Execute Gemini:**
   ```bash
   gemini -p "your prompt here"
   ```
3. **Parse the output** - Gemini will show:
   - Model info (if any) - you can skip this
   - **Gemini's response** - this is what matters!
4. **Extract just Gemini's analysis** and present it clearly to the user
5. **Summarize key findings** in your own words
6. **Ask if user wants to implement** the suggested fix

## Output Format

Present Gemini's response like this:

```
💎 **Gemini Analysis:**

[Gemini's response here - clearly formatted]

---

**Summary:** [Your 2-3 sentence summary of Gemini's findings]

**Next steps:** [Ask if user wants to implement the fix or investigate further]
```

## Example Usage

**User types:** `/gemini investigate the paste bug in update_keyboard.go`

**You do:**
1. Review recent conversation about the paste bug
2. Create focused prompt: "Bug in update_keyboard.go:476 - multi-line pastes rejected. We fixed whitespace validation but Tab navigation still fails. Why?"
3. Execute: `gemini -p "..."`
4. Present Gemini's findings with your summary

## Important Notes

- **Non-interactive mode is inherently read-only** - Gemini cannot modify files via `-p` flag
- **Keep prompts focused** - Don't dump entire files, just relevant snippets
- **Extract signal from noise** - Only show Gemini's actual analysis
- **Follow up intelligently** - If Gemini's answer is unclear, you can query again with clarification
- **Implement fixes yourself** - After getting Gemini's analysis, YOU write the code (not Gemini)
- **One-shot only** - No conversation history between queries (each query is independent)

## Troubleshooting

If Gemini returns an error:
- Check if Gemini CLI is installed: `which gemini`
- Verify authentication: `gemini login` or check API key
- Try simpler prompt if timeout occurs

If Gemini's answer is off-target:
- Refine your prompt with more specific context
- Include actual code snippets
- Ask more focused questions

## Comparison with Codex

**Gemini strengths:**
- Different perspective/approach to problems
- Strong with algorithmic analysis
- Good at explaining complex concepts
- Free tier available

**Use Gemini when:**
- You want a second opinion
- Codex's answer wasn't satisfactory
- You prefer Gemini's reasoning style
- Cost is a concern (free tier)

---

**Remember:** This command is for **investigation only**. Gemini analyzes, you implement.
