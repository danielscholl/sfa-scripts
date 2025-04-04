# Settings Sync - VSCode Settings Sync using Keyvault as a backend

As engineers we often have a .vscode settings folder that has a lot of specific settings like environment variables, launch settings, extensions and general settings. Persisting these settings or making them available to other engineers can be a pain.

This is a simple tool that will allow you to sync your VSCode settings across multiple machines.


THINK ABOUT THIS SPEC BEFORE IMPLEMENTING IT
--------------------------------------------

## Key Features
- Sync settings across multiple machines
- Share settings with other engineers
- Keep settings private and secure
- Easy to setup and use running a uv script

## Project Structure
- All scripts should be placed in the `scripts/` directory
- The project uses pytest.ini and pyproject.toml for configuration
- Tests for each script are included within the script file itself
- Use `uv run pytest scripts/script-name.py` to run tests for a specific script

### Validation Process
1. Code should pass validation using the python black tool.
2. Code should pass static type checking using the python mypy tool.
3. After initial implementation, run `uv run pytest scripts/script-name.py -v` and show the output
4. If any tests fail, fix the implementation and run tests again until all tests pass
5. Demonstrate validation was successful by:
   - Show the test output with all tests passing
   - Include a brief summary of what was validated
   - Confirm that script functionality matches all requirements in the specification
6. Always validate both functionality and code quality (typing, error handling, etc.)
7. Never consider implementation complete until explicit validation is performed and successful

## Tests
1. The script should be written in a way that is testable.
2. Tests should be included within the same file.

## Implementation Notes
- SCRIPT_NAME = `vscode-sync.py`
- CREATE a **single, self-contained Python file** (`scripts/script-name.py`) that contains all functionality including tests
- READ ai_docs/keyvault-doc.md to understand how to work with azure keyvault using the azure cli
- USE ai_docs/pack_format.json to get a rough understanding of how a single file format might be used to store multiple files
- The script should use the uv script header format for dependencies
- The script should use typer for command-line argument parsing

_Example uv script header_
```
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "rich>=13.7.0",
#   "azure-identity>=1.15.0",
#   "azure-keyvault-secrets>=4.7.0",
#   "typer>=0.9.0",
#   "pydantic>=2.5.0",
# ]
# ///
```

## Command Options
Use only the following command options.

1. `--vault TEXT  Azure KeyVault name [default: None]`  * Required
2. `--group TEXT  Group name for the settings [default: None]` * Required
3. `--secret TEXT  Secret name (defaults to {directory}-vscode-settings)` * Optional
4. `--preview Show the .vscode folder in pack format`
5. `--pack Pack .vscode folder and save to vault as secret`
6. `--unpack Retrieve the secret from vault and unpack to the .vscode folder`
7. `--help`

## Important Details
1. The DEFAULT secret name should ALWAYS be the parent directory name of the .vscode folder followed by `-vscode-settings`  Example: `sample-vscode-settings`
2. IF the .vscode folder doesn't exist or a file doesn't exist it should create it.
3. IF the file exists then the user should be prompted if it is okay to overwrite the file.

## CLI Implementation
- Use the Typer library for command-line parsing (NOT argparse)
- Implement as a single command with options, not a multi-command application
- Use `@app.command()` instead of `@app.callback()` for the main function
- All commands are options to the main command, not subcommands

## Script Structure
The script should be a fully self-contained Python file that includes:
1. Main functionality for packing/unpacking/syncing settings
2. CLI argument parsing using Typer
3. Azure KeyVault integration
4. Python Tests
