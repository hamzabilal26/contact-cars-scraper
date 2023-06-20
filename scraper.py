import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from lxml import html

import openpyxl


wb = openpyxl.Workbook()
ws = wb.active

ws.append(['Name', 'City', 'Price', 'Body Type', 'Kilometers', 'Engine Capacity' , 'Img 1', 'Img 2', 'Img 3'])

wb2 = openpyxl.Workbook()
ws2 = wb2.active



options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument('--lang=en_US')
# options.add_experimental_option("detach", True)
options.add_argument("headless");


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
url = "https://www.contactcars.com/en/cars/used/engines?page=1&sortOrder=false&sortBy=CreatedAt"
driver.get(url)
i = 1
while True:

    ads_count = 0

    try:
        ads = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-xl-4 col-md-6 mt-3 px-2 ng-star-inserted']"))
        )
    except Exception as e:
        print(e)

    ads_count = len(ads)
    retry_count = 0


    print(f"page number: {i}")
    while True:
        last_ad = ads[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_ad)
        time.sleep(1)

        ads = driver.find_elements(By.XPATH, "//div[@class='col-xl-4 col-md-6 mt-3 px-2 ng-star-inserted']")
        this_ads_count = len(ads)

        if this_ads_count > ads_count:
            retry_count = 0
            ads_count = this_ads_count
            continue
        else:
            retry_count += 1

        if retry_count > 10:
            break

    urls = driver.find_elements(By.XPATH, "//a[@class='n-engine-card__link']")
    print(len(urls))
    # print(urls)
    for each in urls:
        link = each.get_attribute("href")
        try:
            response = requests.get(link)
        except Exception as e:
            print(e)

        print(response.status_code)
        print(link)
        data = html.fromstring(response.content)
        try:
            name1 = data.xpath("//h3[@class='car-name']//span[1]/text()")[0]
        except Exception as e:
            print(e)
            name1 = ''
        try:
            name2 = data.xpath("//h3[@class='car-name']//span[2]/text()")[0]
        except Exception as e:
            print(e)
            name2 = ''
        try:
            name3 = data.xpath("//h3[@class='car-name']//span[3]/text()")[0]
        except Exception as e:
            print(e)
            name3 = ''

        name = f"{name1} {name2} {name3}"
        print(f"Name: {name}")
        try:
            city = data.xpath("//p/span[3]/text()")[0]
            print(f"City: {city}")
        except Exception as e:
            print(e)
            city = ''
        try:
            price = data.xpath("//div[@class='price']/span/text()")[0]
            print(f"Price: {price}")
        except Exception as e:
            print(e)
            price = ''
        try:
            body_type = data.xpath("//app-spec-item/p[following-sibling::p[text()='Body Shape']]/text()")[0]
            print(f"Body Shape: {body_type}")
        except Exception as e:
            print(e)
            body_type = ''
        try:
            kilometers = data.xpath("//app-spec-item/p[following-sibling::p[text()='Kilometers']]/text()")[0]
            print(f"Kilometers: {kilometers}")
        except Exception as e:
            print(e)
            kilometers = ''
        try:
            capacity = data.xpath("//app-spec-item/p[following-sibling::p[text()='Engine Capacity']]/text()")[0]
            print(f"Engine Capacity: {capacity}")
        except Exception as e:
            print(e)
            capacity = ''
        try:
            imgs = data.xpath("//div/img[@alt='carousel-image']/@src")
        except Exception as e:
            print(e)
            imgs = []
        try:
            img1 = imgs[0]
            print(f"Image 1: {img1}")
        except Exception as e:
            print(e)
            img1 = ''
        try:
            img2 = imgs[1]
            print(f"Image 2: {img2}")
        except Exception as e:
            print(e)
            img2 = ''
        try:
            img3 = imgs[2]
            print(f"Image 3: {img3}")
        except Exception as e:
            print(e)
            img3 = ''
        # urls = []
        for each in imgs:
            ws2.append([each])


        this_row = [name, city, price, body_type, kilometers, capacity, img1, img2, img3]
        ws.append(this_row)
        # ws2.append(urls)

    next_btn = driver.find_element(By.XPATH, "//button[@class='paginator__arrow'][3]")
    next_btn.click()
    i += 1



    wb.save("Data.xlsx")
    wb2.save("Urls.xlsx")

# ads = driver.find_elements(By.XPATH, "//div[@class='col-xl-4 col-md-6 mt-3 px-2 ng-star-inserted']")
# for ad in ads:
#     driver.execute_script("arguments[0].scrollIntoView();", ad)
#     ad.click()
#
#     name = driver.find_element(By.XPATH, "//h3[@class='car-name']//span[1]").text
#     print(f"Name: {name}")