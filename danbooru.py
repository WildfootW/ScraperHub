import requests
from bs4 import BeautifulSoup
import re

for j in range(1 , 90):
	image_url = "https://danbooru.donmai.us/posts?page=" + str(j) + "&tags=spice_and_wolf"
	web_url = "https://danbooru.donmai.us/"
	r = requests.get(image_url)
	soup = BeautifulSoup(r.text, "html.parser")
	image_string = soup.select("article")
	#image_string = [x["data-file-url"] for x in image_string]

	for i, v in enumerate(image_string, 1):
		url = v["data-file-url"]
		ext = v["data-file-ext"]
		print (web_url + url)
		r = requests.get(web_url + url, stream=True)
		with open('horo/danbooru/img' + str(j).zfill(2) + str(i).zfill(2) + '.' + ext, 'wb') as out_file:
			out_file.write(r.raw.data)

