# Project Structure

This document explains the organization and architecture of the Developer Tools Research Agent.

## 📁 Directory Structure

```
developer-tools-research-agent/
├── README.md                 # Main project documentation
├── LICENSE                   # MIT license
├── CHANGELOG.md             # Version history and changes
├── CONTRIBUTING.md          # Contribution guidelines
├── .gitignore              # Git ignore rules
│
├── docs/                   # Documentation
│   └── PROJECT_STRUCTURE.md # This file
│
├── advanced-agent/         # Main application directory
│   ├── .env.example       # Environment configuration template
│   ├── .env               # Your API keys (not in git)
│   ├── pyproject.toml     # UV project configuration
│   ├── uv.lock           # Dependency lock file
│   │
│   ├── src/              # Source code
│   │   ├── __init__.py
│   │   ├── models.py     # Pydantic data models
│   │   ├── prompts.py    # LLM prompts and templates
│   │   ├── workflow.py   # LangGraph workflow logic
│   │   └── utils.py      # Utility functions
│   │
│   ├── main.py           # Application entry point
│   ├── test_precision.py # Validation testing
│   └── exports/          # Generated export files
│
└── simple-agent/          # MCP-based simple agent (legacy)
    └── ...                # Simple agent files
```

## 🏗️ Architecture Components

### Core Files

#### `main.py`
- **Purpose**: Application entry point and user interface
- **Key Features**:
  - Rich terminal interface setup
  - User input handling
  - Workflow orchestration
  - Interactive menu system
  - Export functionality

#### `src/workflow.py`
- **Purpose**: LangGraph state machine implementation
- **Key Components**:
  - `Workflow` class with state management
  - Tool extraction and validation logic
  - Market leaders identification
  - Individual tool analysis
  - Multi-layer filtering system

#### `src/models.py`
- **Purpose**: Pydantic data models for type safety
- **Models**:
  - `Company`: Tool/company information
  - `DetailedAnalysis`: Comprehensive tool analysis
  - `ComparisonMatrix`: Side-by-side comparisons
  - `WorkflowState`: LangGraph state management

#### `src/prompts.py`
- **Purpose**: LLM prompts and templates
- **Key Prompts**:
  - `TOOL_EXTRACTION_SYSTEM`: Tool discovery and filtering
  - `TOOL_ANALYSIS_SYSTEM`: Individual tool analysis
  - `COMPARISON_SYSTEM`: Tool comparison logic
  - `MARKET_LEADERS_SYSTEM`: Market leader identification

### Data Flow

```
User Input → Workflow State → Market Leaders → Tool Extraction → 
Validation → Individual Analysis → Rich Output → Interactive Options
```

### Key Design Patterns

#### 1. **State Machine Pattern (LangGraph)**
- Manages complex workflow states
- Enables persistence and debugging
- Handles error recovery and retries

#### 2. **Multi-Layer Validation**
- Pattern matching for exclusions
- Whitelist validation for known tools
- Context-aware disambiguation
- Technical indicator detection

#### 3. **Rich Terminal Interface**
- Professional formatting with Rich library
- Interactive menus and options
- Progress indicators and status updates
- Clean card-based layouts

## 🔧 Configuration Files

### `pyproject.toml`
- UV project configuration
- Dependencies and versions
- Python version requirements
- Build settings

### `.env` / `.env.example`
- API key configuration
- Optional performance settings
- Debug mode toggles
- Model selection overrides

## 🧪 Testing

### `test_precision.py`
- Validates tool extraction accuracy
- Tests filtering across multiple categories
- Ensures precision improvements work
- Provides performance benchmarks

## 📊 Data Models

### Company Model
```python
class Company(BaseModel):
    name: str
    description: str
    pricing_model: str
    is_open_source: Optional[bool]
    tech_stack: List[str]
    api_available: Optional[bool]
    language_support: List[str]
    integration_capabilities: List[str]
    competitors: List[str]
    
    # Market intelligence
    market_position: str
    company_size: str
    funding_status: str
    user_base_size: str
    github_stars: Optional[int]
    market_trends: List[str]
```

### Workflow State
```python
class WorkflowState(TypedDict):
    query: str
    companies: List[Company]
    analysis: str
    market_leaders: List[str]
```

## 🚀 Performance Optimizations

1. **Concurrent Processing**: Parallel tool analysis
2. **Smart Caching**: Reduced redundant API calls
3. **Efficient State Management**: LangGraph optimization
4. **Rate Limit Handling**: Graceful degradation
5. **Memory Management**: Efficient data structures

## 🔍 Search Strategy

### Enhanced Query Processing
- Developer-specific term injection
- Query optimization for technical content
- Fallback mechanisms for edge cases
- Context-aware search refinement

### Validation Pipeline
1. **Pattern Matching**: Exclude non-developer businesses
2. **Whitelist Check**: Known legitimate tools
3. **Technical Indicators**: Developer-specific terminology
4. **Context Validation**: Query relevance assessment
5. **Final Filtering**: Quality assurance checks

This architecture ensures reliable, accurate, and fast developer tool research across all categories.
