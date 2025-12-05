# Project Plan Validation & Enrichment System

You are helping the user validate and improve a project plan through multiple analysis perspectives. Instead of a simple approval prompt, you'll offer rich validation options.

## Your Task

This is an **iterative plan refinement system**. You will:

1. Read/understand the current plan
2. Offer validation options via `AskUserQuestion`
3. Execute the chosen analysis
4. Present findings and ask what to do next
5. Loop until user approves and proceeds to implementation

---

## Step 1: Identify the Plan

Ask the user which plan to validate:

**Options**:
- Current project's `PLAN.md` file
- Specific file path they provide
- Plan content they'll paste

Read the plan and summarize it briefly (2-3 sentences) so the user confirms you're validating the right thing.

---

## Step 2: Offer Validation Options

Use the `AskUserQuestion` tool with these options:

**Question**: "How should we validate and improve this plan?"
**Header**: "Validation"
**Multi-select**: false

**Options**:

1. **"GPT-5 Deep Reasoning"**
   - **Description**: "Use `codex exec` with o1/o3 model for deep technical analysis and edge case identification"
   - **When to suggest**: Complex algorithms, novel architectures, safety-critical features
   - **Output**: Detailed reasoning document with concerns and suggestions

2. **"Multi-Agent Review"**
   - **Description**: "3 Claude subagents (Security Auditor, UX Specialist, Architecture Analyst) each provide feedback"
   - **When to suggest**: User-facing features, security-sensitive changes, large refactors
   - **Output**: 3 separate review sections appended to plan or new file

3. **"Research Latest Tech"**
   - **Description**: "Web search for new frameworks/tools + Context7 MCP for code examples and library recommendations"
   - **When to suggest**: Choosing tech stack, evaluating new libraries, modernizing approach
   - **Output**: Research findings with links, library suggestions, code snippet references

4. **"Check Competition"**
   - **Description**: "Web search to analyze similar projects, see what competitors do, identify differentiators"
   - **When to suggest**: New products, feature planning, market positioning
   - **Output**: Competitive analysis with key insights and differentiation opportunities

5. **"Tech Stack Validation"**
   - **Description**: "Use Context7 MCP to verify libraries are current, check for better alternatives, validate compatibility"
   - **When to suggest**: Before committing to dependencies, during tech stack decisions
   - **Output**: Library audit with versions, alternatives, compatibility notes

6. **"Approve & Proceed"**
   - **Description**: "Plan looks good, move to implementation phase"
   - **When to suggest**: After sufficient validation, user is confident
   - **Output**: Mark plan as approved, optionally start implementation

---

## Step 3: Execute Chosen Validation

### Option 1: GPT-5 Deep Reasoning

**IMPORTANT**: Only available on PC (not Termux). Check environment first.

```bash
# Check if codex is available
which codex >/dev/null 2>&1 || echo "⚠️ codex not available on this system"

# If available, execute:
codex exec -m o1-preview "You are a technical architect reviewing this project plan.
Provide deep reasoning about:
- Technical feasibility and complexity
- Potential edge cases or failure modes
- Scalability and performance considerations
- Security implications
- Alternative approaches to consider

Plan to review:
$(cat PLAN.md)

Provide detailed, structured feedback."
```

**Save output** to `docs/validation-gpt5-$(date +%Y%m%d).md`

**Present to user**: Summarize key concerns (3-5 bullet points), then loop back to Step 2.

---

### Option 2: Multi-Agent Review

Launch **3 Claude subagents in parallel** using the `Task` tool:

**Agent 1: Security Auditor**
```
You are a security expert reviewing a project plan.

Analyze this plan for:
- Security vulnerabilities or risks
- Authentication/authorization concerns
- Data privacy and compliance issues
- Input validation and sanitization needs
- Secure coding practices to follow

Plan:
[PLAN CONTENT]

Provide 2-3 paragraphs with specific, actionable security recommendations.
Format your response as markdown with:
- ## Security Review
- Key concerns (bullet list)
- Recommendations (numbered list)
```

**Agent 2: UX Specialist**
```
You are a UX designer reviewing a project plan.

Analyze this plan for:
- User experience and usability concerns
- Accessibility considerations
- User flow and friction points
- Error handling and user feedback
- Mobile/responsive design needs

Plan:
[PLAN CONTENT]

Provide 2-3 paragraphs with specific UX improvements.
Format your response as markdown with:
- ## UX Review
- User concerns (bullet list)
- Improvements (numbered list)
```

