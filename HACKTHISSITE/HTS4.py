import HackThisSiteInterface as HTS 
import xmltodict
import bz2
from PIL import Image, ImageDraw

def sendResponse(solution):
    print("sending solution")
    # Di Python 3, pastikan key payload sesuai dengan yang diminta server HTS
    payload = {'solution' : solution, 'submitbutton' : 'submit'}
    return HTS.postPage("https://www.hackthissite.org/missions/prog/4/index.php", payload)

def parseXML(xmlContent):
    colors = {
        'yellow' : '#ffff00',
        'blue' : '#0000ff',
        'green' : '#00ff00',
        'red' : '#ff0000',
        'white' : '#ffffff'
    }

    # Parse XML menggunakan library xmltodict
    xmlDict = xmltodict.parse(xmlContent)
    width, height = 1000, 1000
    
    img = Image.new('RGB', (width, height), "black")
    draw = ImageDraw.Draw(img)

    # 1. Gambar Garis (Line)
    for item in xmlDict['ppcPlot']['Line']:
        color = colors[item['Color']] if "Color" in item else colors['white']
        draw.line((float(item['XStart']), height-float(item['YStart']),
                   float(item['XEnd']), height-float(item['YEnd'])), fill=color)
    
    # 2. Gambar Busur (Arc)
    for item in xmlDict['ppcPlot']['Arc']:
        color = colors[item['Color']] if "Color" in item else colors['white']
        r = float(item['Radius'])
        x, y = float(item['XCenter']), height-float(item['YCenter'])
        # Bounding box untuk Pillow: [x0, y0, x1, y1]
        bbox = [x-r, y-r, x+r, y+r]
        # Transformasi sudut untuk menyesuaikan koordinat kartesius
        start_angle = -1 * (int(item['ArcStart']) + int(item['ArcExtend']))
        end_angle = -1 * int(item['ArcStart'])
        draw.arc(bbox, start=start_angle, end=end_angle, fill=color)

    img.show() # Munculkan gambar untuk dibaca Caca
    solution = input("Masukkan urutan kata (blue,green,red,yellow,white): ")
    return sendResponse(solution)

def downloadXML():
    HTS.loginUserInput() # Meminta user/pass di terminal
    HTS.getPage("https://www.hackthissite.org/missions/prog/4/")
    response = HTS.getPage("https://www.hackthissite.org/missions/prog/4/XML")
    # Data dikompresi dengan bz2
    return bz2.decompress(response.content)

if __name__ == "__main__":
    print(parseXML(downloadXML()))