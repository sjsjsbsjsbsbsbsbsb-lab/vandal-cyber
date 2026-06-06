import os
import platform
import subprocess
import sys

def run(cmd):
    print(f"[+] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=False)

def is_termux():
    return os.path.exists("/data/data/com.termux")

def is_kali():
    return "kali" in platform.platform().lower() or os.path.exists("/etc/debian_version")

def install_termux():
    print("\n[+] Detected: Termux\n")
    
    run(["pkg", "update", "-y"])
    run(["pkg", "upgrade", "-y"])

    packages = [
        "python",
        "nmap",
        "dnsutils",
        "whois",
        "git",
        "curl",
        "clang",
        "make",
        "openssl",
        "libffi",
        "coreutils"
    ]

    for p in packages:
        run(["pkg", "install", p, "-y"])

def install_kali():
    print("\n[+] Detected: Kali Linux\n")
    
    run(["sudo", "apt", "update", "-y"])
    run(["sudo", "apt", "upgrade", "-y"])

    packages = [
        "python3",
        "nmap",
        "dnsutils",
        "whois",
        "git",
        "curl",
        "build-essential",
        "openssl",
        "libffi-dev"
    ]

    for p in packages:
        run(["sudo", "apt", "install", p, "-y"])

def install_pip():
    print("\n[+] Installing Python modules...\n")

    pip_packages = [
        "requests",
        "urllib3",
        "colorama",
        "python-nmap",
        "scapy",
        "prettytable"
    ]

    for p in pip_packages:
        run([sys.executable, "-m", "pip", "install", p])

def main():
    print("=================================")
    print("   ZODIAC INSTALLER SCRIPT")
    print("=================================\n")

    if is_termux():
        install_termux()
    elif is_kali():
        install_kali()
    else:
        print("[-] Unsupported system!")
        sys.exit(1)

    install_pip()

    print("\n[✔] Installation completed successfully!")

if __name__ == "__main__":
    main()