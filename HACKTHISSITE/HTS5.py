import HTSInterface as HTS 
import bz2
import binascii
import sys
import math
from PIL import Image

processedBranches = 0

def getCorruptedByteAddresses(content):
    # Mencari index semua pasangan 0d0a (korupsi FTP Windows)
    addresses = []
    address = content.find('0d0a', 0)
    while(address >= 0):
        addresses.append(address)
        address = content.find('0d0a', address + 4)
    print(f"Alamat korupsi ditemukan: {addresses}")
    return addresses

def groupAddressesRecursive(addresses, allGroups, groupAddress, currentIndex, groupSize, distanceThreshold):
    # Mencari kombinasi alamat untuk di-brute force
    if ((groupAddress is not None and len(groupAddress) >= groupSize) or 
        currentIndex >= len(addresses) or 
        len(addresses) - currentIndex + len(groupAddress) < groupSize):
        return groupAddress

    else:
        # Tanpa menambahkan alamat saat ini
        groupAddressesRecursive(addresses, allGroups, groupAddress, currentIndex + 1, groupSize, distanceThreshold)
        
        # Tambahkan alamat saat ini
        changedGroupAddress = groupAddress + [addresses[currentIndex]]
        
        if len(changedGroupAddress) >= 2:
            distance = abs(int(changedGroupAddress[-1]) - int(changedGroupAddress[-2]))
            if distance >= distanceThreshold:
                if len(changedGroupAddress) >= groupSize:
                    allGroups.append(changedGroupAddress)
                groupAddressesRecursive(addresses, allGroups, changedGroupAddress, currentIndex + 1, groupSize, distanceThreshold)
        else:
            groupAddressesRecursive(addresses, allGroups, changedGroupAddress, currentIndex + 1, groupSize, distanceThreshold)

        return allGroups

def recoverGrouped(addresses, data):
    # Mengubah 0d0a kembali menjadi 0a (menghapus 0d tambahan)
    newData = ""
    lastIndex = 0
    for index in range(0, len(addresses)):
        newData = newData + data[lastIndex:addresses[index]] + data[addresses[index]+2:addresses[index]+4]
        lastIndex = addresses[index] + 4

    newData = newData + data[lastIndex:]

    try:
        # Dekompresi BZ2 sekaligus mengecek CRC
        dec = bz2.decompress(binascii.unhexlify(newData))
        print('\n[+] File Berhasil Dipulihkan! Buka recovered.png\n')
        
        with open('recovered.png', 'wb') as pngRecFile:
            pngRecFile.write(dec)
            
        # Tampilkan gambar secara otomatis
        Image.open('recovered.png').show()
        
        solution = input("Masukkan password yang ada di gambar: ")
        print("Mengirim solusi...")
        payload = {'solution' : solution, 'submitbutton' : 'submit'}
        HTS.postPage("https://www.hackthissite.org/missions/prog/5/index.php", payload)
        sys.exit(0)

    # Perbaikan di sini: Tangkap Exception umum agar tidak crash saat brute-force gagal
    except Exception:
        return

def downloadFile():
    HTS.loginUserInput()
    HTS.getPage("https://www.hackthissite.org/missions/prog/5/")
    print("Mendownload file corrupted.png.bz2...")
    response = HTS.getPage("https://www.hackthissite.org/missions/prog/5/corrupted.png.bz2")
    return response

# Main Execution
if __name__ == "__main__":
    response = downloadFile()
    # Decode ke string agar fungsi .find() bekerja di Python 3
    hexData = binascii.hexlify(response.content).decode('utf-8')
    
    print("Mencari byte yang korup...")
    addresses = getCorruptedByteAddresses(hexData)
    
    print("Memulai pemulihan file (Brute-forcing)...")
    # Mencoba berbagai kombinasi ukuran grup
    for i in range(1, len(addresses)):
        print(f"\nMencoba grup ukuran: {len(addresses)-i}")
        grouped = groupAddressesRecursive(addresses, [], [], 0, len(addresses)-i, 0)
        
        if grouped:
            for itemIndex, item in enumerate(grouped):
                sys.stdout.write(f'\rProgress: {float(100*itemIndex/len(grouped)):.2f}%')
                sys.stdout.flush()
                recoverGrouped(item, hexData)