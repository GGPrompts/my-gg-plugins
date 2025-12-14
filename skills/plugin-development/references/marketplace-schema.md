# Marketplace Schema (marketplace.json)

When publishing a plugin repository as a marketplace source (for `github:` or `local:` loading), you need a `marketplace.json` file in `.claude-plugin/`.

## Why marketplace.json is Required

- **Single plugins** only need `plugin.json` - loaded directly
- **Marketplace sources** (repos with multiple installable plugins) need `marketplace.json` to list available plugins
- Without it, loading from github/local source will fail with "marketplace file not found"

## File Location

```
my-plugin-repo/
├── .claude-plugin/
│   ├── plugin.json        # Plugin manifest (always required)
│   └── marketplace.json   # Marketplace index (required for github/local sources)
├── skills/
├── commands/
└── ...
```

## Complete Schema

```json
{
  "name": "my-marketplace",
  "description": "Description of this plugin collection",
  "owner": {
    "name": "Author Name",
    "url": "https://github.com/author"
  },
  "version": "1.0.0",
  "plugins": [
    {
      "name": "plugin-name",
      "description": "What this plugin does",
      "source": "./path/to/plugin",
      "category": "category-key",
      "tags": ["tag1", "tag2"]
    }
  ],
  "categories": {
    "category-key": "Category description"
  }
}
```

## Required Fields

| Field       | Type   | Description                              |
|-------------|--------|------------------------------------------|
| `name`      | string | Unique marketplace identifier            |
| `plugins`   | array  | List of available plugins                |

## Plugin Entry Fields

| Field         | Type   | Required | Description                                    |
|---------------|--------|----------|------------------------------------------------|
| `name`        | string | Yes      | Plugin identifier (kebab-case)                 |
| `description` | string | Yes      | Brief description for discovery                |
| `source`      | string | Yes      | Path to plugin, **must start with `./`**       |
| `category`    | string | No       | Category key from `categories` object          |
| `tags`        | array  | No       | Keywords for search/filtering                  |

## Critical Rules

1. **All `source` paths must start with `./`** - Relative paths only
   - Correct: `"./skills/my-skill"`, `"./agents/my-agent.md"`, `"./"`
   - Wrong: `"."`, `"skills/my-skill"`, `/absolute/path`

2. **Source can point to:**
   - A skill directory: `"./skills/my-skill"` (must contain SKILL.md)
   - A single file: `"./agents/my-agent.md"`
   - The full plugin: `"./"` (installs everything)

3. **Categories are optional** but improve organization for large marketplaces

## Examples

### Minimal Marketplace

```json
{
  "name": "my-tools",
  "plugins": [
    {
      "name": "my-skill",
      "description": "Does something useful",
      "source": "./skills/my-skill"
    }
  ]
}
```

### Full Plugin as Marketplace Entry

To let users install the entire plugin from a marketplace:

```json
{
  "plugins": [
    {
      "name": "full-plugin",
      "description": "Complete plugin with MCP server, hooks, skills, and commands",
      "source": "./"
    }
  ]
}
```

### Multi-Plugin Marketplace

```json
{
  "name": "developer-toolkit",
  "description": "Curated developer tools",
  "owner": {
    "name": "DevTeam",
    "url": "https://github.com/devteam"
  },
  "version": "1.0.0",
  "plugins": [
    {
      "name": "code-review",
      "description": "Automated code review patterns",
      "source": "./skills/code-review",
      "category": "quality",
      "tags": ["review", "linting"]
    },
    {
      "name": "test-generator",
      "description": "Generate unit tests automatically",
      "source": "./skills/test-generator",
      "category": "testing",
      "tags": ["tests", "automation"]
    },
    {
      "name": "toolkit-full",
      "description": "Everything in this toolkit",
      "source": "./",
      "category": "bundle",
      "tags": ["complete", "all"]
    }
  ],
  "categories": {
    "quality": "Code quality and review tools",
    "testing": "Test automation and generation",
    "bundle": "Complete plugin bundles"
  }
}
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "marketplace file not found" | Missing marketplace.json | Create `.claude-plugin/marketplace.json` |
| "Invalid schema: plugins.N.source: Invalid input: must start with ./" | Source path doesn't start with `./` | Change `"."` to `"./"` |
| "Plugin not found" | Source path doesn't exist | Verify path exists and is correct |
