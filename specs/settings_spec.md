# Settings Sync - VSCode Settings Sync using Keyvault as a backend

As engineers we often have a .vscode settings folder that has a lot of specific settings like environment variables, launch settings, extensions and general settings. Persisting these settings or making them available to other engineers can be a pain.

This is a simple tool that will allow you to sync your VSCode settings across multiple machines.

## Key Features
- Sync settings across multiple machines
- Share settings with other engineers
- Keep settings private and secure
- Easy to setup and use running a uv script

## Implementation Notes
- This will be a **single, self-contained Python file** (settings-sync.py) that contains all functionality including tests
- READ ai_docs/keyvault-command.md to understand how to work with azure keyvault using the azure cli
- USE ai_docs/example.xml to get a rough understanding of how a single file format might be used to store multiple files
- The script should use the uv script header format for dependencies

_Example uv script header_
```
#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "rich>=13.7.0",
#   "azure-identity>=1.15.0",
#   "python-dotenv>=1.0.0",
#   "openai>=1.65.0,<1.66.0"
# ]
# ///
```

## Commands
- `uv run settings-sync.py --help` - Display help
- `uv run settings-sync.py --vault <vault> --group <group>` - If vault does not exist, create it
- `uv run settings-sync.py --pack` - Show .vscode folder in pack format
- `uv run settings-sync.py --pack --vault <vault> --group <group> --secret <secret>` - Pack the .vscode folder and upload to vault
- `uv run settings-sync.py --show --vault <vault> --group <group> --secret <secret>` - Show the contents of the pack
- `uv run settings-sync.py --unpack --vault <vault> --group <group> --secret <secret>` - Download the pack and unpack to .vscode folder

## Script Structure
The script should be a fully self-contained Python file that includes:
1. Main functionality for packing/unpacking/syncing settings
2. CLI argument parsing
3. Azure KeyVault integration
4. Built-in tests that can be run with `uv run settings-sync.py --test`

## Validation
- Use `uv run pytest settings-sync.py` to run the tests within the script
- This command should discover and run all test functions and classes within the script file
- All tests should pass successfully when run with the above command
