# Blind Uchiha MCP Platform

## 🚀 [MCP Integration Demo Video. (watch here)](https://drive.google.com/drive/folders/1yVGcYB9RhNDcoDs0qXCMAatWccarVXM1?usp=sharing)

[![Node.js](https://img.shields.io/badge/Node.js-20%2B-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

A comprehensive Model Context Protocol (MCP) platform providing standardized integrations between AI assistants and various services and APIs. This repository contains both JavaScript and Python implementations of MCP servers and clients for seamless service integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Python Setup](#python-setup)
- [MCP Servers](#sample-mcp-servers)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [API Collections](#api-collections)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

The Vanij MCP Platform enables AI assistants to interact with external services through a standardized protocol. It provides a unified interface for connecting to various APIs and services, making it easier to build sophisticated AI-powered applications.

## ✨ Features

- **Multi-language Support**: JavaScript and Python implementations
- **Extensible Architecture**: Easy to add new MCP servers
- **Standardized Protocol**: Consistent interface across all integrations
- **Production Ready**: Built with scalability and reliability in mind
- **Comprehensive Documentation**: Detailed guides and API references
- **Testing Tools**: Postman collections for easy testing

## 📁 Project Structure

```
.
├── mcp_servers/
│   ├── js/
│   └── python/                       # Python implementation
│       ├── clients/                  # MCP clients
│       │   ├── src/
│       │   │   ├── client_and_server_config.py       # Listed MCP Clients & Servers Configurations.
│       │   │   └── ...
│       │   ├── requirements.txt
│       │   └── ...
│       └── servers/                  # MCP servers
│           ├── MCP-PINGDOM/
│           ├── MCP-ANYTYPE/
│           ├── MCP-APPSIGNAL/
│           ├── MCP-google-classroom/
│           └── MCP-STOCKANALYZER/
├── mcp_servers_documentation/        # Detailed documentation of about MCP servers
├── postman_api_collections/         # API testing collections
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Node.js**208+ (for JavaScript implementation)
- **Python** 3.8+ (for Python implementation)
- **npm** or **yarn** (for JavaScript dependencies)
- **pip** (for Python dependencies)

### Choose Your Implementation

1. **JavaScript**: Follow the [JavaScript Setup](#javascript-setup) guide
2. **Python**: Follow the [Python Setup](#python-setup) guide
3. **Both**: Set up both implementations for maximum flexibility

## 🐍 Python Setup

### 1. Navigate to Python Directory

```bash
cd mcp_servers/python/clients
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Unix/MacOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This command automatically installs all server dependencies as well.

### 5. Run the Client

```bash
python src/main.py
```

### Configuration

Python configuration is managed in:
```
mcp_servers/python/clients/src/client_and_server_config.py
```

## 🔌 MCP Servers

### Python Implementation

| Server | Description | Status |
|--------|-------------|--------|
| **GOOGLE CLASSROOM** | Classroom Courses Management | ✅ Active |
| **APPSIGNAL** | Error Management | ✅ Active |
| **ANYTYPE** | AI based notes management | ✅ Active |
| **STOCK ANALYZER** | Stocks analytics | ✅ Active |
| **PINGDOM** | Error management | ✅ Active |

## ⚙️ Configuration

### Python Configuration

Edit `mcp_servers/python/clients/src/client_and_server_config.py`:

```python
ServersConfig = [
    {
		"server_name": "MCP-GSUITE",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-GSUITE/mcp-gsuite",
			"run",
			"mcp-gsuite"
		]
	},
    //other servers...
]
```

## 📚 Documentation

Comprehensive documentation for each MCP server is available in the `mcp_servers_documentation/` directory:

- Server-specific setup guides
- API reference documentation
- Integration examples
- Troubleshooting guides

### Key Documentation Files

- `mcp_servers_documentation/server_setup.md` - General server setup
- `mcp_servers_documentation/api_reference.md` - API documentation
- `mcp_servers_documentation/examples/` - Integration examples

## 🧪 API Collections

The `postman_api_collections/` directory contains Postman collections for testing and interacting with MCP servers:

1. Import collections into Postman
2. Configure environment variables
3. Test API endpoints
4. Validate integrations

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow existing code style and conventions
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🆘 Support

- **Documentation**: Check the `mcp_servers_documentation/` directory
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

**Built with ❤️ by the Team Team Blind Uchiha**
