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

"""
VSCode Settings Sync

A tool for syncing VSCode settings across multiple machines using Azure KeyVault.
This script allows you to pack, unpack, and preview VSCode settings stored in KeyVault.

Run with:
    uv run scripts/vscode-sync.py --help

Test with:
    uv run pytest scripts/vscode-sync.py
"""

import os
import json
import base64
import pathlib
import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
import uuid

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from pydantic import BaseModel, Field

# Initialize console for rich output
console = Console()

# Initialize typer app
app = typer.Typer()


class FileContent(BaseModel):
    """Model for file content in the pack format"""

    path: str
    content_type: str = "application/json"
    description: str = ""
    content: Optional[Dict[str, Any]] = None
    content_text: Optional[str] = None


class PackFormat(BaseModel):
    """Model for the pack format"""

    metadata: Dict[str, Any] = Field(default_factory=dict)
    directory_structure: Dict[str, List[str]] = Field(default_factory=dict)
    files: List[FileContent] = Field(default_factory=list)


def get_default_secret_name() -> str:
    """Get the default secret name based on the parent directory name"""
    current_dir = os.path.basename(os.getcwd())
    return f"{current_dir}-vscode-settings"


def get_keyvault_client(vault_name: str) -> SecretClient:
    """Create and return a KeyVault secret client"""
    vault_url = f"https://{vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def read_vscode_files() -> Tuple[List[pathlib.Path], List[str]]:
    """Read .vscode directory and return list of files and their relative paths"""
    vscode_dir = pathlib.Path(".vscode")
    if not vscode_dir.exists():
        console.print(
            "[yellow]No .vscode directory found. Will create it when unpacking.[/yellow]"
        )
        return [], []

    files = list(vscode_dir.glob("**/*"))
    file_paths = [str(f.relative_to(vscode_dir)) for f in files if f.is_file()]
    return files, file_paths


def create_pack_format(files: List[pathlib.Path], file_paths: List[str]) -> PackFormat:
    """Create a pack format object from the files in the .vscode directory"""
    pack = PackFormat()

    # Add metadata
    pack.metadata = {
        "format_version": "1.0",
        "created_at": datetime.datetime.now().isoformat(),
        "description": "VS Code settings pack",
    }

    # Add directory structure
    pack.directory_structure = {"vscode": file_paths}

    # Add files
    for i, file in enumerate(files):
        if not file.is_file():
            continue

        # Use the corresponding path from file_paths instead of computing it
        relative_path = file_paths[i] if i < len(file_paths) else file.name
        file_content = FileContent(path=relative_path)

        # Determine content type and read file accordingly
        if file.suffix == ".json":
            try:
                with open(file, "r") as f:
                    content = json.load(f)
                file_content.content_type = "application/json"
                file_content.content = content
            except json.JSONDecodeError:
                # If JSON parsing fails, treat as text
                with open(file, "r") as f:
                    text_content = f.read()
                file_content.content_type = "text/plain"
                file_content.content_text = text_content
        else:
            # For non-JSON files, store as text
            with open(file, "r") as f:
                text_content = f.read()
            file_content.content_type = "text/plain"
            file_content.content_text = text_content

        pack.files.append(file_content)

    return pack


def save_pack_to_keyvault(
    pack: PackFormat, vault_name: str, secret_name: str, group: str
) -> None:
    """Save the pack format to KeyVault as a secret"""
    try:
        # Convert to JSON and save to KeyVault
        secret_client = get_keyvault_client(vault_name)
        json_content = pack.model_dump_json()

        # Add group tag for organization
        tags = {"group": group}

        # Set the secret in KeyVault
        secret_client.set_secret(secret_name, json_content, tags=tags)
        console.print(
            f"[green]Successfully saved settings to KeyVault secret: {secret_name}[/green]"
        )
    except Exception as e:
        console.print(f"[bold red]Error saving to KeyVault: {str(e)}[/bold red]")
        raise typer.Exit(code=1)


def get_pack_from_keyvault(vault_name: str, secret_name: str) -> PackFormat:
    """Retrieve the pack format from KeyVault"""
    try:
        secret_client = get_keyvault_client(vault_name)
        secret = secret_client.get_secret(secret_name)

        # Parse the secret value as JSON and create PackFormat object
        if secret.value is None:
            raise ValueError("Secret value is None")
            
        pack_dict = json.loads(secret.value)
        return PackFormat.model_validate(pack_dict)
    except Exception as e:
        console.print(f"[bold red]Error retrieving from KeyVault: {str(e)}[/bold red]")
        raise typer.Exit(code=1)


def unpack_to_vscode_directory(pack: PackFormat) -> None:
    """Unpack the files from the pack format to the .vscode directory"""
    vscode_dir = pathlib.Path(".vscode")

    # Create .vscode directory if it doesn't exist
    if not vscode_dir.exists():
        vscode_dir.mkdir()
        console.print(f"[green]Created .vscode directory[/green]")

    # Extract files from the pack
    for file_content in pack.files:
        file_path = vscode_dir / file_content.path

        # Create parent directories if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if file exists and prompt for overwrite if it does
        if file_path.exists():
            overwrite = Confirm.ask(f"File {file_path} already exists. Overwrite?")
            if not overwrite:
                console.print(f"[yellow]Skipping {file_path}[/yellow]")
                continue

        # Write the content to the file
        if (
            file_content.content_type == "application/json"
            and file_content.content is not None
        ):
            with open(file_path, "w") as f:
                json.dump(file_content.content, f, indent=2)
        elif file_content.content_text is not None:
            with open(file_path, "w") as f:
                f.write(file_content.content_text)

        console.print(f"[green]Created {file_path}[/green]")


