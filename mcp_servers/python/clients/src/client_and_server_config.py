ClientsConfig =[
    "MCP_CLIENT_AZURE_AI",
    "MCP_CLIENT_OPENAI",
	"MCP_CLIENT_GEMINI"
]
ServersConfig = [
	{
		"server_name": "MCP-APPSIGNAL",
		"command": "uv",
		"args": [
			"--directory",
			"mcp_servers/python/servers/MCP-APPSIGNAL/mcp-appsignal",
			"run",
			"mcp-appsignal"
		]
	},
	{
    "server_name": "MCP-STOCKANALYZER",
    "command": "uv",
    "args": [
        "--directory",
        "mcp_servers/python/servers/MCP-STOCKANALYZER/mcp-stockanalyzer",
        "run",
        "mcp-stockanalyzer"
    ]
	},
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
	,
	{
		"server_name": "MCP-PINGDOM",
		   "command": "python",
				"args": [
						"../servers/MCP-PINGDOM/mcp-pingdom/src/mcp_pingdom/stdio_server.py"
				]
	},
	{
		"server_name": "MCP-GOOGLECLASSROOM",
		"command": "uv",
		"args": [
			"--directory",
			"mcp_servers/python/servers/MCP-GOOGLECLASSROOM/mcp-google-classroom",
			"run",
			"server"
		]
	}
]
