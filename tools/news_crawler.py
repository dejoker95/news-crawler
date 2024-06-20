
# request에 에러처리 넣기 

import requests
from datetime import datetime

class NaverCrawler:

    def __init__(self, client_id, client_secret, endpoint):
        self.client_id = client_id
        self.client_secret = client_secret
        self.endpoint = endpoint
        self.headers = {'X-Naver-Client-Id': self.client_id, 'X-Naver-Client-Secret': self.client_secret}
        
    def get_articles(self, keyword, cnt, sort_option):
        params = {
            'query': keyword,
            'display': cnt,
            'start': 1,
            'sort': sort_option
        }
        response = requests.get(url=self.endpoint, headers=self.headers, params=params)
        return response.json()['items']

    def get_articles_since_date(self, keyword, date):
        articles = []
        it = 0
        done = False
        while not done:
            params = {
                'query': keyword,
                'display': 100,
                'start': (it * 100) + 1,
                'sort': 'date'
            }
            response = requests.get(url=self.endpoint, headers=self.headers, params=params)
            if response.status_code == 200:
                for article in response.json()['items']:
                    pubdate = self.pubdate_to_datetime(article['pubDate'])
                    if pubdate < date:
                        done = True
                        break
                    articles.append(article)
                it += 1
            else:
                break
        return self.transform_articles(articles)
    
    def transform_articles(self, articles):
        articles = self.add_article_id(articles)
        articles = self.filter_naver_domain(articles)
        return articles

    def add_article_id(self, articles):
        for keyword, items in articles.items():
            for item in items:
                id = ''.join(item['link'].split('/')[-2:])
                if '?' in id:
                    id = id.split('?')[0]
                item['id'] = id
        return articles

    def filter_naver_domain(self, articles):
        condition = lambda x: x['originallink'] != x['link']
        for keyword, val in articles.items():
            articles[keyword] = [x for x in val['items'] if condition(x)]
        return articles

    def pubdate_to_datetime(self, pubdate):
        return datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')
    
        