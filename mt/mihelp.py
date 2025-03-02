#!/usr/bin/python

import os
import shutil

print(f"\033[H\033[J")

RESET = "\033[0m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
GRAY = "\033[1;30m"
CYAN = "\033[1;36m"

terminal_width = shutil.get_terminal_size().columns

def print_line():
    print(f"{GRAY}{'━' * terminal_width}{RESET}")

print_line()
print(f"{CYAN}{'MiTool - Help & Guide'.center(terminal_width)}{RESET}")
print_line()

menu = [
    ("Cek Device Info", "➤ checking device info"),
    ("Unlock Bootloader", "➤ to unlock bootloader"),
    ("Request Unlock Bootloader", "➤ request unlock permission"),
    ("Flash Fastboot ROM", "➤ flashing ROM via fastboot"),
    ("Flash Zip (Sideload)", "➤ flashing zip via sideload"),
    ("Bypass", "➤ bypass Mi Account"),
    ("Mi Assistant", "➤ enter Mi Assistant mode"),
    ("Firmware Content Extractor", "➤ extract firmware contents"),
    ("ADB & FASTBOOT Helper", "➤ quick ADB & Fastboot tools"),
    ("Exit MiTool", "➤ exit the tool")
]

for item in menu:
    feature, description = item
    print(f"{CYAN}{feature.ljust(35)} {GRAY}{description}{RESET}")

print_line()

print(f"""
{CYAN}MiTool Shortcuts:{RESET}
- To update manually: {GREEN}mi-tool u{RESET}
- For help anytime: {GREEN}mihelp{RESET}

{CYAN}Notes:{RESET}
- Make sure your device is in {YELLOW}Fastboot Mode{RESET} or {YELLOW}Recovery Mode{RESET} when performing specific operations.
- Always backup important data before flashing or unlocking.

{CYAN}Contact & Feedback:{RESET}
- Telegram: https://t.me/+62895331944545
""")

print_line()

# Tambahkan fitur tekan enter agar tidak langsung keluar
input(f"\n{YELLOW}Press Enter to exit...{RESET}")
