#!/usr/bin/python3
# GhostTrack - OSINT Tool
# Original by HUNX04 / HunxByts
# Improved version - refactored for reliability and usability

import json
import requests
import time
import os
import sys
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── ANSI COLOR CODES ────────────────────────────────────────────────────────
Re   = '\033[1;31m'
Gr   = '\033[1;32m'
Ye   = '\033[1;33m'
Blu  = '\033[1;34m'
Mage = '\033[1;35m'
Cy   = '\033[1;36m'
Wh   = '\033[1;37m'
Rst  = '\033[0m'

# ─── UTILITIES ────────────────────────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    clear()
    print(f"""{Cy}
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \____/_/ /_/\____/____/\__/     /_/ /_/   \__,_/\___/_/|_| {Rst}

              {Wh}[ + ]  C O D E   B Y  H U N X  [ + ]{Rst}
    """)


def run_banner(title="GHOST TRACKER"):
    clear()
    print(f"""{Wh}
         .-.
       .'   `.          {Wh}----------------------------------
       :g g   :         {Wh}| {Cy}{title:<32}{Wh}|
       : o    `.        {Wh}|       {Cy}@CODE BY HUNXBYTS      {Wh}|
      :         ``.     {Wh}----------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:'
           :              `.
            `.              `.     .
              `'`'`'`---..,___`;.-'{Rst}
    """)


