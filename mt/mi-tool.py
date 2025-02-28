#!/usr/bin/python

version = "1.1.0"
gg = "1.5.3"
import subprocess, requests, shutil, re, sys, os, time
from os import get_terminal_size

os.system('clear')





c1 = "\033[1;32m"
c2 = "\033[0m"
c3 = "\033[1;34m"
c4 = "\033[1;31m"
c5 = "\033[1;33m"
c6 = "\033[1;36m"
c7 = "\033[1;35m"
c8 = "\033[1;37m"
bold = "\033[1m"


def loading_animation(text="Loading"):
    bar_length = 30
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = f"[{'=' * i}{' ' * (bar_length - i)}] {percent}%"
        sys.stdout.write(f"\r{c5}{text}: {bar}{c2}")
        sys.stdout.flush()
        time.sleep(0.1)
    print("")


if not os.path.isdir(os.path.expanduser('~/storage')):
    print(f"\n{c4}Please grant permission via command:{c2}")
    print(f"{c6}termux-setup-storage{c2}\n")
    exit()

if 'u' in sys.argv or 'update' in sys.argv:
    print(f"{c6}Updating MiTool...{c2}")
    loading_animation("Downloading")
    subprocess.run("curl -s https://raw.githubusercontent.com/adhit21/mi-tool/main/install.sh | bash", shell=True)
    exit()

try:
    print(f"{c6}Checking for updates...{c2}")
    loading_animation("Checking")

    response = requests.get("https://raw.githubusercontent.com/adhit21/Android-Mod-Inject/master/mt/mi-tool.py", timeout=3)
    response.raise_for_status()

    if response.status_code == 200:
        version_match = re.search(r'version\s*=\s*"([^"]+)"', response.text)
        if version_match:
            vcloud = version_match.group(1)
            if vcloud > version:
                print(f"\n{c5}An update is available!{c2}")
                print(f"Updating from {c1}{version}{c2} to {c1}{vcloud}{c2} ...")
                loading_animation("Downloading update")
                subprocess.run("curl -s https://raw.githubusercontent.com/adhit21/mi-tool/main/install.sh | bash", shell=True)
                exit()
except requests.exceptions.ConnectionError:
    print(f"{c4}No internet connection! Skipping update check.{c2}")
except requests.exceptions.Timeout:
    print(f"{c4}Update check timed out!{c2}")

while True:
    _l = c1 + "═" * 56 + c2
    print(_l)

    ver = f"{c6}MiTool {bold}{version}{c2}"
    b = '━' * (len(ver) + 4)
    p = ' ' * ((get_terminal_size().columns - len(b)) // 2)

    furl = f"""
{p}{c5}┏{b}┓{c2}
{p}{c5}┃  {ver}  ┃{c2}
{p}{c5}┗{b}┛{c2}
"""
    print(furl + f" ━ {c3}Type 'help' for guide!{c2}")

    menu = f"""
{c7}╔════════════════════════════════════════╗
{c7}║  {c8}⚡ {c6}MiTool Main Menu {c8}⚡                {c7}║
{c7}╠════════════════════════════════════════╣
{c7}║ {c1}1{c2} ➤ {c5}Unlock Bootloader                  {c7}║
{c7}║ {c1}2{c2} ➤ {c5}Flash Fastboot ROM                 {c7}║
{c7}║ {c1}3{c2} ➤ {c5}Flash Zip (Sideload)               {c7}║
{c7}║ {c1}4{c2} ➤ {c5}Bypass                             {c7}║
{c7}║ {c1}5{c2} ➤ {c5}Mi Assistant                       {c7}║
{c7}║ {c1}6{c2} ➤ {c5}Firmware Content Extractor         {c7}║
{c7}║ {c4}exit{c2} ➤ {c5}Exit                            {c7}║
{c7}╚════════════════════════════════════════╝
"""
    print(menu)

    sys.stdout.write(f'{c4}Enter your {c1}choice{c2}: ')
    sys.stdout.flush()
    choice = input().strip().lower()

    if choice == "1":
        subprocess.run("$PREFIX/bin/miunlock", shell=True)
    elif choice == "2":
        subprocess.run("$PREFIX/bin/miflashf", shell=True)
    elif choice == "3":
        subprocess.run("$PREFIX/bin/miflashs", shell=True)
    elif choice == "4":
        subprocess.run("$PREFIX/bin/mibypass", shell=True)
    elif choice == "5":
        subprocess.run("$PREFIX/bin/miasst", shell=True)
    elif choice == "6":
        subprocess.run("$PREFIX/bin/mifce", shell=True)
    elif choice in ["h", "help"]:
        subprocess.run("$PREFIX/bin/mihelp", shell=True)
    elif choice in ["u", "update"]:
        print(f"{c6}Updating MiTool...{c2}")
        loading_animation("Downloading")
        subprocess.run("curl -s https://raw.githubusercontent.com/adhit21/mi-tool/main/install.sh | bash", shell=True)
        exit()
    elif choice == "exit":
        print(f"{c5}Exiting MiTool...{c2}")
        loading_animation("Closing")
        exit()
    else:
        for i in range(3):
            sys.stdout.write(f"\r{c4}Invalid choice! Please try again{'.' * (i+1)}{c2}")
            sys.stdout.flush()
            time.sleep(0.5)
        print(f"\r{c4}Invalid choice! Please enter a valid option.{c2}\n")
