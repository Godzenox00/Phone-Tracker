#!/usr/bin/python
# << CODE BY HUNX04
# << MAU RECODE ??? IZIN DULU LAH,  MINIMAL TAG AKUN GITHUB MIMIN YANG MENGARAH KE AKUN INI, LEBIH GAMPANG SI PAKE FORK
# << KALAU DI ATAS TIDAK DI IKUTI MAKA AKAN MENDAPATKAN DOSA KARENA MIMIN GAK IKHLAS
# “Wahai orang-orang yang beriman! Janganlah kamu saling memakan harta sesamamu dengan jalan yang batil,” (QS. An Nisaa': 29). Rasulullah SAW juga melarang umatnya untuk mengambil hak orang lain tanpa izin.

# IMPORT MODULE

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
from concurrent.futures import ThreadPoolExecutor, as_completed

Bl = '\033[30m'  # VARIABLE BUAT WARNA CUYY
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'


# HTTP Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

REQUEST_TIMEOUT = 10  # seconds
MAX_WORKERS = 20      # concurrent threads


# utilities

# decorator for attaching run_banner to a function
def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)


    return wrapper


# FUNCTIONS FOR MENU
@is_option
def IP_Track():
    ip = input(f"{Wh}\n Enter IP target : {Gr}")  # INPUT IP ADDRESS
    print()
    print(f' {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============')
    req_api = requests.get(f"http://ipwho.is/{ip}", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    ip_data = json.loads(req_api.text)
    if not ip_data.get('success', True):
        print(f"\n {Re}Error: {ip_data.get('message', 'Invalid IP address')}")
        return
    time.sleep(2)
    print(f"{Wh}\n IP target       :{Gr}", ip)
    print(f"{Wh} Type IP         :{Gr}", ip_data["type"])
    print(f"{Wh} Country         :{Gr}", ip_data["country"])
    print(f"{Wh} Country Code    :{Gr}", ip_data["country_code"])
    print(f"{Wh} City            :{Gr}", ip_data["city"])
    print(f"{Wh} Continent       :{Gr}", ip_data["continent"])
    print(f"{Wh} Continent Code  :{Gr}", ip_data["continent_code"])
    print(f"{Wh} Region          :{Gr}", ip_data["region"])
    print(f"{Wh} Region Code     :{Gr}", ip_data["region_code"])
    print(f"{Wh} Latitude        :{Gr}", ip_data["latitude"])
    print(f"{Wh} Longitude       :{Gr}", ip_data["longitude"])
    lat = ip_data['latitude']
    lon = ip_data['longitude']
    print(f"{Wh} Maps            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
    print(f"{Wh} EU              :{Gr}", ip_data["is_eu"])
    print(f"{Wh} Postal          :{Gr}", ip_data["postal"])
    print(f"{Wh} Calling Code    :{Gr}", ip_data["calling_code"])
    print(f"{Wh} Capital         :{Gr}", ip_data["capital"])
    print(f"{Wh} Borders         :{Gr}", ip_data["borders"])
    print(f"{Wh} Country Flag    :{Gr}", ip_data["flag"]["emoji"])
    print(f"{Wh} ASN             :{Gr}", ip_data["connection"]["asn"])
    print(f"{Wh} ORG             :{Gr}", ip_data["connection"]["org"])
    print(f"{Wh} ISP             :{Gr}", ip_data["connection"]["isp"])
    print(f"{Wh} Domain          :{Gr}", ip_data["connection"]["domain"])
    print(f"{Wh} ID              :{Gr}", ip_data["timezone"]["id"])
    print(f"{Wh} ABBR            :{Gr}", ip_data["timezone"]["abbr"])
    print(f"{Wh} DST             :{Gr}", ip_data["timezone"]["is_dst"])
    print(f"{Wh} Offset          :{Gr}", ip_data["timezone"]["offset"])
    print(f"{Wh} UTC             :{Gr}", ip_data["timezone"]["utc"])
    print(f"{Wh} Current Time    :{Gr}", ip_data["timezone"]["current_time"])


@is_option
def phoneGW():
    User_phone = input(
        f"\n {Wh}Enter phone number target {Gr}Ex [+6281xxxxxxxxx] {Wh}: {Gr}")  # INPUT NUMBER PHONE
    default_region = "ID"  # DEFAULT NEGARA INDONESIA

    parsed_number = phonenumbers.parse(User_phone, default_region)  # VARIABLE PHONENUMBERS
    region_code = phonenumbers.region_code_for_number(parsed_number)
    jenis_provider = carrier.name_for_number(parsed_number, "en")
    location = geocoder.description_for_number(parsed_number, "id")
    is_valid_number = phonenumbers.is_valid_number(parsed_number)
    is_possible_number = phonenumbers.is_possible_number(parsed_number)
    formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formatted_number_for_mobile = phonenumbers.format_number_for_mobile_dialing(parsed_number, default_region,
                                                                                with_formatting=True)
    number_type = phonenumbers.number_type(parsed_number)
    timezone1 = timezone.time_zones_for_number(parsed_number)
    timezoneF = ', '.join(timezone1)

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION PHONE NUMBERS {Wh}==========")
    print(f"\n {Wh}Location             :{Gr} {location}")
    print(f" {Wh}Region Code          :{Gr} {region_code}")
    print(f" {Wh}Timezone             :{Gr} {timezoneF}")
    print(f" {Wh}Operator             :{Gr} {jenis_provider}")
    print(f" {Wh}Valid number         :{Gr} {is_valid_number}")
    print(f" {Wh}Possible number      :{Gr} {is_possible_number}")
    print(f" {Wh}International format :{Gr} {formatted_number}")
    print(f" {Wh}Mobile format        :{Gr} {formatted_number_for_mobile}")
    print(f" {Wh}Original number      :{Gr} {parsed_number.national_number}")
    print(
        f" {Wh}E.164 format         :{Gr} {phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)}")
    print(f" {Wh}Country code         :{Gr} {parsed_number.country_code}")
    print(f" {Wh}Local number         :{Gr} {parsed_number.national_number}")
    if number_type == phonenumbers.PhoneNumberType.MOBILE:
        print(f" {Wh}Type                 :{Gr} This is a mobile number")
    elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
        print(f" {Wh}Type                 :{Gr} This is a fixed-line number")
    else:
        print(f" {Wh}Type                 :{Gr} This is another type of number")


# Social media sites list — each entry can have:
#   url        : profile URL template (use {} for username)
#   name       : display name
#   err_code   : HTTP code that means "not found" (default 404)
#   err_text   : if the site returns 200 for missing users, a string to look for in the body
SOCIAL_MEDIA = [
    # --- Major platforms ---
    {"url": "https://www.facebook.com/{}",              "name": "Facebook"},
    {"url": "https://www.instagram.com/{}",             "name": "Instagram"},
    {"url": "https://x.com/{}",                         "name": "X (Twitter)"},
    {"url": "https://www.tiktok.com/@{}",               "name": "TikTok"},
    {"url": "https://www.youtube.com/@{}",              "name": "YouTube"},
    {"url": "https://www.linkedin.com/in/{}",           "name": "LinkedIn"},
    {"url": "https://www.snapchat.com/add/{}",          "name": "Snapchat"},
    {"url": "https://www.threads.net/@{}",              "name": "Threads"},

    # --- Dating (popular in Brazil) ---
    {"url": "https://tinder.com/@{}",                   "name": "Tinder"},
    {"url": "https://badoo.com/profile/{}",             "name": "Badoo"},
    {"url": "https://www.happn.com/app/user/{}",        "name": "Happn"},
    {"url": "https://bumble.com/profile/{}",            "name": "Bumble"},
    {"url": "https://hinge.co/profile/{}",              "name": "Hinge"},
    {"url": "https://www.okcupid.com/profile/{}",       "name": "OkCupid"},
    {"url": "https://www.pof.com/viewprofile.aspx?profile_id={}", "name": "Plenty of Fish"},
    {"url": "https://www.parperfeito.com.br/profile/{}", "name": "Par Perfeito"},
    {"url": "https://www.inner.circle/profile/{}",      "name": "Inner Circle"},
    {"url": "https://grindr.com/profile/{}",            "name": "Grindr"},
    {"url": "https://hornet.com/@{}",                   "name": "Hornet"},

    # --- Dev / Tech ---
    {"url": "https://github.com/{}",                    "name": "GitHub"},
    {"url": "https://gitlab.com/{}",                    "name": "GitLab"},
    {"url": "https://bitbucket.org/{}",                 "name": "Bitbucket"},
    {"url": "https://codepen.io/{}",                    "name": "CodePen"},
    {"url": "https://replit.com/@{}",                   "name": "Replit"},
    {"url": "https://stackoverflow.com/users/?tab=Accounts&SearchText={}", "name": "StackOverflow", "err_text": "page not found"},
    {"url": "https://dev.to/{}",                        "name": "DEV.to"},
    {"url": "https://hackernoon.com/@{}",               "name": "HackerNoon"},

    # --- Creative ---
    {"url": "https://www.behance.net/{}",               "name": "Behance"},
    {"url": "https://dribbble.com/{}",                  "name": "Dribbble"},
    {"url": "https://www.deviantart.com/{}",            "name": "DeviantArt"},
    {"url": "https://www.flickr.com/people/{}",         "name": "Flickr"},
    {"url": "https://unsplash.com/@{}",                 "name": "Unsplash"},
    {"url": "https://500px.com/p/{}",                   "name": "500px"},

    # --- Music / Video ---
    {"url": "https://soundcloud.com/{}",                "name": "SoundCloud"},
    {"url": "https://open.spotify.com/user/{}",         "name": "Spotify"},
    {"url": "https://www.twitch.tv/{}",                 "name": "Twitch"},
    {"url": "https://vimeo.com/{}",                     "name": "Vimeo"},
    {"url": "https://www.dailymotion.com/{}",           "name": "Dailymotion"},

    # --- Blogging / Writing ---
    {"url": "https://medium.com/@{}",                   "name": "Medium"},
    {"url": "https://www.tumblr.com/{}",                "name": "Tumblr"},
    {"url": "https://substack.com/@{}",                 "name": "Substack"},
    {"url": "https://{}.wordpress.com",                 "name": "WordPress"},
    {"url": "https://{}.blogspot.com",                  "name": "Blogger"},

    # --- Social / Community ---
    {"url": "https://www.reddit.com/user/{}",           "name": "Reddit"},
    {"url": "https://www.quora.com/profile/{}",         "name": "Quora"},
    {"url": "https://www.pinterest.com/{}",             "name": "Pinterest"},
    {"url": "https://mastodon.social/@{}",              "name": "Mastodon"},
    {"url": "https://t.me/{}",                          "name": "Telegram"},
    {"url": "https://www.weheartit.com/{}",             "name": "We Heart It"},
    {"url": "https://ello.co/{}",                       "name": "Ello"},
    {"url": "https://www.producthunt.com/@{}",          "name": "Product Hunt"},
    {"url": "https://about.me/{}",                      "name": "About.me"},
    {"url": "https://gravatar.com/{}",                  "name": "Gravatar"},
    {"url": "https://keybase.io/{}",                    "name": "Keybase"},
    {"url": "https://hub.docker.com/u/{}",              "name": "Docker Hub"},

    # --- Gaming ---
    {"url": "https://steamcommunity.com/id/{}",         "name": "Steam"},
    {"url": "https://www.roblox.com/user.aspx?username={}", "name": "Roblox", "err_text": "Page cannot be found"},
    {"url": "https://namemc.com/profile/{}",            "name": "NameMC (Minecraft)"},
    {"url": "https://osu.ppy.sh/users/{}",              "name": "osu!"},

    # --- Finance ---
    {"url": "https://cash.app/${}",                     "name": "Cash App"},
    {"url": "https://www.patreon.com/{}",               "name": "Patreon"},

    # --- Misc ---
    {"url": "https://www.thingiverse.com/{}",           "name": "Thingiverse"},
    {"url": "https://www.instructables.com/member/{}",   "name": "Instructables"},
    {"url": "https://tryhackme.com/p/{}",               "name": "TryHackMe"},
    {"url": "https://www.fiverr.com/{}",                "name": "Fiverr"},
    {"url": "https://linktr.ee/{}",                     "name": "Linktree"},
]


def _check_site(site, username, session):
    """Check a single site for a username. Returns (name, url|None)."""
    url = site['url'].format(username)
    try:
        resp = session.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)

        # Some sites return 200 even for missing users; check body text
        if 'err_text' in site:
            if resp.status_code == 200 and site['err_text'].lower() not in resp.text.lower():
                return (site['name'], url)
            return (site['name'], None)

        # Default: treat 200 as found
        if resp.status_code == 200:
            return (site['name'], url)

        return (site['name'], None)
    except requests.exceptions.RequestException:
        return (site['name'], None)


@is_option
def TrackLu():
    try:
        username = input(f"\n {Wh}Enter Username : {Gr}").strip()
        if not username:
            print(f"\n {Re}Username cannot be empty!")
            return

        print(f"\n {Wh}[{Gr} * {Wh}] Searching {Gr}{len(SOCIAL_MEDIA)}{Wh} sites for \"{Gr}{username}{Wh}\" ...\n")

        found = []
        not_found = []

        session = requests.Session()
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {
                pool.submit(_check_site, site, username, session): site
                for site in SOCIAL_MEDIA
            }
            for future in as_completed(futures):
                name, url = future.result()
                if url:
                    found.append((name, url))
                    print(f" {Wh}[ {Gr}+ {Wh}] {name}: {Gr}{url}")
                else:
                    not_found.append(name)
                    print(f" {Wh}[ {Ye}- {Wh}] {name}: {Ye}Not Found")

        print(f"\n {Wh}========== {Gr}SEARCH COMPLETE {Wh}==========")
        print(f" {Wh}[{Gr} + {Wh}] Found    : {Gr}{len(found)}{Wh} sites")
        print(f" {Wh}[{Ye} - {Wh}] Not Found: {Ye}{len(not_found)}{Wh} sites")

    except Exception as e:
        print(f"\n{Re}Error : {e}")


@is_option
def showIP():
    respone = requests.get('https://api.ipify.org/', headers=HEADERS, timeout=REQUEST_TIMEOUT)
    Show_IP = respone.text

    print(f"\n {Wh}========== {Gr}SHOW INFORMATION YOUR IP {Wh}==========")
    print(f"\n {Wh}[{Gr} + {Wh}] Your IP Adrress : {Gr}{Show_IP}")
    print(f"\n {Wh}==============================================")


# OPTIONS
options = [
    {
        'num': 1,
        'text': 'IP Tracker',
        'func': IP_Track
    },
    {
        'num': 2,
        'text': 'Show Your IP',
        'func': showIP

    },
    {
        'num': 3,
        'text': 'Phone Number Tracker',
        'func': phoneGW
    },
    {
        'num': 4,
        'text': 'Username Tracker',
        'func': TrackLu
    },
    {
        'num': 0,
        'text': 'Exit',
        'func': exit
    }
]


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')


def call_option(opt):
    if not is_in_options(opt):
        raise ValueError('Option not found')
    for option in options:
        if option['num'] == opt:
            if 'func' in option:
                option['func']()
            else:
                print('No function detected')


def execute_option(opt):
    try:
        call_option(opt)
        input(f'\n{Wh}[ {Gr}+ {Wh}] {Gr}Press enter to continue')
        main()
    except ValueError as e:
        print(e)
        time.sleep(2)
        execute_option(opt)
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()


def option_text():
    text = ''
    for opt in options:
        text += f'{Wh}[ {opt["num"]} ] {Gr}{opt["text"]}\n'
    return text


def is_in_options(num):
    for opt in options:
        if opt['num'] == num:
            return True
    return False


def option():
    # BANNER TOOLS
    clear()
    banner_art = r"""
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \____/_/ /_/\____/____/\__/     /_/ /_/   \__,_/\___/_/|_| 
"""
    stderr.writelines(f"""{banner_art}
              {Wh}[ + ]  C O D E   B Y  H U N X  [ + ]
    """)

    stderr.writelines(f"\n\n\n{option_text()}")


def run_banner():
    clear()
    time.sleep(1)
    stderr.writelines(f"""{Wh}
         .-.
       .'   `.          {Wh}--------------------------------
       :g g   :         {Wh}| {Gr}GHOST - TRACKER - IP ADDRESS {Wh}|
       : o    `.        {Wh}|       {Gr}@CODE BY HUNXBYTS      {Wh}|
      :         ``.     {Wh}--------------------------------
     :             `.
    :  :         .   `.
    :   :          ` . `.
     `.. :            `. ``;
        `:;             `:'
           :              `.
            `.              `.     .
              `'`'`'`---..,___`;.-'
        """)
    time.sleep(0.5)


def main():
    clear()
    option()
    time.sleep(1)
    try:
        opt = int(input(f"{Wh}\n [ + ] {Gr}Select Option : {Wh}"))
        execute_option(opt)
    except ValueError:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Please input number')
        time.sleep(2)
        main()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Wh}[ {Re}! {Wh}] {Re}Exit')
        time.sleep(2)
        exit()
