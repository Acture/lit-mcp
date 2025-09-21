# lit-mcp (Literature Review Assistant MCP Server)

A powerful Model Context Protocol (MCP) server that provides seamless access to academic literature databases, helping researchers accelerate their literature review process using LLMs and MCP clients like Claude, Cursor, and others.

## 🚀 Features

- **arXiv Integration**: Search and retrieve academic papers from arXiv
- **MCP Compatible**: Works with any MCP client (Claude, Cursor, etc.)
- **Structured Data**: Returns well-formatted paper metadata
- **Fast & Reliable**: Built on FastMCP for optimal performance
- **Extensible**: Easy to add new academic databases

## 🛠️ Installation

### Prerequisites

- Python 3.12
- uv package manager

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/gauravfs-14/lit-mcp.git
   cd lit-mcp
   ```

2. **Install dependencies**

   Install UV with this command if not already installed.

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Now that we have UV setup, let's install the dependencies.

   ```bash
   uv sync
   ```

3. **Run the MCP server**

   ```bash
   uv run main.py
   ```

## 📖 Usage

### Available Tools

#### `arxiv_search`

Search for academic papers on arXiv with advanced query capabilities.

**Parameters:**

- `query` (string): Search query (supports arXiv syntax like `au:Author_Name`, `ti:Title`, etc.)
- `max_results` (integer, optional): Maximum number of results (default: 10)

**Returns:**

- List of paper objects with title, authors, publication date, summary, PDF URL, categories, and DOI

**Example Queries:**

```python
# Search by author
"au:Gaurab_Chhetri"

# Search by title keywords
"ti:machine learning"

# Search by category
"cat:cs.AI"

# Combined search
"au:Chhetri AND ti:transport"
```

### MCP Client Integration

#### Example: With Cursor

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "lit-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<absolute_path_to_the_cloned_repo>",
        "run",
        "main.py"
      ]
    }
  }
}
```

## 🔧 Development

### Project Structure

```bash
lit-mcp/
├── main.py              # MCP server entry point
├── utils/
│   ├── __init__.py      # Package initialization
│   └── arxiv.py         # arXiv API wrapper
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

### Adding New Tools

1. Create a new function in `utils/` directory
2. Add the `@mcp.tool()` decorator
3. Update the imports in `main.py`

Example:

```python
@mcp.tool()
def dblp_search(query: str, max_results: int = 10) -> list[dict]:
    """Search DBLP database for computer science papers."""
    # Implementation here
    pass
```

## 📊 Example Output

```json
{
  "title": "Model Context Protocols in Adaptive Transport Systems: A Survey",
  "authors": ["Gaurab Chhetri", "Shriyank Somvanshi", "..."],
  "published": "2025-08-26T17:58:56+00:00",
  "summary": "The rapid expansion of interconnected devices...",
  "entry_id": "http://arxiv.org/abs/2508.19239v1",
  "pdf_url": "http://arxiv.org/pdf/2508.19239v1",
  "categories": ["cs.AI"],
  "doi": null
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [arXiv](https://arxiv.org/) for providing free access to academic papers
- [arxiv-py](https://pypi.org/project/arxiv/) developers for the excellent Python wrapper
- [FastMCP](https://github.com/modelcontextprotocol/fastmcp) for the MCP server framework

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/lit-mcp/issues) page
2. Create a new issue with detailed information
3. Join our community discussions
