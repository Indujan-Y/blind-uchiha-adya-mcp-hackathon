from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from typing import Dict, Any

TOKEN_ARG = "__token__"
ORGANIZATION_SLUG_ARG = "__organization_slug__"
CREDENTIALS_ARG = "__credentials__"
SERVER_CREDENTIALS_ARG = "server_credentials"

class ToolHandler():
    def __init__(self, tool_name: str):
        self.name = tool_name

    def get_credentials_arg_schema(self) -> dict:
        return {
            "type": "object",
            "description": "Google Classroom credentials object containing service account or OAuth2 credentials"
        }

    # def extract_credentials(self, args: dict) -> tuple[str, str]:
    #     """Extract personal API token and app ID from credentials or direct arguments."""
    #     # Check for credentials object first
    #     credentials = args.get(CREDENTIALS_ARG) or args.get(SERVER_CREDENTIALS_ARG)
        
    #     if credentials:
    #         personal_api = credentials.get("personal_api")
    #         app_id = credentials.get("app_id")
            
    #         if personal_api and app_id:
    #             return personal_api, app_id
        
    #     # Fallback to direct arguments
    #     token = args.get(TOKEN_ARG)
    #     app_id = args.get("app_id")
        
    #     if not token:
    #         raise RuntimeError(f"Missing required credential: personal_api token")
    #     if not app_id:
    #         raise RuntimeError("Missing required credential: app_id")
    #     print("token:",token)
    #     print("app_id",app_id)
    #     return token, app_id

    def extract_classroom_credentials(self, args: dict) -> Dict[str, Any]:
        """Extract Google Classroom credentials from arguments."""
        credentials = args.get(CREDENTIALS_ARG) or args.get(SERVER_CREDENTIALS_ARG)
        
        if not credentials:
            raise RuntimeError("Missing required credentials for Google Classroom")
        
        # Validate credentials format
        if isinstance(credentials, dict):
            # Check for service account credentials
            if 'type' in credentials and credentials['type'] == 'service_account':
                required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email', 'client_id']
                missing_fields = [field for field in required_fields if field not in credentials]
                if missing_fields:
                    raise RuntimeError(f"Missing required service account fields: {', '.join(missing_fields)}")
                return credentials
            
            # Check for OAuth2 credentials
            elif 'installed' in credentials and 'client_id' in credentials['installed'] and 'client_secret' in credentials['installed']:
                return credentials

            
            else:
                raise RuntimeError("Invalid credentials format. Expected service account or OAuth2 credentials")
        
        raise RuntimeError("Credentials must be a dictionary")

    def get_tool_description(self) -> Tool:
        raise NotImplementedError()

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        raise NotImplementedError()