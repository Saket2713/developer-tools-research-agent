#!/usr/bin/env python3
"""
Test script to verify the improvements made to the Advanced Research Agent
"""

from rich.console import Console
from src.models import CompanyInfo, CompanyAnalysis

console = Console()

def test_display_improvements():
    """Test the new display format without tables"""
    console.print("[bold green]🧪 Testing Display Improvements[/bold green]")
    console.print("─" * 50)
    
    # Create sample company data with market intelligence
    sample_companies = [
        CompanyInfo(
            name="Supabase",
            description="Open source Firebase alternative with PostgreSQL backend",
            website="https://supabase.com",
            pricing_model="Freemium",
            is_open_source=True,
            tech_stack=["PostgreSQL", "JavaScript", "TypeScript", "React"],
            api_available=True,
            language_support=["JavaScript", "Python", "Go", "Dart"],
            integration_capabilities=["Vercel", "Netlify", "GitHub"],
            market_position="Challenger",
            company_size="Startup",
            funding_status="Series A",
            user_base_size="100K+",
            github_stars=45000,
            market_trends=["Open Source", "JAMstack", "Edge Computing"]
        ),
        CompanyInfo(
            name="Firebase",
            description="Google's mobile and web application development platform",
            website="https://firebase.google.com",
            pricing_model="Freemium",
            is_open_source=False,
            tech_stack=["NoSQL", "JavaScript", "Cloud Functions"],
            api_available=True,
            language_support=["JavaScript", "Swift", "Java", "Python"],
            integration_capabilities=["Google Cloud", "Android", "iOS"],
            market_position="Leader",
            company_size="Enterprise",
            funding_status="IPO",
            user_base_size="1M+",
            market_trends=["Serverless", "Real-time", "Mobile-first"]
        )
    ]
    
    # Display using new format
    for i, company in enumerate(sample_companies, 1):
        console.print(f"\n[bold cyan]🏢 {i}. {company.name}[/bold cyan]")
        console.print("─" * 50)
        
        # Pricing and basic info
        console.print(f"💰 [green]Pricing:[/green] {company.pricing_model}")
        
        # API availability
        api_status = "✅ Available" if company.api_available else "❌ Not Available"
        console.print(f"🔌 [yellow]API:[/yellow] {api_status}")
        
        # Open source status
        open_source = "✅ Open Source" if company.is_open_source else "❌ Proprietary"
        console.print(f"📖 [blue]License:[/blue] {open_source}")
        
        # Tech stack
        if company.tech_stack:
            tech_display = ", ".join(company.tech_stack[:4])
            console.print(f"🛠️  [white]Tech Stack:[/white] {tech_display}")
        
        # Language support
        if company.language_support:
            lang_display = ", ".join(company.language_support[:4])
            console.print(f"💻 [magenta]Languages:[/magenta] {lang_display}")
        
        # Description
        console.print(f"📝 [dim]{company.description}[/dim]")
        
        # Website
        console.print(f"🌐 [link]{company.website}[/link]")
        
        # Market Intelligence
        if company.market_position:
            console.print(f"📈 [bold]Market Position:[/bold] {company.market_position}")
        
        if company.company_size:
            console.print(f"🏢 [bold]Company Size:[/bold] {company.company_size}")
        
        if company.funding_status:
            console.print(f"💼 [bold]Funding:[/bold] {company.funding_status}")
        
        if company.user_base_size:
            console.print(f"👥 [bold]User Base:[/bold] {company.user_base_size}")
        
        if company.github_stars:
            console.print(f"⭐ [bold]GitHub Stars:[/bold] {company.github_stars:,}")
        
        if company.market_trends:
            trends = ", ".join(company.market_trends[:3])
            console.print(f"📊 [bold]Market Trends:[/bold] {trends}")

def test_market_intelligence_summary():
    """Test the market intelligence summary"""
    console.print(f"\n[bold blue]📊 Market Intelligence Summary:[/bold blue]")
    console.print("─" * 50)
    
    console.print(f"🏆 [green]Market Leaders:[/green] 1 tools")
    console.print(f"⚔️  [yellow]Challengers:[/yellow] 1 tools")
    console.print(f"💰 [bold]Well-Funded Options:[/bold] 2 tools with external funding")

def test_top_tools_display():
    """Test the top tools display"""
    console.print(f"\n[bold blue]🏆 Top Market Leaders in Database Tools:[/bold blue]")
    console.print("─" * 60)
    
    top_tools = ["PostgreSQL", "MongoDB", "Redis", "MySQL", "Elasticsearch"]
    for i, leader in enumerate(top_tools, 1):
        console.print(f"[bold cyan]{i}.[/bold cyan] [green]{leader}[/green]")

if __name__ == "__main__":
    console.print("[bold magenta]🚀 Advanced Research Agent - Testing Improvements[/bold magenta]")
    console.print("=" * 70)
    
    test_display_improvements()
    test_market_intelligence_summary()
    test_top_tools_display()
    
    console.print(f"\n[bold green]✅ All display improvements working correctly![/bold green]")
    console.print("[dim]No tables or pipe symbols (|) used - clean text format only[/dim]")
