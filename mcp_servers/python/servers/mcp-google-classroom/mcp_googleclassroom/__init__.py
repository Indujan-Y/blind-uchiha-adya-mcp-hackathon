from . import server
import asyncio


def main():
    """Main entry point for the Google Classroom MCP server."""
    print("Starting Google Classroom MCP Server")
    asyncio.run(server.main())


# Expose important items at package level
__all__ = ['main', 'server']