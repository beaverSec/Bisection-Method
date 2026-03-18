import requests

# Menggunakan Session agar cookie dikelola secara persisten
session = requests.Session()

def loginUserInput():
    # Masukkan kredensial HTS kamu
    username = input("username: ") # raw_input diganti input agar tidak oren
    password = input("password: ") 

    # Header browser standar agar tidak diblokir
    headers = {
        "Referer": "https://www.hackthissite.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    # HTS butuh parameter tombol (btn_login)
    payload = {
        "username": username, 
        "password": password, 
        "btn_login": "Log in"
    }

    response = session.post("https://www.hackthissite.org/user/login", data=payload, headers=headers)
    
    if response.status_code == 200 and ("logout" in response.text.lower() or "logged in" in response.text.lower()):
        print("authenticated")
        return response
    else:
        print("not authenticated - cek username/password kamu")
        return None

def getPage(url):
    # Mengambil halaman menggunakan session yang sudah login
    headers = {"Referer": "https://www.hackthissite.org/"}
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response
    print(f"Error getPage: {response.status_code}")
    return None

def postPage(url, payload):
    # Mengirim data menggunakan session yang sudah login
    headers = {"Referer": "https://www.hackthissite.org/"}
    response = session.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response
    print(f"Error postPage: {response.status_code}")
    return None