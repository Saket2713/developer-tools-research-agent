# Contributing to Developer Tools Research Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature/fix
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/developer-tools-research-agent.git
cd developer-tools-research-agent

# Install dependencies
cd advanced-agent
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 🧪 Testing

Before submitting a PR, please run:

```bash
# Test precision improvements
uv run test_precision.py

# Test the main application
uv run main.py
```

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions and classes
- Keep functions focused and small
- Use type hints where appropriate

## 🐛 Bug Reports

When reporting bugs, please include:

- Python version
- UV version
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## 💡 Feature Requests

For new features, please:

- Check if it already exists
- Describe the use case
- Explain the expected behavior
- Consider backward compatibility

## 🔄 Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Use clear, descriptive commit messages

## 📞 Questions?

Feel free to open an issue for any questions or discussions about the project.
