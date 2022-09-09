from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

# db 초기 설정
client = MongoClient('mongodb+srv://test:sparta@cluster0.nbw8ry5.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# 크롤링 초기 설정
url = "https://perfumegraphy.com/category/best-50/512/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
soup1 = soup.find_all('div', class_="thumbnail")
soup2 = soup.find_all('div', class_="description")

# 변수 초기화
id = [];
img = [];
name = [];
brand = [];
desc = [];
price = [];

# 변수 채우기
for i in soup1:
    soup1_1 = i.find_all('img')
    print(soup1_1)
    for j in range(len(soup1_1)):
        if j/2 != 0:
            img.append(soup1_1[j]['src'])

for i in soup2:
    soup10 = i.find_all('li', class_='price ')

for i in soup2:
    soup2_1 = i.find_all('strong')
    soup2_2 = i.find_all('li', class_='summary')
    soup2_3 = i.find_all('li', class_='price ')
    for j in soup2_1:
        name.append(j.find_all('a')[0].string)
    for j in soup2_2:
        desc.append(j.string)
    for j in soup2_3:
        price.append(j.get_text())

for i in range(len(name)):
    split1 = name[i].split()
    split2 = split1[0]
    brand.append(split2)
    id.append(i)

# 향수 db 저장
for i in range(len(name)):
    doc = {
        'id': id[i],
        'img': img[i],
        'name': name[i],
        'desc': desc[i],
        'brand': brand[i],
        'like': False
    }
    db.perfumes.insert_one(doc)