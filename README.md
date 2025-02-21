# GhostTrack - Version 2.2
# Author: 𝑫𝑨𝑹𝑲 𝑯𝑨𝑪𝑲𝑬𝑹
# Telegram: @FTX_l
# Useful tool to track location, phone numbers, and usernames.
# This tool is for OSINT (Open-Source Intelligence) and information gathering purposes only.

import requests

def track_ip(ip):
    """ وظيفة لجلب بيانات عن عنوان IP """
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url).json()
    
    if response["status"] == "fail":
        return "❌ فشل في جلب المعلومات، تأكد من صحة عنوان IP."
    
    info = f"""
    📍 IP: {response['query']}
    🌎 الدولة: {response['country']}
    🏙️ المدينة: {response['city']}
    📡 مزود الخدمة: {response['isp']}
    🌐 المنطقة الزمنية: {response['timezone']}
    """
    return info

def track_phone(number):
    """ وظيفة لجلب بيانات عن رقم الهاتف """
    url = f"https://api.apilayer.com/number_verification/validate?number={number}"
    headers = {"apikey": "YOUR_API_KEY"}  # استبدل "YOUR_API_KEY" بمفتاح API الخاص بك
    response = requests.get(url, headers=headers).json()

    if not response["valid"]:
        return "❌ فشل في جلب المعلومات، تأكد من صحة رقم الهاتف."
    
    info = f"""
    📞 الرقم: {response['international_format']}
    🌎 الدولة: {response['country_name']}
    📶 مزود الخدمة: {response['carrier']}
    """
    return info

if __name__ == "__main__":
    print("📌 مرحبًا بك في GhostTrack")
    print("1️⃣ تتبع عنوان IP")
    print("2️⃣ تتبع رقم هاتف")
    
    choice = input("🔹 اختر الخيار: ")
    
    if choice == "1":
        ip = input("🖥️ أدخل عنوان IP: ")
        print(track_ip(ip))
    
    elif choice == "2":
        phone = input("📱 أدخل رقم الهاتف (مع كود الدولة): ")
        print(track_phone(phone))
    
    else:
        print("❌ اختيار غير صالح!")
