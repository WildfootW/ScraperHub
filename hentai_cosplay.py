import requests
from bs4 import BeautifulSoup
import re
import os

while 1:
    web_url = input('Keyin the web url(*.com/image/*/attachment/1/) : ')
    r = requests.get(web_url)
    soup = BeautifulSoup(r.text, "html.parser")

    directory_name = soup.html.head.title
    directory_name = str(directory_name)
    directory_name = directory_name[7:len(directory_name) - 32]
    directory_name = 'horo/hentai-cosplay/' + directory_name
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    directory_name = directory_name + "/"

    total_page = int(re.findall("\d*", re.findall("\/\d*\"", r.text.split('\n')[6])[0])[1])

    img_url = re.findall("\/upload\/\d*\/\d*\/\d*\/\d*....", str(soup.html.body.find(id="display_image_detail")))[0]
    img_url_1 = img_url[0:len(img_url) - 5]
    img_url_2 = img_url[len(img_url) - 4:len(img_url)]

    for i in range(104, total_page + 1):
        image_url = "http://static.hentai-cosplay.com" + img_url_1 + str(i) + img_url_2
        print(image_url)
        s = requests.get(image_url, stream = True)
        with open( directory_name + 'img' + str(i).zfill(4) + '.' + img_url_2, 'wb' ) as out_file:
            out_file.write(s.raw.data)

