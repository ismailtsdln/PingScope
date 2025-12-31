#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from source.utils import clear_screen, get_ping_command, get_subnet_hosts
from source.scanner import scan_hosts, trace_route
from source.database import get_history
from source.stats import generate_graph
from source.config import config
from source.ping_test_tool_core import run_ping, VERSION 

console = Console()

def show_history_table(limit=10):
    """Displays ping history from the database."""
    rows = get_history(limit)
    if not rows:
        console.print("[yellow]Geçmiş kaydı bulunamadı.[/yellow]")
        return

    table = Table(title=f"Ping Geçmişi (Son {len(rows)} Kayıt)", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("Tarih")
    table.add_column("Hedef")
    table.add_column("G/A")
    table.add_column("Kayıp")
    table.add_column("Min/Max/Avg (ms)")

    for r in rows:
        table.add_row(
            str(r[0]), r[1], r[2], f"{r[3]}/{r[4]}", f"{r[5]:.1f}%",
            f"{r[6]:.1f}/{r[7]:.1f}/{r[8]:.1f}"
        )
    console.print("\n", table)

def show_scan_results(results, title="Tarama Sonuçları"):
    """Displays scan results in a nice table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Host", style="dim")
    table.add_column("Durum")
    table.add_column("Ort. Gecikme (ms)")

    for r in sorted(results, key=lambda x: x['host']):
        status_style = "green" if r['status'] == "UP" else "red"
        table.add_row(
            r['host'], 
            f"[{status_style}]{r['status']}[/{status_style}]", 
            str(round(r['avg_ms'], 2)) if r['avg_ms'] is not None else "-"
        )
    console.print("\n", table)

def main():
    parser = argparse.ArgumentParser(description="Python Ping Test Tool - Modern Edition")
    parser.add_argument("host", nargs="?", help="Hedef IP adresi veya domain")
    
    # Defaults from config
    p_cfg = config.get("ping", {})
    s_cfg = config.get("scanner", {})
    h_cfg = config.get("history", {})
    
    parser.add_argument("-c", "--count", type=int, default=p_cfg.get("count", 4), help="Gönderilecek paket sayısı")
    parser.add_argument("-s", "--size", type=int, default=p_cfg.get("size", 32), help="Paket boyutu")
    parser.add_argument("-t", "--timeout", type=int, default=p_cfg.get("timeout", 2), help="Zaman aşımı")
    parser.add_argument("-C", "--continuous", action="store_true", help="Sürekli ping")
    parser.add_argument("-o", "--output", help="Sonuçların kaydedileceği dosya yolu")
    parser.add_argument("-f", "--format", choices=['json', 'csv', 'txt'], default='txt', help="Dışa aktarma formatı")
    parser.add_argument("-m", "--multi", nargs="+", help="Birden fazla hedefi aynı anda tara")
    parser.add_argument("-S", "--sweep", help="Belirli bir subnet'i tara (örn: 192.168.1.0/24)")
    parser.add_argument("-T", "--trace", action="store_true", help="Traceroute gerçekleştir")
    parser.add_argument("-H", "--history", action="store_true", help="Ping geçmişini görüntüle")
    parser.add_argument("-g", "--graph", action="store_true", help="Gecikme grafiği oluştur")
    parser.add_argument("--threads", type=int, default=s_cfg.get("threads", 10), help="Tarama için thread sayısı")
    parser.add_argument("-v", "--version", action="version", version=f"PyPing {VERSION}")
    
    args = parser.parse_args()
    
    if args.history:
        show_history_table(h_cfg.get("limit", 10))
        return

    if args.graph:
        console.print("[bold blue][*] Grafik oluşturuluyor...[/bold blue]")
        success = generate_graph(host=args.host, output=args.output if args.output else "ping_graph.png")
        if success:
            console.print(f"[bold green][+] Grafik kaydedildi: {args.output if args.output else 'ping_graph.png'}[/bold green]")
        else:
            console.print("[red][!] Grafik oluşturmak için yeterli veri bulunamadı.[/red]")
        return

    if args.trace and args.host:
        console.print(Panel(f"[bold blue]Traceroute başlatılıyor: {args.host}[/bold blue]"))
        process = trace_route(args.host)
        if process:
            for line in process.stdout:
                console.print(line.strip())
            process.wait()
        else:
            console.print("[red][!] Traceroute başlatılamadı.[/red]")
        return

    if args.sweep:
        hosts = get_subnet_hosts(args.sweep)
        if not hosts:
            console.print(f"[red][!] Geçersiz subnet: {args.sweep}[/red]")
            return
        console.print(Panel(f"[bold blue]Subnet Taraması Başlatılıyor: {args.sweep}[/bold blue]\n[dim]Toplam Host: {len(hosts)}[/dim]"))
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description=f"Scanning {args.sweep}...", total=None)
            results = scan_hosts(hosts, threads=args.threads, timeout=args.timeout)
        show_scan_results([r for r in results if r['status'] == "UP"], title=f"{args.sweep} Aktif Hostlar")

    elif args.multi:
        console.print(Panel(f"[bold blue]Multi-Host Taraması Başlatılıyor[/bold blue]\n[dim]Hedef Sayısı: {len(args.multi)}[/dim]"))
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
            progress.add_task(description="Scanning hosts...", total=None)
            results = scan_hosts(args.multi, threads=args.threads, timeout=args.timeout)
        show_scan_results(results)

    elif args.host:
        command = get_ping_command(args.host, args.count, args.size, args.timeout, args.continuous)
        run_ping(command, output=args.output, fmt=args.format)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
