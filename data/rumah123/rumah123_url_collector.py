from bs4 import BeautifulSoup
from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url_list = []
with open('url.txt','r') as f:
    lines = f.readlines()
for i in lines:
    url_list.append(i.rstrip())

for i in url_list:
    print(i)
    url = i
    j = 0
    urls = []
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'lxml')
    main_url = 'https://www.rumah123.com'
    while True:
        time.sleep(2)
        get_div = soup.find_all('div',{'class':'sc-eCssSg hmocIu'})
        for i in get_div:
            try:
                urls.append(main_url+i.div.div.a['href'])
            except:
                pass
        try:
            j+=1
            next_button = driver.find_element_by_xpath("//li[@class='ui-molecule-paginate__item--next flex']/a")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
            if j%10==0:
                print(f'{j} times clicked')
        except Exception as e:
            print(e)
            break
    print('done')
    print(f'{len(urls)} urls was collected\n')
    with open('rumah.txt','a+') as f:
        for i in urls:
            f.write(f'{i}\n')
    driver.close()