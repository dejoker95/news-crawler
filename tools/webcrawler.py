from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
