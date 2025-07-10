# AppSignal MCP Server Features

## Overview
The AppSignal MCP server provides programmatic access to AppSignal's monitoring and error tracking capabilities through their GraphQL API.

## Available Tools

### 1. Search Errors (`search_appsignal_errors`)
Search for exception errors in AppSignal using the Search GraphQL API.

**Parameters:**
- `organization_slug` (required): AppSignal organization slug
- `query_string` (optional): Search query string
- `namespace` (optional): Filter errors by namespace

**Credentials:** Automatically injected via `personal_api` token

### 2. Get All Errors (`get_appsignal_all_errors`)
Get all open exception incidents from AppSignal.

**Parameters:**
- `limit` (optional): Number of incidents to fetch (default: 100)
- `offset` (optional): Offset for pagination (default: 0)

**Credentials:** Automatically injected via `personal_api` token and `app_id`

### 3. Get Incident Details (`get_appsignal_incident_details`)
Get detailed information for a specific incident.

**Parameters:**
- `incident_number` (required): Incident number
- `sample_id` (optional): Sample ID
- `timestamp` (optional): Timestamp
- `timerange` (optional): Time range array

**Credentials:** Automatically injected via `personal_api` token and `app_id`

### 4. Get All Incidents (`get_appsignal_all_incidents`)
Get all performance incidents from AppSignal.

**Parameters:**
- `limit` (optional): Number of incidents to fetch (default: 100)
- `offset` (optional): Offset for pagination (default: 0)
- `state` (optional): Incident state filter

**Credentials:** Automatically injected via `personal_api` token and `app_id`

## Dynamic Credential System

The server now supports dynamic credential injection:

### Credential Injection
When using the MCP client, credentials are automatically injected into tool calls:
```json
{
  "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
  "app_id": "68639bbe15207808b81b328b"
}
```

### Fallback Support
Tools also support direct parameter passing for backward compatibility:
- `__token__` or `personal_api`: Personal API token
- `app_id`: AppSignal App ID

## API Integration
- **Base URL**: `https://appsignal.com/graphql`
- **Authentication**: Personal API token via URL parameter
- **Data Format**: GraphQL queries and responses

## Error Handling
- Comprehensive error handling for API failures
- Detailed error messages for missing credentials
- Graceful fallback for credential extraction

## Security Features
- Credential isolation per server instance
- No hardcoded credentials in tool definitions
- Support for environment variable configuration

## Data Types

### Error Samples
- **ID**: Unique identifier for the error sample
- **Time**: Timestamp of when the error occurred
- **Action**: The action/endpoint where the error occurred
- **Namespace**: Application namespace (web, background, etc.)
- **Exception**: Error details including name and message
- **Incident**: Associated incident information
- **App**: Application details

### Incidents
- **ID**: Unique incident identifier
- **Number**: Incident number for reference
- **Count**: Number of occurrences
- **Last Occurred**: Timestamp of last occurrence
- **Exception Name**: Type of exception
- **Action Names**: Affected actions/endpoints
- **Namespace**: Application namespace
- **Severity**: Error severity level
- **State**: Current incident state

### Performance Data
- **Duration**: Response time metrics
- **Overview**: Performance metrics and key-value pairs
- **Notification Threshold**: Performance thresholds
- **Description**: Performance incident description

## Integration Capabilities

### Error Monitoring Workflows
1. **Proactive Monitoring**: Regularly check for new errors
2. **Error Analysis**: Get detailed information about specific errors
3. **Trend Analysis**: Monitor error patterns over time
4. **Alert Integration**: Use error data for alerting systems

### Performance Monitoring Workflows
1. **Performance Tracking**: Monitor application performance metrics
2. **Bottleneck Identification**: Identify slow operations
3. **Threshold Monitoring**: Track performance against thresholds
4. **Performance Optimization**: Use data for optimization decisions

## Performance Considerations

- **Pagination Support**: Large datasets are handled efficiently
- **Optional Filtering**: Reduce data transfer with targeted queries
- **Caching**: Consider implementing caching for frequently accessed data
- **Rate Limiting**: Respect AppSignal API rate limits

## Future Enhancements

Potential future features could include:
- Error resolution tracking
- Custom alert creation
- Performance metric aggregation
- Multi-application dashboard data
- Historical trend analysis
- Integration with external monitoring tools 