import subprocess
import json

# Kode warna ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def get_usb_device_path():
    try:
        print(f"{CYAN}Detecting USB devices...{RESET}")
        # Jalankan `termux-usb -l`
        result = subprocess.run(['termux-usb', '-l'], capture_output=True, text=True)

        # Parse JSON hasilnya
        usb_list = json.loads(result.stdout)

        if len(usb_list) == 0:
            print(f"{RED}No USB device detected.{RESET}")
            return None

        # Ambil device pertama
        usb_device_path = usb_list[0]
        print(f"{GREEN}USB device detected: {YELLOW}{usb_device_path}{RESET}")

        return usb_device_path

    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return None

def run_usbtest(device_path):
    try:
        
        subprocess.run(['termux-usb', '-r', '-e', './usbtest', device_path])
    except Exception as e:
        print(f"{RED}Error running usbtest: {e}{RESET}")

def main():
    device_path = get_usb_device_path()
    if device_path:
        run_usbtest(device_path)

    # Tunggu user tekan Enter sebelum keluar
    input(f"\n{GREEN}Press Enter to exit...{RESET}")

if __name__ == '__main__':
    main()
