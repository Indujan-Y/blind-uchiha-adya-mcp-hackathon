# AppSignal MCP Server Credentials

## Overview
The AppSignal MCP server requires authentication using a Personal API token and App ID to access AppSignal's GraphQL API.

## Credentials Structure
The AppSignal MCP server expects credentials in the following format:

```json
{
  "personal_api": "your_personal_api_token",
  "app_id": "your_app_id"
}
```

## Provided Credentials
For this implementation, the following credentials are configured:

```json
{
  "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
  "app_id": "68639bbe15207808b81b328b"
}
```

## Additional Information
- **Push API Key**: `884eed53-8118-4bd8-9397-dc6885bafbf1` (for reference, not used in current implementation)
- **Personal API Token**: `gl5tk_WvUKDCkVbgXTaKzg` (used for GraphQL API authentication)
- **App ID**: `68639bbe15207808b81b328b` (used to identify the specific AppSignal application)

## Usage
The credentials are automatically injected into tool calls when using the MCP client. The server supports both:

1. **Credential Injection**: Credentials are automatically passed via `__credentials__` or `server_credentials` parameters
2. **Direct Parameters**: You can also pass `personal_api` and `app_id` directly as tool parameters

## Security Notes
- Keep your Personal API token secure and do not expose it in client-side code
- The token provides access to your AppSignal organization data
- Consider using environment variables for production deployments

## API Endpoints
The server connects to AppSignal's GraphQL API at: `https://appsignal.com/graphql`

## Required Credentials

The AppSignal MCP server requires the following credentials to authenticate with the AppSignal API:

### 1. Personal API Token

**What it is:** A personal access token that provides authentication for the AppSignal GraphQL API.

**How to get it:**
1. Log in to your AppSignal dashboard
2. Navigate to **Settings** → **Personal API Tokens**
3. Click **Create new token**
4. Give your token a descriptive name
5. Select the appropriate permissions (read access for monitoring tools)
6. Copy the generated token immediately (it won't be shown again)

**Security Note:** Keep your API token secure and never commit it to version control.

### 2. Organization Slug

**What it is:** A unique identifier for your AppSignal organization.

**How to find it:**
- **Method 1:** Check your AppSignal dashboard URL
  - Format: `https://appsignal.com/apps/{organization_slug}/...`
  - The organization slug is the part after `/apps/` and before the next `/`

- **Method 2:** Check your AppSignal configuration
  - Look in your app's configuration files
  - Usually found in environment variables or config files

## Configuration Methods

### Method 1: Environment Variables (Recommended)

Create a `.env` file in the project root:

```env
APPSIGNAL_TOKEN=your_personal_api_token_here
APPSIGNAL_ORGANIZATION_SLUG=your_organization_slug_here
```

### Method 2: Direct Tool Parameters

Pass credentials directly in tool calls:

```json
{
  "__token__": "your_personal_api_token",
  "__organization_slug__": "your_organization_slug"
}
```

## Example Configuration

```env
# .env file
APPSIGNAL_TOKEN=aps_1234567890abcdef1234567890abcdef12345678
APPSIGNAL_ORGANIZATION_SLUG=my-company
```

## Permissions Required

For the MCP server to function properly, your Personal API Token should have the following permissions:

- **Read access** to error samples and incidents
- **Read access** to performance data
- **Read access** to application information

## Troubleshooting

### Common Issues

1. **"Invalid token" error**
   - Verify your token is correct and hasn't expired
   - Check that you copied the entire token

2. **"Organization not found" error**
   - Verify your organization slug is correct
   - Check the URL format in your AppSignal dashboard

3. **"Permission denied" error**
   - Ensure your token has the required read permissions
   - Contact your AppSignal administrator if needed

### Testing Your Credentials

You can test your credentials by making a simple API call:

```bash
curl -X POST "https://appsignal.com/graphql?token=YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { organization(slug: \"YOUR_ORG_SLUG\") { name } }"}'
```

## Security Best Practices

1. **Never commit credentials to version control**
2. **Use environment variables for production deployments**
3. **Rotate your API tokens regularly**
4. **Use the minimum required permissions**
5. **Monitor token usage for suspicious activity** 