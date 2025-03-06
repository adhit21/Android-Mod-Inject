#!/usr/bin/python


import os
import re
import time
import requests

def fetch_page(url):
    os.system(f"wget -q -O workflow_page.html '{url}'")

def parse_steps():
    with open("workflow_page.html", "r", encoding="utf-8") as f:
        content = f.read()

    steps = re.findall(
        r'data-name="(.*?)".*?data-number="(\d+)".*?data-conclusion="(success|failure|skipped|cancelled)"',
        content, re.DOTALL
    )
    return steps

def monitor_workflow(url):
    print("process is running... ", end="", flush=True)

    dots = 0
    while True:
        fetch_page(url)
        steps = parse_steps()

        
        for name, number, conclusion in steps:
            if conclusion == "failure":
                os.remove("workflow_page.html")
                if number in ["7", "8"]:
                    print(f'\nFailed to fetch "{name}" because the file is not available')
                else:
                    print("\nProcess failed")
                return False 

        
        if ('21', 'success') in [(n, c) for _, n, c in steps]:
            print("\nProcess complete")
            os.remove("workflow_page.html")
            return True  

        
        dots = (dots + 1) % 5
        print("\rprocess unpacking firmware is running" + "." * dots + " ", end="", flush=True)

        time.sleep(1)

def download_file(url, folder_path):
    filename = url.split('/')[-1]
    filepath = os.path.join(folder_path, filename)

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                progress = int(50 * downloaded_size / total_size)
                bar = f"[{'=' * progress}{' ' * (50 - progress)}]"
                print(f"\rDownloading: {bar} {downloaded_size}/{total_size} bytes", end="", flush=True)

    print(f"\nFile '{filename}' saved to Downloads/firmware-extractor folder")

def main():
    os.system("clear")
    print("\n\033[1;36m\nGet file.img from a ROM without downloading the ROM!\n")
    print("*Firmware-Content-Extractor* is here to help:\n")
    print("➤ Step 1: Analyzes the ROM on external servers")
    print("➤ Step 2: Provides you with a direct download link")
    print("\n✨ **Saving both data and time** by avoiding the download of large ROM files!\n\033[0m\n")

    c1 = "\033[1;32m"
    c2 = "\033[0m"
    c4 = "\033[1;31m"

    while True:
        print("\nGet:\n")
        print(f"  ━ {c1}1{c2} boot.img")
        print(f"  ━ {c1}2{c2} init_boot.img")
        print(f"\n\n  ━ {c4}ctrl+d to exit main menu{c2}")
        choice = input(f"\nEnter your {c1}choice{c2}: ").strip()

        option_map = {"1": "boot_img", "2": "init_boot_img"}

        if choice in option_map:
            option = option_map[choice]
            break
        else:
            print("\nInvalid choice !\n")

    while True:
        firmware_url = input("\nEnter the firmware URL\n    (Recovery/Custom Rom): ").strip()

        if firmware_url.startswith("http"):
            break
        else:
            print("\nInvalid URL. Please enter a valid URL starting with http:// or https://\n")

    api_url = f"https://dw.nanalegends353.workers.dev?get={option}&url={firmware_url}"
    print("\nanalizyng url..\n")
    response = requests.get(api_url)
    

    if "result: available" in response.text:
        download_link = re.search(r'link: (https?://\S+)', response.text).group(1)
        print("\nDirect file available, starting download...")
        os.makedirs(os.path.expanduser("~/storage/downloads/firmware-extractor/"), exist_ok=True)
        download_file(download_link, os.path.expanduser("~/storage/downloads/firmware-extractor/"))
        return

    progress_url = re.search(r'Track progress: (https?://\S+)', response.text).group(1)
    #print(f"\nMonitoring progress at: {progress_url}\n")

    if monitor_workflow(progress_url):
        final_link = re.search(r'It will be available at this link: (https?://\S+)', response.text).group(1)
        print("\nProcess completed successfully, starting download...")
        os.makedirs(os.path.expanduser("~/storage/downloads/firmware-extractor/"), exist_ok=True)
        download_file(final_link, os.path.expanduser("~/storage/downloads/firmware-extractor/"))
    else:
        print("\nProcess failed, no file to download.")

if __name__ == "__main__":
    main()