def display_pack_preview(pack: PackFormat) -> None:
    """Display a preview of the pack format"""
    # Create metadata panel
    metadata_table = Table(title="Pack Metadata")
    metadata_table.add_column("Key", style="cyan")
    metadata_table.add_column("Value", style="green")

    for key, value in pack.metadata.items():
        metadata_table.add_row(key, str(value))

    # Create files table
    files_table = Table(title="Files")
    files_table.add_column("Path", style="cyan")
    files_table.add_column("Type", style="yellow")
    files_table.add_column("Size", style="green")

    for file in pack.files:
        if file.content is not None:
            size = len(json.dumps(file.content))
        elif file.content_text is not None:
            size = len(file.content_text)
        else:
            size = 0

        files_table.add_row(file.path, file.content_type, f"{size} bytes")

    # Create content preview table
    content_table = Table(title="File Contents")
    content_table.add_column("Path", style="cyan")
    content_table.add_column("Content", style="green")

    for file in pack.files:
        if file.content is not None:
            # For JSON content, format it nicely
            content = json.dumps(file.content, indent=2)
        elif file.content_text is not None:
            content = file.content_text
        else:
            content = "(empty)"

        # Truncate content if it's too long
        if len(content) > 500:
            content = content[:500] + "...(truncated)"

        content_table.add_row(file.path, content)

    # Display the preview
    console.print(Panel(metadata_table, title="VSCode Settings Pack"))
    console.print(files_table)
    console.print(Panel(content_table, title="File Contents Preview"))


@app.command()
def main(
    vault: str = typer.Option(None, help="Azure KeyVault name"),
    group: str = typer.Option(None, help="Group name for the settings"),
    secret: Optional[str] = typer.Option(
        None, help="Secret name (defaults to {directory}-vscode-settings)"
    ),
    preview: bool = typer.Option(
        False, "--preview", help="Show the .vscode folder in pack format"
    ),
    pack: bool = typer.Option(
        False, "--pack", help="Pack .vscode folder and save to vault as secret"
    ),
    unpack: bool = typer.Option(
        False,
        "--unpack",
        help="Retrieve the secret from vault and unpack to the .vscode folder",
    ),
) -> None:
    """
    VSCode Settings Sync - Sync VSCode settings across multiple machines using Azure KeyVault
    """

    # Validate required parameters
    if (pack or unpack) and (vault is None or group is None):
        console.print(
            "[bold red]Error: --vault and --group are required for --pack and --unpack operations[/bold red]"
        )
        raise typer.Exit(code=1)

    # Set default secret name if not provided
    if secret is None:
        secret = get_default_secret_name()
        console.print(f"[blue]Using default secret name: {secret}[/blue]")

    # Handle preview option
    if preview:
        files, file_paths = read_vscode_files()
        if not files:
            console.print("[yellow]No files to preview in .vscode directory[/yellow]")
            return

        pack_format = create_pack_format(files, file_paths)
        display_pack_preview(pack_format)
        return

    # Handle pack option
    if pack:
        files, file_paths = read_vscode_files()
        if not files:
            console.print("[yellow]No files to pack in .vscode directory[/yellow]")
            return

        pack_format = create_pack_format(files, file_paths)
        save_pack_to_keyvault(pack_format, vault, secret, group)
        return

    # Handle unpack option
    if unpack:
        pack_format = get_pack_from_keyvault(vault, secret)
        unpack_to_vscode_directory(pack_format)
        return

    # If no action specified, show help
    if not (preview or pack or unpack):
        console.print(
            "[yellow]No action specified. Use --preview, --pack, or --unpack[/yellow]"
        )
        console.print("Run 'uv run scripts/vscode-sync.py --help' for more information")


# Test functions
def test_default_secret_name():
    """Test that the default secret name is correctly generated"""
    # Mock current directory
    original_getcwd = os.getcwd

    try:
        os.getcwd = lambda: "/path/to/project"

        # Expected value should be based on the directory name
        expected = "project-vscode-settings"
        assert get_default_secret_name() == expected
    finally:
        # Restore original function
        os.getcwd = original_getcwd


def test_create_pack_format_empty():
    """Test creating pack format with no files"""
    pack = create_pack_format([], [])

    # Validate basic structure
    assert "metadata" in pack.model_dump()
    assert "directory_structure" in pack.model_dump()
    assert "files" in pack.model_dump()

    # No files should be present
    assert len(pack.files) == 0


def test_create_pack_format_with_files(tmp_path):
    """Test creating pack format with sample files"""
    # Create temporary .vscode directory with files
    vscode_dir = tmp_path / ".vscode"
    vscode_dir.mkdir()

    # Create a sample settings.json file
    settings_file = vscode_dir / "settings.json"
    settings_content = {"editor.fontSize": 14, "files.autoSave": "afterDelay"}
    settings_file.write_text(json.dumps(settings_content))

    # Create a sample .env file
    env_file = vscode_dir / ".env"
    env_content = "API_KEY=test-key\nDEBUG=true"
    env_file.write_text(env_content)

    # Test with the created files
    files = [settings_file, env_file]
    file_paths = ["settings.json", ".env"]

    # Create the pack format
    pack = create_pack_format(files, file_paths)

    # Validate structure and content
    assert len(pack.files) == 2

    # Find the settings.json file in the pack
    settings_in_pack = next((f for f in pack.files if f.path == "settings.json"), None)
    assert settings_in_pack is not None
    assert settings_in_pack.content_type == "application/json"
    assert settings_in_pack.content == settings_content

    # Find the .env file in the pack
    env_in_pack = next((f for f in pack.files if f.path == ".env"), None)
    assert env_in_pack is not None
    assert env_in_pack.content_type == "text/plain"
    assert env_in_pack.content_text == env_content


if __name__ == "__main__":
    app()
