---
description: Generate a handoff summary and copy to clipboard for new session
---

Generate a concise handoff summary of our conversation that I can use to continue in a new Claude Code session.

Use this exact format:

```
## What we're working on
- [Primary task/topic]
- [Secondary items if applicable]

## Current state
- [Where we left off]
- [Any pending questions or decisions]

## Key decisions made
- [Important choices/conclusions from this conversation]

## Recent changes
- [Files modified, if any]
- [Commands run or actions taken]

## Important context
- [Facts, preferences, or constraints I mentioned]
- [Technical details that matter for continuing]

## Next steps
- [Immediate next action]
- [Follow-up tasks]
```

Requirements:
- Be concise but complete - capture what's needed to continue without re-explaining
- Focus on actionable state, not conversation history
- Include file paths and technical specifics where relevant
- Skip sections that don't apply (e.g., "Recent changes" if no files were modified)

After generating the summary, copy it to clipboard using this bash command:

```bash
# Detect environment and copy accordingly
if command -v clip.exe &> /dev/null; then
    # WSL with Windows clipboard
    cat <<'HANDOFF_EOF' | clip.exe
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
    echo "✅ Handoff copied to clipboard (WSL/Windows)"
elif command -v xclip &> /dev/null; then
    # Linux with xclip
    cat <<'HANDOFF_EOF' | xclip -selection clipboard -i &>/dev/null &
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
    sleep 0.2
    echo "✅ Handoff copied to clipboard (xclip)"
elif command -v xsel &> /dev/null; then
    # Linux with xsel
    cat <<'HANDOFF_EOF' | xsel --clipboard --input
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
    echo "✅ Handoff copied to clipboard (xsel)"
elif command -v wl-copy &> /dev/null; then
    # Wayland
    cat <<'HANDOFF_EOF' | wl-copy
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
    echo "✅ Handoff copied to clipboard (Wayland)"
elif command -v termux-clipboard-set &> /dev/null; then
    # Termux
    cat <<'HANDOFF_EOF' | termux-clipboard-set
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
    echo "✅ Handoff copied to clipboard (Termux)"
else
    echo "⚠️ No clipboard tool found. Install xclip, xsel, or wl-clipboard"
    echo ""
    echo "Manual copy - here's the handoff:"
    echo "================================"
    cat <<'HANDOFF_EOF'
[INSERT THE GENERATED HANDOFF SUMMARY HERE]
HANDOFF_EOF
fi
```

Then display:

```
✅ Handoff summary copied to clipboard!

To continue in a new session:
1. Start new Claude Code session: claude
2. Paste the handoff (Ctrl+V or Ctrl+Shift+V)
3. Add your next question/task after the handoff

💡 The handoff provides context so Claude understands where you left off.
```
