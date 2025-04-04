# Settings Sync - VSCode Settings Sync using Keyvault as a backend

As engineers we often have a .vscode settings folder that has a lot of specific settings like environment variables, launch settings, extensions and general settings.  Persisting these settings or making them available to other engineers can be a pain.

This is a simple tool that will allow you to sync your VSCode settings across multiple machines.

## Key Features
- Sync settings across multiple machines
- Share settings with other engineers
- Keep settings private and secure
- Easy to setup and use running a uv script

_Example uv script tag_
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

To implement this we'll...
1. Build the script functionality
2. Test the functionality with pytest
3. Expose the functionality as a single file uv script.


## Implementation Notes
- READ ai_docs/keyvault-command.md to understand how to work with azure keyvault using the azure cli.
- USE ai_docs/example.xml to get a rough understanding of how a single file format might be used to store multiple files.
- CREATE a single file uv script that will perform all the functionality and tests.

## Commands
uv run setting-sync.py --help
uv run settings-sync.py --vault --group (If vault does not exist, create it)
uv run settings-sync.py --pack (show .vscode folder in pack format)
uv run settings-sync.py --pack --vault --group --secret (pack the .vscode folder and upload pack to vault)
uv run settings-sync.py --show --vault --group --secret (show the contents of the pack)
uv run settings-sync.py --unpack --vault --group --secret (download the pack and unpack it to the .vscode folder overwriting existing files.


## Project Structure
- src/
    - setting-sync.py
    - tests/
        - test_setting_sync.py
 

## Validation (close the loop)
- use `uv run pytest` to validate the tests pass.
