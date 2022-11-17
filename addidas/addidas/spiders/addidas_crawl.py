from random import randint

import scrapy
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")

    # # initialize driver
    # driver = webdriver.Remote(
    #         command_executor='http://localhost:4444/wd/hub',
    #         desired_capabilities=DesiredCapabilities.CHROME)

    driver = webdriver.Chrome(executable_path='/home/ikhwan/coading/scrapy_project/addidas_crawl/chromedriver', options=options)
    # driver = webdriver.Chrome('/home/ikhwan/coading/scrapy_project/addidas_crawl/chromedriver')

    return driver


SCROLL_PAUSE_TIME = 10


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

        # driver.get('https://shop.adidas.jp/item/?gender=mens')
        # # //div[@class="articleDisplayCard itemCardArea-cards test-card css-1lhtig4"]
        # time.sleep(5)

        # next_arrow_element = driver.find_element(By.XPATH, '(//ul[@class="buttonArrowArea"])[2]')

        # Get scroll height
        # last_height = driver.execute_script("return document.body.scrollHeight")
        #
        # while True:
        #     # Scroll down to bottom
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #
        #     # Wait to load page
        #     time.sleep(SCROLL_PAUSE_TIME)
        #
        #     # Calculate new scroll height and compare with last scroll height
        #     new_height = driver.execute_script("return document.body.scrollHeight")
        #     if new_height == last_height:
        #         break
        #     last_height = new_height

        # delay = 3  # seconds
        # try:
        #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")

        # time.sleep(5)
        # product_links = driver.find_elements(By.XPATH, "//div[@class='articleDisplayCard itemCardArea-cards test-card css-1lhtig4']//a")
        # print(len(product_links))

        driver.get('https://shop.adidas.jp/products/HB9386/')

        time.sleep(80)

        # Get the xpath of a certain word on webpage
        # element = driver.find_elements(By.XPATH, '//div[@class="sizeChart test-sizeChart css-l7ym9o"]//table')
        # Scroll to where the xpath is in
        # driver.execute_script("return arguments[0].scrollIntoView();", element)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        breadcrumb_list = []
        links = driver.find_elements(By.XPATH, '//div[@class="breadcrumb_wrap"]/ul/li/a')[1:]
        for link in links:
            breadcrumb_list.append(link.text.strip())

        category = driver.find_element(By.XPATH, '//a[@class="groupName"]//span')
        # print("category", category.text.strip())

        product_name = driver.find_element(By.XPATH, '//h1[@class="itemTitle test-itemTitle"]')
        # print('title', product_name.text.strip())

        pricing = driver.find_element(By.XPATH, '//span[@class="price-value test-price-value"]')
        # print('pricing', pricing.text.strip())

        image_url_list = []
        image_urls = driver.find_elements(By.XPATH, '//ul[@class="slider-list test-slider-list"]//img')

        for image_url in image_urls:
            image_url_list.append(image_url.get_attribute('src'))
        # print("image_url_list", image_url_list)

        available_size_list = []
        available_sizes = driver.find_elements(By.XPATH, '//div[@class="test-sizeSelector css-958jrr"]//ul//li//button')

        for available_size in available_sizes:
            available_size_list.append(available_size.text.strip())

        # print("available_size_list", available_size_list)

        sense_of_the_size_list = []
        sense_of_the_sizes = driver.find_elements(By.XPATH, '//div[@class="sizeFitBar css-zrdet1"]//span')
        for sense_of_the_size in sense_of_the_sizes:
            sense_of_the_size_list.append(sense_of_the_size.text.strip())
        # print('sense_of_the_size_list', sense_of_the_size_list)

        title_of_description = driver.find_element(By.XPATH,
                                                   '//h4[@class="itemFeature heading test-commentItem-subheading"]')
        # print("Title of description", title_of_description.text.strip())

        general_description_of_the_product = driver.find_element(By.XPATH,
                                                                 '//div[@class="details description_part test-itemComment-descriptionPart"]//div')
        # print("general_description_of_the_product", general_description_of_the_product.text.strip())

        general_description_itemization_list = []
        general_description_itemizations = driver.find_elements(By.XPATH,
                                                                '//ul[@class="articleFeatures description_part css-woei2r"]//li')
        for general_description_itemization in general_description_itemizations:
            general_description_itemization_list.append(general_description_itemization.text.strip())
        # print("general_description_itemization_list", general_description_itemization_list)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(5)

        size_chart_headers_item = driver.find_elements(By.XPATH,
                                                  '//div[@class="sizeChart test-sizeChart css-l7ym9o"]//table')
        delay = 5  # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, size_chart_headers_item)))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        size_chart_headers_list = []
        size_chart_headers = driver.find_elements(By.XPATH, '//html//body//div//main//div//div[@class="js-sizeDescription css-1a9ggpu"]//div//div//table//thead//tr//th')
        print("size_chart_headers", size_chart_headers)



        # for size_chart_header in size_chart_headers:
        #     size_chart_headers_list.append(size_chart_header.text.strip())
        # print("size_chart_headers_list", size_chart_headers_list)



        data = {
            "chest": {
                "XS": "40.00cm",
                "M": "50.00cm"
            }
        }

        yield {
            'breadcrumb(Category)': breadcrumb_list,
            'Category': category.text.strip(),
            'Product name': product_name.text.strip(),
            "Pricing": pricing.text.strip(),
            "Image URL": image_url_list,
            "Available size": available_size_list,
            "Sense of the size": sense_of_the_size_list,
            "Title of description": title_of_description.text.strip(),
            "General Description of the product": general_description_of_the_product.text.strip(),
            "general_description_itemization_list": general_description_itemization_list,
            "size_chart": data
        }

        driver.quit()