def safe_get(d, *keys, default="N/A"):
    """Safely traverse nested dicts without KeyError."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d if d is not None else default


def check_internet():
    """Quick connectivity check before making API calls."""
    try:
        requests.get("https://api.ipify.org/", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        print(f"\n {Re}[!] No internet connection detected. Please check your network.{Rst}")
        return False


# ─── FEATURES ─────────────────────────────────────────────────────────────────

def IP_Track():
    run_banner("IP TRACKER")
    ip = input(f"{Wh}\n Enter IP target : {Gr}").strip()

    if not ip:
        print(f"{Re} [!] No IP address entered.{Rst}")
        return

    print(f"\n{Wh} Looking up {Cy}{ip}{Wh}...{Rst}")

    try:
        req_api = requests.get(f"https://ipwho.is/{ip}", timeout=10)
        req_api.raise_for_status()
        ip_data = req_api.json()
    except requests.exceptions.Timeout:
        print(f"{Re} [!] Request timed out. Try again.{Rst}")
        return
    except requests.exceptions.RequestException as e:
        print(f"{Re} [!] Request failed: {e}{Rst}")
        return
    except json.JSONDecodeError:
        print(f"{Re} [!] Failed to parse API response.{Rst}")
        return

    if not ip_data.get("success", False):
        print(f"{Re} [!] Invalid IP or API error: {ip_data.get('message', 'Unknown error')}{Rst}")
        return

    # Coordinates — keep as float for accurate map link
    lat = ip_data.get("latitude", 0)
    lon = ip_data.get("longitude", 0)
    maps_link = f"https://www.google.com/maps/@{lat},{lon},8z"

    print(f'\n {Wh}{"="*12} {Gr}SHOW INFORMATION IP ADDRESS {Wh}{"="*12}')
    rows = [
        ("IP Target",      ip),
        ("Type",           safe_get(ip_data, "type")),
        ("Country",        safe_get(ip_data, "country")),
        ("Country Code",   safe_get(ip_data, "country_code")),
        ("City",           safe_get(ip_data, "city")),
        ("Continent",      safe_get(ip_data, "continent")),
        ("Continent Code", safe_get(ip_data, "continent_code")),
        ("Region",         safe_get(ip_data, "region")),
        ("Region Code",    safe_get(ip_data, "region_code")),
        ("Latitude",       lat),
        ("Longitude",      lon),
        ("Maps",           maps_link),
        ("EU",             safe_get(ip_data, "is_eu")),
        ("Postal",         safe_get(ip_data, "postal")),
        ("Calling Code",   safe_get(ip_data, "calling_code")),
        ("Capital",        safe_get(ip_data, "capital")),
        ("Borders",        safe_get(ip_data, "borders")),
        ("Country Flag",   safe_get(ip_data, "flag", "emoji")),
        ("ASN",            safe_get(ip_data, "connection", "asn")),
        ("ORG",            safe_get(ip_data, "connection", "org")),
        ("ISP",            safe_get(ip_data, "connection", "isp")),
        ("Domain",         safe_get(ip_data, "connection", "domain")),
        ("Timezone ID",    safe_get(ip_data, "timezone", "id")),
        ("Timezone ABBR",  safe_get(ip_data, "timezone", "abbr")),
        ("DST",            safe_get(ip_data, "timezone", "is_dst")),
        ("Offset",         safe_get(ip_data, "timezone", "offset")),
        ("UTC",            safe_get(ip_data, "timezone", "utc")),
        ("Current Time",   safe_get(ip_data, "timezone", "current_time")),
    ]
    for label, value in rows:
        print(f" {Wh}{label:<18}:{Gr} {value}{Rst}")


def phoneGW():
    run_banner("PHONE NUMBER TRACKER")
    user_phone = input(f"\n {Wh}Enter phone number {Gr}(e.g. +6281xxxxxxxxx){Wh}: {Gr}").strip()

    if not user_phone:
        print(f"{Re} [!] No phone number entered.{Rst}")
        return

    try:
        parsed_number = phonenumbers.parse(user_phone, None)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        print(f"{Re} [!] Could not parse number: {e}{Rst}")
        return

    if not phonenumbers.is_valid_number(parsed_number):
        print(f"{Ye} [!] Warning: This number may not be valid.{Rst}")

    region_code         = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider      = carrier.name_for_number(parsed_number, "en") or "Unknown"
    location            = geocoder.description_for_number(parsed_number, "en") or "Unknown"
    is_valid            = phonenumbers.is_valid_number(parsed_number)
    is_possible         = phonenumbers.is_possible_number(parsed_number)
    fmt_intl            = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    fmt_e164            = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    fmt_mobile          = phonenumbers.format_number_for_mobile_dialing(parsed_number, region_code, with_formatting=True)
    number_type         = phonenumbers.number_type(parsed_number)
    tz_list             = timezone.time_zones_for_number(parsed_number)
    tz_str              = ', '.join(tz_list) if tz_list else "Unknown"

    type_map = {
        phonenumbers.PhoneNumberType.MOBILE:          "Mobile",
        phonenumbers.PhoneNumberType.FIXED_LINE:      "Fixed Line",
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        phonenumbers.PhoneNumberType.TOLL_FREE:       "Toll Free",
        phonenumbers.PhoneNumberType.PREMIUM_RATE:    "Premium Rate",
        phonenumbers.PhoneNumberType.VOIP:            "VoIP",
        phonenumbers.PhoneNumberType.PAGER:           "Pager",
        phonenumbers.PhoneNumberType.SHARED_COST:     "Shared Cost",
        phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    }
    type_str = type_map.get(number_type, "Unknown")

    print(f'\n {Wh}{"="*10} {Gr}SHOW INFORMATION PHONE NUMBER {Wh}{"="*10}')
    rows = [
        ("Location",           location),
        ("Region Code",        region_code),
        ("Timezone",           tz_str),
        ("Operator",           jenis_provider),
        ("Valid Number",       is_valid),
        ("Possible Number",    is_possible),
        ("Type",               type_str),
        ("International Fmt",  fmt_intl),
        ("E.164 Format",       fmt_e164),
        ("Mobile Dial Format", fmt_mobile),
        ("National Number",    parsed_number.national_number),
        ("Country Code",       f"+{parsed_number.country_code}"),
    ]
    print()
    for label, value in rows:
        print(f" {Wh}{label:<20}:{Gr} {value}{Rst}")


def TrackLu():
    run_banner("USERNAME TRACKER")
    username = input(f"\n {Wh}Enter Username : {Gr}").strip()

    if not username:
        print(f"{Re} [!] No username entered.{Rst}")
        return

    social_media = [
        {"url": "https://www.facebook.com/{}",          "name": "Facebook"},
        {"url": "https://www.twitter.com/{}",           "name": "Twitter / X"},
        {"url": "https://www.instagram.com/{}/",        "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}/",      "name": "LinkedIn"},
        {"url": "https://github.com/{}",                "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}/",        "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}",            "name": "Tumblr"},
        {"url": "https://www.youtube.com/@{}",          "name": "YouTube"},
        {"url": "https://soundcloud.com/{}",            "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}",      "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}",           "name": "TikTok"},
        {"url": "https://www.behance.net/{}",           "name": "Behance"},
        {"url": "https://medium.com/@{}",               "name": "Medium"},
        {"url": "https://www.quora.com/profile/{}",     "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}",     "name": "Flickr"},
        {"url": "https://www.twitch.tv/{}",             "name": "Twitch"},
        {"url": "https://dribbble.com/{}",              "name": "Dribbble"},
        {"url": "https://www.producthunt.com/@{}",      "name": "Product Hunt"},
        {"url": "https://t.me/{}",                      "name": "Telegram"},
        {"url": "https://www.reddit.com/user/{}",       "name": "Reddit"},
        {"url": "https://open.spotify.com/user/{}",     "name": "Spotify"},
        {"url": "https://www.deviantart.com/{}",        "name": "DeviantArt"},
        {"url": "https://www.patreon.com/{}",           "name": "Patreon"},
        {"url": "https://www.twitch.tv/{}",             "name": "Twitch"},
        {"url": "https://steamcommunity.com/id/{}",     "name": "Steam"},
    ]

    print(f"\n {Wh}Checking {Cy}{len(social_media)}{Wh} platforms for '{Cy}{username}{Wh}' ...{Rst}\n")

    found    = {}
    not_found = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def check_site(site):
        url = site["url"].format(username)
        try:
            resp = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            return site["name"], url, resp.status_code
        except requests.exceptions.RequestException:
            return site["name"], url, None

    # Deduplicate list before checking
    seen = set()
    unique_sites = []
    for s in social_media:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique_sites.append(s)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_site, site): site for site in unique_sites}
        for future in as_completed(futures):
            name, url, status = future.result()
            if status == 200:
                found[name] = url
            else:
                not_found.append(name)

    print(f' {Wh}{"="*10} {Gr}SHOW INFORMATION USERNAME {Wh}{"="*10}\n')

    if found:
        print(f" {Gr}[+] Found on {len(found)} platform(s):{Rst}\n")
        for site, url in sorted(found.items()):
            print(f"   {Wh}[ {Gr}✔ {Wh}] {Gr}{site:<20}{Wh}: {Cy}{url}{Rst}")
    else:
        print(f" {Ye} No profiles found.{Rst}")

    if not_found:
        print(f"\n {Re}[-] Not found / unavailable ({len(not_found)}):{Rst}")
        print(f"   {Ye}{', '.join(sorted(not_found))}{Rst}")


def showIP():
    run_banner("YOUR PUBLIC IP")
    try:
        response = requests.get("https://api.ipify.org/", timeout=10)
        response.raise_for_status()
        my_ip = response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"{Re} [!] Failed to retrieve IP: {e}{Rst}")
        return

    print(f'\n {Wh}{"="*10} {Gr}YOUR PUBLIC IP ADDRESS {Wh}{"="*10}')
    print(f"\n {Wh}[ {Gr}+ {Wh}] Your IP Address : {Cy}{my_ip}{Rst}")
    print(f" {Wh}[ {Gr}+ {Wh}] Check details   : {Cy}https://ipwho.is/{my_ip}{Rst}")
    print(f'\n {Wh}{"="*44}{Rst}')


# ─── MENU ─────────────────────────────────────────────────────────────────────

options = [
    {"num": 1, "text": "IP Tracker",           "func": IP_Track},
    {"num": 2, "text": "Show Your IP",          "func": showIP},
    {"num": 3, "text": "Phone Number Tracker",  "func": phoneGW},
    {"num": 4, "text": "Username Tracker",      "func": TrackLu},
    {"num": 0, "text": "Exit",                  "func": None},
]


def option_text():
    lines = ""
    for opt in options:
        color = Re if opt["num"] == 0 else Gr
        lines += f'  {Wh}[ {color}{opt["num"]}{Wh} ]  {color}{opt["text"]}{Rst}\n'
    return lines


def is_in_options(num):
    return any(opt["num"] == num for opt in options)


def call_option(opt_num):
    for option in options:
        if option["num"] == opt_num:
            if option["func"] is None:
                print(f"\n{Wh}[ {Gr}+ {Wh}] {Gr}Goodbye!{Rst}")
                time.sleep(1)
                sys.exit(0)
            option["func"]()
            return
    raise ValueError("Option not found")


def execute_option(opt_num):
    if not is_in_options(opt_num):
        print(f"{Re} [!] Invalid option. Please choose from the menu.{Rst}")
        time.sleep(1.5)
        return
    try:
        call_option(opt_num)
        input(f'\n{Wh}  [ {Gr}+ {Wh}] {Gr}Press ENTER to return to menu...{Rst}')
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Interrupted. Returning to menu...{Rst}')
        time.sleep(1)


def main():
    if not check_internet():
        sys.exit(1)

    while True:
        clear()
        banner()
        print(option_text())
        try:
            choice = input(f"{Wh}  [ + ] {Gr}Select Option : {Wh}").strip()
            if not choice.isdigit():
                print(f'{Re}  [!] Please enter a valid number.{Rst}')
                time.sleep(1.5)
                continue
            execute_option(int(choice))
        except KeyboardInterrupt:
            print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exiting...{Rst}')
            time.sleep(1)
            sys.exit(0)


if __name__ == '__main__':
    main()
