from PIL import Image
from PIL import ImageOps
import requests
from bs4 import BeautifulSoup
import imagehash
from io import BytesIO
import json
import imghdr
##import keepalive

##keepalive.keep_alive()

limit = 42069 # hahhaha 420 sex number hhaha

data = requests.get("https://pokeapi.co/api/v2/pokemon/?limit=" + str(limit)).json()["results"] # pkapi
data = [x for x in data if not x['name'].endswith('-mega')] # remove mega variants

images = []

pokenames = []

def download(pId, pName):
	pName = pName.capitalize() # pokemon name
	pId = str(pId).rjust(3, "0") # pokemon id
	res = requests.get(f"https://bulbapedia.bulbagarden.net/wiki/File:{pId}{pName}.png")
	#resp = urllib.request.urlretrieve(f'https://bulbapedia.bulbagarden.net/wiki/File:{pId}{pName}.png', f"{pId}{pName}.png")
	#print (f'https://bulbapedia.bulbagarden.net/wiki/File:{pId}{pName}.png')
	if res.status_code == 200:
		soup = BeautifulSoup(res.content, features = "html.parser")
		img = soup.find('img', {'alt': f'File:{pId}{pName}.png'})
		if (img):
			image = requests.get('https:' + img['src'])
			print(f"https:{img['src']}")
			return BytesIO(image.content)

aisnone = 0

pokehashes = []

for c, i in enumerate(data):
	print("Downloading " + i["name"] + " " + str(c))
	a = download(c + 1, i["name"])

	if (a == None): # i dont undersantd lol
		print(f"A IS EQUAL TO NONE!!! PANICCCC OMG GUES THERE ARE {aisnone} NONES SO FAR!!!")
		aisnone += 1
		continue

	atype = imghdr.what(a)
	#print (atype)
	if not atype == 'png':
		print(f"A IS EQUAL TO NONE!!! PANICCCC OMG GUES THERE ARE {aisnone} NONES SO FAR!!!")
		aisnone += 1
		continue
	b = Image.open(a)
	#b = b.resize((453, 453))
	#b = ImageOps.expand(b, border=22, fill='transparent')
	print(b.size)
	imagebox = b.getbbox()
	b = b.crop(imagebox) # autocrop, removes transparent borders
	images.append(b)
	print(b.size)
	pokenames.append(i["name"])
	#print(a)
	pokehashes.append(str(imagehash.whash(b))) # hash the image
	print("Hashed!")
print("Done Downloading and hashing")

print(f"bruh dude {aisnone} pokemon failed to download dude wtf man")

#print("Starting hashing")


for i in pokehashes:
	#pokehashes.append(str(imagehash.whash(i)))
	print(pokehashes[i])

tooutput = dict(zip(pokehashes, pokenames))
jsonoutput = json.dumps(tooutput)
print(jsonoutput)
