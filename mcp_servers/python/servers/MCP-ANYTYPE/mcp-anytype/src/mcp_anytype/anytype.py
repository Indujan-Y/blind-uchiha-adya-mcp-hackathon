import requests
import json
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

# Static base URL for Anytype API
ANYTYPE_BASE_URL = "http://localhost:31009"

class AnytypeClient:
    """Client for interacting with the Anytype API."""
    
    def __init__(self, token: Optional[str] = None, credentials: Optional[Dict[str, Any]] = None):
       
        print("credentials", credentials  )
        # Priority: credentials dict > token parameter > environment variable
        if credentials and isinstance(credentials, dict):
            self.token = credentials.get('token') or credentials.get('api_token') or credentials.get('ANYTYPE_API_TOKEN')
            
       
        
        # Use static base URL - ensure it's always set
        self.base_url = ANYTYPE_BASE_URL
        
        
        if not self.token:
            raise ValueError("Anytype API token is required. Set ANYTYPE_API_TOKEN environment variable, pass token parameter, or provide credentials dict with 'api_token' key.")
        
        # Validate base URL is set
        if not self.base_url:
            raise ValueError("Base URL is not set. This should not happen with the static configuration.")
        
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
    
    def search_objects(self, query: str, sort: Dict[str, str], types: List[str]) -> Dict[str, Any]:
        """Search for objects across all spaces."""
        url = f"http://localhost:31009/v1/search"
        
        payload = {
            "query": query,
            "sort": sort,
            "types": types
        }
        
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    
    def list_spaces(self) -> Dict[str, Any]:
        """Retrieve a list of all spaces."""
        url = f"http://localhost:31009/v1/spaces"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def create_space(self, name: str, description: str) -> Dict[str, Any]:
        """Create a new space."""
        url = f"http://localhost:31009/v1/spaces"
        payload = {
            "name": name,
            "description": description
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Space '{name}' added successfully. just now ",
            "data": data
        }
    
    def get_space(self, space_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def update_space(self, space_id: str, name: str, description: str) -> Dict[str, Any]:
        """Update a specific space's name and description."""
        url = f"http://localhost:31009/v1/spaces/{space_id}"
        payload = {
            "name": name,
            "description": description
        }
        response = requests.patch(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Space '{space_id}' updated successfully.",
            "data": data
        }
    
    def list_space_objects(self, space_id: str) -> Dict[str, Any]:
        """Retrieve all objects in a specific space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}/objects"
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def create_object_in_space(self, space_id: str, name: str, body: str, 
                              type_key: str, template_id: str, icon: Dict[str, str]) -> Dict[str, Any]:
        """Create an object in a specific space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}/objects"
        payload = {
            "name": name,
            "body": body,
            "type_key": type_key,
            "template_id": template_id,
            "icon": icon
        }
        response = requests.post(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Object '{name}' added successfully to space '{space_id}' just now.",
            "data": data
        }
    
    def delete_object_in_space(self, space_id: str, object_id: str) -> Dict[str, Any]:
        """Delete an object in a specific space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}/objects/{object_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Object '{object_id}' deleted successfully from space '{space_id}'.",
            "data": data
        }
    
    def list_type_templates(self, space_id: str, type_id: str) -> Dict[str, Any]:
        """Retrieve all templates for a specific type in a space."""
    
        
        url = f"http://localhost:31009/v1/spaces/{space_id}/types/{type_id}/templates"
        
        
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def delete_object(self, space_id: str, object_id: str) -> Dict[str, Any]:
        """Delete a specific object in a space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}/objects/{object_id}"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Object '{object_id}' deleted successfully from space '{space_id}'.",
            "data": data
        }
    
    def update_object(self, space_id: str, object_id: str, name: str, icon: Dict[str, str]) -> Dict[str, Any]:
        """Update an object in a specific space."""
        url = f"http://localhost:31009/v1/spaces/{space_id}/objects/{object_id}"
        
        payload = {
            "name": name,
            "icon": icon,
        }
        
        response = requests.patch(url, headers=self._get_headers(), json=payload)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "message": f"Object '{object_id}' updated successfully in space '{space_id}'.",
            "data": data
        } 