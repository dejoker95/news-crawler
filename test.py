import os
import json
import pprint
import requests
from dotenv import load_dotenv


# Import Env
load_dotenv()
CLIENT_ID = os.getenv('N_CLIENT_ID')
CLIENT_SECRET = os.getenv('N_CLIENT_SECRET')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PWD = os.getenv('MYSQL_PWD')


# Search keyword
keyword = '해외축구'

url = "https://openapi.naver.com/v1/search/news.json"
headers = {'X-Naver-Client-Id': CLIENT_ID, 'X-Naver-Client-Secret': CLIENT_SECRET}
params = {
    'query': keyword,
    'display': 10,
    'start': 11,
    'sort': 'date'
    }

response = requests.get(url=url, headers=headers, params=params)

result = response.json()

pp = pprint.PrettyPrinter()
pp.pprint(result)
