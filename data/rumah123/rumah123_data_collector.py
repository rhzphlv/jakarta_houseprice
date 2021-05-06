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
source = set(source)
source = list(source)
feature_dict={}
j=0
for i in source:
	try:
		url = i
		driver = webdriver.Safari()
		driver.get(url)
		time.sleep(2)
		soup = BeautifulSoup(driver.page_source,'lxml')
		#Feature
		#1
		try:
			feature_dict['price'] = driver.find_element_by_class_name('ui-atomic-text ui-atomic-text--styling-heading-4 ui-atomic-text--typeface-primary r123-o-listing-summary__detail--price__title').text.split(' ')[1]
		except:
			feature_dict['price'] = np.nan
		#2
		try:
			feature_dict['lokasi'] = driver.find_element_by_class_name('ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary r123-o-listing-summary__detail--address__info').text.split(',')[0]
		except:
			feature_dict['lokasi'] = np.nan
		#3
		try:
			feature_dict['lt'] = driver.find_element_by_class_name('ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary r123-o-listing-summary__detail--address__info').text.split(',')[0]
		except:
			feature_dict['lt'] = np.nan
		#4
		try:
			feature_dict['lb'] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_p_sqr_building'}).string
		except:
			feature_dict['lb'] = np.nan
		#5
		try:
			feature_dict['lantai'] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_p_floor'}).string
		except:
			feature_dict['lantai'] = np.nan
		#6
		try:
			feature_dict['tipe'] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_type'}).string
		except:
			feature_dict['tipe'] = np.nan
		#7
		try:
			feature_dict['kamar'] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_p_bedroom'}).string
		except:
			feature_dict['kamar'] = np.nan
		#8
		try:
			feature_dict['km'] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_p_bathroom'}).string
		except:
			feature_dict['km'] = np.nan
		#9
		try:
			feature_dict["sertifikat"] = soup.find('span',{'class':'_2vNpt','data-aut-id':'value_p_certificate'}).string
		except:
			feature_dict['sertifikat'] = np.nan
		#10
		try:
			fasilitas = soup.find('div',{'class':'_3FF8P'})
			feature_dict['fasilitas_total'] = [i.string for i in fasilitas.find_all('span')]
		except:
			feature_dict['fasilitas_total'] = np.nan
		#11
		try:
			desc = soup.find('div',{'data-aut-id':'itemDescriptionContent'})
			feature_dict['desc'] = [i.string for i in desc.find_all('p')]
		except:
			feature_dict['desc'] = np.nan
		df = df.append(feature_dict,ignore_index=True)
	except:
		pass
	driver.close()
	j+=1
	if j%20==0:
		print(f'{j} rows have been collected')
print('complete')
df.to_csv('jakarta_houseprice.csv')