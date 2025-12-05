#!/bin/bash

# Read JSON input from stdin
input=$(cat)

# Extract data from JSON
model_name=$(echo "$input" | jq -r '.model.display_name // .model.id')
current_dir=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')
output_style=$(echo "$input" | jq -r '.output_style.name // "default"')
transcript_path=$(echo "$input" | jq -r '.transcript_path // ""')

# Color codes (dimmed for status line)
GREEN='\033[2;32m'
BLUE='\033[2;34m'
YELLOW='\033[2;33m'
MAGENTA='\033[2;35m'
CYAN='\033[2;36m'
RED='\033[2;31m'
GRAY='\033[2;37m'
RESET='\033[0m'
BOLD='\033[1m'

# Initialize status parts array
status_parts=()

# 1. Session Status (Working vs Ready)
# Read status from state-tracker hook if available
status_text="✓ Ready"
status_color="$GREEN"

# Calculate session ID the same way as state-tracker.sh
# Priority: 1. CLAUDE_SESSION_ID env var, 2. Working directory hash, 3. PID
if [[ -n "${CLAUDE_SESSION_ID:-}" ]]; then
    SESSION_ID="$CLAUDE_SESSION_ID"
elif [[ -n "$current_dir" ]]; then
    SESSION_ID=$(echo "$current_dir" | md5sum | cut -d' ' -f1 | head -c 12)
else
    SESSION_ID="$$"
fi

STATE_FILE="/tmp/claude-code-state/${SESSION_ID}.json"

# Try to read state from state-tracker file
if [ -f "$STATE_FILE" ]; then
    state_status=$(jq -r '.status // ""' "$STATE_FILE" 2>/dev/null)
    current_tool=$(jq -r '.current_tool // ""' "$STATE_FILE" 2>/dev/null)

    # Map state-tracker status to display text
    case "$state_status" in
        idle)
            status_text="✓ Ready"
            status_color="$GREEN"
            ;;
        awaiting_input)
            status_text="✓ Ready"
            status_color="$GREEN"
            ;;
        processing)
            status_text="⏳ Processing..."
            status_color="$YELLOW"
            ;;
        tool_use)
            if [ -n "$current_tool" ]; then
                status_text="🔧 ${current_tool}..."
            else
                status_text="🔧 Using tool..."
            fi
            status_color="$CYAN"
            ;;
        working)
            status_text="⚙️  Working..."
            status_color="$YELLOW"
            ;;
    esac
else
    # Fallback: Determine status by checking transcript file modification time
    if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
        # Get file modification time in seconds since epoch
        file_mtime=$(stat -c %Y "$transcript_path" 2>/dev/null || stat -f %m "$transcript_path" 2>/dev/null)
        current_time=$(date +%s)

        if [ -n "$file_mtime" ]; then
            time_diff=$((current_time - file_mtime))

            # If transcript modified within last 2 seconds, consider Claude as "working"
            if [ $time_diff -le 2 ]; then
                status_text="⏳ Working..."
                status_color="$YELLOW"
            fi
        fi
    fi
fi

status_parts+=("${status_color}${status_text}${RESET}")

# 3. Current Directory (with ~ substitution)
formatted_dir=$(echo "$current_dir" | sed "s|^$HOME|~|")
status_parts+=("${BLUE}${formatted_dir}${RESET}")

# 4. Git Branch (if in git repository)
if git rev-parse --git-dir >/dev/null 2>&1; then
    # Skip git locks to avoid blocking
    git_branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    git_status=""
    
    # Check for uncommitted changes (quick check)
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        git_status="*"
    elif ! git diff-index --quiet --cached HEAD -- 2>/dev/null; then
        git_status="+"
    fi
    
    status_parts+=("${YELLOW}⎇ ${git_branch}${git_status}${RESET}")
fi

# 5. Python Virtual Environment
if [ -n "$VIRTUAL_ENV" ]; then
    venv_name=$(basename "$VIRTUAL_ENV")
    status_parts+=("${MAGENTA}🐍 ${venv_name}${RESET}")
fi

# 6. Node.js Version (if node is available and package.json exists)
if command -v node >/dev/null 2>&1 && [ -f "package.json" ]; then
    node_version=$(node --version 2>/dev/null | sed 's/^v//')
    status_parts+=("${GREEN}⬢ ${node_version}${RESET}")
fi

# 7. Claude Model
if [ "$model_name" != "null" ] && [ -n "$model_name" ]; then
    # Clean up model name for display (remove "Claude" prefix, keep version numbers)
    display_model=$(echo "$model_name" | sed 's/^Claude //; s/3.5 Sonnet/3.5S/; s/3 Opus/3O/; s/3 Haiku/3H/')
    status_parts+=("${BOLD}${MAGENTA}🤖 ${display_model}${RESET}")
fi

# 8. Output Style (if not default)
if [ "$output_style" != "null" ] && [ "$output_style" != "default" ] && [ -n "$output_style" ]; then
    status_parts+=("${CYAN}📝 ${output_style}${RESET}")
fi

# 9. Exit Code of Last Command (if available from environment)
if [ -n "$CLAUDE_LAST_EXIT_CODE" ] && [ "$CLAUDE_LAST_EXIT_CODE" != "0" ]; then
    status_parts+=("${RED}✗ ${CLAUDE_LAST_EXIT_CODE}${RESET}")
fi

# 10. Load Average (Linux/Unix systems)
if [ -f /proc/loadavg ]; then
    load=$(cut -d' ' -f1 /proc/loadavg)
    # Only show if load is > 1.0
    if command -v bc >/dev/null 2>&1 && [ $(echo "$load > 1.0" | bc -l 2>/dev/null || echo 0) -eq 1 ]; then
        status_parts+=("${YELLOW}⚡ ${load}${RESET}")
    fi
fi

# 11. Docker Context (if docker is available)
if command -v docker >/dev/null 2>&1; then
    # Redirect both stdout and stderr to avoid WSL Docker integration messages
    docker_context=$(docker context show 2>/dev/null)
    if [ $? -eq 0 ] && [ "$docker_context" != "default" ] && [ -n "$docker_context" ]; then
        status_parts+=("${BLUE}🐳 ${docker_context}${RESET}")
    fi
fi

# Join all parts with separator
separator="${GRAY} │ ${RESET}"
status_line=""
for i in "${!status_parts[@]}"; do
    if [ $i -eq 0 ]; then
        status_line="${status_parts[i]}"
    else
        status_line="${status_line}${separator}${status_parts[i]}"
    fi
done

# Print the final status line
printf "%b\n" "$status_line"