# coding : utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver 
import time
import pandas as pd
import numpy as np


source = []
df = pd.DataFrame([])
with open('rumah.txt','r') as f:
    lines = f.readlines()
for i in lines:
    source.append(i.rstrip())

feature_dict={}
k=0
for i in source[10000:13000]:
    try:
        url = i
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'lxml')
        #Feature
        #1
        try:
            xpath = "//div[@class='medium-6 small-6 columns PriceSection']/span/span"
            feature_dict['price'] = driver.find_element_by_xpath(xpath).text.split(' ')[1]
        except:
            feature_dict['price'] = np.nan
        #2
        try:
            xpath = "//div[@class='Navigation-wrapper']/div[4]/a"
            feature_dict['lokasi'] = driver.find_element_by_xpath(xpath).text.strip().rstrip()
        except:
            feature_dict['lokasi'] = np.nan
        #3
        try:
            feature_dict['lb'] = soup.find('span',{'class':'Overview-attribute icon-livingsize-v4'}).string.strip().split(' ')[0]
        except:
            feature_dict['lb'] = np.nan   
        #4
        try:
            feature_dict['lt'] = soup.find('span',{'class':'Overview-attribute icon-land_size-v4'}).string.strip().split(' ')[0]
        except:
            feature_dict['lt'] = np.nan
        #5
        try:
            rincian = soup.find_all('div',{'class':'columns-2'})
            for j in rincian:
                child = j.findChildren('div',recursive = False)
                feature = child[0]['data-attr-name']
                val = child[1].string.strip()
                feature_dict[feature] = val
        except:
            pass

        #6
        try:
            xpath = "//*[@id='listing-description']/div/div/div"
            feature_dict['deskripsi'] = driver.find_element_by_xpath(xpath).text.strip().rstrip()
        except:
            pass

        #7
        try:
            xpath = "//*[@id='listing-amenities']/div/div"
            feature_dict['fasilitas'] = driver.find_element_by_xpath(xpath).text.strip().rstrip()
        except:
            pass
        try:
            xpath = "//*[@id='js-landmark-accordion-head']/div/ul"
            feature_dict['terdekat'] = driver.find_element_by_xpath(xpath).text.strip().rstrip()
        except:
            pass

        df = df.append(feature_dict,ignore_index=True)
        driver.close()
        time.sleep(2)
    except:
        pass
    k+=1
    if k%20==0:
        print(f'{k} rows have been collected')
print('complete')
print(df)
df.to_csv('jakarta_houseprice.csv')
