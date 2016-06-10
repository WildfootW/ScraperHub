import requests
from bs4 import BeautifulSoup
import re
import os
    
if not os.path.exists("horo/anime_reactor"):
    os.makedirs("horo/anime_reactor")

web_url = "http://anime.reactor.cc/tag/Spice%2Band%2BWolf/"
for i in range(1, 90):
    web_url_c = web_url + str(i)
    r = requests.get(web_url_c)
    soup = BeautifulSoup(r.text, "html.parser")
    web_html = str(soup)
    #img_list = re.findall("(http:\/\/img\d\.reactor\.cc\/pics\/post\/.{10,300}\.(jpeg|png|gif))",web_html)
    img_list = re.findall("(http:\/\/img\d\.reactor\.cc\/pics\/post\/[^\.]*\.(jpeg|png|gif|webm|mp4|bmp))",web_html)
    correct = re.findall("http:\/\/img\d\.reactor\.cc\/pics\/post\/",web_html)
    
    if not len(correct) == len(img_list):
        print("There is an error in page : " + str(i))
        pause = input("Please press Enter to continue")

    for j in range(0, len(img_list)):
        img_url = img_list[j][0]
        print(img_url)
        s = requests.get(img_url, stream = True)
        with open( "horo/anime_reactor/" + 'img' + str(i).zfill(2) + str(j).zfill(2) + "." + img_list[j][1], 'wb' ) as out_file:
            out_file.write(s.raw.data)
