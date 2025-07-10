# Anytype MCP Server - Client Integration

## Overview

The Anytype MCP server has been successfully integrated with the client system and will now properly receive credentials when called through the MCP client.

## Changes Made

### 1. Client Configuration Updates

#### Added to `mcp_servers/python/clients/src/client_and_server_config.py`:
```python
{
    "server_name": "MCP-ANYTYPE",
    "command": "uv",
    "args": [
        "--directory",
        "mcp_servers/python/servers/MCP-ANYTYPE/mcp-anytype",
        "run",
        "mcp-anytype"
    ]
}
```

#### Added to `mcp_servers/python/clients/src/client_and_server_execution.py`:
```python
case "MCP-ANYTYPE":
    args["__credentials__"] = creds
    args["server_credentials"] = creds
```

### 2. Anytype Server Updates

#### Updated `AnytypeClient` constructor in `anytype.py`:
- Added support for credentials dictionary parameter
- Priority order: credentials dict > token parameter > environment variable
- Supports multiple credential key formats: `token`, `api_token`, `ANYTYPE_API_TOKEN`

#### Updated all tool handlers in `tools_anytype.py`:
- All tools now extract credentials from `args["__credentials__"]` or `args["server_credentials"]`
- Credentials are passed to `AnytypeClient` constructor
- Fallback to environment variables if no credentials provided

## How Credentials Are Passed

### 1. Client Request Structure
When making requests to the client API, include Anytype credentials:

```json
{
  "selected_server_credentials": {
    "MCP-ANYTYPE": {
      "token": "your_anytype_api_token",
      "base_url": "http://localhost:31009"
    }
  },
  "selected_servers": ["MCP-ANYTYPE"],
  "selected_client": "MCP_CLIENT_AZURE_AI",
  "client_details": {
    "input": "List all my spaces",
    "prompt": "You are an Anytype assistant"
  }
}
```

### 2. Credential Injection Flow
1. Client receives request with `selected_server_credentials`
2. Client extracts credentials for "MCP-ANYTYPE" from the credentials object
3. Client injects credentials into tool arguments using `__credentials__` and `server_credentials` keys
4. Anytype MCP server receives credentials in tool arguments
5. Anytype server extracts credentials and passes them to `AnytypeClient`

### 3. Credential Priority
The Anytype server uses this priority order for credentials:
1. **Credentials from client** (highest priority)
2. **Token/base_url parameters** (if passed directly)
3. **Environment variables** (fallback)

## Testing the Integration

### Run the Integration Test
```bash
cd mcp_servers/python/servers/MCP-ANYTYPE/mcp-anytype
python test_client_integration.py
```

### Test Individual Components
```bash
# Test the Anytype server directly
python test_anytype_mcp.py

# Test the client system
cd ../../../../clients
python run.py
```

## Usage Examples

### Example 1: List Spaces
```json
{
  "selected_server_credentials": {
    "MCP-ANYTYPE": {
      "token": "your_token_here"
    }
  },
  "selected_servers": ["MCP-ANYTYPE"],
  "selected_client": "MCP_CLIENT_AZURE_AI",
  "client_details": {
    "input": "Show me all my spaces",
    "prompt": "You are an Anytype assistant. Use the list_spaces tool to show all spaces."
  }
}
```

### Example 2: Create a Space
```json
{
  "selected_server_credentials": {
    "MCP-ANYTYPE": {
      "token": "your_token_here"
    }
  },
  "selected_servers": ["MCP-ANYTYPE"],
  "selected_client": "MCP_CLIENT_AZURE_AI",
  "client_details": {
    "input": "Create a new space called 'Project Alpha' for my new project",
    "prompt": "You are an Anytype assistant. Create a new space with the given name and description."
  }
}
```

### Example 3: Search Objects
```json
{
  "selected_server_credentials": {
    "MCP-ANYTYPE": {
      "token": "your_token_here"
    }
  },
  "selected_servers": ["MCP-ANYTYPE"],
  "selected_client": "MCP_CLIENT_AZURE_AI",
  "client_details": {
    "input": "Find all pages that contain 'meeting notes'",
    "prompt": "You are an Anytype assistant. Search for objects containing the specified text."
  }
}
```

## Available Tools

The Anytype MCP server provides these tools that can be called through the client:

1. **`list_spaces`** - Retrieve all spaces
2. **`create_space`** - Create a new space
3. **`get_space`** - Get space details
4. **`update_space`** - Update space metadata
5. **`list_space_objects`** - List objects in a space
6. **`create_object_in_space`** - Create new objects
7. **`update_object`** - Update object properties
8. **`delete_object`** - Delete objects
9. **`search_objects`** - Search across all spaces
10. **`list_type_templates`** - List available templates

## Troubleshooting

### Common Issues

1. **"Server MCP-ANYTYPE not found in MCPServers"**
   - Ensure the Anytype server is properly configured in `ServersConfig`
   - Check that the server directory exists and is accessible

2. **"Anytype API token is required"**
   - Verify credentials are included in the request payload
   - Check that the token is valid and has proper permissions

3. **"Connection refused" errors**
   - Ensure the Anytype API is running on the specified port
   - Verify the `base_url` in credentials is correct

4. **Tool not found errors**
   - Check that the Anytype MCP server is running
   - Verify the server is properly initialized in the client

### Debug Steps

1. **Check server configuration**:
   ```bash
   python test_client_integration.py
   ```

2. **Test server directly**:
   ```bash
   cd mcp_servers/python/servers/MCP-ANYTYPE/mcp-anytype
   python test_anytype_mcp.py
   ```

3. **Check client logs**:
   - Look for initialization messages in the client logs
   - Verify the Anytype server appears in the available servers list

4. **Verify credentials**:
   - Test the Anytype API token directly
   - Ensure the API is accessible from the server location

## Security Notes

- Credentials are passed through the MCP protocol and should be handled securely
- The Anytype server validates credentials before making API calls
- Environment variables provide a fallback for local development
- Always use HTTPS for production deployments

## Next Steps

The Anytype MCP server is now fully integrated with the client system and ready for use. You can:

1. **Start using it immediately** with the client API
2. **Add more tools** by extending the `tools_anytype.py` file
3. **Customize the credential handling** if needed
4. **Deploy to production** with proper security measures 