---
name: cursor-update-cursor-settings
description: >-
  Modify Cursor/VSCode user settings in settings.json. Use when you want to
  change editor settings, preferences, configuration, themes, font size, tab
  size, format on save, auto save, keybindings, or any settings.json values.
metadata:
  version: "0.1.0"
---
# Updating Cursor Settings

Modify Cursor/VSCode user settings. Use this when you want to change editor settings, preferences, configuration, themes, keybindings, or any `settings.json` values.

## Settings File Location

| OS | Path |
|----|------|
| macOS | ~/Library/Application Support/Cursor/User/settings.json |
| Linux | ~/.config/Cursor/User/settings.json |
| Windows | %APPDATA%\Cursor\User\settings.json |

## Before Modifying Settings

1. **Read the existing settings file** to understand current configuration
2. **Preserve existing settings** — only add/modify what the user requested
3. **Validate JSON syntax** before writing to avoid breaking the editor

## Modifying Settings

### Step 1: Read Current Settings

Read the settings file first to get current contents.

### Step 2: Identify the Setting to Change

Common setting categories:
- **Editor**: `editor.fontSize`, `editor.tabSize`, `editor.wordWrap`, `editor.formatOnSave`
- **Workbench**: `workbench.colorTheme`, `workbench.iconTheme`, `workbench.sideBar.location`
- **Files**: `files.autoSave`, `files.exclude`, `files.associations`
- **Terminal**: `terminal.integrated.fontSize`, `terminal.integrated.shell.*`
- **Cursor-specific**: Settings prefixed with `cursor.` or `aipopup.`

### Step 3: Update the Setting

1. Parse the existing JSON (handle comments — VSCode settings support JSON with comments)
2. Add or update the requested setting
3. Preserve all other existing settings
4. Write back with proper formatting (2-space indentation)

## Important Notes

1. **JSON with Comments**: VSCode/Cursor settings.json supports comments (`//` and `/* */`). Preserve comments when possible.
2. **Restart May Be Required**: Some settings take effect immediately, others require reloading.
3. **Workspace vs User Settings**:
   - User settings: Apply globally to all projects
   - Workspace settings (`.vscode/settings.json`): Apply only to the current project
4. **Commit Attribution**: For CLI agent, modify `~/.cursor/cli-config.json`. For IDE agent, it is controlled from **Cursor Settings > Agent > Attribution**.

## Common User Requests → Settings

| User Request | Setting |
|--------------|---------|
| "bigger/smaller font" | `editor.fontSize` |
| "change tab size" | `editor.tabSize` |
| "format on save" | `editor.formatOnSave` |
| "word wrap" | `editor.wordWrap` |
| "change theme" | `workbench.colorTheme` |
| "hide minimap" | `editor.minimap.enabled` |
| "auto save" | `files.autoSave` |
| "line numbers" | `editor.lineNumbers` |
| "bracket matching" | `editor.bracketPairColorization.enabled` |
| "smooth scrolling" | `editor.smoothScrolling` |

## Workflow

1. Read the settings file
2. Parse the JSON content
3. Add/modify the requested setting(s)
4. Write the updated JSON back
5. Inform the user whether a reload is needed
