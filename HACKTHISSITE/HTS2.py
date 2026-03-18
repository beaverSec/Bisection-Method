from PIL import Image

# Dictionary to translate morse
CODE = {'.-':   'A',    '-...': 'B',    '-.-.': 'C',
		'-..':  'D',    '.':    'E',    '..-.': 'F',
		'--.':  'G',    '....': 'H',    '..':   'I',
		'.---': 'J',    '-.-':  'K',    '.-..': 'L',
		'--':   'M',    '-.':   'N',    '---':  'O',
		'.--.': 'P',    '--.-': 'Q',    '.-.':  'R',
		'...':  'S',    '-':    'T',    '..-':  'U',
		'...-': 'V',    '.--':  'W',    '-..-': 'X',
		'-.--': 'Y',    '--..': 'Z',

		'-----':'0',    '.----': '1',   '..---': '2',
		'...--':'3',    '....-': '4',   '.....': '5',
		'-....':'6',    '--...': '7',   '---..': '8',
		'----.':'9'}

# Put here the image
with Image.open("download (3).png") as im:
	pixel = im.load()

last = 0
pos = -1
morse = []

for i in range(30):
	for j in range(100):
		pos += 1
		if pixel[j, i] == 1:
			morse.append(chr(pos - last))
			last = pos

morse = "".join([x for x in morse]).split()
morse = "".join([CODE[x] for x in morse])
print(morse)