**Agent 3: Architecture Analyst**
```
You are a software architect reviewing a project plan.

Analyze this plan for:
- Architecture and design patterns
- Scalability and performance
- Code organization and modularity
- Dependencies and technical debt
- Maintainability and testability

Plan:
[PLAN CONTENT]

Provide 2-3 paragraphs with architectural recommendations.
Format your response as markdown with:
- ## Architecture Review
- Design concerns (bullet list)
- Recommendations (numbered list)
```

**After all agents complete**:
- Combine their reviews into a single document
- Save to `docs/validation-multi-agent-$(date +%Y%m%d).md`
- Summarize key themes across all 3 reviews (what did they agree on?)
- Loop back to Step 2

---

### Option 3: Research Latest Tech

**Part A: Web Search**

Use the `WebSearch` tool to find:
1. "latest [primary technology] best practices 2025"
2. "[key library] alternatives comparison"
3. "modern [tech stack] architecture patterns"

**Part B: Context7 MCP (if available)**

Check for Context7 MCP server:
```bash
# Check if MCP server is configured
# If available, query for:
# - Latest library versions
# - Popular code patterns
# - Example implementations
```

**Format findings**:
```markdown
# Research Findings: Latest Tech

## Web Search Results

### Best Practices (2025)
- Finding 1 [source link]
- Finding 2 [source link]

### Library Alternatives
| Library | Pros | Cons | Popularity |
|---------|------|------|------------|
| [name]  | ...  | ...  | GitHub stars |

### Architecture Patterns
- Pattern 1: [description]
- Pattern 2: [description]

## Context7 Recommendations (if available)

### Recommended Libraries
- [library name] v[version] - [why it's recommended]

### Code Examples
- [relevant snippet or pattern]

## Recommendations for Plan

Based on research:
1. Consider switching from [X] to [Y] because...
2. Adopt [pattern] for [use case]...
3. Update dependencies to...
```

**Save** to `docs/validation-research-$(date +%Y%m%d).md`

**Loop back** to Step 2

---

### Option 4: Check Competition

Use `WebSearch` tool to research:
1. "[project type] similar projects"
2. "[key feature] implementation examples"
3. "[competitor name] architecture"

**Format findings**:
```markdown
# Competitive Analysis

## Similar Projects

### Project 1: [Name]
- **What they do**: [description]
- **Key features**: [list]
- **Tech stack**: [technologies]
- **Strengths**: [what they do well]
- **Weaknesses**: [gaps we can exploit]
- **Link**: [URL]

### Project 2: [Name]
[same structure]

## Key Insights

### What competitors do well:
- [pattern 1]
- [pattern 2]

### Gaps in the market:
- [opportunity 1]
- [opportunity 2]

### Differentiation opportunities:
1. [how our plan differs/improves]
2. [unique value proposition]

## Recommendations for Plan

Based on competitive analysis:
- Add [feature] to differentiate
- Avoid [approach] that competitors struggle with
- Focus on [gap] as key differentiator
```

**Save** to `docs/validation-competition-$(date +%Y%m%d).md`

**Loop back** to Step 2

---

### Option 5: Tech Stack Validation

**If Context7 MCP available**: Use it to verify libraries

**Otherwise**: Use `WebSearch` to check:
1. "[library] latest version 2025"
2. "[library] security vulnerabilities"
3. "[library] vs [alternative] comparison"

**For each library in the plan**:
```markdown
# Tech Stack Validation

## Current Dependencies

### [Library 1]
- **Current version in plan**: v[X.Y.Z]
- **Latest version**: v[A.B.C]
- **Status**: ✅ Up to date / ⚠️ Outdated / 🚨 Deprecated
- **Security**: [any known vulnerabilities]
- **Alternatives**: [better options if any]
- **Recommendation**: Keep / Update / Replace with [X]

### [Library 2]
[same structure]

## Compatibility Matrix

| Library | Version | Compatible With | Notes |
|---------|---------|-----------------|-------|
| [name]  | [ver]   | [others]        | [any issues] |

## Recommendations

### Must Update:
- [library] v[old] → v[new] (security fix)

### Consider Replacing:
- [library] → [alternative] (better performance/maintenance)

### Architecture Suggestions:
- Use [pattern] to reduce dependency coupling
```

**Save** to `docs/validation-techstack-$(date +%Y%m%d).md`

**Loop back** to Step 2

---

### Option 6: Approve & Proceed

