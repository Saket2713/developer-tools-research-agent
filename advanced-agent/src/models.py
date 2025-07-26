from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    pricing_model: str  # Free, Freemium, Paid, Enterprise, Unknown
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    # Market intelligence fields
    market_position: str = ""  # Leader, Challenger, Niche, Emerging
    company_size: str = ""  # Startup, SMB, Enterprise, Public
    funding_status: str = ""  # Bootstrapped, Seed, Series A/B/C, IPO, Acquired
    user_base_size: str = ""  # <1K, 1K-10K, 10K-100K, 100K+, 1M+
    github_stars: Optional[int] = None
    market_trends: List[str] = []


class CompanyInfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent
    # Market intelligence fields
    market_position: Optional[str] = None  # Leader, Challenger, Niche, Emerging
    company_size: Optional[str] = None  # Startup, SMB, Enterprise, Public
    funding_status: Optional[str] = None  # Bootstrapped, Seed, Series A/B/C, IPO, Acquired
    user_base_size: Optional[str] = None  # <1K, 1K-10K, 10K-100K, 100K+, 1M+
    github_stars: Optional[int] = None
    market_trends: List[str] = []
    business_model: Optional[str] = None  # SaaS, Open Core, Freemium, Enterprise
    target_market: List[str] = []  # Startups, SMB, Enterprise, Individual Developers


class DetailedAnalysis(BaseModel):
    """Comprehensive analysis of a single tool"""
    tool_name: str
    overview: str = ""
    pros: List[str] = []
    cons: List[str] = []
    technical_details: str = ""
    use_cases_best_for: List[str] = []
    use_cases_not_ideal: List[str] = []
    developer_experience: str = ""
    pricing_analysis: str = ""
    alternatives_comparison: str = ""
    recommendation_score: Optional[int] = None  # 1-10 scale


class ComparisonMatrix(BaseModel):
    """Side-by-side comparison of multiple tools"""
    tools_compared: List[str] = []
    feature_comparison: str = ""
    technical_comparison: str = ""
    developer_experience_comparison: str = ""
    business_considerations: str = ""
    recommendation_matrix: str = ""


class ResearchState(BaseModel):
    query: str
    extracted_tools: List[str] = []  # Tools extracted from articles
    companies: List[CompanyInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None
    detailed_analyses: List[DetailedAnalysis] = []  # For deep-dive analysis
    comparison_matrix: Optional[ComparisonMatrix] = None  # For tool comparisons
    analysis_mode: str = "basic"  # basic, detailed, comparison
