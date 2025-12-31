#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import csv
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from source.utils import get_ping_command, parse_ping_line
from source.database import init_db, save_history
from source.logger import logger

VERSION = "1.5.0"
console = Console()

# Initialize DB
init_db()

def calculate_jitter(latencies):
    """Calculates jitter (average variation between consecutive samples)."""
    if len(latencies) < 2: return 0
    diffs = [abs(latencies[i] - latencies[i-1]) for i in range(1, len(latencies))]
    return sum(diffs) / len(diffs)

def export_results(filename, fmt, stats):
    """Exports ping statistics to a file."""
    try:
        if fmt == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4, ensure_ascii=False)
        elif fmt == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=stats.keys())
                writer.writeheader()
                writer.writerow(stats)
        else: # txt
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"PyPing Test Results - {stats['timestamp']}\n")
                f.write("-" * 40 + "\n")
                for k, v in stats.items():
                    f.write(f"{k}: {v}\n")
        console.print(f"[bold green][+] Sonuçlar dışa aktarıldı: {filename}[/bold green]")
    except Exception as e:
        console.print(f"[bold red][!] Dışa aktarma hatası: {e}[/bold red]")

def run_ping(command, output=None, fmt='txt'):
    """Executes the ping command, streams output, and calculates stats."""
    latencies = []
    packets_received = 0
    host = command[-1]
    
    try:
        logger.info(f"Starting ping test for {host}")
        console.print(Panel(f"[bold blue]Pinging {host}[/bold blue]\n[dim]Command: {' '.join(command)}[/dim]", expand=False))
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            line = line.strip()
            if not line: continue
            latency = parse_ping_line(line)
            if latency is not None:
                latencies.append(latency)
                packets_received += 1
                console.print(f"[green]✔[/green] {line}")
            elif any(x in line.lower() for x in ["timeout", "timed out", "kayıp", "unreachable"]):
                console.print(f"[red]✘[/red] {line}")
            else:
                console.print(f"[dim]{line}[/dim]")
        process.wait()

        # Packets sent logic
        if "-c" in command: sent = int(command[command.index("-c")+1])
        elif "-n" in command: sent = int(command[command.index("-n")+1])
        else: sent = len(latencies) if packets_received > 0 else 4 # Fallback

        stats = show_stats(latencies, packets_received, sent, host)
        if stats:
            save_history(stats)
            logger.info(f"Test completed for {host}: {stats['packet_loss_pct']}% loss, {stats['avg_ms']}ms avg")
        if output and stats:
            export_results(output, fmt, stats)
            
    except KeyboardInterrupt:
        logger.info(f"Test cancelled by user for {host}")
        console.print("\n[bold red][!] İşlem kullanıcı tarafından iptal edildi.[/bold red]")
    except Exception as e:
        logger.error(f"Unexpected error during ping to {host}: {e}")
        console.print(f"\n[bold red][!] Beklenmedik bir hata oluştu: {e}[/bold red]")

def show_stats(latencies, received, sent, host):
    """Displays statistics and returns them as a dict."""
    if not latencies:
        console.print("\n[bold red]İstatistik hesaplanamadı.[/bold red]")
        return None

    loss = ((sent - received) / sent) * 100 if sent > 0 else 0
    avg = sum(latencies) / len(latencies)
    mini = min(latencies)
    maxi = max(latencies)
    jitter = calculate_jitter(latencies)

    # Threshold alerts
    latency_threshold = 100 # ms
    loss_threshold = 5 # %
    
    table = Table(title="Ping Test İstatistikleri", show_header=True, header_style="bold magenta")
    table.add_column("Parametre", style="dim"); table.add_column("Değer")
    table.add_row("Hedef", host)
    table.add_row("Gönderilen / Alınan", f"{sent} / {received}")
    
    loss_color = "red" if loss > loss_threshold else "green"
    table.add_row("Paket Kaybı", f"[{loss_color}]{loss:.1f}%[/{loss_color}]")
    
    avg_color = "red" if avg > latency_threshold else "green"
    table.add_row("Min / Max / Avg", f"{mini:.2f} / {maxi:.2f} / [{avg_color}]{avg:.2f}[/{avg_color}] ms")
    table.add_row("Jitter", f"{jitter:.2f} ms")
    
    if loss > loss_threshold:
        console.print(f"[bold red][!] UYARI: Yüksek paket kaybı tespit edildi! ({loss:.1f}%)[/bold red]")
    if avg > latency_threshold:
        console.print(f"[bold red][!] UYARI: Yüksek gecikme tespit edildi! ({avg:.2f} ms)[/bold red]")
        
    console.print("\n", table)

    stats = {
        "host": host,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sent": sent,
        "received": received,
        "packet_loss_pct": round(loss, 2),
        "min_ms": round(mini, 2),
        "max_ms": round(maxi, 2),
        "avg_ms": round(avg, 2),
        "jitter_ms": round(jitter, 2)
    }
    return stats
