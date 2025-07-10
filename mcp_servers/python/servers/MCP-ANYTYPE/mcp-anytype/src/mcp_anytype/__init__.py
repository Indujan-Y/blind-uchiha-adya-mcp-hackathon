"""MCP Anytype Server Package."""

from . import server
import asyncio


def main():
    """Main entry point for the package."""
    print("Running MCP Anytype Server")
    asyncio.run(server.main())

__version__ = "0.1.0"
__all__ = ["main"] 