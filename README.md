# Vandal-Bomber

# Features
 یک فریم‌ورک پنتست که ابزارهایی برای اسکن شبکه (nmap، ping sweep)، کشف ساب‌دامین، تحلیل DNS، OSINT و WHOIS، و بررسی وب (SQLi، XSS، دایرکتوری دارد 

همچنین قابلیت‌های لینوکس مثل بررسی SUID، کرون‌جاب‌ها، قابلیت‌ها و وضعیت sudo را برای privilege escalation دارد
ابزارهایی برای تولید payload، reverse shell، و اجرای Metasploit و sqlmap هم در آن گنجانده شده است
سیستم لاگینگ ، مدیریت کانفیگ و تشخیص پلتفرم (Windows/Linux/Android) هم دارد

# termux

pkg update && pkg upgrade
pkg install python
pkg install nmap
pkg install dnsutils
pkg install whois
pkg install git
pkg install curl
pkg install clang
pkg install make
pkg install openssl
pkg install libffi
pkg install coreutils

# kali linux

sudo apt update && sudo apt upgrade
sudo apt install python3
sudo apt install nmap
sudo apt install dnsutils
sudo apt install whois
sudo apt install git
sudo apt install curl
sudo apt install build-essential
sudo apt install openssl
sudo apt install libffi-dev

# Modules for both ( for Kali Linux and Termux )

pip install requests
pip install urllib3
pip install colorama
pip install python-nmap
pip install scapy
pip install prettytable

# Install the tool

sudo apt install sqlmap metasploit-framework gobuster hashcat
sudo apt install sublist3r theharvester

# Run

git clone https://github.com/sjsjsbsjsbsbsbsbsb-lab/vandal-cyber

cd vandal-cyber

python3 atak.py

# Owner = Zodiac