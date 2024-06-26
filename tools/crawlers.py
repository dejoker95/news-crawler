import requests
import pytz
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class KeywordCrawler:
    def __init__(self):
        pass

    def get_google_trends(hl, tz, pn):
        pytrends = TrendReq(hl=hl, tz=tz)
        trends_df = pytrends.trending_searches(pn=pn)
        return trends_df[0].to_list()

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


class WebCrawler:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def crawl_naver_news(self, url, timeout):
        self.driver.get(url)
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "_article_content")))
        title = self.driver.find_element(By.XPATH, "/html/head/title").get_attribute("innerText")
        description = "\n".join([element.get_attribute("innerText") for element in self.driver.find_elements(By.CLASS_NAME, "_article_content")])
        return title, description
