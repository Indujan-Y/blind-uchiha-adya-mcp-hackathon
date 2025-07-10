# Anytype MCP Server - Credentials Setup

## Overview

The Anytype MCP server requires authentication using a Bearer token to interact with the Anytype API.

## Required Credentials

### API Token
- **Type**: Bearer Token
- **Source**: Anytype API
- **Required**: Yes

## Setup Instructions

### 1. Get Your Anytype API Token

1. Open Anytype application
2. Go to Settings → API
3. Generate a new API token
4. Copy the token to a secure location

### 2. Configure Environment Variables

Create a `.env` file in the MCP server directory with the following variables:

```env
ANYTYPE_API_TOKEN=your_anytype_api_token_here
```

### 3. Alternative Configuration

You can also set this environment variable in your system:

```bash
export ANYTYPE_API_TOKEN=your_anytype_api_token_here
```

## API Base URL

The API base URL is statically set to `http://localhost:31009`. This assumes you're running the Anytype API locally. The base URL cannot be changed through configuration and is hardcoded in the server.

## Security Notes

- Keep your API token secure and never commit it to version control
- The token provides full access to your Anytype workspace
- Rotate tokens regularly for security
- Use environment variables instead of hardcoding tokens in your code

## Troubleshooting

### Common Issues

1. **"Anytype API token is required" error**
   - Ensure `ANYTYPE_API_TOKEN` is set in your environment
   - Check that the `.env` file is in the correct location

2. **Connection refused errors**
   - Verify that the Anytype API is running on port 31009
   - Check that the Anytype application is accessible at `http://localhost:31009`

3. **Authentication errors**
   - Verify your API token is valid and not expired
   - Ensure the token has the necessary permissions 