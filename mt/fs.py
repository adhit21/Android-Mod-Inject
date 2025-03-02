#!/usr/bin/python

import subprocess, sys, time, os

# Warna terminal
c1 = "\033[1;32m"
c2 = "\033[0m"
c3 = "\033[1;34m"
c4 = "\033[1;31m"
c5 = "\033[1;33m"

def clear_screen():
    os.system('clear')

def wait_for_device(mode="adb"):
    while True:
        if mode == "adb":
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            devices_output = result.stdout.strip()
        elif mode == "fastboot":
            result = subprocess.run(["fastboot", "devices"], capture_output=True)
            devices_output = result.stdout.decode(errors="ignore").strip()

        print(f"\n{c5}{mode.capitalize()} Devices Output:{c2}\n{devices_output}\n")

        devices = []
        for line in devices_output.split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) == 2 and (mode == "adb" or parts[1] == "fastboot"):
                    devices.append(parts[0])

        if len(devices) > 0:
            return True

        print(f"{c5}Waiting for the device to connect in {mode} mode...{c2}")
        time.sleep(2)
        sys.stdout.flush()
        time.sleep(1)

def run_command(cmd, message, mode="adb"):
    wait_for_device(mode)
    print(f"\n{c1}{message}{c2}")
    subprocess.run(cmd, shell=True)

def main():
    while True:
        clear_screen()
        print(f"{c3}ADB & Fastboot Helper Menu{c2}\n")
        print("╔══════════════════════════════════════╗")
        print("║ 1 ➤ ADB Reboot to Bootloader          ║")
        print("║ 2 ➤ ADB Reboot to Recovery            ║")
        print("║ 3 ➤ Fastboot Reboot                   ║")
        print("║ 4 ➤ Fastboot Reboot to Recovery       ║")
        print("║ 5 ➤ Fix DM-Verity Corruption          ║")
        print("║ 6 ➤ Exit                              ║")
        print("╚══════════════════════════════════════╝")
        
        choice = input(f"\n{c4}Enter options: {c2}").strip()

        if choice == "1":
            run_command("adb reboot bootloader", "Rebooting to Bootloader...", mode="adb")
        elif choice == "2":
            run_command("adb reboot recovery", "Rebooting to Recovery...", mode="adb")
        elif choice == "3":
            run_command("fastboot reboot", "Rebooting device...", mode="fastboot")
        elif choice == "4":
            run_command("fastboot reboot recovery", "Rebooting to Recovery (Fastboot)...", mode="fastboot")
        elif choice == "5":
            run_command("fastboot oem cmds fix", "Fixing DM-Verity Corruption...", mode="fastboot")
        elif choice == "6":
            print(f"{c5}Exiting...{c2}")
            break
        else:
            print(f"{c4}Invalid selection!{c2}")
            time.sleep(1)

if __name__ == "__main__":
    main()
