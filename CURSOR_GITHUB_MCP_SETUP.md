# GitHub MCP in Cursor (this project)

This repository includes a **template** for GitHub’s official remote MCP server. After you add your token, Cursor will show **github** under **Settings → Tools & Integrations → MCP**.

## Prerequisites

1. **Cursor v0.48.0 or later** (needed for GitHub’s Streamable HTTP endpoint).  
   - **Cursor → About** (or check for updates).

2. A **GitHub Personal Access Token** (recommended: **fine-grained**, limited to this repository for least privilege).  
   - Create: [Fine-grained token](https://github.com/settings/personal-access-tokens/new)  
   - **Repository access**: only this repo.  
   - **Permissions**: start with **Contents: Read**; add **Issues** / **Pull requests** if you want the agent to create or update them via GitHub.

## One-time setup (exact steps)

1. **Copy the template to the real config file** (the real file is gitignored so your token is not committed):

   ```bash
   cd /path/to/Internal_Docs
   mkdir -p .cursor
   cp .cursor/mcp.json.example .cursor/mcp.json
   ```

2. **Edit `.cursor/mcp.json`** and replace `REPLACE_WITH_YOUR_GITHUB_PAT` with your actual token (keep the word `Bearer` in the header value: `Bearer ghp_...` is the full value after `Bearer ` — the example file already includes the `Bearer ` prefix in the string; your token replaces only the placeholder).

3. **Validate JSON**: the file must be valid JSON (no comments, no trailing commas). You can use:

   ```bash
   python3 -m json.tool .cursor/mcp.json
   ```

4. **Fully restart Cursor** (quit the app, open it again).

5. **Verify in UI**  
   - Open **Cursor → Settings → Tools & Integrations → MCP** (or **Cursor Settings → MCP** depending on version).  
   - You should see a server named **github** (or whatever key you use under `mcpServers`) with a **healthy** / green status.  
   - In chat or Agent, check **available tools** for GitHub-related tools.

6. **Smoke test** in Cursor chat:

   ```text
   List my GitHub repositories (use MCP tools if available).
   ```

## File locations

| File | Purpose |
|------|--------|
| `.cursor/mcp.json.example` | Safe template in git — no secrets. |
| `.cursor/mcp.json` | **Your** config with PAT — **not** committed (see `.gitignore`). |

## Official reference

- GitHub MCP server repo and Cursor install guide: [github/github-mcp-server — install Cursor](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-cursor.md)  
- The npm package `@modelcontextprotocol/server-github` is **deprecated**; this setup uses GitHub’s **remote** server at `https://api.githubcopilot.com/mcp/`.

## Troubleshooting

| Issue | What to try |
|--------|-------------|
| Server red / not loading | Confirm Cursor version ≥ 0.48; fix JSON; restart Cursor. |
| 401 / auth errors | Regenerate PAT; ensure `Authorization` is exactly `Bearer <token>`. |
| Tools not listed | Wait a few seconds after restart; open MCP panel and refresh if present. |
| Corporate proxy / firewall | Remote MCP may be blocked; use GitHub’s [Docker local option](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-cursor.md) instead. |

## Optional: Docker-based GitHub MCP (no hosted endpoint)

If the remote URL does not work in your environment, follow the **Local Server Setup** section in the same [install-cursor.md](https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-cursor.md) and put that `mcpServers.github` block in `.cursor/mcp.json` instead, with `GITHUB_PERSONAL_ACCESS_TOKEN` in `env`.
