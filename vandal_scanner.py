#!/usr/bin/env python3
# Ultimate Vandal Scanner - Part 1
# Author: HackerAI
# Termux Ready

import os
import sys
import socket
import threading
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt

console = Console()

# ------------------------------
# Clear Screen Function
# ------------------------------
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ------------------------------
# Banner
# ------------------------------
def print_banner():
    clear_screen()
    banner = """
╭──────────────────────────────────────────────────────────────────────╮
│                                                                      │
│ ┌────────────────────────────────────────────────────────────┐       │
│ │ ██▒   █▓ ▄▄▄       ███▄    █ ▓█████▄ ▄▄▄       ██▓         │       │
│ │▓██░   █▒▒████▄     ██ ▀█   █ ▒██▀ ██▒████▄    ▓██▒         │       │
│ │ ▓██  █▒░▒██  ▀█▄  ▓██  ▀█ ██▒░██   █▒██  ▀█▄  ▒██░         │       │
│ │  ▒██ █░░░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█▄   ▌██▄▄▄▄██ ▒██░         │       │
│ │   ▒▀█░   ▓█   ▓██▒▒██░   ▓██░░▒████▓ ▓█   ▓██▒░██████▒     │       │
│ │   ░ ▐░   ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒▓  ▒ ▒▒   ▓▒█░░ ▒░▓  ░     │       │
│ │   ░ ░░    ▒   ▒▒ ░░ ░░   ░ ▒░ ░ ▒  ▒  ▒   ▒▒ ░░ ░ ▒  ░     │       │
│ │     ░░    ░   ▒      ░   ░ ░  ░ ░  ░  ░   ▒     ░ ░        │       │
│ │      ░        ░  ░         ░    ░         ░  ░    ░  ░    │        │
│ │     ░                              ░                      │        │
│ │                V A N D A L   S C A N N E R                 │       │
│ └────────────────────────────────────────────────────────────┘       │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
"""
    console.print(banner, style="bold red")

# ------------------------------
# Resolve Hostname
# ------------------------------
def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

# ------------------------------
# Display Live Hosts Table
# ------------------------------
def display_live_hosts(live_hosts):
    table = Table(title="📊 Live Hosts", box=box.ROUNDED)
    table.add_column("IP", style="cyan")
    table.add_column("Hostname", style="green")
    table.add_column("Status", style="bold green")
    
    for host in live_hosts:
        table.add_row(host.get("ip", "N/A"),
                      host.get("hostname", "Unknown"),
                      "🟢 UP")
    console.print(table)

# ------------------------------
# Main Menu
# ------------------------------
def main_menu():
    console.print("\nSelect scan type:")
    console.print("1) Quick Scan")
    console.print("2) Full Scan")
    console.print("3) Web Scan")
    console.print("4) Root Scan (Requires root)")
    choice = Prompt.ask("Enter option [1-4]", choices=["1","2","3","4"])
    return choice

# ------------------------------
# Example Live Hosts Placeholder
# ------------------------------
live_hosts = [
    {"ip":"192.168.1.1","hostname":"router.local"},
    {"ip":"192.168.1.100","hostname":"device1.local"},
]

# ------------------------------
# Run Part 1 Demo
# ------------------------------
if __name__ == "__main__":
    print_banner()
    display_live_hosts(live_hosts)
    selected = main_menu()
    console.print(f"Selected option: {selected}")
