from random import randint

import scrapy
import time
import json

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

    driver = webdriver.Chrome(executable_path='/home/mhmasuk/coding/scrapy_project/adidas_project/chromedriver',
                              options=options)
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

        time.sleep(10)

        # data_table = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/main[1]/div[1]/div[1]/div[5]/div[1]/div[1]/table[1]/thead[1]/tr[2]/th[1]')
        # print("data_table", data_table)

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

        # title of description
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

        # scroll to that element
        desired_y = (general_description_of_the_product.size['height'] / 2) + \
                    general_description_of_the_product.location['y']
        window_h = driver.execute_script('return window.innerHeight')
        window_y = driver.execute_script('return window.pageYOffset')
        current_y = (window_h / 2) + window_y
        scroll_y_by = desired_y - current_y

        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        time.sleep(10)

        # all the sizes
        all_the_size_list = []
        all_the_sizes = driver.find_elements(By.XPATH, '//table[@class="sizeChartTable"]//tbody//tr[1]//td//span')
        for size in all_the_sizes:
            all_the_size_list.append(size.text.strip())

        # print('all_the_size_list', all_the_size_list)

        all_the_chest_list = []
        all_the_chest = driver.find_elements(By.XPATH, '//table[@class="sizeChartTable"]//tbody//tr[2]//td//span')

        for chest in all_the_chest:
            all_the_chest_list.append(chest.text.strip())
        # print("all_the_chest_list", all_the_chest_list)

        data_zip = dict(zip(all_the_size_list, all_the_chest_list))
        # print("data zip", data_zip)

        all_size_value_list = []
        all_size_values = driver.find_elements(By.XPATH, '//table[@class="sizeChartTable"]//tbody//tr')

        all_value_zip_list = []
        count = 2
        for i in range(1, len(all_the_size_list) - 1):
            value_list = []
            for all_size_value in all_size_values:
                value_data_list = all_size_value.find_elements(By.XPATH,
                                                               f'//table[@class="sizeChartTable"]//tbody//tr[{count}]/td/span')

                for value_data in value_data_list:
                    value_list.append(value_data.text.strip())
                    # print("all_size_value", value_data.text.strip())
                    # print("main value list", value_list)
            data_zip = dict(zip(all_the_size_list, value_list))
            # print("all_size_value_list data_zip", data_zip)
            all_value_zip_list.append(data_zip)
            value_list.clear()
            count += 1

        # print("all_value_zip_list", all_value_zip_list)
        # print("all_the_size_list", all_the_size_list)

        size_chart_headers_list = []
        # size_chart_headers = driver.find_elements(By.XPATH, '//html//body//div//main//div//div[@class="js-sizeDescription css-1a9ggpu"]//div//div//table//thead//tr//th')
        size_chart_headers = driver.find_elements(
            By.XPATH,
            '//div[@class="sizeChart test-sizeChart css-l7ym9o"]//table[@class="sizeChartTable"]//thead//tr//th')
        # print("size_chart_headers", size_chart_headers)

        for size_chart_header in size_chart_headers[1:]:
            size_chart_headers_list.append(size_chart_header.text.strip())
        # print("size_chart_headers_list", size_chart_headers_list)

        chart_data = dict(zip(size_chart_headers_list, all_value_zip_list))

        # print(json.dumps(chart_data))

        rating = driver.find_element(By.XPATH, '//span[@class="BVRRNumber BVRRRatingNumber"]')

        number_of_reviews = driver.find_element(By.XPATH, '//span[@class="BVRRNumber BVRRBuyAgainTotal"]')

        recommended_rate = driver.find_element(By.XPATH, '//span[@class="BVRRBuyAgainPercentage"]//span')

        reviews = driver.find_elements(By.XPATH, '//div[starts-with(@id, "BVRRDisplayContentReviewID_")]')

        for review in reviews:
            review.find_element(By.XPATH, '//*[contains(@itemprop, "ratingValue")]').text.strip()

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
            "size_chart": data,
            "chart_data": chart_data,
            "Rating": rating.text.strip(),
            "Number Of Reviews": number_of_reviews.text.strip(),
            "Recommended rate": recommended_rate.text.strip(),
        }

        driver.quit()
