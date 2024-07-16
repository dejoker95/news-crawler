import os
from enum import Enum
import requests
from dotenv import load_dotenv
import redis
import time
from tools.crawlers import NaverApiCrawler, WebCrawler
from elasticsearch import Elasticsearch, helpers

class TaskStatus(Enum):
    RUNNING = 'RUNNING'
    DONE = 'DONE'
    FAILED = 'FAILED'

def process_message(message, es_endpoint, es_user, es_password, task_endpoint):
    # Process the message
    print('======== TASK START ========')
    print(f'Received message: {message}')
    url = '/'.join([task_endpoint, message['id'], 'status'])
    update_task_status(url, {'status': TaskStatus.RUNNING.value})

    # Initialize Crawlers
    naver = NaverApiCrawler()
    web = WebCrawler()
    # Initialize ES client
    es = Elasticsearch(es_endpoint, basic_auth=(es_user, es_password))

    try:
    # Find articles with Naver API
        articles = naver.get_articles(message['keyword'], int(message['hours']))
        print('Found {} articles.'.format(len(articles)))

        # Collect Articles with Chromium
        i = 0
        for article in articles:
            try:
                print(article['link'])
                article['title'], article['description'] = web.crawl_naver_news(article['link'])
                i += 1
                print(i)
            except Exception as e:
                print(e)
        print('Finished Web crawling')

        articles = list(map(transform_article, articles))
        success, failed = helpers.bulk(es, articles)
        es.close()
    except Exception as e:
        print(e)
        update_task_status(url, TaskStatus.FAILED.value)
    print('Finished inserting to Elasticsearch')
    print('Success: {}, Failed: {}'.format(success, failed))
    body = {'status': TaskStatus.DONE.value,'success': success, 'failed': len(failed)}
    update_task_status(url, body)
    print('======== TASK FINISHED ========')

def transform_article(article):
    index_name = "".join([os.getenv('ARTICLE_INDEX_PREFIX'), article['pubDate'].strftime('%Y.%m.%d')])
    article_id = article["id"]
    del article['id']
    doc = {
        "_index": index_name,
        "_id": article_id,
        "_source": article
    }
    return doc

def update_task_status(url, body):
    response = requests.post(url=url, json=body)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")


def main():
    # Load environment variables
    load_dotenv()
    # Change redis host and consumer name if running in a docker container
    if os.path.exists('/.dockerenv'):
        REDIS_HOST = os.getenv("REDIS_CONTAINER_NAME")
        ELASTICSEARCH_ENDPOINT = os.getenv('ELASTICSEARCH_ENDPOINT')
        CONSUMER_NAME = os.getenv('HOSTNAME')
    else:
        REDIS_HOST = 'localhost'
        ELASTICSEARCH_ENDPOINT = 'localhost'
        CONSUMER_NAME = 'localhost'

    ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_ADMIN_USER')
    ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_ADMIN_PASSWORD')
    STREAM_KEY = os.getenv('REDIS_STREAM_KEY')
    CONSUMER_GROUP = os.getenv('REDIS_CONSUMER_GROUP')
    TASK_STATUS_UPDATE_ENDPOINT = os.getenv('TASK_STATUS_UPDATE_ENDPOINT')

    print('======== Consumer Configuration ========')
    print("REDIS HOST: {}".format(REDIS_HOST))
    print("ELASTICSEARCH ENDPOINT: {}".format(ELASTICSEARCH_ENDPOINT))
    print("STREAM KEY: {}".format(STREAM_KEY))
    print("CONSUMER GROUP: {}".format(CONSUMER_GROUP))
    print("CONSUMER NAME: {}".format(CONSUMER_NAME))
    
    # Connect to the Redis server
    r = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

    # Create a consumer group (if it doesn't already exist)
    try:
        r.xgroup_create(STREAM_KEY, CONSUMER_GROUP, id='0', mkstream=True)
    except redis.exceptions.ResponseError as e:
        # Ignore the error if the group already exists
        if "BUSYGROUP Consumer Group name already exists" not in str(e):
            raise

    print(f"Listening for messages in stream '{STREAM_KEY}' as consumer '{CONSUMER_NAME}'...")

    while True:
        # Read messages from the stream
        try:
            messages = r.xreadgroup(CONSUMER_GROUP, CONSUMER_NAME, {STREAM_KEY: '>'}, count=1, block=5000)
            if messages:
                for stream, message_list in messages:
                    for message_id, message in message_list:
                        process_message(message, ELASTICSEARCH_ENDPOINT, ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD, TASK_STATUS_UPDATE_ENDPOINT)
                        # Acknowledge the message
                        r.xack(STREAM_KEY, CONSUMER_GROUP, message_id)
        except Exception as e:
            print(f"Error reading messages: {e}")
            time.sleep(1)  # Wait a bit before retrying

if __name__ == '__main__':
    main()