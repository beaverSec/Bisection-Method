import requests

# Menggunakan Session agar cookie dikelola otomatis oleh library
session = requests.Session()

def loginUserInput():
    # Gunakan kredensial yang kamu berikan tadi secara langsung jika malas mengetik
    username = "beav3r"
    password = "5#8!*Mke-NA/Cpy"
    
    headers = {
        "Referer": "https://www.hackthissite.org/",
        "User-Agent": "Mozilla/5.0" # Tambahkan User-Agent agar tidak dikira bot sederhana
    }
    
    # HTS terkadang butuh btn_login atau btn_submit
    payload = {"username": username, "password": password, "btn_login": "Log in"}
    
    response = session.post("https://www.hackthissite.org/user/login", data=payload, headers=headers)
    
    # Cek apakah cookie 'phpbb3_..._u' atau session HTS sudah ada
    if "logged in" in response.text.lower() or session.cookies.get("autologin"):
        print("authenticated")
        return response
    else:
        print("Login Gagal! Cek kembali username/password.")
        return None

def getPage(url):
    headers = {"Referer": "https://www.hackthissite.org/"}
    return session.get(url, headers=headers)

def postPage(url, payload):
    headers = {"Referer": "https://www.hackthissite.org/"}
    return session.post(url, headers=headers, data=payload)