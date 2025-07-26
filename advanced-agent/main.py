from dotenv import load_dotenv
from src.workflow import Workflow
from rich.console import Console

from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich import print as rprint

from rich.markdown import Markdown
import json
import datetime

load_dotenv()

console = Console()


def export_results(query, result):
    """Export results in multiple formats"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"research_{query.replace(' ', '_')}_{timestamp}"

    # Export as JSON
    json_data = {
        "query": query,
        "timestamp": timestamp,
        "companies": [
            {
                "name": company.name,
                "website": company.website,
                "pricing_model": company.pricing_model,
                "is_open_source": company.is_open_source,
                "tech_stack": company.tech_stack,
                "language_support": company.language_support,
                "api_available": company.api_available,
                "integration_capabilities": company.integration_capabilities,
                "description": company.description
            }
            for company in result.companies
        ],
        "analysis": result.analysis
    }

    json_filename = f"{filename_base}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    # Export as Markdown
    md_content = f"# Developer Tools Research: {query}\n\n"
    md_content += f"*Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

    md_content += "## 📊 Results Summary\n\n"
    md_content += "| Tool | Pricing | API | Open Source | Tech Stack |\n"
    md_content += "|------|---------|-----|-------------|------------|\n"

    for company in result.companies:
        api_status = "✅" if company.api_available else "❌" if company.api_available is not None else "❓"
        open_source = "✅" if company.is_open_source else "❌" if company.is_open_source is not None else "❓"
        tech_stack = ", ".join(company.tech_stack[:3]) if company.tech_stack else "Not specified"

        md_content += f"| **{company.name}** | {company.pricing_model or 'Unknown'} | {api_status} | {open_source} | {tech_stack} |\n"

    md_content += "\n## 🏢 Detailed Information\n\n"
    for i, company in enumerate(result.companies, 1):
        md_content += f"### {i}. {company.name}\n\n"
        md_content += f"- **Website:** {company.website}\n"
        md_content += f"- **Pricing:** {company.pricing_model or 'Unknown'}\n"
        md_content += f"- **Open Source:** {'Yes' if company.is_open_source else 'No' if company.is_open_source is not None else 'Unknown'}\n"

        if company.tech_stack:
            md_content += f"- **Tech Stack:** {', '.join(company.tech_stack)}\n"
        if company.language_support:
            md_content += f"- **Language Support:** {', '.join(company.language_support)}\n"
        if company.api_available is not None:
            md_content += f"- **API Available:** {'Yes' if company.api_available else 'No'}\n"
        if company.integration_capabilities:
            md_content += f"- **Integrations:** {', '.join(company.integration_capabilities)}\n"
        if company.description:
            md_content += f"- **Description:** {company.description}\n"

        md_content += "\n"

    if result.analysis:
        md_content += "## 🤖 AI Recommendations\n\n"
        md_content += result.analysis + "\n"

    md_filename = f"{filename_base}.md"
    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(md_content)

    console.print(f"[bold green]✅ Results exported:[/bold green]")
    console.print(f"   📄 JSON: [cyan]{json_filename}[/cyan]")
    console.print(f"   📝 Markdown: [cyan]{md_filename}[/cyan]")


def show_demo():
    """Show a demo with pre-loaded results"""
    console.print("\n[bold yellow]🎬 Demo Mode - Showing sample results for 'database tools for python'[/bold yellow]")
    console.print("─" * 80)

    # Demo data in clean card format
    demo_tools = [
        ("PostgreSQL", "Free/Paid", "✅ Available", "✅ Open Source", "SQL, ACID", "Advanced open-source relational database"),
        ("MongoDB", "Free/Paid", "✅ Available", "✅ Open Source", "NoSQL, JSON", "Document-oriented NoSQL database"),
        ("Redis", "Free/Paid", "✅ Available", "✅ Open Source", "In-memory, Cache", "In-memory data structure store"),
        ("SQLite", "Free", "✅ Available", "✅ Open Source", "SQL, Embedded", "Lightweight embedded SQL database"),
    ]

    for i, tool_data in enumerate(demo_tools, 1):
        tool_name, pricing, api, open_source, tech_stack, description = tool_data
        console.print(f"\n[bold cyan]🏢 {i}. {tool_name}[/bold cyan]")
        console.print("─" * 40)
        console.print(f"💰 [green]Pricing:[/green] {pricing}")
        console.print(f"🔌 [yellow]API:[/yellow] {api}")
        console.print(f"📖 [blue]License:[/blue] {open_source}")
        console.print(f"🛠️  [white]Tech Stack:[/white] {tech_stack}")
        console.print(f"📝 [dim]{description}[/dim]")

    # Demo recommendations
    console.print("\n")
    console.print(Panel(
        "[bold white]For Python projects, I recommend PostgreSQL for complex applications requiring ACID compliance, "
        "MongoDB for flexible document storage, Redis for caching and real-time features, and SQLite for "
        "lightweight applications or prototyping. PostgreSQL offers the best balance of features and performance.[/bold white]",
        title="[bold green]🤖 AI Recommendations[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

    console.print("\n[dim]💡 This was a demo. Try a real query to see live results![/dim]")


def detailed_analysis_mode(result):
    """Interactive detailed analysis of selected tools"""
    if not result.companies:
        console.print("[red]❌ No tools available for detailed analysis[/red]")
        return

    console.print("\n[bold cyan]🔍 Select tools for detailed analysis:[/bold cyan]")

    # Show numbered list of tools
    for i, company in enumerate(result.companies, 1):
        console.print(f"  {i}. [bold]{company.name}[/bold] - {company.pricing_model or 'Unknown pricing'}")

    # Get user selection
    max_choice = len(result.companies)
    choices = [str(i) for i in range(1, max_choice + 1)]

    selected = IntPrompt.ask(
        f"Choose a tool for detailed analysis (1-{max_choice})",
        choices=choices
    )

    selected_tool = result.companies[selected - 1]

    # Show loading message
    console.print(f"\n[bold yellow]🔬 Generating detailed analysis for {selected_tool.name}...[/bold yellow]")

    # Get detailed analysis from workflow
    workflow = Workflow()
    detailed_analysis = workflow.get_detailed_analysis(selected_tool.name, selected_tool.website)

    if detailed_analysis:
        show_detailed_analysis(detailed_analysis)
    else:
        console.print("[red]❌ Failed to generate detailed analysis[/red]")


def comparison_mode(result):
    """Interactive comparison of multiple tools"""
    if len(result.companies) < 2:
        console.print("[red]❌ Need at least 2 tools for comparison[/red]")
        return

    console.print("\n[bold cyan]⚖️ Select tools to compare:[/bold cyan]")

    # Show numbered list
    for i, company in enumerate(result.companies, 1):
        console.print(f"  {i}. [bold]{company.name}[/bold]")

    console.print("\n[dim]Enter tool numbers separated by commas (e.g., 1,3,4)[/dim]")
    selection = Prompt.ask("Select tools to compare")

    try:
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_tools = [result.companies[i] for i in indices if 0 <= i < len(result.companies)]

        if len(selected_tools) < 2:
            console.print("[red]❌ Please select at least 2 tools[/red]")
            return

        console.print(f"\n[bold yellow]⚖️ Comparing {len(selected_tools)} tools...[/bold yellow]")

        # Generate comparison
        workflow = Workflow()
        comparison = workflow.get_comparison_matrix(selected_tools)

        if comparison:
            show_comparison_matrix(comparison)
        else:
            console.print("[red]❌ Failed to generate comparison[/red]")

    except (ValueError, IndexError):
        console.print("[red]❌ Invalid selection format[/red]")


def show_detailed_analysis(analysis):
    """Display detailed analysis with simple text formatting"""
    console.print(f"\n[bold blue]📊 Detailed Analysis: {analysis.tool_name}[/bold blue]")
    console.print("=" * 80)

    # Overview
    if analysis.overview:
        console.print(f"\n[bold green]📋 Overview[/bold green]")
        console.print(f"{analysis.overview}\n")

    # Pros and Cons
    if analysis.pros or analysis.cons:
        console.print(f"[bold green]👍 Advantages[/bold green]")
        if analysis.pros:
            for pro in analysis.pros:
                console.print(f"  ✅ {pro}")
        else:
            console.print("  No advantages listed")

        console.print(f"\n[bold red]👎 Disadvantages[/bold red]")
        if analysis.cons:
            for con in analysis.cons:
                console.print(f"  ❌ {con}")
        else:
            console.print("  No disadvantages listed")
        console.print()

    # Technical Details
    if analysis.technical_details:
        console.print(f"[bold cyan]🔧 Technical Deep Dive[/bold cyan]")
        console.print(f"{analysis.technical_details}\n")

    # Use Cases
    if analysis.use_cases_best_for or analysis.use_cases_not_ideal:
        console.print(f"[bold green]🎯 Best For[/bold green]")
        if analysis.use_cases_best_for:
            for case in analysis.use_cases_best_for:
                console.print(f"  ✅ {case}")
        else:
            console.print("  No specific use cases listed")

        console.print(f"\n[bold red]⚠️ Not Ideal For[/bold red]")
        if analysis.use_cases_not_ideal:
            for case in analysis.use_cases_not_ideal:
                console.print(f"  ❌ {case}")
        else:
            console.print("  No limitations listed")
        console.print()

    # Developer Experience
    if analysis.developer_experience:
        console.print(f"[bold magenta]👨‍💻 Developer Experience[/bold magenta]")
        console.print(f"{analysis.developer_experience}\n")

    # Pricing Analysis
    if analysis.pricing_analysis:
        console.print(f"[bold yellow]💰 Pricing & Value[/bold yellow]")
        console.print(f"{analysis.pricing_analysis}\n")

    # Alternatives Comparison
    if analysis.alternatives_comparison:
        console.print(f"[bold blue]🔄 Alternatives Comparison[/bold blue]")
        console.print(f"{analysis.alternatives_comparison}\n")

    # Recommendation Score
    if analysis.recommendation_score:
        score_color = "green" if analysis.recommendation_score >= 7 else "yellow" if analysis.recommendation_score >= 5 else "red"
        console.print(f"[bold {score_color}]⭐ Recommendation Score: {analysis.recommendation_score}/10[/bold {score_color}]\n")


def show_comparison_matrix(comparison):
    """Display comparison matrix with simple text formatting"""
    console.print(f"\n[bold blue]⚖️ Tool Comparison Matrix[/bold blue]")
    console.print(f"[dim]Comparing: {', '.join(comparison.tools_compared)}[/dim]")
    console.print("=" * 80)

    # Display the full comparison as simple text
    if comparison.feature_comparison:
        console.print(f"\n[bold cyan]🔧 Detailed Comparison[/bold cyan]")
        console.print(f"{comparison.feature_comparison}\n")
    else:
        console.print("[red]❌ No comparison data available[/red]")


def main():
    workflow = Workflow()

    # Welcome banner
    console.print(Panel.fit(
        "[bold blue]🚀 Developer Tools Research Agent[/bold blue]\n"
        "[dim]Powered by AI • Find the perfect tools for your project[/dim]\n\n"
        "[yellow]💡 Try these examples:[/yellow]\n"
        "[dim]• alternate to placid\n"
        "• database tools for python\n"
        "• CI/CD platforms\n"
        "• demo (for quick demonstration)[/dim]",
        border_style="blue"
    ))

    while True:
        query = Prompt.ask("\n[bold cyan]🔍 Developer Tools Query[/bold cyan]", default="").strip()
        if query.lower() in {"quit", "exit", ""}:
            console.print("[dim]👋 Goodbye![/dim]")
            break

        # Demo mode with pre-loaded results
        if query.lower() == "demo":
            show_demo()
            continue

        if query:
            # First, show market leaders in this category
            category = query.replace("alternate for", "").replace("alternative to", "").replace("tools for", "").strip()
            market_leaders = workflow.get_market_leaders(category)

            if market_leaders:
                console.print(f"\n[bold blue]🏆 Top Market Leaders in {category.title()}:[/bold blue]")
                console.print("─" * 60)
                for i, leader in enumerate(market_leaders, 1):
                    console.print(f"[bold cyan]{i}.[/bold cyan] [green]{leader}[/green]")
                console.print()

            result = workflow.run(query)

            # Results header
            console.print(f"\n[bold green]📊 Results for:[/bold green] [yellow]{query}[/yellow]")
            console.print("─" * 80)

            # Display results in clean card format
            for i, company in enumerate(result.companies, 1):
                console.print(f"\n[bold cyan]🏢 {i}. {company.name}[/bold cyan]")
                console.print("─" * 50)

                # Pricing and basic info
                pricing = company.pricing_model or "Unknown"
                console.print(f"💰 [green]Pricing:[/green] {pricing}")

                # API availability
                api_status = "✅ Available" if company.api_available else "❌ Not Available" if company.api_available is not None else "❓ Unknown"
                console.print(f"🔌 [yellow]API:[/yellow] {api_status}")

                # Open source status
                open_source = "✅ Open Source" if company.is_open_source else "❌ Proprietary" if company.is_open_source is not None else "❓ Unknown"
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
                if company.description:
                    desc = company.description[:100] + "..." if len(company.description) > 100 else company.description
                    console.print(f"📝 [dim]{desc}[/dim]")

                # Website
                console.print(f"🌐 [link]{company.website}[/link]")

                # Market Intelligence (if available)
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

            # Display recommendations with market intelligence
            if result.analysis:
                console.print("\n")
                console.print(Panel(
                    f"[bold white]{result.analysis}[/bold white]",
                    title="[bold green]🤖 AI Recommendations & Market Intelligence[/bold green]",
                    border_style="green",
                    padding=(1, 2)
                ))

                # Additional market insights summary
                console.print(f"\n[bold blue]📊 Market Intelligence Summary:[/bold blue]")
                console.print("─" * 50)

                # Count market positions
                leaders = sum(1 for c in result.companies if c.market_position == "Leader")
                challengers = sum(1 for c in result.companies if c.market_position == "Challenger")
                emerging = sum(1 for c in result.companies if c.market_position == "Emerging")

                if leaders > 0:
                    console.print(f"🏆 [green]Market Leaders:[/green] {leaders} tools")
                if challengers > 0:
                    console.print(f"⚔️  [yellow]Challengers:[/yellow] {challengers} tools")
                if emerging > 0:
                    console.print(f"🌱 [cyan]Emerging Players:[/cyan] {emerging} tools")

                # Show funding trends
                funded_companies = [c for c in result.companies if c.funding_status and c.funding_status not in ["Unknown", "Bootstrapped"]]
                if funded_companies:
                    console.print(f"💰 [bold]Well-Funded Options:[/bold] {len(funded_companies)} tools with external funding")

            # Ask for detailed analysis or export
            console.print("\n[bold yellow]📋 What would you like to do next?[/bold yellow]")
            console.print("1. 🔍 Get detailed analysis of specific tools")
            console.print("2. ⚖️  Compare tools side-by-side")
            console.print("3. 💾 Export results")
            console.print("4. ➡️  Continue with new query")

            choice = IntPrompt.ask("Choose an option", choices=["1", "2", "3", "4"], default=4)

            if choice == 1:
                detailed_analysis_mode(result)
            elif choice == 2:
                comparison_mode(result)
            elif choice == 3:
                export_results(query, result)


if __name__ == "__main__":
    main()
