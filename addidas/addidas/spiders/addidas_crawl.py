import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# import time
#
# from selenium import webdriver #install selenium
# from webdriver_manager.chrome import ChromeDriverManager #install webdriver-manager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import WebDriverException, InvalidSessionIdException
# from selenium.webdriver import Firefox
# from webdriver_manager.firefox import GeckoDriverManager


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # # initialize driver
    # driver = webdriver.Remote(
    #         command_executor='http://localhost:4444/wd/hub',
    #         desired_capabilities=DesiredCapabilities.CHROME)

    driver = webdriver.Chrome('/home/ikhwan/coading/scrapy_project/addidas_crawl/chromedriver')

    return driver


class AddidasCrawlSpider(scrapy.Spider):
    name = 'addidas_crawl'
    allowed_domains = ['shop.adidas.jp']
    start_urls = ['https://shop.adidas.jp/men/']

    def parse(self, response):
        print("response data", response.url)
        driver = get_driver()

        # driver.get("https://shop.adidas.jp/men/")
        # time.sleep(3)
        # all_menu = driver.find_element(By.XPATH, "//a[@data-ga-event-label='mens-all']")
        # print("all_mens", all_menu.click())
        # all_menu.click()
        # time.sleep(3)

        driver.get('https://shop.adidas.jp/item/?gender=mens')
        # //div[@class="articleDisplayCard itemCardArea-cards test-card css-1lhtig4"]
        time.sleep(5)

        product_links = driver.find_elements(
            By.XPATH, "//div[@class='articleDisplayCard itemCardArea-cards test-card css-1lhtig4']//a"
        )

        print(len(product_links))

        # for product in product_links:
        #     # print(product.get_attribute("href"))
        #     link = product.get_attribute("href")
        #     print("link data", link)
        # print("product_links", product_links)
        driver.quit()

