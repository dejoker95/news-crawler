import os
import requests
import pytz
from datetime import datetime, timedelta
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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

    def __init__(self, ):
        self.client_id = os.getenv('NAVER_CLIENT_ID')
        self.client_secret = os.getenv('NAVER_CLIENT_SECRET')
        self.endpoint = os.getenv('NAVER_API_ENDPOINT')
        self.headers = {'X-Naver-Client-Id': self.client_id, 'X-Naver-Client-Secret': self.client_secret}

    def get_articles(self, keyword, days):
        articles = []
        it = 0
        done = False

        while not done:
            params = {
                'query': keyword,
                'display': 100,
                'start': (it * 100) + 1,
                'sort': 'sim'
            }
            response = requests.get(url=self.endpoint, headers=self.headers, params=params)
            if response.status_code == 200:
                for article in response.json()['items']:
                    articles.append(article)
                it += 1
            else:
                break
        return self.transform_articles(articles, days)

    # transform articles for Elasticsearch insert operation
    def transform_articles(self, articles, days):
        articles = self.filter_naver_domain(articles)
        articles = self.filter_days(articles, days)
        for article in articles:
            article['id'] = self.add_article_id(article['link'])
        return articles

    def filter_naver_domain(self, articles):
        condition = lambda x: x['originallink'] != x['link']
        return [x for x in articles if condition(x)]
    
    def filter_days(self, articles, days):
        past_date = self.get_past_date(days)
        for article in articles:
            article['pubDate'] = self.pubdate_to_datetime(article['pubDate'])
        return [x for x in articles if past_date < x['pubDate']]
            

    def add_article_id(self, link):
        id = ''.join(link.split('/')[-2:])
        if '?' in id:
            id = id.split('?')[0]
        return id

    def pubdate_to_datetime(self, pubdate):
        return datetime.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %z')

    def get_past_date(self, days):
        today = datetime.today().replace(tzinfo=pytz.timezone('Asia/Seoul'))
        return today - timedelta(days=days)

class WebCrawler:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        service = Service("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(options=options, service=service)
        self.timeout = int(os.getenv('SELENIUM_TIMEOUT_SECONDS'))

    def crawl_naver_news(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, "_article_content")))
        title = self.driver.find_element(By.XPATH, "/html/head/title").get_attribute("innerText")
        description = "\n".join([element.get_attribute("innerText") for element in self.driver.find_elements(By.CLASS_NAME, "_article_content")])
        return title, description
