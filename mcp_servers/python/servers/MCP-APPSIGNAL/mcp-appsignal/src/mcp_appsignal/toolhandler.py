from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

TOKEN_ARG = "__token__"
ORGANIZATION_SLUG_ARG = "__organization_slug__"
CREDENTIALS_ARG = "__credentials__"
SERVER_CREDENTIALS_ARG = "server_credentials"

class ToolHandler():
    def __init__(self, tool_name: str):
        self.name = tool_name

    def get_token_arg_schema(self) -> dict:
        return {
            "type": "string",
            "description": "AppSignal Personal API Token for authentication"
        }

    def get_organization_slug_arg_schema(self) -> dict:
        return {
            "type": "string",
            "description": "AppSignal organization slug"
        }

    def get_credentials_arg_schema(self) -> dict:
        return {
            "type": "object",
            "description": "AppSignal credentials object containing personal_api and app_id"
        }

    def extract_credentials(self, args: dict) -> tuple[str, str]:
        """Extract personal API token and app ID from credentials or direct arguments."""
        # Check for credentials object first
        credentials = args.get(CREDENTIALS_ARG) or args.get(SERVER_CREDENTIALS_ARG)
        
        if credentials:
            personal_api = credentials.get("personal_api")
            app_id = credentials.get("app_id")
            
            if personal_api and app_id:
                return personal_api, app_id
        
        # Fallback to direct arguments
        token = args.get(TOKEN_ARG)
        app_id = args.get("app_id")
        
        if not token:
            raise RuntimeError(f"Missing required credential: personal_api token")
        if not app_id:
            raise RuntimeError("Missing required credential: app_id")
        print("token:",token)
        print("app_id",app_id)
        return token, app_id

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        raise NotImplementedError() 