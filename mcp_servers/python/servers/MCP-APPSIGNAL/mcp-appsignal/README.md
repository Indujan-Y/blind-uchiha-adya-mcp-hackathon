# AppSignal MCP Server

A Model Context Protocol (MCP) server for integrating with AppSignal's monitoring and error tracking platform.

## Features

- 🔍 **Search Errors**: Search for exception errors across your organization
- 📊 **Get All Errors**: Retrieve all open exception incidents
- 🔎 **Get Incident Details**: Get detailed information about specific incidents
- 📈 **Get All Incidents**: Retrieve all performance incidents
- 🔐 **Dynamic Credentials**: Automatic credential injection and management

## Dynamic Credential System

The server now supports dynamic credential injection, making it easier to manage authentication:

### Credential Structure
```json
{
  "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
  "app_id": "68639bbe15207808b81b328b"
}
```

### Automatic Injection
When using the MCP client, credentials are automatically injected into tool calls via:
- `__credentials__` parameter
- `server_credentials` parameter

### Fallback Support
Tools also support direct parameter passing for backward compatibility:
- `__token__` or `personal_api`: Personal API token
- `app_id`: AppSignal App ID

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up credentials (optional, can be passed dynamically):
```bash
export APPSIGNAL_PERSONAL_API="gl5tk_WvUKDCkVbgXTaKzg"
export APPSIGNAL_APP_ID="68639bbe15207808b81b328b"
```

## Usage

### Running the Server
```bash
python -m src.mcp_appsignal.server
```

### Testing Dynamic Credentials
```bash
python test_dynamic_credentials.py
```

### Example MCP Client Usage
```python
# Credentials are automatically injected
payload = {
    "selected_server": "MCP-APPSIGNAL",
    "selected_server_credentials": {
        "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
        "app_id": "68639bbe15207808b81b328b"
    },
    "client_details": {
        "input": "Get all errors for my application"
    }
}

# The server will automatically use the injected credentials
result = await client_and_server_execution(payload)
```

## Available Tools

### 1. Search Errors
Search for exception errors using AppSignal's GraphQL API.

**Required Parameters:**
- `organization_slug`: Your AppSignal organization slug

**Optional Parameters:**
- `query_string`: Custom search query
- `namespace`: Filter by namespace

### 2. Get All Errors
Retrieve all open exception incidents.

**Parameters:**
- `limit` (optional): Number of incidents (default: 100)
- `offset` (optional): Pagination offset (default: 0)

### 3. Get Incident Details
Get detailed information about a specific incident.

**Required Parameters:**
- `incident_number`: The incident number

**Optional Parameters:**
- `sample_id`: Specific sample ID
- `timestamp`: Time-based filtering
- `timerange`: Time range array

### 4. Get All Incidents
Retrieve all performance incidents.

**Parameters:**
- `limit` (optional): Number of incidents (default: 100)
- `offset` (optional): Pagination offset (default: 0)
- `state` (optional): Filter by incident state

## API Integration

- **Base URL**: `https://appsignal.com/graphql`
- **Authentication**: Personal API token via URL parameter
- **Data Format**: GraphQL queries and responses

## Security

- Credentials are isolated per server instance
- No hardcoded credentials in tool definitions
- Support for environment variable configuration
- Personal API tokens provide read-only access to your AppSignal data

## Error Handling

- Comprehensive error handling for API failures
- Detailed error messages for missing credentials
- Graceful fallback for credential extraction
- JSON-serializable error responses

## Development

### Project Structure
```
mcp-appsignal/
├── src/
│   └── mcp_appsignal/
│       ├── __init__.py
│       ├── server.py          # Main server implementation
│       ├── appsignal.py       # AppSignal API client
│       ├── toolhandler.py     # Base tool handler
│       └── tools_errors.py    # Error-related tools
├── test_dynamic_credentials.py
├── pyproject.toml
└── README.md
```

### Adding New Tools

1. Create a new tool handler class in `tools_errors.py`
2. Inherit from `ToolHandler`
3. Implement `get_tool_description()` and `run_tool()`
4. Register the tool in `server.py`

### Testing
```bash
# Run the test script
python test_dynamic_credentials.py

# Test with actual API calls (requires valid credentials)
python -m src.mcp_appsignal.server
```

## License

This project is licensed under the MIT License. 