import pytz
import requests
from datetime import date, datetime, timedelta

class NaverApiCrawler:

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

    def get_articles_since_date(self, keyword, days):
        articles = []
        it = 0
        done = False
        since = self.get_date_week_ago(days)

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
                    if pubdate < since:
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
        articles = self.add_has_content_flag(articles)
        return articles

    # add ID in MongoDB format
    def add_article_id(self, articles):
        for article in articles:
            id = ''.join(article['link'].split('/')[-2:])
            if '?' in id:
                id = id.split('?')[0]
            article['_id'] = id
        return articles

    def filter_naver_domain(self, articles):
        condition = lambda x: x['originallink'] != x['link']
        return [x for x in articles if condition(x)]

    def pubdate_to_datetime(self, pubdate):
        return datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')

    def get_date_week_ago(self, days):
        today = datetime.today().replace(tzinfo=pytz.timezone('Asia/Seoul'))
        today.replace(hour=0, minute=0)
        week_ago = today - timedelta(days=days)
        return week_ago

    def add_has_content_flag(self, articles):
        for article in articles:
            article['has_content'] = False
        return articles

    
        