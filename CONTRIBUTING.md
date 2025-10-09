# Contributing to lit-mcp

Thank you for your interest in contributing to lit-mcp! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Adding New Tools](#adding-new-tools)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md) that ensures a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

**Key principles:**

- Be respectful and inclusive in all interactions
- Use welcoming and constructive language
- Focus on what's best for the community
- Show empathy towards other community members
- Be patient with newcomers and those learning

For the complete Code of Conduct, see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Installation

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

   ```bash
   git clone https://github.com/your-username/lit-mcp.git
   cd lit-mcp
   ```

3. **Add the upstream remote**:

   ```bash
   git remote add upstream https://github.com/gauravfs-14/lit-mcp.git
   ```

## Development Setup

1. **Install uv** (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Run tests** to ensure everything works:

   ```bash
   uv run python tests/test_basic.py
   ```

4. **Test the MCP server**:

   ```bash
   # Test that the server starts (will timeout after 5 seconds)
   timeout 5 uv run lit-mcp || true
   ```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues and improve reliability
- **New tools**: Add support for new academic databases (DBLP, PubMed, etc.)
- **Enhancements**: Improve existing functionality
- **Documentation**: Improve docs, examples, and guides
- **Tests**: Add test coverage for new features

### Before You Start

1. **Check existing issues** to see if your contribution is already being worked on
2. **Open an issue** for significant changes to discuss the approach
3. **Keep changes focused** - one feature or bug fix per pull request

## Adding New Tools

### Step-by-Step Guide

1. **Create a new module** in `src/lit_mcp/utils/`:

   ```python
   # src/lit_mcp/utils/dblp.py
   import requests
   
   def search_dblp(query: str, max_results: int = 10) -> list[dict]:
       """Search DBLP database for computer science papers."""
       # Implementation here
       pass
   ```

2. **Add the tool to the main module**:

   ```python
   # src/lit_mcp/__main__.py
   from .utils.dblp import search_dblp
   
   @mcp.tool()
   def dblp_search(query: str, max_results: int = 10) -> list[dict]:
       """Search DBLP database for computer science papers.
       
       Args:
           query: The search query
           max_results: Maximum number of results to return
           
       Returns:
           List of paper dictionaries with metadata
       """
       return search_dblp(query, max_results)
   ```

3. **Add dependencies** to `pyproject.toml` if needed:

   ```toml
   dependencies = [
       "arxiv>=2.2.0",
       "httpx>=0.28.1",
       "mcp[cli]>=1.14.1",
       "requests>=2.31.0",  # New dependency
   ]
   ```

4. **Add tests** in `tests/test_basic.py`:

   ```python
   def test_dblp_search_function():
       """Test that the dblp_search function is properly decorated."""
       import lit_mcp.__main__ as main
       assert callable(main.dblp_search)
   ```

### Tool Development Best Practices

- **Follow the existing pattern**: Use the same structure as `arxiv_search`
- **Add comprehensive docstrings**: Include parameter descriptions and return types
- **Handle errors gracefully**: Use try-catch blocks for network requests
- **Return consistent data**: Follow the same dictionary structure as existing tools
- **Add type hints**: Use proper type annotations for all functions

## Testing

### Running Tests

```bash
# Run all tests
uv run python tests/test_basic.py

# Run with verbose output
uv run python -m pytest tests/ -v
```

### Test Requirements

- **All tests must pass** before submitting a PR
- **Add tests for new functionality**
- **Update existing tests** if you change behavior
- **Test error conditions** and edge cases

### Writing Good Tests

```python
def test_new_tool():
    """Test the new tool functionality."""
    import lit_mcp.__main__ as main
    
    # Test that the function exists
    assert callable(main.new_tool)
    
    # Test with a simple query
    try:
        results = main.new_tool("test query", max_results=1)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0], dict)
            assert 'title' in results[0]
    except Exception as e:
        # Handle API failures gracefully in tests
        print(f"API call failed (expected in some environments): {e}")
```

## Submitting Changes

### Pull Request Process

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write your code
   - Add tests
   - Update documentation
   - Run tests to ensure everything works

3. **Commit your changes**:

   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

4. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request** on GitHub

### Pull Request Guidelines

- **Use descriptive titles** that explain what the PR does
- **Provide a detailed description** of changes and motivation
- **Link to related issues** using "Fixes #123" or "Closes #123"
- **Include screenshots** for UI changes
- **Update documentation** for new features
- **Ensure all tests pass** in CI

### Commit Message Format

Use clear, descriptive commit messages:

```
Add feature: DBLP search support

- Add DBLP API integration
- Add dblp_search tool function
- Update tests for new functionality
- Add documentation for DBLP usage
```

## Project Structure

```
lit-mcp/
├── src/lit_mcp/           # Main package code
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # MCP server entry point
│   └── utils/             # Utility modules
│       ├── __init__.py    # Utils package
│       └── arxiv.py       # arXiv integration
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_basic.py      # Basic functionality tests
├── .github/workflows/     # GitHub Actions
│   ├── ci.yml            # Continuous Integration
│   └── publish.yml        # Publishing workflow
├── pyproject.toml         # Project configuration
├── README.md             # Main documentation
├── CONTRIBUTING.md       # This file
└── LICENSE               # MIT License
```

## Development Workflow

### Daily Development

1. **Sync with upstream**:

   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes and test**:

   ```bash
   # Make your changes
   uv run python tests/test_basic.py
   ```

4. **Commit and push**:

   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin feature/your-feature
   ```

### Code Style

- **Follow PEP 8** for Python code style
- **Use type hints** for function parameters and return types
- **Write docstrings** for all public functions
- **Use meaningful variable names**
- **Keep functions focused** and single-purpose

### Documentation

- **Update README.md** for user-facing changes
- **Add docstrings** to all new functions
- **Update examples** if you add new tools
- **Keep CONTRIBUTING.md** up to date

## Getting Help

If you need help:

1. **Check existing issues** for similar problems
2. **Open a new issue** with detailed information
3. **Join discussions** in GitHub Discussions
4. **Ask questions** in your pull request

## Recognition

Contributors will be recognized in:

- **README.md** acknowledgments
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to lit-mcp! 🎉
