# 멀티프로세싱 적용하기
import os
import time
import multiprocessing
from dotenv import load_dotenv
from tools.google_trends import get_trends
from tools.news_crawler import NaverApiCrawler
from tools.mongo_handler import MongoHandler
from tools.webcrawler import WebCrawler

# 환경변수 로드
load_dotenv()

NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')
NAVER_API_ENDPOINT = os.getenv('NAVER_API_ENDPOINT')
DAYS = os.get_env("DAYS")
MONGODB_HOST = os.getenv('MONGODB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE')
MONGODB_COLLECTION = os.getenv('MONGODB_COLLECTION')
SELENIUM_TIMEOUT_SECONDS = int(os.getenv('SELENIUM_TIMEOUT_SECONDS'))
ENABLE_MULTIPROCESSING = int(os.getenv("ENABLE_MULTIPROCESSING"))
N_PROCESS = int(os.getenv("N_PROCESS"))

def get_article_contents(docs):
    crawler = WebCrawler()
    client = MongoHandler(MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE, MONGODB_COLLECTION, dict)
    for doc in docs:
        doc['title'], doc['description'] = crawler.crawl_naver_news(doc['link'], SELENIUM_TIMEOUT_SECONDS)
        doc['has_content'] = True
        client.replace_one_by_id(doc)

if __name__ == "__main__":
    start_time = time.time()

    # 구글 트렌드 키워드 받아오기
    keywords = get_trends('ko', 540, 'south_korea')

    # Naver API Crawler 생성
    api_crawler = NaverApiCrawler(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, NAVER_API_ENDPOINT)

    # Naver Crawler로 과거 날짜까지 키워드별 기사 크롤링 (너무 과거의 기사는 배제하기 위함)
    # 일주일치만 받아오는걸로 설정
    
    article_dict = {}
    for keyword in keywords:
        article_dict[keyword] = api_crawler.get_articles_since_date(keyword, DAYS)

    for keyword, articles in article_dict.items():
        print('키워드: %s / count: %d' % (keyword, len(articles)))


    # MongoDB에 저장
    client = MongoHandler(MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE, MONGODB_COLLECTION, dict)
    client.create_index('has_content')

    for keyword, articles in article_dict.items():
        client.insert_docs(articles)

    # 기사 제목, 내용 크롤링 안된 문서 조회
    docs = list(client.find_no_content_docs())

    # Selenium으로 기사 제목, 내용 수집
    print('Use multiprocessing? %s ' % str(ENABLE_MULTIPROCESSING))
    if not ENABLE_MULTIPROCESSING:
        content_crawler = WebCrawler()
        for doc in docs:
            doc['title'], doc['description'] = content_crawler.crawl_naver_news(doc['link'], SELENIUM_TIMEOUT_SECONDS)
            doc['has_content'] = True
            client.replace_one_by_id(doc)
    else:
        processes = []
        split = len(docs) // N_PROCESS
        for i in range(N_PROCESS):
            sub_docs = docs[split * i:] if i == N_PROCESS else docs[split * i:split * (i + 1)]
            p = multiprocessing.Process(target=get_article_contents, args=(sub_docs,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

    duration_minutes = (time.time() - start_time) / 60
    print('Execution Time: %.2f minutes' % duration_minutes)

    