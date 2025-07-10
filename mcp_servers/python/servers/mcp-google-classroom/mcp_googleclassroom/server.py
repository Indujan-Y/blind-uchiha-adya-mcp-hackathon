import logging
import traceback
import json
from typing import Any, Optional, Sequence, Union
from collections.abc import Sequence
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Local imports
from . import classroom_tools
from . import toolhandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-googleclassroom")

# Create MCP Server instance
app = Server("mcp-googleclassroom")

# Tool handlers registry
tool_handlers: dict[str, toolhandler.ToolHandler] = {}

def add_tool_handler(handler: toolhandler.ToolHandler):
    """Register a tool handler by its unique name."""
    tool_handlers[handler.name] = handler

def get_tool_handler(name: str) -> Optional[toolhandler.ToolHandler]:
    """Retrieve a tool handler by name."""
    return tool_handlers.get(name)

# Register all classroom tools
add_tool_handler(classroom_tools.ListCoursesToolHandler())
add_tool_handler(classroom_tools.GetCourseToolHandler())
add_tool_handler(classroom_tools.ListStudentsToolHandler())
add_tool_handler(classroom_tools.ListAssignmentsToolHandler())
add_tool_handler(classroom_tools.GetAssignmentToolHandler())
add_tool_handler(classroom_tools.ListSubmissionsToolHandler())
add_tool_handler(classroom_tools.CreateAssignmentToolHandler())
add_tool_handler(classroom_tools.GradeSubmissionToolHandler())
add_tool_handler(classroom_tools.ListAnnouncementsToolHandler())
add_tool_handler(classroom_tools.CreateAnnouncementToolHandler())
add_tool_handler(classroom_tools.GetUserProfileToolHandler())
add_tool_handler(classroom_tools.ListTeachersToolHandler())
add_tool_handler(classroom_tools.CreateCourseToolHandler())
add_tool_handler(classroom_tools.UpdateCourseToolHandler())
add_tool_handler(classroom_tools.DeleteCourseToolHandler())
add_tool_handler(classroom_tools.GetCourseSummaryToolHandler())
add_tool_handler(classroom_tools.AddStudentToolHandler())
add_tool_handler(classroom_tools.BulkAddStudentsToolHandler())
add_tool_handler(classroom_tools.RemoveStudentToolHandler())
add_tool_handler(classroom_tools.AddTeacherToolHandler())
add_tool_handler(classroom_tools.GetSubmissionToolHandler())
add_tool_handler(classroom_tools.UpdateAssignmentToolHandler())
add_tool_handler(classroom_tools.DeleteAssignmentToolHandler())
add_tool_handler(classroom_tools.ReturnSubmissionToolHandler())
add_tool_handler(classroom_tools.UpdateAnnouncementToolHandler())
add_tool_handler(classroom_tools.DeleteAnnouncementToolHandler())
add_tool_handler(classroom_tools.GetGuardianInvitationsToolHandler())
add_tool_handler(classroom_tools.InviteGuardianToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all registered tool descriptions for MCP."""
    return [handler.get_tool_description() for handler in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[Union[TextContent, ImageContent, EmbeddedResource]]:
    """
    Handle the invocation of a tool with the provided arguments.
    
    Args:
        name (str): Tool name to invoke.
        arguments (dict): Arguments for the tool.
    
    Returns:
        Sequence of MCP response content.
    """
    try:
        if not isinstance(arguments, dict):
            raise RuntimeError("arguments must be dictionary")

        handler = get_tool_handler(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")

        return handler.run_tool(arguments)

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f"Error during call_tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")

async def main():
    """
    Entry point to run the MCP server using stdio transport.
    """
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

# Optional: For running via `python server.py`
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
