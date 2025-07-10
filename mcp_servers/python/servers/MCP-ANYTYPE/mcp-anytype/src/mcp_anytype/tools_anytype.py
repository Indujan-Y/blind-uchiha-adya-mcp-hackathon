from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
import json
from . import toolhandler
from . import anytype

class ListSpacesToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_spaces")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve a list of all spaces in Anytype.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        spaces = client.list_spaces()
        
        return [
            TextContent(
                type="text",
                text=json.dumps(spaces, indent=2)
            )
        ]

class CreateSpaceToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("create_space")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new space in Anytype.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the space to create"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the space"
                    }
                },
                "required": ["name", "description"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        if "name" not in args or "description" not in args:
            raise RuntimeError("Missing required arguments: name, description")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        space = client.create_space(name=args["name"], description=args["description"])
        
        return [
            TextContent(
                type="text",
                text=json.dumps(space, indent=2)
            )
        ]

class GetSpaceToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_space")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve details of a specific space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space to retrieve"
                    }
                },
                "required": ["space_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        if "space_id" not in args:
            raise RuntimeError("Missing required argument: space_id")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        space = client.get_space(space_id=args["space_id"])
        
        return [
            TextContent(
                type="text",
                text=json.dumps(space, indent=2)
            )
        ]

class UpdateSpaceToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("update_space")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Update a specific space's name and description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name for the space"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description for the space"
                    }
                },
                "required": ["space_id", "name", "description"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["space_id", "name", "description"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        space = client.update_space(
            space_id=args["space_id"],
            name=args["name"],
            description=args["description"]
        )
        
        return [
            TextContent(
                type="text",
                text=json.dumps(space, indent=2)
            )
        ]

class ListSpaceObjectsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_space_objects")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all objects in a specific space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space"
                    }
                },
                "required": ["space_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        if "space_id" not in args:
            raise RuntimeError("Missing required argument: space_id")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        objects = client.list_space_objects(space_id=args["space_id"])
        
        return [
            TextContent(
                type="text",
                text=json.dumps(objects, indent=2)
            )
        ]

class CreateObjectInSpaceToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("create_object_in_space")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create an object in a specific space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space where to create the object"
                    },
                    "name": {
                        "type": "string",
                        "description": "Name of the object"
                    },
                    "body": {
                        "type": "string",
                        "description": "Body content of the object"
                    },
                    "type_key": {
                        "type": "string",
                        "description": "Type key of the object (e.g., 'page', 'task', 'bookmark')"
                    },
                    "template_id": {
                        "type": "string",
                        "description": "Template ID for the object"
                    },
                    "icon": {
                        "type": "object",
                        "description": "Icon configuration (e.g., {'emoji': '📄', 'format': 'emoji'})"
                    }
                },
                "required": ["space_id", "name", "body", "type_key", "template_id", "icon"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["space_id", "name", "body", "type_key", "template_id", "icon"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        obj = client.create_object_in_space(
            space_id=args["space_id"],
            name=args["name"],
            body=args["body"],
            type_key=args["type_key"],
            template_id=args["template_id"],
            icon=args["icon"]
        )
        
        return [
            TextContent(
                type="text",
                text=json.dumps(obj, indent=2)
            )
        ]

class UpdateObjectToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("update_object")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Update an object in a specific space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space containing the object"
                    },
                    "object_id": {
                        "type": "string",
                        "description": "ID of the object to update"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name for the object"
                    },
                    "icon": {
                        "type": "object",
                        "description": "New icon configuration (e.g., {'emoji': '📄', 'format': 'emoji'})"
                    }
                },
                "required": ["space_id", "object_id", "name", "icon"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["space_id", "object_id", "name", "icon"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        obj = client.update_object(
            space_id=args["space_id"],
            object_id=args["object_id"],
            name=args["name"],
            icon=args["icon"]
        )
        
        return [
            TextContent(
                type="text",
                text=json.dumps(obj, indent=2)
            )
        ]

class DeleteObjectToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("delete_object")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Delete an object from a space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space containing the object"
                    },
                    "object_id": {
                        "type": "string",
                        "description": "ID of the object to delete"
                    }
                },
                "required": ["space_id", "object_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["space_id", "object_id"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        result = client.delete_object(space_id=args["space_id"], object_id=args["object_id"])
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class SearchObjectsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("search_objects")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Search for objects across all spaces with various filters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "sort": {
                        "type": "object",
                        "description": "Sorting configuration (e.g., {'direction': 'desc', 'property_key': 'last_modified_date'})"
                    },
                    "types": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of object types to search for (e.g., ['page', 'task', 'bookmark'])"
                    }
                },
                "required": ["query", "sort", "types"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["query", "sort", "types"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        client = anytype.AnytypeClient(credentials=credentials)
        results = client.search_objects(
            query=args["query"],
            sort=args["sort"],
            types=args["types"]
        )
        
        return [
            TextContent(
                type="text",
                text=json.dumps(results, indent=2)
            )
        ]

class ListTypeTemplatesToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_type_templates")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Retrieve all templates for a specific type in a space.",
            inputSchema={
                "type": "object",
                "properties": {
                    "space_id": {
                        "type": "string",
                        "description": "ID of the space"
                    },
                    "type_id": {
                        "type": "string",
                        "description": "ID of the type"
                    }
                },
                "required": ["space_id", "type_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        required = ["space_id", "type_id"]
        if not all(key in args for key in required):
            raise RuntimeError(f"Missing required arguments: {', '.join(required)}")
        
        # Get credentials from args (passed by client)
        credentials = args.get("__credentials__") or args.get("server_credentials") or {}
        print(f"DEBUG: Tool handler - credentials: {credentials}")
        print(f"DEBUG: Tool handler - credentials type: {type(credentials)}")
        
        client = anytype.AnytypeClient(credentials=credentials)
        print(f"DEBUG: Tool handler - client created, base_url: {client.base_url}")
        
        templates = client.list_type_templates(space_id=args["space_id"], type_id=args["type_id"])
        
        return [
            TextContent(
                type="text",
                text=json.dumps(templates, indent=2)
            )
        ] 