#!/usr/bin/python

version = "1.3.1"

import subprocess, requests, shutil, re, sys, os, time
from os import get_terminal_size
from datetime import datetime

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

os.system('clear')

def show_header():
    now = datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%H:%M")

    print(c1 + "=" * 56 + c2)
    ver = f"{c6}MiTool {bold}{version}{c2}"
    print(f"{c6}📅 {date_str}  ⏰ {time_str}{c2}")
    print(f"{c5}MiTool Version: {ver}{c2}")
    print(f"{c5}Author: adhit21{c2}")
    print(f"{c3}Type 'help' for guide!{c2}\n")

while True:
    show_header()

    menu = f"""
{c5}1. {c5}Cek Device Info
2. {c5}Unlock Bootloader
3. {c5}Request Unlock Bootloader
4. {c5}Flash Fastboot ROM
5. {c5}Flash Zip (Sideload)
6. {c5}Bypass
7. {c5}Mi Assistant
8. {c5}Firmware Content Extractor
9. {c5}ADB & FASTBOOT Helper
10. {c5}Exit
"""
    os.system('clear')
    show_header()
    print(menu)
    

    choice = input(f'{c4}Enter your choice(number): {c2}').strip().lower()

    if choice == "1":
        subprocess.run("$PREFIX/bin/mi-ck", shell=True)
    elif choice == "2":
        subprocess.run("$PREFIX/bin/miunlock", shell=True)
    elif choice == "3":
        subprocess.run("$PREFIX/bin/micomu", shell=True)
    elif choice == "4":
        subprocess.run("$PREFIX/bin/miflashf", shell=True)
    elif choice == "5":
        subprocess.run("$PREFIX/bin/miflashs", shell=True)
    elif choice == "6":
        subprocess.run("$PREFIX/bin/mibypass", shell=True)
    elif choice == "7":
        subprocess.run("$PREFIX/bin/miasst", shell=True)
    elif choice == "8":
        subprocess.run("$PREFIX/bin/mifce", shell=True)
    elif choice == "9":
        subprocess.run("$PREFIX/bin/mi-fastboot-h", shell=True)
    elif choice == "10":
        print(f"{c5}Exiting MiTool...{c2}")
        loading_animation("Closing")
        os.system('clear')
        exit()
    elif choice in ["h", "help"]:
        subprocess.run("$PREFIX/bin/mihelp", shell=True)
    elif choice in ["u", "update"]:
        print(f"{c6}Updating MiTool...{c2}")
        loading_animation("Downloading")
        subprocess.run("curl -s https://raw.githubusercontent.com/adhit21/mi-tool/main/install.sh | bash", shell=True)
        exit()
    else:
        for i in range(3):
            sys.stdout.write(f"\r{c4}Invalid choice! Please try again{'.' * (i+1)}{c2}")
            sys.stdout.flush()
            time.sleep(0.5)
        print(f"\r{c4}Invalid choice! Please enter a valid option.{c2}\n")
        
