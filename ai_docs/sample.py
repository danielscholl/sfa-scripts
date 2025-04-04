#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "rich>=13.7.0"
# ]
# ///

"""
Simple Hello World Example with UV

This example demonstrates a very basic Python script that can be run with UV.
It includes a simple function to print "Hello, World!" and a test case.

Run with:
    uv run hello_world.py

Test with:
    uv run pytest hello_world.py
"""

import sys

def hello_world():
    """Return a hello world message"""
    return "Hello, World!"

def main():
    """Main function to display the hello world message"""
    try:
        # Only import rich when running the main script, not during testing
        from rich.console import Console
        from rich.panel import Panel
        
        # Initialize console
        console = Console()
        message = hello_world()
        console.print(Panel(message, title="Hello World", border_style="green"))
    except ImportError:
        # Fallback to simple print if rich is not available
        print(hello_world())

# Test function
def test_hello_world():
    """Test that the hello_world function returns the correct message."""
    assert hello_world() == "Hello, World!"
    
if __name__ == "__main__":
    main()