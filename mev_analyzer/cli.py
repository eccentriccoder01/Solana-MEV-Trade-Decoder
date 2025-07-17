import asyncio
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from .rpc import SolanaRPCClient
from .analyzer import TransactionAnalyzer
from .models import TransactionSummary

class MEVAnalyzerCLI:
    def __init__(self):
        self.console = Console()
        self.rpc_client = SolanaRPCClient()
        self.analyzer = TransactionAnalyzer(self.rpc_client)

    def display_summary(self, summary: TransactionSummary):
        color = "red" if summary.is_mev else "green"
        mev_status = "✓ MEV DETECTED" if summary.is_mev else "✗ No MEV"

        content = f"""
[bold]Transaction:[/bold] {summary.signature[:20]}...
[bold]Wallet:[/bold] {summary.wallet[:20]}...
[bold]Timestamp:[/bold] {summary.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
[bold]Trade Path:[/bold] {' → '.join(summary.trade_path) if summary.trade_path else 'None'}
[bold]Platforms:[/bold] {', '.join(summary.platforms) if summary.platforms else 'None'}
[bold]Profit (USDC):[/bold] {summary.profit_usdc:.4f}
[bold]Pattern:[/bold] {summary.mev_pattern.value}
[bold]Confidence:[/bold] {summary.confidence_score:.2%}
        """
        panel = Panel(content.strip(), title=f"[{color}]{mev_status}[/{color}]", border_style=color)
        self.console.print(panel)

    async def analyze_recent_transactions(self, address: str, limit: int = 5):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=self.console) as progress:
            fetch_task = progress.add_task("Fetching recent transactions...", total=None)
            signatures = await self.rpc_client.get_signatures_for_address(address, limit)
            progress.update(fetch_task, completed=True)

            if not signatures:
                self.console.print("[red]No transactions found[/red]")
                return

            analyze_task = progress.add_task("Analyzing transactions...", total=len(signatures))
            for sig_obj in signatures:
                signature = sig_obj["signature"]
                summary = await self.analyzer.analyze_transaction(signature)
                if summary:
                    self.display_summary(summary)
                    self.console.print()
                progress.advance(analyze_task)

    def display_statistics(self, summaries: list[TransactionSummary]):
        if not summaries:
            return
        total = len(summaries)
        mev_count = sum(1 for s in summaries if s.is_mev)
        total_profit = sum(s.profit_usdc for s in summaries)

        table = Table(title="Analysis Statistics")
        table.add_column("Metric", style="bold")
        table.add_column("Value", style="cyan")

        table.add_row("Total Transactions", str(total))
        table.add_row("MEV Transactions", f"{mev_count} ({mev_count/total:.1%})")
        table.add_row("Total Profit (USDC)", f"{total_profit:.4f}")
        table.add_row("Avg Profit per MEV", f"{total_profit/mev_count:.4f}" if mev_count > 0 else "N/A")

        self.console.print(table)

@click.group()
@click.option('--log-level', default='INFO', help='Set logging level')
def cli(log_level):
    import logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@cli.command()
@click.option('--address', required=False, default=None, help='Solana program address')
@click.option('--limit', default=5, help='Number of transactions to analyze')
def analyze(address, limit):
    """Analyze recent transactions for MEV patterns"""
    from .config import Config
    address = address or Config.DEFAULT_PROGRAM

    async def run():
        app = MEVAnalyzerCLI()
        await app.analyze_recent_transactions(address, limit)

    asyncio.run(run())

@cli.command()
@click.argument('signature')
def single(signature):
    """Analyze a single transaction by signature"""
    async def run():
        app = MEVAnalyzerCLI()
        summary = await app.analyzer.analyze_transaction(signature)
        if summary:
            app.display_summary(summary)
        else:
            app.console.print("[red]Failed to analyze transaction[/red]")

    asyncio.run(run())
