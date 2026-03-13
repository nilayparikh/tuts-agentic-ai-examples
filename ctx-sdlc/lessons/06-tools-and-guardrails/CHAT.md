# Lesson 06 — VS Code Copilot Chat Guide

## Steps

### 1. Set up the workspace

```bash
python util.py --setup
cd src && npm install
```

### 2. Trigger the file protection hook

In Agent mode, ask Copilot to edit a protected file:

```
Update the database connection string in src/backend/src/db/connection.ts to use a different port.
```

**Observe:** The `file-protection` hook intercepts the `editFiles` tool call. The `check_protected_files.py` script reads the tool input, detects the protected path, and returns a deny decision. Copilot cannot edit the file.

### 3. Trigger the post-save formatter

Ask Copilot to create a new file:

```
Create a new route file at src/backend/src/routes/preferences.ts for notification preferences.
```

**Observe:** After Copilot writes the file, the `post-save-format` hook runs `format_file.py` to auto-format the output.

### 4. Inspect hook behavior in the output panel

Open the **Output** panel (Ctrl+Shift+U) and select **GitHub Copilot** to see hook execution logs.

### 5. Review MCP server integration

Check `.github/mcp.json` to see how external tools are configured. MCP servers can provide database queries, API calls, or custom analysis tools to Copilot.

### 6. Cleanup

```bash
python util.py --clean
```
