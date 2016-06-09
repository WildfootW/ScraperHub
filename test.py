import requests
from bs4 import BeautifulSoup
import re

r = requests.get("http://hentai-cosplay.com/image/rococo-whi
stle-around-the-world-1/attachment/1/") 
soup = BeautifulSoup(r.text, "html.parser")


#total_page
url_prefixs = r.text.split('\n')
url_prefixs_2 = url_prefixs[6]
url_prefixs_3 = re.findall("\/\d*\"", url_prefixs_2)[0]
url_prefixs_4 = re.findall("\d*", url_prefixs_3)[1]
url_prefixs_5 = int(url_prefixs_4)

url_prefixs_6 = int(re.findall("\d*", re.findall("\/\d*\"", r.text.split('\n')[6])[0])[1])

#img_url
body_prefixs_1 = soup.html.body.find(id="display_image_detail")  
str1 = str(body_prefixs_1)
body_prefixs_2 = re.findall("\/upload\/\d*\/\d*\/\d*\/\d*....", str1)
body_prefixs_3 = body_prefixs_2[0]

body_prefixs_4 = re.findall("\/upload\/\d*\/\d*\/\d*\/\d*....", str(soup.html.body.find(id="display_image_detail")))[0]

title_prefixs_1 = soup.html.head.title
title_prefixs_2 = str(title_prefixs_1)
title_prefixs_3 = title_prefixs_2[7:len(title_prefixs_2)-32]


