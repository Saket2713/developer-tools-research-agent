from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich import print as rprint
from .models import ResearchState, CompanyInfo, CompanyAnalysis, DetailedAnalysis, ComparisonMatrix
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts
import os
from typing import List


class Workflow:
    def __init__(self):
        self.console = Console()
        self.firecrawl = FirecrawlService()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",  # Faster model with higher rate limits
            temperature=0.1,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()

    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        self.console.print(f"[bold blue]🔍 Finding articles about:[/bold blue] [cyan]{state.query}[/cyan]")

        # Improve search strategy with developer-focused terms
        if "alternate" in state.query.lower() or "alternative" in state.query.lower():
            # Extract the tool name from queries like "alternate for X" or "alternative to X"
            tool_name = state.query.lower().replace("alternate for", "").replace("alternative to", "").replace("alternative for", "").strip()
            article_query = f"{tool_name} alternatives developer tools comparison software engineering best"
        else:
            # Add developer-specific terms to improve search precision
            dev_terms = "developer tools software engineering programming"
            article_query = f"best {state.query} {dev_terms} comparison top tools 2024"

        search_results = self.firecrawl.search_companies(article_query, num_results=4)

        all_content = ""
        # Handle both list and object with data attribute
        results_list = search_results.data if hasattr(search_results, 'data') else search_results
        for result in results_list:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped:
                all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            raw_tool_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]

            # Validate and filter tools to ensure they're relevant
            validated_tools = self._validate_developer_tools(raw_tool_names, state.query)

            self.console.print(f"[bold green]✅ Extracted tools:[/bold green] [yellow]{', '.join(validated_tools[:5])}[/yellow]")
            return {"extracted_tools": validated_tools}
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                self.console.print(f"[yellow]⚠️ Rate limit reached. Please wait a few minutes before trying again.[/yellow]")
                self.console.print(f"[dim]💡 Tip: You can upgrade to Groq Dev Tier for higher limits at https://console.groq.com/settings/billing[/dim]")
            else:
                self.console.print(f"[bold red]❌ Error extracting tools:[/bold red] {e}")
            return {"extracted_tools": []}

    def _validate_developer_tools(self, tool_names: List[str], query: str) -> List[str]:
        """Validate that extracted tools are actually developer tools and relevant to the query"""
        validated_tools = []

        # Comprehensive list of non-developer business patterns to exclude
        exclude_patterns = [
            # E-commerce & Retail
            "watch", "jewelry", "fashion", "clothing", "retail", "shop", "store", "marketplace", "ecommerce",
            "boutique", "outlet", "mall", "shopping", "cart", "checkout", "payment", "wallet",

            # Food & Hospitality
            "restaurant", "food", "cafe", "coffee", "dining", "menu", "recipe", "kitchen", "cooking",
            "hotel", "travel", "booking", "vacation", "tourism", "flight", "airline",

            # Finance & Insurance (non-fintech)
            "insurance", "loan", "mortgage", "credit", "bank", "investment", "trading", "forex",
            "accounting", "tax", "audit", "financial advisor", "wealth management",

            # Healthcare & Medical
            "medical", "healthcare", "hospital", "clinic", "doctor", "pharmacy", "medicine", "health",
            "fitness", "gym", "workout", "nutrition", "wellness", "therapy",

            # Real Estate & Automotive
            "real estate", "property", "house", "home", "apartment", "rental", "lease",
            "automotive", "car", "vehicle", "auto", "mechanic", "garage", "dealership",

            # Entertainment & Media
            "movie", "film", "music", "game", "entertainment", "media", "news", "magazine",
            "sports", "betting", "casino", "gambling",

            # Education (non-technical)
            "school", "university", "college", "education", "learning", "course", "training",
            "tutoring", "academic", "student",

            # Legal & Professional Services
            "legal", "law", "lawyer", "attorney", "court", "consulting", "advisory",
            "marketing", "advertising", "agency", "design studio"
        ]

        # Comprehensive developer tool categories and technologies
        dev_categories = [
            # Development & Programming
            "api", "sdk", "framework", "library", "ide", "editor", "compiler", "interpreter",
            "programming", "coding", "development", "software", "application", "app",

            # DevOps & Infrastructure
            "ci/cd", "continuous integration", "continuous deployment", "pipeline", "build",
            "deployment", "devops", "infrastructure", "provisioning", "automation",
            "orchestration", "configuration management",

            # Cloud & Hosting
            "cloud", "hosting", "server", "serverless", "paas", "iaas", "saas", "platform",
            "aws", "azure", "gcp", "google cloud", "digital ocean", "heroku", "vercel", "netlify",

            # Databases & Storage
            "database", "db", "sql", "nosql", "mongodb", "postgresql", "mysql", "redis",
            "elasticsearch", "storage", "data", "warehouse", "lake", "cache", "memory",

            # Containers & Orchestration
            "container", "docker", "kubernetes", "k8s", "pod", "cluster", "microservice",
            "service mesh", "istio", "helm", "container registry",

            # Monitoring & Observability
            "monitoring", "observability", "logging", "metrics", "tracing", "alerting",
            "dashboard", "analytics", "performance", "apm", "error tracking",

            # Security & Authentication
            "security", "authentication", "authorization", "oauth", "jwt", "sso", "identity",
            "access control", "encryption", "certificate", "ssl", "tls", "firewall",

            # Testing & Quality
            "testing", "test", "qa", "quality assurance", "automation", "unit test",
            "integration test", "e2e", "performance test", "load test", "security test",

            # Version Control & Collaboration
            "version control", "git", "github", "gitlab", "bitbucket", "repository", "repo",
            "collaboration", "code review", "pull request", "merge request",

            # Communication & Project Management (dev-focused)
            "slack", "discord", "teams", "jira", "confluence", "notion", "trello", "asana",
            "project management", "issue tracking", "bug tracking", "agile", "scrum",

            # Development Tools
            "webpack", "babel", "npm", "yarn", "pip", "maven", "gradle", "make", "cmake",
            "linter", "formatter", "debugger", "profiler", "bundler", "transpiler"
        ]

        # Known legitimate developer tools (whitelist for common cases)
        known_dev_tools = [
            # CI/CD & DevOps
            "jenkins", "github actions", "gitlab ci", "circleci", "travis ci", "azure devops",
            "docker", "kubernetes", "terraform", "ansible", "chef", "puppet",

            # Cloud & Hosting
            "aws", "azure", "gcp", "heroku", "vercel", "netlify", "digital ocean",

            # Databases
            "mongodb", "postgresql", "mysql", "redis", "elasticsearch", "cassandra",

            # Frameworks & Libraries
            "react", "vue", "angular", "node.js", "express", "django", "flask", "spring",

            # Monitoring & Analytics
            "prometheus", "grafana", "datadog", "new relic", "splunk", "elk stack",

            # Testing & API Tools
            "jest", "cypress", "selenium", "postman", "insomnia", "swagger",

            # Code Editors & IDEs
            "vscode", "intellij", "sublime", "atom", "vim", "emacs", "cursor", "zed",
            "webstorm", "pycharm", "phpstorm", "rubymine", "goland", "clion", "notepad++",

            # AI Coding Assistants
            "github copilot", "copilot", "claude code", "codemate", "tabnine", "kite",
            "codium", "codewhisperer", "replit", "ghostwriter",

            # Version Control
            "git", "github", "gitlab", "bitbucket", "subversion"
        ]

        for tool_name in tool_names:
            tool_lower = tool_name.lower().strip()
            query_lower = query.lower()

            # Skip empty or very short names
            if len(tool_lower) < 2:
                continue

            # Skip if tool name contains excluded business patterns (but be smart about context)
            is_excluded = False
            for pattern in exclude_patterns:
                if pattern in tool_lower:
                    # Check if it's a false positive (e.g., "Weather Cloud Service" has "cloud" which is dev-related)
                    dev_context_words = ["cloud", "server", "platform", "service", "api", "database", "monitor", "security", "system"]
                    has_dev_context = any(dev_word in tool_lower for dev_word in dev_context_words)

                    # Only exclude if it's clearly non-dev and doesn't have dev context
                    if not has_dev_context or pattern in ["watch", "fashion", "restaurant", "hotel", "insurance", "medical"]:
                        is_excluded = True
                        break

            if is_excluded:
                self.console.print(f"[dim]❌ Filtered out non-dev tool: {tool_name}[/dim]")
                continue

            # Include if it's a known developer tool
            is_known_dev_tool = any(known_tool in tool_lower for known_tool in known_dev_tools)

            # Include if it matches developer categories
            matches_dev_category = any(category in tool_lower for category in dev_categories)

            # Include if query context suggests it's a dev tool
            query_suggests_dev = any(category in query_lower for category in dev_categories)

            # Additional validation: check if tool name has technical indicators
            technical_indicators = [
                # Programming languages & extensions
                "js", "py", "go", "rs", "ts", "java", "cpp", "php", "rb", "swift",

                # Technical domains
                "io", "dev", "tech", "code", "soft", "app", "ai", "ml", "data",

                # Infrastructure & platforms
                "hub", "lab", "cloud", "server", "base", "stack", "kit", "tool", "platform",
                "api", "sdk", "framework", "service", "system", "engine", "db", "sql",

                # Development concepts
                "editor", "ide", "copilot", "assistant", "mate", "pilot", "studio",
                "workspace", "terminal", "shell", "cli", "gui", "ui", "ux"
            ]
            has_technical_indicators = any(indicator in tool_lower for indicator in technical_indicators)

            # Enhanced decision logic with better context awareness
            should_include = (
                is_known_dev_tool or
                matches_dev_category or
                (query_suggests_dev and has_technical_indicators and len(tool_lower) > 2) or  # Relaxed length requirement
                (len(validated_tools) < 3 and has_technical_indicators and len(tool_lower) > 2)  # Keep at least 3 if they seem technical
            )

            # Special handling for ambiguous cases (but be more lenient for coding tools)
            ambiguous_patterns = ["monitor", "weather", "health"]  # Removed "security" as it's often dev-related
            if any(pattern in tool_lower for pattern in ambiguous_patterns):
                # For ambiguous tools, require stronger dev context
                strong_dev_indicators = ["prometheus", "grafana", "datadog", "splunk", "newrelic", "sentry", "security"]
                if not any(indicator in tool_lower.replace(" ", "") for indicator in strong_dev_indicators):
                    should_include = False

            # Special boost for common coding tool patterns
            coding_tool_patterns = ["code", "editor", "ide", "copilot", "assistant", "mate", "pilot", "studio"]
            if any(pattern in tool_lower for pattern in coding_tool_patterns):
                should_include = True  # Always include obvious coding tools

            if should_include:
                validated_tools.append(tool_name)
                self.console.print(f"[dim]✅ Validated dev tool: {tool_name}[/dim]")
            else:
                self.console.print(f"[dim]❓ Uncertain tool filtered: {tool_name}[/dim]")

        return validated_tools[:5]  # Limit to 5 tools

    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            self.console.print(f"[bold red]❌ Analysis error:[/bold red] {e}")
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )


    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])

        if not extracted_tools:
            self.console.print("[bold yellow]⚠️ No extracted tools found, falling back to direct search[/bold yellow]")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            results_list = search_results.data if hasattr(search_results, 'data') else search_results
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in results_list
            ]
        else:
            tool_names = extracted_tools[:4]

        self.console.print(f"[bold magenta]🔬 Researching specific tools:[/bold magenta] [green]{', '.join(tool_names)}[/green]")

        companies = []
        for tool_name in tool_names:
            # Add developer-specific search terms to improve precision
            search_terms = f"{tool_name} developer tool software engineering official site"
            tool_search_results = self.firecrawl.search_companies(search_terms, num_results=1)

            if tool_search_results:
                results_list = tool_search_results.data if hasattr(tool_search_results, 'data') else tool_search_results
                result = results_list[0] if results_list else None

                if result:
                    url = result.get("url", "")

                    company = CompanyInfo(
                        name=tool_name,
                        description=result.get("markdown", ""),
                        website=url,
                        tech_stack=[],
                        competitors=[]
                    )

                    scraped = self.firecrawl.scrape_company_pages(url)
                    if scraped:
                        content = scraped.markdown
                        analysis = self._analyze_company_content(company.name, content)

                        company.pricing_model = analysis.pricing_model
                        company.is_open_source = analysis.is_open_source
                        company.tech_stack = analysis.tech_stack
                        company.description = analysis.description
                        company.api_available = analysis.api_available
                        company.language_support = analysis.language_support
                        company.integration_capabilities = analysis.integration_capabilities
                        # Market intelligence fields
                        company.market_position = analysis.market_position
                        company.company_size = analysis.company_size
                        company.funding_status = analysis.funding_status
                        company.user_base_size = analysis.user_base_size
                        company.github_stars = analysis.github_stars
                        company.market_trends = analysis.market_trends

                    companies.append(company)

        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        self.console.print("[bold cyan]🤖 Generating recommendations...[/bold cyan]")

        company_data = ", ".join([
            company.json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        try:
            response = self.llm.invoke(messages)
            return {"analysis": response.content}
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                error_msg = "⚠️ Rate limit reached. Please wait a few minutes before trying again.\n💡 Tip: You can upgrade to Groq Dev Tier for higher limits."
                self.console.print(f"[yellow]{error_msg}[/yellow]")
                return {"analysis": f"Analysis temporarily unavailable due to rate limits. Please try again in a few minutes."}
            else:
                self.console.print(f"[bold red]❌ Error generating analysis:[/bold red] {e}")
                return {"analysis": "Analysis failed due to an error."}

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)

    def get_market_leaders(self, category: str, num_results: int = 5) -> List[str]:
        """Get top market leaders in a specific category"""
        try:
            self.console.print(f"[dim]📊 Finding market leaders in {category}...[/dim]")

            # Search for market leader articles with developer-specific terms (aligned with main search)
            search_query = f"best {category} developer tools 2024 top popular software engineering comparison"
            search_results = self.firecrawl.search_companies(search_query, num_results=3)

            all_content = ""
            results_list = search_results.data if hasattr(search_results, 'data') else search_results
            for result in results_list:
                url = result.get("url", "")
                scraped = self.firecrawl.scrape_company_pages(url)
                if scraped:
                    all_content += scraped.markdown[:2000] + "\n\n"

            # Extract top tools using LLM with strict validation
            messages = [
                SystemMessage(content="""You are a senior software engineer and market analyst specializing in developer tools.
                                      Extract ONLY legitimate developer tools that are market leaders in the specified category.

                                      STRICT RULES:
                                      - Only include tools specifically designed for software development
                                      - Exclude any non-tech companies, e-commerce sites, or irrelevant businesses
                                      - Focus on tools that developers actually use for coding, deployment, or infrastructure
                                      - Verify each tool is relevant to the category before including

                                      Return only tool names, one per line, no descriptions."""),
                HumanMessage(content=f"Category: {category}\nContent: {all_content}\n\nExtract the top 5 legitimate developer tools that are market leaders in {category}:")
            ]

            try:
                response = self.llm.invoke(messages)
                raw_tools = [
                    name.strip()
                    for name in response.content.strip().split("\n")
                    if name.strip()
                ]

                # Validate the market leaders are actually developer tools
                validated_leaders = self._validate_developer_tools(raw_tools, category)
                return validated_leaders[:5]
            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    self.console.print(f"[yellow]⚠️ Rate limit reached for market analysis.[/yellow]")
                    return []
                else:
                    self.console.print(f"[red]❌ Error getting market leaders: {e}[/red]")
                    return []

        except Exception as e:
            self.console.print(f"[red]❌ Error in market analysis: {e}[/red]")
            return []

    def get_detailed_analysis(self, tool_name: str, website: str) -> DetailedAnalysis:
        """Generate detailed analysis for a specific tool"""
        try:
            self.console.print(f"[dim]🌐 Scraping {website} for detailed information...[/dim]")

            # Scrape the website for detailed content
            scraped_data = self.firecrawl.scrape_company_pages(website)
            if not scraped_data:
                self.console.print(f"[red]❌ Failed to scrape {website}[/red]")
                return None

            content = scraped_data.markdown if hasattr(scraped_data, 'markdown') else str(scraped_data)

            # Generate detailed analysis using LLM
            messages = [
                SystemMessage(content=self.prompts.DETAILED_ANALYSIS_SYSTEM),
                HumanMessage(content=self.prompts.detailed_analysis_user(tool_name, content, ""))
            ]

            try:
                response = self.llm.invoke(messages)
            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    self.console.print(f"[yellow]⚠️ Rate limit reached for detailed analysis. Please wait a few minutes.[/yellow]")
                    return None
                else:
                    self.console.print(f"[red]❌ Error generating detailed analysis: {e}[/red]")
                    return None

            # Parse the response into structured format
            analysis_text = response.content

            # Extract sections using simple parsing (could be enhanced with structured output)
            detailed_analysis = DetailedAnalysis(
                tool_name=tool_name,
                overview=self._extract_section(analysis_text, "## Overview"),
                pros=self._extract_list_section(analysis_text, "### Advantages:"),
                cons=self._extract_list_section(analysis_text, "### Disadvantages:"),
                technical_details=self._extract_section(analysis_text, "## Technical Deep Dive"),
                use_cases_best_for=self._extract_list_section(analysis_text, "### Best For:"),
                use_cases_not_ideal=self._extract_list_section(analysis_text, "### Not Ideal For:"),
                developer_experience=self._extract_section(analysis_text, "## Developer Experience"),
                pricing_analysis=self._extract_section(analysis_text, "## Pricing & Value"),
                alternatives_comparison=self._extract_section(analysis_text, "## Alternatives Comparison"),
                recommendation_score=self._extract_score(analysis_text)
            )

            return detailed_analysis

        except Exception as e:
            self.console.print(f"[red]❌ Error generating detailed analysis: {e}[/red]")
            return None

    def get_comparison_matrix(self, tools: List[CompanyInfo]) -> ComparisonMatrix:
        """Generate comparison matrix for multiple tools"""
        try:
            tool_names = [tool.name for tool in tools]
            self.console.print(f"[dim]⚖️ Generating comparison for {', '.join(tool_names)}...[/dim]")

            # Prepare tools data for comparison
            tools_data = "\n\n".join([
                f"Tool: {tool.name}\n"
                f"Website: {tool.website}\n"
                f"Pricing: {tool.pricing_model}\n"
                f"Tech Stack: {', '.join(tool.tech_stack)}\n"
                f"API Available: {tool.api_available}\n"
                f"Description: {tool.description}"
                for tool in tools
            ])

            # Generate comparison using LLM
            messages = [
                SystemMessage(content=self.prompts.COMPARISON_MATRIX_SYSTEM),
                HumanMessage(content=self.prompts.comparison_matrix_user(tools_data, "comprehensive comparison"))
            ]

            try:
                response = self.llm.invoke(messages)
                comparison_text = response.content
            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    self.console.print(f"[yellow]⚠️ Rate limit reached for comparison. Please wait a few minutes.[/yellow]")
                    return None
                else:
                    raise e

            # Instead of trying to parse sections, just use the full response as a single comparison
            comparison = ComparisonMatrix(
                tools_compared=tool_names,
                feature_comparison=comparison_text,  # Use full text for main comparison
                technical_comparison="",  # Leave empty - all content in feature_comparison
                developer_experience_comparison="",
                business_considerations="",
                recommendation_matrix=""
            )

            return comparison

        except Exception as e:
            self.console.print(f"[red]❌ Error generating comparison: {e}[/red]")
            return None

    def _extract_section(self, text: str, section_header: str) -> str:
        """Extract content from a specific section"""
        lines = text.split('\n')
        in_section = False
        section_content = []

        # Try different header formats
        possible_headers = [
            section_header,
            section_header.replace("## ", ""),
            f"**{section_header.replace('## ', '')}**",
            f"# {section_header.replace('## ', '')}"
        ]

        for line in lines:
            line_stripped = line.strip()

            # Check if this line starts a section we want
            if any(line_stripped.startswith(header) or header in line_stripped for header in possible_headers):
                in_section = True
                continue
            # Check if this line starts a new section (stop extraction)
            elif (line_stripped.startswith('##') or line_stripped.startswith('**') or line_stripped.startswith('# ')) and in_section:
                break
            elif in_section:
                section_content.append(line)

        result = '\n'.join(section_content).strip()
        return result if result else None

    def _extract_list_section(self, text: str, section_header: str) -> List[str]:
        """Extract list items from a section"""
        section_text = self._extract_section(text, section_header)
        items = []

        for line in section_text.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                items.append(line[2:])
            elif line.startswith('* '):
                items.append(line[2:])

        return items

    def _extract_score(self, text: str) -> int:
        """Extract recommendation score from text"""
        import re
        score_match = re.search(r'(\d+)/10', text)
        if score_match:
            return int(score_match.group(1))
        return None