1. **Summarize validation** done so far:
   ```
   ✅ Plan validated via:
   - Multi-agent review (Security, UX, Architecture)
   - Tech stack validation (all libraries current)

   📁 Validation documents:
   - docs/validation-multi-agent-20251030.md
   - docs/validation-techstack-20251030.md
   ```

2. **Ask if user wants to update PLAN.md** with findings

3. **Ask what to do next**:
   - "Start implementation" → Proceed with building
   - "Update documentation first" → Revise plan based on feedback
   - "More validation" → Loop back to Step 2

---

## Step 4: Iterative Refinement

After each validation (Options 1-5):

**Show summary** of findings (3-5 key points)

**Then loop back** with `AskUserQuestion`:

**Question**: "What should we do next with this plan?"
**Header**: "Next step"
**Multi-select**: false

**Options**:
1. **"More validation"** → Back to Step 2 (different validation type)
2. **"Revise plan"** → User edits PLAN.md based on feedback
3. **"Approve & proceed"** → Move to implementation
4. **"Save & exit"** → Save all validation docs, exit without implementing

---

## Best Practices

### When to Suggest Each Option

**GPT-5 Deep Reasoning**:
- Novel algorithms or data structures
- Safety-critical features (auth, payments)
- Performance-sensitive code
- Complex state management

**Multi-Agent Review**:
- User-facing features (UX important)
- Security-sensitive (auth, data handling)
- Large refactors (architecture important)
- Public APIs (all perspectives needed)

**Research Latest Tech**:
- Choosing between frameworks
- Starting greenfield project
- Modernizing legacy stack
- Unsure about best practices

**Check Competition**:
- Building new product/feature
- Entering competitive market
- Need differentiation ideas
- Validating product-market fit

**Tech Stack Validation**:
- Before major dependency decisions
- Annual dependency audits
- After security advisories
- Considering library upgrades

### Combining Validations

Suggest combinations for thorough validation:
1. **"New project"**: Research Latest Tech → Tech Stack Validation → Multi-Agent Review
2. **"Security feature"**: Multi-Agent Review (focus security) → GPT-5 Deep Reasoning → Approve
3. **"Product launch"**: Check Competition → Research Latest Tech → Multi-Agent Review → Approve

---

## Output Format

After each validation, present findings like this:

```
🔍 [Validation Type] Complete

📊 Key Findings:
1. [Most important insight]
2. [Second most important]
3. [Third most important]

⚠️ Critical Concerns:
- [Any blockers or major issues]

💡 Top Recommendations:
1. [Highest priority suggestion]
2. [Second priority]

📄 Full report saved to: docs/validation-[type]-[date].md

[Then immediately show AskUserQuestion for "What next?"]
```

---

## Notes

- **Save all validation docs** to `docs/validation-*` for future reference
- **Track validation history** in plan comments if user wants
- **Don't require all validations** - user decides what's needed
- **PC vs Termux**: Some tools (codex, Context7 MCP) may only work on PC
- **Parallel execution**: Multi-agent review should run agents in parallel for speed
- **Cost awareness**: Mention if external API calls will incur costs

---

## Example Session Flow

```
User: /validate-plan

Claude: I'll help validate your project plan. Which plan should we review?
[reads PLAN.md]

Plan Summary: Adding a fuzzy search feature to TFE using fzf...

🔍 How should we validate and improve this plan?
[AskUserQuestion with 6 options]

User selects: "Multi-Agent Review"

Claude: Launching 3 specialized agents in parallel...
[3 agents analyze the plan]

🔍 Multi-Agent Review Complete

📊 Key Themes:
1. All agents agree: fzf integration is solid approach
2. Security: No major concerns (read-only operation)
3. UX: Suggest adding preview pane in fzf
4. Architecture: Consider caching search results

⚠️ Critical Concerns: None

💡 Top Recommendations:
1. Add fzf preview with file contents (UX Specialist)
2. Cache fd results for faster repeat searches (Architecture Analyst)

📄 Full report: docs/validation-multi-agent-20251030.md

🔍 What should we do next with this plan?
[AskUserQuestion: More validation / Revise plan / Approve / Exit]

User selects: "Revise plan"

Claude: Great! I'll update PLAN.md to include:
- fzf preview pane configuration
- Search result caching strategy

Updated plan saved. Ready to validate again?

User: /validate-plan

Claude: How should we validate this revised plan?
[Shows options again]

User selects: "Approve & Proceed"

Claude: ✅ Plan approved!

Validation summary:
- Multi-agent review (all concerns addressed)

Ready to implement? I can start with the fuzzy search feature now.
```

---

Execute this validation system now. Start by asking which plan to validate.
