#!/usr/bin/env python3
"""
Test script for the Anytype MCP Server
"""

import asyncio
import json
import os
from dotenv import load_dotenv
from src.mcp_anytype.anytype import AnytypeClient

load_dotenv()

def test_anytype_client():
    """Test the AnytypeClient class"""
    print("Testing AnytypeClient...")
    
    try:
        # Initialize client
        client = AnytypeClient()
        print("✓ AnytypeClient initialized successfully")
        
        # Test list spaces
        print("\nTesting list_spaces...")
        spaces = client.list_spaces()
        print(f"✓ Found {len(spaces.get('spaces', []))} spaces")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_mcp_server():
    """Test the MCP server tools"""
    print("\nTesting MCP Server Tools...")
    
    try:
        from src.mcp_anytype import tools_anytype
        
        # Test tool handlers
        handlers = [
            tools_anytype.ListSpacesToolHandler(),
            tools_anytype.CreateSpaceToolHandler(),
            tools_anytype.GetSpaceToolHandler(),
            tools_anytype.UpdateSpaceToolHandler(),
            tools_anytype.ListSpaceObjectsToolHandler(),
            tools_anytype.CreateObjectInSpaceToolHandler(),
            tools_anytype.UpdateObjectToolHandler(),
            tools_anytype.DeleteObjectToolHandler(),
            tools_anytype.SearchObjectsToolHandler(),
            tools_anytype.ListTypeTemplatesToolHandler(),
        ]
        
        print(f"✓ Created {len(handlers)} tool handlers")
        
        # Test tool descriptions
        for handler in handlers:
            tool_desc = handler.get_tool_description()
            print(f"✓ Tool '{tool_desc.name}': {tool_desc.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_list_spaces_tool():
    """Test the list_spaces tool specifically"""
    print("\nTesting list_spaces tool...")
    
    try:
        from src.mcp_anytype import tools_anytype
        
        handler = tools_anytype.ListSpacesToolHandler()
        result = handler.run_tool({})
        
        print("✓ list_spaces tool executed successfully")
        print(f"✓ Result type: {type(result)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Main test function"""
    print("Anytype MCP Server Test Suite")
    print("=" * 40)
    
    # Check environment
    token = os.getenv('ANYTYPE_API_TOKEN')
    if not token:
        print("⚠️  Warning: ANYTYPE_API_TOKEN not set")
        print("   Some tests may fail without proper authentication")
    else:
        print("✓ ANYTYPE_API_TOKEN found")
    
    base_url = os.getenv('ANYTYPE_API_BASE_URL', 'http://localhost:31009')
    print(f"✓ Using API base URL: {base_url}")
    
    # Run tests
    tests = [
        ("MCP Server Tools", test_mcp_server),
        ("AnytypeClient", test_anytype_client),
        ("List Spaces Tool", test_list_spaces_tool),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*20} Test Summary {'='*20}")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The MCP server is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the configuration and try again.")

if __name__ == "__main__":
    main() 