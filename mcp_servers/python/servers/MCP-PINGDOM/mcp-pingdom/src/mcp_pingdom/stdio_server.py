import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp.server import Server
from mcp.types import Tool
from mcp_pingdom.tools_checks import get_all_checks, get_check_details, create_check, update_check, delete_check
from mcp_pingdom.tools_maintenance import get_all_maintenance, create_maintenance, update_maintenance, delete_maintenance
from mcp_pingdom.tools_probes import get_all_probes
from mcp_pingdom.tools_results import get_check_results
from mcp_pingdom.tools_summary import get_summary_average, get_summary_outage, get_summary_performance, get_summary_pagespeed
from mcp_pingdom.tools_transactions import get_all_transactions, get_transaction_details, create_transaction, update_transaction, delete_transaction
import asyncio
import time
import logging
logging.basicConfig(filename='stdio_server_debug.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

logging.info("Server started")

app = Server("mcp-pingdom")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_all_checks",
            description="Get all Pingdom checks",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_check_details",
            description="Get details for a specific Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="create_check",
            description="Create a new Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="update_check",
            description="Update an existing Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="delete_check",
            description="Delete a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_all_maintenance",
            description="Get all Pingdom maintenance windows",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="create_maintenance",
            description="Create a Pingdom maintenance window",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="update_maintenance",
            description="Update a Pingdom maintenance window",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="delete_maintenance",
            description="Delete a Pingdom maintenance window",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_all_probes",
            description="Get all Pingdom probes",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_check_results",
            description="Get results for a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_summary_average",
            description="Get average summary for a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_summary_outage",
            description="Get outage summary for a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_summary_performance",
            description="Get performance summary for a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_summary_pagespeed",
            description="Get pagespeed summary for a Pingdom check",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_all_transactions",
            description="Get all Pingdom transactions",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_transaction_details",
            description="Get details for a Pingdom transaction",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="create_transaction",
            description="Create a Pingdom transaction",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="update_transaction",
            description="Update a Pingdom transaction",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="delete_transaction",
            description="Delete a Pingdom transaction",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    logging.info(f"Tool call invoked: {name}, arguments: {arguments}")
    try:
    if name == "get_all_checks":
        return get_all_checks(arguments)
    elif name == "get_check_details":
        return get_check_details(arguments.get("check_id"), arguments)
    elif name == "create_check":
        return create_check(arguments.get("check_data", {}), arguments)
    elif name == "update_check":
        return update_check(arguments.get("check_id"), arguments.get("update_data", {}), arguments)
    elif name == "delete_check":
        return delete_check(arguments.get("check_id"), arguments)
    elif name == "get_all_maintenance":
        return get_all_maintenance(arguments)
    elif name == "create_maintenance":
        return create_maintenance(arguments.get("maintenance_data", {}), arguments)
    elif name == "update_maintenance":
        return update_maintenance(arguments.get("maintenanceid"), arguments.get("update_data", {}), arguments)
    elif name == "delete_maintenance":
        return delete_maintenance(arguments.get("maintenanceid"), arguments)
    elif name == "get_all_probes":
        return get_all_probes(arguments)
    elif name == "get_check_results":
        return get_check_results(arguments.get("check_id"), arguments)
    elif name == "get_summary_average":
        return get_summary_average(arguments.get("check_id"), arguments)
    elif name == "get_summary_outage":
        return get_summary_outage(arguments.get("check_id"), arguments)
    elif name == "get_summary_performance":
        return get_summary_performance(arguments.get("check_id"), arguments)
    elif name == "get_summary_pagespeed":
        return get_summary_pagespeed(arguments.get("check_id"), arguments)
    elif name == "get_all_transactions":
        return get_all_transactions(arguments)
    elif name == "get_transaction_details":
        return get_transaction_details(arguments.get("transaction_id"), arguments)
    elif name == "create_transaction":
        return create_transaction(arguments.get("transaction_data", {}), arguments)
    elif name == "update_transaction":
        return update_transaction(arguments.get("transaction_id"), arguments.get("update_data", {}), arguments)
    elif name == "delete_transaction":
        return delete_transaction(arguments.get("transaction_id"), arguments)
    else:
            logging.error(f"Unknown tool: {name}")
        return {"error": f"Unknown tool: {name}", "status": False}
    except Exception as e:
        logging.exception(f"Exception in tool call {name}: {e}")
        return {"error": f"Exception in tool call {name}: {e}", "status": False}

async def main():
    logging.info("Main loop entered")
    time.sleep(2)  # Wait for 2 seconds to keep the server alive at startup
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
    logging.info("Server exiting")

if __name__ == "__main__":
    asyncio.run(main()) 