#!/usr/bin/env python3
"""
Test script for AppSignal MCP Server Dynamic Credentials

This script demonstrates how the dynamic credential system works
with the AppSignal MCP server.
"""

import json
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mcp_appsignal.tools_errors import (
    SearchErrorsToolHandler,
    GetAllErrorsToolHandler,
    GetIncidentDetailsToolHandler,
    GetAllIncidentsToolHandler
)

# Test credentials
TEST_CREDENTIALS = {
    "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
    "app_id": "68639bbe15207808b81b328b"
}

def test_credential_extraction():
    """Test the credential extraction functionality."""
    print("🧪 Testing AppSignal MCP Server Dynamic Credentials\n")
    
    # Test tools
    tools = [
        ("Search Errors", SearchErrorsToolHandler()),
        ("Get All Errors", GetAllErrorsToolHandler()),
        ("Get Incident Details", GetIncidentDetailsToolHandler()),
        ("Get All Incidents", GetAllIncidentsToolHandler())
    ]
    
    for tool_name, tool_handler in tools:
        print(f"📋 Testing {tool_name} Tool")
        print(f"   Tool Name: {tool_handler.name}")
        
        # Test with credential injection
        print("   🔐 Testing with credential injection...")
        try:
            args_with_creds = {
                "__credentials__": TEST_CREDENTIALS,
                "organization_slug": "test-org"  # For search tool
            }
            
            personal_api, app_id = tool_handler.extract_credentials(args_with_creds)
            print(f"   ✅ Credentials extracted successfully:")
            print(f"      Personal API: {personal_api[:8]}...")
            print(f"      App ID: {app_id}")
            
        except Exception as e:
            print(f"   ❌ Error with credential injection: {e}")
        
        # Test with server credentials
        print("   🔐 Testing with server credentials...")
        try:
            args_with_server_creds = {
                "server_credentials": TEST_CREDENTIALS,
                "organization_slug": "test-org"  # For search tool
            }
            
            personal_api, app_id = tool_handler.extract_credentials(args_with_server_creds)
            print(f"   ✅ Server credentials extracted successfully:")
            print(f"      Personal API: {personal_api[:8]}...")
            print(f"      App ID: {app_id}")
            
        except Exception as e:
            print(f"   ❌ Error with server credentials: {e}")
        
        # Test with direct parameters
        print("   🔐 Testing with direct parameters...")
        try:
            args_direct = {
                "__token__": TEST_CREDENTIALS["personal_api"],
                "app_id": TEST_CREDENTIALS["app_id"],
                "organization_slug": "test-org"  # For search tool
            }
            
            personal_api, app_id = tool_handler.extract_credentials(args_direct)
            print(f"   ✅ Direct parameters extracted successfully:")
            print(f"      Personal API: {personal_api[:8]}...")
            print(f"      App ID: {app_id}")
            
        except Exception as e:
            print(f"   ❌ Error with direct parameters: {e}")
        
        print()

def test_tool_schemas():
    """Test the tool schema definitions."""
    print("📋 Testing Tool Schemas\n")
    
    tools = [
        ("Search Errors", SearchErrorsToolHandler()),
        ("Get All Errors", GetAllErrorsToolHandler()),
        ("Get Incident Details", GetIncidentDetailsToolHandler()),
        ("Get All Incidents", GetAllIncidentsToolHandler())
    ]
    
    for tool_name, tool_handler in tools:
        print(f"🔧 {tool_name} Schema:")
        tool_desc = tool_handler.get_tool_description()
        
        # Check if credential parameters are included
        schema = tool_desc.inputSchema
        properties = schema.get("properties", {})
        
        has_credentials = "__credentials__" in properties
        has_server_credentials = "server_credentials" in properties
        has_token = "__token__" in properties
        
        print(f"   ✅ Credential injection support: {has_credentials}")
        print(f"   ✅ Server credentials support: {has_server_credentials}")
        print(f"   ✅ Direct token support: {has_token}")
        print(f"   📝 Description: {tool_desc.description}")
        print()

if __name__ == "__main__":
    print("🚀 AppSignal MCP Server Dynamic Credentials Test")
    print("=" * 50)
    
    # Run tests
    test_credential_extraction()
    test_tool_schemas()
    
    print("✅ All tests completed!")
    print("\n📚 Usage Example:")
    print("""
    # When using the MCP client, credentials are automatically injected:
    {
        "selected_server": "MCP-APPSIGNAL",
        "selected_server_credentials": {
            "personal_api": "gl5tk_WvUKDCkVbgXTaKzg",
            "app_id": "68639bbe15207808b81b328b"
        }
    }
    
    # The server will automatically extract and use these credentials
    # for all tool calls without requiring manual parameter passing.
    """) 