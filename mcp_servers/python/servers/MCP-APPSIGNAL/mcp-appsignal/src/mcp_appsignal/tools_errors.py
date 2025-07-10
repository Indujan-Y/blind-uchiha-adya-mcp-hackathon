from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from . import appsignal
import json
from . import toolhandler

class SearchErrorsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("search_appsignal_errors")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Search for exception errors in AppSignal using the Search GraphQL API.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.TOKEN_ARG: self.get_token_arg_schema(),
                    toolhandler.ORGANIZATION_SLUG_ARG: self.get_organization_slug_arg_schema(),
                    "query_string": {
                        "type": "string",
                        "description": "Search query string (optional)"
                    },
                    "namespace": {
                        "type": "string",
                        "description": "Filter errors by namespace (optional)"
                    }
                },
                "required": [toolhandler.ORGANIZATION_SLUG_ARG]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Extract credentials
        personal_api, app_id = self.extract_credentials(args)
        
        organization_slug = args.get(toolhandler.ORGANIZATION_SLUG_ARG)
        if not organization_slug:
            raise RuntimeError(f"Missing required argument: {toolhandler.ORGANIZATION_SLUG_ARG}")

        appsignal_service = appsignal.AppSignalService(token=personal_api)
        query_string = args.get('query_string')
        namespace = args.get('namespace')
        
        result = appsignal_service.search_errors(
            organization_slug=organization_slug,
            query_string=query_string,
            namespace=namespace
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetAllErrorsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_appsignal_all_errors")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get all open exception incidents from AppSignal.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.TOKEN_ARG: self.get_token_arg_schema(),
                    "app_id": {
                        "type": "string",
                        "description": "AppSignal App ID (if not provided in credentials)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of incidents to fetch (default: 100)",
                        "default": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0)",
                        "default": 0
                    }
                },
                "required": []
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Extract credentials
        personal_api, app_id = self.extract_credentials(args)

        appsignal_service = appsignal.AppSignalService(token=personal_api)
        limit = args.get('limit', 100)
        offset = args.get('offset', 0)
        
        result = appsignal_service.get_all_errors(
            app_id=app_id,
            limit=limit,
            offset=offset
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetIncidentDetailsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_appsignal_incident_details")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get details for a specific incident in AppSignal.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.TOKEN_ARG: self.get_token_arg_schema(),
                    "app_id": {
                        "type": "string",
                        "description": "AppSignal App ID (if not provided in credentials)"
                    },
                    "incident_number": {
                        "type": "integer",
                        "description": "Incident number"
                    },
                    "sample_id": {
                        "type": "string",
                        "description": "Sample ID (optional)"
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "Timestamp (optional)"
                    },
                    "timerange": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Time range array (optional)"
                    }
                },
                "required": ["incident_number"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Extract credentials
        personal_api, app_id = self.extract_credentials(args)

        incident_number = args.get('incident_number')
        if incident_number is None:
            raise RuntimeError("Missing required argument: incident_number")

        appsignal_service = appsignal.AppSignalService(token=personal_api)
        sample_id = args.get('sample_id')
        timestamp = args.get('timestamp')
        timerange = args.get('timerange')
        
        result = appsignal_service.get_incident_details(
            app_id=app_id,
            incident_number=incident_number,
            sample_id=sample_id,
            timestamp=timestamp,
            timerange=timerange
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetAllIncidentsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_appsignal_all_incidents")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get all performance incidents from AppSignal.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.TOKEN_ARG: self.get_token_arg_schema(),
                    "app_id": {
                        "type": "string",
                        "description": "AppSignal App ID (if not provided in credentials)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of incidents to fetch (default: 100)",
                        "default": 100
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Offset for pagination (default: 0)",
                        "default": 0
                    },
                    "state": {
                        "type": "string",
                        "description": "Incident state filter (optional)"
                    }
                },
                "required": []
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Extract credentials
        personal_api, app_id = self.extract_credentials(args)

        appsignal_service = appsignal.AppSignalService(token=personal_api)
        limit = args.get('limit', 100)
        offset = args.get('offset', 0)
        state = args.get('state')
        
        result = appsignal_service.get_all_incidents(
            app_id=app_id,
            limit=limit,
            offset=offset,
            state=state
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ] 