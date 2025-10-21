"""
Entry point for running magic_research as a module.

Usage:
    python -m magic_research.web_app    # Start web interface
    python -m magic_research.app        # Start CLI interface
    python -m magic_research            # Start web interface (default)
"""

import sys
import os

def main():
    """Main entry point for the magic_research package."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "web":
            from .web_app import main as web_main
            web_main()
        elif sys.argv[1] == "cli":
            from .models.model import main as app_main
            app_main()
        else:
            print("Usage: python -m magic_research [web|cli]")
            print("  web: Start web interface (default)")
            print("  cli: Start command-line interface")
    else:
        # Default to web interface
        from .web_app import main as web_main
        web_main()

if __name__ == "__main__":
    main()