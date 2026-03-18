from PIL import Image

# 1. Buka gambar
im = Image.open('12.bmp', 'r')
width, height = im.size
pix = im.load()

# 2. Gunakan list of integers untuk menampung data biner
binary_data = []

for i in range(height):
    for j in range(width):
        n = pix[j, i]
        # Logika stego: membalikkan nilai warna (255 - n)
        binary_data.append(255 - n)

# 3. Ubah list menjadi object bytes
text = bytes(binary_data)

# 4. Tulis ke file dengan mode 'wb' (Write Binary)
# Ini kunci agar tidak kena UnicodeEncodeError
with open('12.zip', 'wb') as f:
    f.write(text)

print("File 12.zip berhasil dibuat!")