# Anytype MCP Server - Features

## Overview

The Anytype MCP server provides comprehensive integration with the Anytype API, allowing AI assistants to manage spaces, objects, and perform searches within Anytype workspaces.

## Available Tools

### Space Management

#### `list_spaces`
- **Description**: Retrieve a list of all spaces in Anytype
- **Parameters**: None
- **Returns**: JSON array of all available spaces
- **Use Case**: Get an overview of all workspaces before performing operations

#### `create_space`
- **Description**: Create a new space in Anytype
- **Parameters**:
  - `name` (string): Name of the space to create
  - `description` (string): Description of the space
- **Returns**: JSON object with the created space details
- **Use Case**: Set up new workspaces for different projects or topics

#### `get_space`
- **Description**: Retrieve details of a specific space
- **Parameters**:
  - `space_id` (string): ID of the space to retrieve
- **Returns**: JSON object with space details
- **Use Case**: Get specific information about a workspace

#### `update_space`
- **Description**: Update a specific space's name and description
- **Parameters**:
  - `space_id` (string): ID of the space to update
  - `name` (string): New name for the space
  - `description` (string): New description for the space
- **Returns**: JSON object with updated space details
- **Use Case**: Modify workspace metadata

### Object Management

#### `list_space_objects`
- **Description**: Retrieve all objects in a specific space
- **Parameters**:
  - `space_id` (string): ID of the space
- **Returns**: JSON array of all objects in the space
- **Use Case**: Browse contents of a workspace

#### `create_object_in_space`
- **Description**: Create an object in a specific space
- **Parameters**:
  - `space_id` (string): ID of the space where to create the object
  - `name` (string): Name of the object
  - `body` (string): Body content of the object
  - `type_key` (string): Type key of the object (e.g., 'page', 'task', 'bookmark')
  - `template_id` (string): Template ID for the object
  - `icon` (object): Icon configuration (e.g., {'emoji': '📄', 'format': 'emoji'})
- **Returns**: JSON object with the created object details
- **Use Case**: Create new pages, tasks, or other content types

#### `update_object`
- **Description**: Update an object in a specific space
- **Parameters**:
  - `space_id` (string): ID of the space containing the object
  - `object_id` (string): ID of the object to update
  - `name` (string): New name for the object
  - `icon` (object): New icon configuration
- **Returns**: JSON object with updated object details
- **Use Case**: Modify existing content

#### `delete_object`
- **Description**: Delete an object from a space
- **Parameters**:
  - `space_id` (string): ID of the space containing the object
  - `object_id` (string): ID of the object to delete
- **Returns**: JSON object with deletion confirmation
- **Use Case**: Remove unwanted content

### Search and Discovery

#### `search_objects`
- **Description**: Search for objects across all spaces with various filters
- **Parameters**:
  - `query` (string): Search query string
  - `sort` (object): Sorting configuration (e.g., {'direction': 'desc', 'property_key': 'last_modified_date'})
  - `types` (array): List of object types to search for (e.g., ['page', 'task', 'bookmark'])
- **Returns**: JSON object with search results
- **Use Case**: Find specific content across all workspaces

#### `list_type_templates`
- **Description**: Retrieve all templates for a specific type in a space
- **Parameters**:
  - `space_id` (string): ID of the space
  - `type_id` (string): ID of the type
- **Returns**: JSON array of available templates
- **Use Case**: Discover available templates for creating new objects

## Object Types

The Anytype API supports various object types:

- **page**: Regular pages/documents
- **task**: Task items with status tracking
- **bookmark**: Web bookmarks and links
- **note**: Quick notes
- **collection**: Collections of objects
- **set**: Sets of related items

## Icon Formats

Objects can have icons in different formats:

- **Emoji**: `{'emoji': '📄', 'format': 'emoji'}`
- **Image**: `{'image': 'url_to_image', 'format': 'image'}`
- **None**: `{'format': 'none'}`

## Error Handling

The server provides comprehensive error handling:

- **Missing Parameters**: Clear error messages for required parameters
- **API Errors**: Proper HTTP error handling and reporting
- **Authentication Errors**: Token validation and refresh handling
- **Network Errors**: Connection timeout and retry logic

## Performance Considerations

- **Batch Operations**: Consider using search for bulk operations
- **Caching**: The server doesn't implement caching; consider client-side caching for frequently accessed data
- **Rate Limiting**: Respect Anytype API rate limits

## Integration Examples

### Creating a Project Workspace
1. Use `create_space` to set up a new project workspace
2. Use `list_type_templates` to find appropriate templates
3. Use `create_object_in_space` to add project documentation

### Content Discovery
1. Use `list_spaces` to see all available workspaces
2. Use `search_objects` to find specific content
3. Use `get_space` and `list_space_objects` to explore workspace contents

### Content Management
1. Use `create_object_in_space` to add new content
2. Use `update_object` to modify existing content
3. Use `delete_object` to remove outdated content 