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
    j=0 
    url = i
    urls=[]
    driver = webdriver.Chrome()
    driver.get(url)
    while True :
        try:
            time.sleep(2)
            loadMoreButton = driver.find_element_by_class_name('JbJAl')
            loadMoreButton.click()
            if j%10==0:
                print(f'{j} times click')
        except Exception as e:
            time.sleep(2)
            break
        j+=1
    main_url = 'https://www.olx.co.id'
    soup = BeautifulSoup(driver.page_source,'lxml')
    get_li = soup.find_all('li',{'class':'EIR5N'})
    for li in get_li:
	    urls.append(main_url+li.a['href'])
    print(f"{i} Complete")
    print(f'{len(urls)} urls was collected\n')
    with open('rumah.txt','a+') as f:
	    for i in urls:
	        f.write(f'{i}\n')
    
    driver.close()

print('Done')