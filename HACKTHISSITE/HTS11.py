import requests
import re
import sys

url_login = "https://www.hackthissite.org/user/login"
url_objective = "https://www.hackthissite.org/missions/prog/11/"

# ==============================
# GANTI DENGAN AKUN KAMU
# ==============================
payload_login = {
    "username": "beav3r",
    "password": "5#8!*Mke-NA/Cpy"
}

headers = {
    "Referer": "https://www.hackthissite.org/"
}

try:
    session = requests.Session()

    # Login
    login_response = session.post(url_login, data=payload_login, headers=headers)

    # Ambil halaman mission
    response = session.get(url_objective)

    # ==============================
    # Parsing Generated String
    # ==============================
    gen_match = re.search(r'Generated String:\s*(.*?)<br', response.text, re.DOTALL)
    shift_match = re.search(r'Shift:\s*(-?\d+)', response.text)

    if not gen_match or not shift_match:
        print("Parsing gagal. Cek login atau struktur halaman berubah.")
        session.close()
        sys.exit()

    generated_string = gen_match.group(1)
    shift = int(shift_match.group(1))

    # Ambil hanya angka dari generated string
    ascii_numbers = re.findall(r'\d+', generated_string)

    # Decode
    decoded = ""
    for num in ascii_numbers:
        value = int(num) - shift
        if 0 <= value <= 0x10FFFF:
            decoded += chr(value)
        else:
            print("Nilai ASCII tidak valid:", value)
            session.close()
            sys.exit()

    print("Shift:", shift)
    print("Generated:", generated_string)
    print("Decoded:", decoded)

    # ==============================
    # Submit jawaban
    # ==============================
    payload_solution = {"solution": decoded}
    submit_response = session.post(url_objective, data=payload_solution, headers=headers)

    print("Submit Status:", submit_response.status_code)
    print("Response Length:", len(submit_response.text))

    session.close()

except Exception as e:
    print("Error:", e)