#!/usr/bin/python

import os
import json
import importlib
import requests
import hashlib
import threading
import sys
from datetime import datetime, timedelta, timezone

version = "1.1"


for lib in ['requests', 'ntplib']:
    try:
        importlib.import_module(lib)
    except ModuleNotFoundError:
        os.system(f'pip install {lib}')
        break

headers = {"User-Agent": "offici5l/MiCommunityTool"}
login_file = "login.json"

# Fungsi menyimpan data login
def save_login_data(user, pwd):
    with open(login_file, "w") as f:
        json.dump({"user": user, "pwd": pwd}, f)

# Fungsi mengambil data login
def load_login_data():
    if os.path.exists(login_file):
        with open(login_file, "r") as f:
            return json.load(f)
    return None

# Fungsi hapus data login
def delete_login_data():
    if os.path.exists(login_file):
        os.remove(login_file)

# Fungsi meminta login data
def get_login_data():
    login_data = load_login_data()
    if login_data:
        saved_user = login_data["user"]
        print(f"Use saved login data? ({saved_user})\n(Press Enter to use saved login, Ctrl+D to logout)")
        try:
            input()
            return login_data["user"], login_data["pwd"]
        except EOFError:
            delete_login_data()
            print("\nLogin data deleted. Please enter new credentials.")

    user = input('\nEnter user: ')
    pwd = input('\nEnter pwd: ')
    save_login_data(user, pwd)
    return user, pwd

print(f"\n[V{version}] For issues or feedback:\n- Telegram: t.me/Offici5l_Group\n")


user, pwd = get_login_data()


try:
    r1 = requests.post("https://account.xiaomi.com/pass/serviceLoginAuth2", headers=headers, data={
        "callback": "https://sgp-api.buy.mi.com/bbs/api/global/user/login-back?followup=https%3A%2F%2Fnew.c.mi.com%2Fglobal%2F&sign=NTRhYmNhZWI1ZWM2YTFmY2U3YzU1NzZhOTBhYjJmZWI1ZjY3MWNiNQ%2C%2C",
        "sid": "18n_bbs_global",
        "_sign": "Phs2y/c0Xf7vJZG9Z6n9c+Nbn7g=",
        "user": user,
        "hash": hashlib.md5(pwd.encode('utf-8')).hexdigest().upper(),
        "_json": "true",
        "serviceParam": '{"checkSafePhone":false,"checkSafeAddress":false,"lsrp_score":0.0}'
    })

    json_data = json.loads(r1.text[11:])
    if json_data["code"] == 70016:
        exit("Invalid user or password")

    if "notificationUrl" in json_data:
        check = json_data["notificationUrl"]
        if "SetEmail" in check:
            exit(f"Verification required: Add email to your account: {check}")
        elif "BindAppealOrSafePhone" in check:
            exit(f"Verification required: Add phone number to your account: {check}")
        else:
            exit(f"Check: {check}")

    region = json.loads(requests.get(f"https://account.xiaomi.com/pass/user/login/region", headers=headers, cookies=r1.cookies.get_dict()).text[11:])["data"]["region"]
    print(f"\nAccount Region: {region}")
    location_url = json_data['location']
    r2 = requests.get(location_url, headers=headers, allow_redirects=False)
    cookies = r2.cookies.get_dict()

except Exception as e:
    exit(f"Error: {e}")

api = "https://sgp-api.buy.mi.com/bbs/api/global/"
url_state = api + "user/bl-switch/state"
url_apply = api + "apply/bl-auth"


def state_request():
    print("\n[STATE]:")
    try:
        state = requests.get(url_state, headers=headers, cookies=cookies).json()
    except Exception as e:
        exit(f"State error: {e}")

    if 'data' in state:
        state_data = state.get("data")
        is_pass = state_data.get("is_pass")
        button_state = state_data.get("button_state")
        deadline_format = state_data.get("deadline_format", "")

        if is_pass == 1:
            print(f"Unlock permission granted until Beijing time {deadline_format}\n")
            exit()
        else:
            if button_state == 1:
                print("Ready to apply for unlocking\n")
            elif button_state == 2:
                print(f"Account locked. Try again after {deadline_format}\n")
                exit()
            elif button_state == 3:
                print("Account must be at least 30 days old\n")
                exit()


def apply_request():
    data = '{"is_retry":true}'
    try:
        apply = requests.post(url_apply, headers=headers, data=data, cookies=cookies).json()
    except Exception as e:
        exit(f"Apply error: {e}")

    data = apply["data"]
    code = apply["code"]

    if code == 0:
        apply_result = data.get("apply_result")
        if apply_result == 1:
            print("Application successful")
            state_request()
            exit()
        elif apply_result == 4:
            deadline_format = data.get("deadline_format")
            print(f"Account locked. Try again after {deadline_format}\n")
            exit()
        elif apply_result == 3:
            deadline_format = data.get("deadline_format")
            date, time = deadline_format.split()
            print(f"Quota reached. Try again after {date} at {time} (GMT+8)\n")
            return 1
        elif apply_result == 5:
            print("Application failed. Please try again later\n")
            exit()
        elif apply_result == 6:
            print("Please try again in a minute\n")
            exit()
        elif apply_result == 7:
            print("Please try again later\n")
            exit()
    elif code == 100003:
        print("Failed\n")
        exit()
    elif code == 100001:
        print("Invalid parameters\n")
        exit()


state_request()

def china_time():
    print("\nPress Enter to send the request\n")
    stop = False

    def check_input():
        nonlocal stop
        input()
        stop = True

    threading.Thread(target=check_input, daemon=True).start()

    while not stop:
        china_time = datetime.now(timezone(timedelta(hours=8)))
        local_time = datetime.now().astimezone()
        sys.stdout.write(f"\rTime: [China: {china_time.strftime('%H:%M:%S.%f')[:-3]}]  |  [Local: {local_time.strftime('%H:%M:%S.%f')[:-3]}]")
        sys.stdout.flush()

china_time()

# Proses apply
if apply_request() == 1:
    while True:
        try:
            input("\nPress Enter to try again\n(Ctrl+D to exit)\n")
            apply_request()
        except (EOFError):
            exit()
