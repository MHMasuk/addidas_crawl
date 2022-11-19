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


def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")

    # # initialize driver
    # driver = webdriver.Remote(
    #         command_executor='http://localhost:4444/wd/hub',
    #         desired_capabilities=DesiredCapabilities.CHROME)

    driver = webdriver.Chrome(executable_path='/home/ikhwan/coading/scrapy_project/addidas_crawl/chromedriver',
                              options=options)
    # driver = webdriver.Chrome('/home/ikhwan/coading/scrapy_project/addidas_crawl/chromedriver')

    return driver


SCROLL_PAUSE_TIME = 10


class AddidasCrawlSpider(scrapy.Spider):

    name = 'addidas_crawl'
    allowed_domains = ['shop.adidas.jp']
    start_urls = ['https://shop.adidas.jp/men/']
    driver = get_driver()

    def parse(self, response):
        driver = get_driver()
        driver.get("https://shop.adidas.jp/men/")
        time.sleep(5)
        all_menu_url = driver.find_element(By.XPATH, "//a[@data-ga-event-label='mens-all']").get_attribute('href')
        print("all_mens", all_menu_url)
        time.sleep(5)

        driver.get(str(all_menu_url))
        time.sleep(10)

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

        product_links = driver.find_elements(
            By.XPATH, "//div[@class='articleDisplayCard itemCardArea-cards test-card css-1lhtig4']//a"
        )
        print(len(product_links))

        product_links = [product.get_attribute('href') for product in product_links]
        print(product_links)

        next_arrow_elements = driver.find_elements(By.XPATH, '//ul[@class="buttonArrowArea"]//li//a')

        for product_link in product_links:
            yield scrapy.Request(url=product_link, callback=self.parse_detail)

        if next_arrow_elements:
            next_link = None
            print("next_arrow_element", next_arrow_elements)
            for next_arrow_element in next_arrow_elements[:-1]:
                print("next_arrow_element", next_arrow_element.get_attribute('href'))
                next_link = next_arrow_element.get_attribute('href')

            driver.get(str(next_link))

        driver.quit()

    def parse_detail(self, response):
        driver = get_driver()
        driver.get(str(response.url))
        time.sleep(15)

        # breadcrumb data
        breadcrumb_list = []
        links = driver.find_elements(By.XPATH, '//div[@class="breadcrumb_wrap"]/ul/li/a')[1:]
        for link in links:
            breadcrumb_list.append(link.text.strip())

        # category data
        category = driver.find_element(By.XPATH, '//a[@class="groupName"]//span')

        # product name data
        product_name = driver.find_element(By.XPATH, '//h1[@class="itemTitle test-itemTitle"]')

        # pricing data
        pricing = driver.find_element(By.XPATH, '//span[@class="price-value test-price-value"]')

        image_url_list = []
        image_urls = driver.find_elements(By.XPATH, '//ul[@class="slider-list test-slider-list"]//img')
        for image_url in image_urls:
            image_url_list.append(image_url.get_attribute('src'))

        available_size_list = []
        available_sizes = driver.find_elements(By.XPATH, '//div[@class="test-sizeSelector css-958jrr"]//ul//li//button')
        for available_size in available_sizes:
            available_size_list.append(available_size.text.strip())

        sense_of_the_size_list = []
        sense_of_the_sizes = driver.find_elements(By.XPATH, '//div[@class="sizeFitBar css-zrdet1"]//span')
        for sense_of_the_size in sense_of_the_sizes:
            sense_of_the_size_list.append(sense_of_the_size.text.strip())

        # title of description
        title_of_description = driver.find_element(
            By.XPATH,
            '//h4[@class="itemFeature heading test-commentItem-subheading"]'
        )

        # general description data
        general_description_of_the_product = driver.find_element(
            By.XPATH,
            '//div[@class="details description_part test-itemComment-descriptionPart"]//div'
        )

        general_description_itemization_list = []
        general_description_itemizations = driver.find_elements(
            By.XPATH,
            '//ul[@class="articleFeatures description_part css-woei2r"]//li'
        )
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

        # all_the_chest_list = []
        # all_the_chest = driver.find_elements(By.XPATH, '//table[@class="sizeChartTable"]//tbody//tr[2]//td//span')
        #
        # for chest in all_the_chest:
        #     all_the_chest_list.append(chest.text.strip())
        # # print("all_the_chest_list", all_the_chest_list)
        #
        # data_zip = dict(zip(all_the_size_list, all_the_chest_list))
        # # print("data zip", data_zip)

        all_size_values = driver.find_elements(By.XPATH, '//table[@class="sizeChartTable"]//tbody//tr')

        all_value_zip_list = []
        count = 2
        for i in range(1, len(all_the_size_list) - 1):
            value_list = []
            for all_size_value in all_size_values:
                value_data_list = all_size_value.find_elements(
                    By.XPATH,
                    f'//table[@class="sizeChartTable"]//tbody//tr[{count}]/td/span'
                )

                for value_data in value_data_list:
                    value_list.append(value_data.text.strip())
            data_zip = dict(zip(all_the_size_list, value_list))
            all_value_zip_list.append(data_zip)
            value_list.clear()
            count += 1

        size_chart_headers_list = []
        size_chart_headers = driver.find_elements(
            By.XPATH,
            '//div[@class="sizeChart test-sizeChart css-l7ym9o"]//table[@class="sizeChartTable"]//thead//tr//th')
        # print("size_chart_headers", size_chart_headers)

        for size_chart_header in size_chart_headers[1:]:
            size_chart_headers_list.append(size_chart_header.text.strip())
        # print("size_chart_headers_list", size_chart_headers_list)

        chart_data = dict(zip(size_chart_headers_list, all_value_zip_list))

        # rating data
        try:
            rating = driver.find_element(By.XPATH, '//span[@class="BVRRNumber BVRRRatingNumber"]')
        except:
            rating = ""

        # Number of reviews data
        try:
            number_of_reviews = driver.find_element(By.XPATH, '//span[@class="BVRRNumber BVRRBuyAgainTotal"]')
        except:
            number_of_reviews = ""

        # recommended rate data
        try:
            recommended_rate = driver.find_element(By.XPATH, '//span[@class="BVRRBuyAgainPercentage"]//span')

            # scroll to that element
            desired_y = (recommended_rate.size['height'] / 2) + recommended_rate.location['y']
            window_h = driver.execute_script('return window.innerHeight')
            window_y = driver.execute_script('return window.pageYOffset')
            current_y = (window_h / 2) + window_y
            scroll_y_by = desired_y - current_y

            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
        except:
            recommended_rate = ''

        time.sleep(10)

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

        try:
            # single review information
            review_rating_list = driver.find_elements(By.XPATH, '//*[@class="BVRRRatingNormalImage"]//img')
            review_rating_list = [review_rating.get_attribute('title').strip().split("/")[0] for review_rating in
                                  review_rating_list]
        except:
            review_rating_list = []

        try:
            review_title_list = driver.find_elements(By.XPATH, '//*[@class="BVRRValue BVRRReviewTitle"]')
            review_title_list = [review_title.text.strip() for review_title in review_title_list]
        except:
            review_title_list = []

        try:
            review_text_list = driver.find_elements(By.XPATH, '//span[@class="BVRRReviewText"]')
            review_text_list = [review_text.text.strip() for review_text in review_text_list]
        except:
            review_text_list = []

        try:
            review_date_list = driver.find_elements(By.XPATH, '//meta[@itemprop="datePublished"]')
            review_date_list = [review_date.get_attribute('content') for review_date in review_date_list]
        except:
            review_date_list = []

        try:
            review_id_list = driver.find_elements(By.XPATH, '//span[@class="BVRRNickname"]')
            review_id_list = [review_id.text.strip() for review_id in review_id_list]
        except:
            review_id_list = []

        user_review_zip = list(
            zip(review_date_list, review_rating_list, review_title_list, review_text_list, review_id_list))

        try:
            # sense of filtering data
            sense_of_fitting = driver.find_element(By.XPATH,
                                                   '//*[@class="BVRRSecondaryRatingsContainer"]//*[@class="BVRRRatingContainerRadio"]//*[@class="BVRRRating BVRRRatingRadio BVRRRatingFit"]//div//img')
            sense_of_fitting = sense_of_fitting.get_attribute('title')
        except:
            sense_of_fitting = ''


        try:
            # appropriation of length data
            appropriation_of_length = driver.find_element(By.XPATH,
                                                          '//*[@class="BVRRSecondaryRatingsContainer"]//*[@class="BVRRRatingContainerRadio"]//*[@class="BVRRRating BVRRRatingRadio BVRRRatingLength"]//div//img')
            appropriation_of_length = appropriation_of_length.get_attribute('title')
        except:
            appropriation_of_length = ""


        try:
            # quality of material data
            quality_of_material = driver.find_element(By.XPATH,
                                                      '//*[@class="BVRRSecondaryRatingsContainer"]//*[@class="BVRRRatingContainerRadio"]//*[@class="BVRRRating BVRRRatingRadio BVRRRatingQuality"]//div//img')
            quality_of_material = quality_of_material.get_attribute('title')
        except:
            quality_of_material = ""

        try:
            # comfort data
            comfort = driver.find_element(By.XPATH,
                                          '//*[@class="BVRRSecondaryRatingsContainer"]//*[@class="BVRRRatingContainerRadio"]//*[@class="BVRRRating BVRRRatingRadio BVRRRatingComfort"]//div//img')
            comfort = comfort.get_attribute('title')
        except:
            comfort = ""

        # keywords
        kws = driver.find_elements(By.XPATH, '//div[@class="itemTagsPosition"]//div//div//a')
        kws = [kw.text.strip() for kw in kws]

        yield {
            "Product URL": str(response.url),
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
            "chart_data": chart_data,
            "Rating": rating.text.strip() if rating else None,
            "Number Of Reviews": number_of_reviews.text.strip() if number_of_reviews else None,
            "Recommended rate": recommended_rate.text.strip() if recommended_rate else None,
            "User Review": user_review_zip,
            "Sense of Fitting/Rating": sense_of_fitting,
            "Appropriation of Length/Rating": appropriation_of_length,
            "Quality of material/Rating": quality_of_material,
            "comfort": comfort,
            "KWs": kws,
        }
        driver.quit()
