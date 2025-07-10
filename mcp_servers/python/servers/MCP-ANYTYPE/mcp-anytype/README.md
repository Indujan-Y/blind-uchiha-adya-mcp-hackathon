# MCP Anytype Server

This MCP (Model Context Protocol) server provides integration with the Anytype API, allowing AI assistants to interact with Anytype workspaces, objects, and spaces.

## Features

- **Space Management**: Create, list, get, and update spaces
- **Object Management**: Create, update, delete objects within spaces
- **Search**: Search for objects across all spaces with various filters
- **Template Management**: List type templates for creating objects

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

Set up your Anytype API token in a `.env` file:
```
ANYTYPE_API_TOKEN=your_token_here
```

The server uses the Anytype API at `http://localhost:31009/v1/` by default. All requests require Bearer token authentication.

## Usage

Run the MCP server:
```bash
mcp-anytype
```

## Available Tools

- `list_spaces` - Retrieve all spaces
- `create_space` - Create a new space
- `get_space` - Get details of a specific space
- `update_space` - Update space name and description
- `list_space_objects` - List all objects in a space
- `create_object_in_space` - Create an object in a space
- `update_object` - Update an object's properties
- `delete_object` - Delete an object from a space
- `search_objects` - Search for objects across spaces
- `list_type_templates` - List templates for a specific type

## API Reference

The server uses the Anytype API at `http://localhost:31009/v1/` by default. All requests require Bearer token authentication. Only the API token needs to be provided in the credentials. 