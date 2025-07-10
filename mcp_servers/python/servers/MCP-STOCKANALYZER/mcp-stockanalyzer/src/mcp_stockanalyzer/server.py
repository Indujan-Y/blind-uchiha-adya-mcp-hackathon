import logging
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from . import tools_stock
from . import toolhandler
from collections.abc import Sequence
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-stockanalyzer")

app = Server("mcp-stockanalyzer")

tool_handlers = {}

def add_tool_handler(tool_class: toolhandler.ToolHandler):
    global tool_handlers
    tool_handlers[tool_class.name] = tool_class

def get_tool_handler(name: str) -> toolhandler.ToolHandler | None:
    return tool_handlers.get(name)

# Register stock tool handlers
add_tool_handler(tools_stock.StockDetailsToolHandler())
add_tool_handler(tools_stock.StockNewsToolHandler())
add_tool_handler(tools_stock.SimilarStocksToolHandler())
add_tool_handler(tools_stock.StockAnalysisToolHandler())

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [th.get_tool_description() for th in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    try:
        tool_handler = get_tool_handler(name)
        if not tool_handler:
            raise ValueError(f"Unknown tool: {name}")
        return tool_handler.run_tool(arguments)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f"Error during call_tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        ) 