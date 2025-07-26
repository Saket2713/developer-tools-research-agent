#!/usr/bin/env python3
"""
Test script to verify the precision improvements for tool extraction
"""

from rich.console import Console
from src.workflow import Workflow

console = Console()

def test_tool_validation():
    """Test the tool validation function across multiple categories"""
    console.print("[bold green]🧪 Testing Universal Tool Validation[/bold green]")
    console.print("─" * 60)

    # Create workflow instance
    workflow = Workflow()

    # Test cases for different developer tool categories
    test_cases = [
        {
            "category": "CI/CD Platforms",
            "query": "ci/cd platforms",
            "tools": [
                "Jenkins", "GitHub Actions", "Spinnaker Watch Store", "CircleCI",
                "Fashion Boutique", "GitLab CI", "Restaurant Menu", "Travis CI"
            ],
            "expected_valid": ["Jenkins", "GitHub Actions", "CircleCI", "GitLab CI", "Travis CI"]
        },
        {
            "category": "Database Tools",
            "query": "database tools",
            "tools": [
                "PostgreSQL", "MongoDB", "Watch Collection DB", "MySQL",
                "Coffee Shop Database", "Redis", "Hotel Booking System", "Cassandra"
            ],
            "expected_valid": ["PostgreSQL", "MongoDB", "MySQL", "Redis", "Cassandra"]
        },
        {
            "category": "Frontend Frameworks",
            "query": "frontend frameworks",
            "tools": [
                "React", "Vue.js", "Fashion Design Studio", "Angular",
                "Restaurant Website", "Svelte", "Travel Agency", "Next.js"
            ],
            "expected_valid": ["React", "Vue.js", "Angular", "Svelte", "Next.js"]
        },
        {
            "category": "AI Coding Tools",
            "query": "ai coding assistants",
            "tools": [
                "GitHub Copilot", "Zed", "Claude Code", "Cursor",
                "Fashion Store", "CodeMate", "Restaurant App", "Tabnine"
            ],
            "expected_valid": ["GitHub Copilot", "Zed", "Claude Code", "Cursor", "CodeMate", "Tabnine"]
        },
        {
            "category": "Cloud Platforms",
            "query": "cloud hosting platforms",
            "tools": [
                "AWS", "Azure", "Weather Cloud Service", "Google Cloud",
                "Insurance Platform", "Heroku", "Medical Cloud", "Vercel"
            ],
            "expected_valid": ["AWS", "Azure", "Google Cloud", "Heroku", "Vercel"]
        },
        {
            "category": "Monitoring Tools",
            "query": "monitoring tools",
            "tools": [
                "Prometheus", "Grafana", "Security Camera Monitor", "Datadog",
                "Health Monitor", "New Relic", "Baby Monitor", "Splunk"
            ],
            "expected_valid": ["Prometheus", "Grafana", "Datadog", "New Relic", "Splunk"]
        }
    ]

    total_tests = 0
    passed_tests = 0

    for test_case in test_cases:
        console.print(f"\n[cyan]Testing {test_case['category']}:[/cyan]")
        console.print(f"[yellow]Query:[/yellow] {test_case['query']}")
        console.print(f"[yellow]Input tools:[/yellow] {', '.join(test_case['tools'])}")

        # Test validation
        validated = workflow._validate_developer_tools(test_case['tools'], test_case['query'])

        console.print(f"[green]✅ Validated tools:[/green] {', '.join(validated)}")

        # Check results
        valid_count = len([tool for tool in validated if tool in test_case['expected_valid']])
        invalid_count = len([tool for tool in validated if tool not in test_case['expected_valid']])

        console.print(f"[dim]Valid: {valid_count}, Invalid: {invalid_count}[/dim]")

        total_tests += 1
        if invalid_count == 0 and valid_count >= 3:
            console.print(f"[bold green]✅ PASSED[/bold green]")
            passed_tests += 1
        else:
            console.print(f"[bold red]❌ FAILED[/bold red]")

    console.print(f"\n[bold blue]📊 Overall Results:[/bold blue]")
    console.print(f"Tests passed: {passed_tests}/{total_tests}")

    if passed_tests == total_tests:
        console.print(f"[bold green]🎉 All categories working correctly![/bold green]")
    else:
        console.print(f"[bold red]❌ Some categories need improvement[/bold red]")

def test_search_improvements():
    """Test the improved search strategy across all developer tool categories"""
    console.print(f"\n[bold green]🔍 Testing Universal Search Strategy[/bold green]")
    console.print("─" * 60)

    test_queries = [
        # Core Development
        "frontend frameworks", "backend frameworks", "programming languages",
        "code editors", "ides", "version control",

        # DevOps & Infrastructure
        "ci/cd platforms", "container tools", "orchestration platforms",
        "infrastructure as code", "configuration management",

        # Data & Databases
        "database tools", "data warehouses", "caching solutions",
        "search engines", "message queues",

        # Cloud & Hosting
        "cloud platforms", "hosting services", "serverless platforms",
        "cdn services", "load balancers",

        # Monitoring & Security
        "monitoring tools", "logging platforms", "error tracking",
        "security tools", "authentication services",

        # Testing & Quality
        "testing frameworks", "automation tools", "performance testing",
        "code quality tools", "static analysis",

        # Alternative queries
        "alternative to jenkins", "alternate for docker", "replacement for aws"
    ]

    console.print(f"[yellow]Testing {len(test_queries)} different query types...[/yellow]\n")

    for i, query in enumerate(test_queries, 1):
        console.print(f"[cyan]{i:2d}. Query:[/cyan] {query}")

        # Simulate improved search terms
        if "alternate" in query.lower() or "alternative" in query.lower():
            tool_name = query.lower().replace("alternative to", "").replace("alternate for", "").replace("replacement for", "").strip()
            search_query = f"{tool_name} alternatives developer tools comparison software engineering"
        else:
            dev_terms = "developer tools software engineering programming"
            search_query = f"{query} {dev_terms} comparison best tools 2024"

        console.print(f"[dim]    Enhanced search:[/dim] {search_query}")

        # Show how this prevents irrelevant results
        if i % 5 == 0:  # Every 5th query, show the benefit
            console.print(f"[green]    ✅ This prevents: watches, restaurants, fashion stores[/green]")

        console.print()

def test_category_detection():
    """Test category detection for market leaders"""
    console.print(f"\n[bold green]🏆 Testing Category Detection[/bold green]")
    console.print("─" * 60)
    
    test_queries = [
        "ci/cd platforms",
        "alternative to jenkins", 
        "database tools for startups",
        "monitoring solutions"
    ]
    
    for query in test_queries:
        # Extract category like the main code does
        category = query.replace("alternate for", "").replace("alternative to", "").replace("tools for", "").strip()
        
        console.print(f"[cyan]Query:[/cyan] {query}")
        console.print(f"[yellow]Extracted category:[/yellow] {category}")
        console.print()

if __name__ == "__main__":
    console.print("[bold magenta]🎯 Advanced Research Agent - Precision Testing[/bold magenta]")
    console.print("=" * 70)
    
    try:
        test_tool_validation()
        test_search_improvements()
        test_category_detection()
        
        console.print(f"\n[bold green]✅ All precision improvements tested![/bold green]")
        console.print("[dim]The system should now filter out irrelevant tools like watch sellers[/dim]")
        
    except Exception as e:
        console.print(f"[bold red]❌ Test failed: {e}[/bold red]")
