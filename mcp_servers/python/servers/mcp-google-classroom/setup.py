from setuptools import setup, find_packages

setup(
    name="mcp-google-classroom",
    version="0.1.0",
    description="MCP server for Google Classroom",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    python_requires=">=3.10",
    packages=find_packages(include=["mcp_googleclassroom", "mcp_googleclassroom.*"]),
    install_requires=[
        "mcp>=1.1.0",
        "requests>=2.32.3",
        "python-dotenv>=1.0.1",
        "google-api-python-client>=2.108.0",
        "google-auth>=2.23.4",
        "google-auth-oauthlib>=1.1.0",
        "google-auth-httplib2>=0.1.1",
    ],
    extras_require={
        "dev": [
            "pyright>=1.1.389",
        ],
    },
    entry_points={
        "console_scripts": [
            "server = mcp_googleclassroom:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
