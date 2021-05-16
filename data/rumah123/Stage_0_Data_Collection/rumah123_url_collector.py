### Collect ulrs of houses from rumah123.com
### We collect houses specifically from urls in the url.txt, and stored to rumah.txt
### 11/05/2021

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

main_url = 'https://www.rumah123.com'
for i in url_list:
    print(i)
    j = 0
    urls = []
    no_page = 1
    url = i+'/?page='+str(no_page)
    
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'lxml')
    print(f'PAGE {no_page} : {url}')
          
    while True:
        time.sleep(2)
        u = len(urls)
        get_div = soup.find_all('div',{'class':'sc-eCssSg hmocIu'})
        for k in get_div:
            try:
                urls.append(main_url+k.div.div.a['href'])
            except:
                pass
        print(f'{len(urls)-u} urls collected')
        if len(urls)-u == 0:
            break
        else:
            try:
                j+=1
                no_page+=1
                url = i+'/?page='+str(no_page)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source,'lxml')
                print(f'PAGE {no_page} : {url}')
                time.sleep(5)
            except Exception as e:
                print(e)
                break
    print(f'Done scrapping from {i}, Total {len(urls)} urls was collected\n')
    with open('rumah.txt','a+') as f:
        for i in urls:
            f.write(f'{i}\n')
    driver.close()