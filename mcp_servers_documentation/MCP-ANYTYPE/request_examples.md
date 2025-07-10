# MCP-ANYTYPE Server Request Examples

## Updated Request Bodies (API Token Only)

### 1. **List Spaces** (No parameters required)
```json
{
  "name": "list_spaces",
  "arguments": {
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 2. **Create Space**
```json
{
  "name": "create_space",
  "arguments": {
    "name": "My New Workspace",
    "description": "A workspace for project management",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 3. **Get Space**
```json
{
  "name": "get_space",
  "arguments": {
    "space_id": "your_space_id_here",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 4. **Update Space**
```json
{
  "name": "update_space",
  "arguments": {
    "space_id": "your_space_id_here",
    "name": "Updated Workspace Name",
    "description": "Updated workspace description",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 5. **List Space Objects**
```json
{
  "name": "list_space_objects",
  "arguments": {
    "space_id": "your_space_id_here",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 6. **Create Object in Space**
```json
{
  "name": "create_object_in_space",
  "arguments": {
    "space_id": "your_space_id_here",
    "name": "My New Page",
    "body": "This is the content of my new page",
    "type_key": "page",
    "template_id": "your_template_id_here",
    "icon": {
      "emoji": "📄",
      "format": "emoji"
    },
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 7. **Update Object**
```json
{
  "name": "update_object",
  "arguments": {
    "space_id": "your_space_id_here",
    "object_id": "your_object_id_here",
    "name": "Updated Object Name",
    "icon": {
      "emoji": "📝",
      "format": "emoji"
    },
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 8. **Delete Object**
```json
{
  "name": "delete_object",
  "arguments": {
    "space_id": "your_space_id_here",
    "object_id": "your_object_id_here",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 9. **Search Objects**
```json
{
  "name": "search_objects",
  "arguments": {
    "query": "project management",
    "sort": {
      "direction": "desc",
      "property_key": "last_modified_date"
    },
    "types": ["page", "task", "bookmark"],
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

### 10. **List Type Templates**
```json
{
  "name": "list_type_templates",
  "arguments": {
    "space_id": "your_space_id_here",
    "type_id": "your_type_id_here",
    "__credentials__": {
      "api_token": "your_anytype_api_token"
    }
  }
}
```

## Gemini Client Request Examples

### Basic Request Format
```json
{
  "selected_server_credentials": {
    "MCP-ANYTYPE": {
      "api_token": "your_anytype_api_token"
    }
  },
  "client_details": {
    "api_key": "your_gemini_api_key",
    "temperature": 0.1,
    "max_token": 20000,
    "input": "list all my spaces",
    "input_type": "text",
    "prompt": "you are a helpful assistant",
    "chat_model": "gemini-2.0-flash-lite",
    "chat_history": [
      {
        "role": "user",
        "content": "Hello"
      }
    ]
  },
  "selected_client": "MCP_CLIENT_GEMINI",
  "selected_servers": [
    "MCP-ANYTYPE"
  ]
}
```

### Example Natural Language Requests

1. **List Spaces**: `"input": "list all my spaces"`
2. **Create Space**: `"input": "create a new space called 'Project Management' with description 'Workspace for managing projects and tasks'"`
3. **Get Space**: `"input": "get details for space with ID 'your_space_id_here'"`
4. **Update Space**: `"input": "update space with ID 'your_space_id_here' to have name 'Updated Workspace' and description 'Updated description'"`
5. **List Objects**: `"input": "list all objects in space with ID 'your_space_id_here'"`
6. **Create Object**: `"input": "create a new page in space 'your_space_id_here' with name 'My New Page', body 'This is the content of my new page', type 'page', template ID 'your_template_id_here', and emoji icon '📄'"`
7. **Update Object**: `"input": "update object with ID 'your_object_id_here' in space 'your_space_id_here' to have name 'Updated Object' and emoji icon '📝'"`
8. **Delete Object**: `"input": "delete object with ID 'your_object_id_here' from space 'your_space_id_here'"`
9. **Search Objects**: `"input": "search for objects with query 'project management', sorted by last modified date in descending order, for types 'page', 'task', and 'bookmark'"`
10. **List Templates**: `"input": "list all templates for type ID 'your_type_id_here' in space 'your_space_id_here'"`

## Notes

- Replace `your_anytype_api_token` with your actual Anytype API token
- Replace `your_gemini_api_key` with your actual Gemini API key
- Replace `your_space_id_here`, `your_object_id_here`, etc. with actual IDs from your Anytype workspace
- The base URL is statically set to `http://localhost:31009` and cannot be changed
- Make sure your Anytype application is running and accessible at `http://localhost:31009` 