import requests

# Menggunakan Session agar login tetap awet
session = requests.Session()

def loginUserInput():
    # Masukkan kredensial kamu di sini
    username = "beav3r"
    password = "5#8!*Mke-NA/Cpy"
    
    headers = {
        "Referer": "https://www.hackthissite.org/",
        "User-Agent": "Mozilla/5.0"
    }
    
    # HTS butuh parameter btn_login agar dianggap login valid
    payload = {
        "username": username, 
        "password": password, 
        "btn_login": "Log in"
    }
    
    print(f"[+] Login sebagai {username}...")
    response = session.post("https://www.hackthissite.org/user/login", data=payload, headers=headers)
    
    if "logged in" in response.text.lower() or "logout" in response.text.lower():
        print("authenticated")
        return response
    else:
        print("Gagal Login!")
        return None

def getPage(url):
    headers = {"Referer": "https://www.hackthissite.org/"}
    return session.get(url, headers=headers)

def postPage(url, payload):
    headers = {"Referer": "https://www.hackthissite.org/"}
    return session.post(url, data=payload, headers=headers)