---
description: Generate handoff, clear context, and auto-continue in fresh session
---

Generate a concise handoff summary, then automatically clear context and resume with the handoff in a fresh session.

## Step 1: Generate Handoff Summary

Use this format (skip sections that don't apply):

```
## What we're working on
- [Primary task/topic]

## Current state
- [Where we left off]
- [Any pending questions or decisions]

## Key decisions made
- [Important choices/conclusions]

## Recent changes
- [Files modified, commands run]

## Important context
- [Facts, preferences, constraints, technical details]

## Next steps
- [Immediate next action]
```

## Step 2: Save and Schedule

After generating the summary, execute this bash script. Replace `HANDOFF_CONTENT` with the actual handoff you generated (properly escaped):

```bash
# Save handoff to temp file
HANDOFF_FILE="/tmp/claude-handoff-$$.txt"
cat > "$HANDOFF_FILE" << 'HANDOFF_EOF'
Here's the context from my previous session:

[INSERT YOUR GENERATED HANDOFF SUMMARY HERE]

---
Please acknowledge you've received this context, then let me know what you'd suggest we do next.
HANDOFF_EOF

# Also copy to clipboard as backup
if command -v clip.exe &> /dev/null; then
    cat "$HANDOFF_FILE" | clip.exe
    echo "Backup copied to clipboard (WSL)"
elif command -v xclip &> /dev/null; then
    cat "$HANDOFF_FILE" | xclip -selection clipboard -i &>/dev/null &
    sleep 0.2
    echo "Backup copied to clipboard (xclip)"
elif command -v wl-copy &> /dev/null; then
    cat "$HANDOFF_FILE" | wl-copy
    echo "Backup copied to clipboard (Wayland)"
fi

# Detect tmux session info (capture everything upfront)
if [ -n "$TMUX" ]; then
    TMUX_SOCKET=$(echo "$TMUX" | cut -d',' -f1)
    TARGET_PANE=$(tmux display-message -p '#{session_name}:#{window_index}.#{pane_index}')

    echo "Target: $TARGET_PANE"

    # Schedule: clear context, wait, then send handoff
    (
        sleep 3
        # Send /clear with delay before submit (prevents newline issue)
        tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" "/clear"
        sleep 0.3
        tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" C-m
        sleep 4
        # Use load-buffer for safe content transfer
        tmux -S "$TMUX_SOCKET" load-buffer "$HANDOFF_FILE"
        tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" ""
        sleep 0.3
        tmux -S "$TMUX_SOCKET" paste-buffer -t "$TARGET_PANE"
        sleep 0.3
        tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" C-m
        sleep 1
        rm -f "$HANDOFF_FILE"
    ) &
    disown

    echo ""
    echo "================================================"
    echo "WIPE SCHEDULED"
    echo "================================================"
    echo "  - Context will clear in 3 seconds"
    echo "  - Handoff will arrive 4 seconds after clear"
    echo "  - Backup saved to clipboard"
    echo ""
    echo "Just wait... or press Ctrl+C to abort"
    echo "================================================"
else
    echo ""
    echo "ERROR: Not running in tmux!"
    echo ""
    echo "Handoff saved to: $HANDOFF_FILE"
    echo "Backup copied to clipboard"
    echo ""
    echo "Manual steps:"
    echo "  1. Run /clear"
    echo "  2. Paste from clipboard (Ctrl+V)"
fi
```

## Important

- This only works inside tmux
- The handoff is saved to clipboard as backup in case timing fails
- If something goes wrong, just paste from clipboard in a new session
- Timing: 3s delay before /clear, 4s after for handoff to arrive
