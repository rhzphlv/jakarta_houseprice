### We collect house price data for each houses in rumah.txt
### 11/05/2021

my_file = open('rumah.txt')
my_file.seek(0)
links = my_file.readlines()
my_file.close()
links = [link[:-2] for link in links]

from selenium import webdriver
import json
import time

start_time = time.time()
data_part = []
counter = 0

for link in links:
    kamus = {'harga' : '', 'lokasi' : ''}
    while kamus['harga'] == '' and kamus['lokasi'] == '':
        path = r'../chromedriver.exe'
        driver = webdriver.Chrome(path)
        driver.get(link)

        data = {}
        kamus = {}
        time.sleep(5)
        print(f'House {counter} : {link}')
        ## Harga dan Lokasi
        try:
            xpath_price = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[1]/span'
            price = driver.find_element_by_xpath(xpath_price).text
            kamus['harga'] = price
        except:
            kamus['harga'] = ''

        try:
            xpath_loc = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/h1' 
            loc = driver.find_element_by_xpath(xpath_loc).text
            kamus['lokasi'] = loc
        except:
            kamus['lokasi'] = ''
        
        ## Pengecekan Halaman Tidak Ditemukan
        try:
            xpath_halaman = '//*[@id="99-root-app"]/div/div/div[2]/p[1]'
            halaman = driver.find_element_by_xpath(xpath_halaman).text
        except:
            halaman = ''
            
        if halaman != '':
            print('Halaman Tidak Ditemukan', '\n')
            counter += 1
            driver.quit()
            break
        elif kamus['harga'] == '' and kamus['lokasi'] == '':
            print('Lagi dikira bot')
            driver.quit()
            time.sleep(10)
            pass
        else:
            counter+=1
            ## Luas Bangunan/Luas Tanah
            try:
                xpath_lb = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/div/div/div[1]/a/span'
                lb = driver.find_element_by_xpath(xpath_lb).text
                kamus['lb'] = lb
            except:
                kamus['lb'] = ''

            try:
                xpath_lt = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div/div/div/div[2]/a/span'
                lt = driver.find_element_by_xpath(xpath_lt).text
                kamus['lt'] = lt
            except:
                kamus['lt'] = ''


            ## Kamar Tidur, Kamar Mandi, Garasi
            try:
                xpath_kt = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[4]/div/div/div/div[1]/a/span[2]'
                kt = driver.find_element_by_xpath(xpath_kt).text
                kamus['kt'] = kt
            except:
                kamus['kt'] = ''

            try:
                xpath_km = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[4]/div/div/div/div[2]/a/span[2]'
                km = driver.find_element_by_xpath(xpath_km).text
                kamus['km'] = km
            except:
                kamus['km'] = ''

            try:
                xpath_car = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[4]/div/div/div/div[3]/a/span[2]'
                car = driver.find_element_by_xpath(xpath_car).text
                kamus['car'] = car
            except:
                kamus['car'] = ''

            # Klik menampilkan lebih banyak untuk kolom Deskripsi
            keklik = False
            cobaklik = 0
            while keklik == False and cobaklik < 20:
                try:
                    button = driver.find_element_by_xpath(
                        '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/span')
            #         '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]')
                    button.click()
                    print("Berhasil menampilkan lebih banyak KOLOM DESKRIPSI")
                    keklik = True
                except:
                    cobaklik += 1

            if keklik == False:
                print("Gagal menampilkan lebih banyak KOLOM DESKRIPSI atau button memang tidak ada")

            # Judul Deskripsi/Deskripsi Kalau ada peta
            ada_peta = True
            try:
                xpath_jdl = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/h2'
                jdl = driver.find_element_by_xpath(xpath_jdl).text
            except:
                jdl = ''
                ada_peta = False

            try:
                xpath_desc = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div[1]/div[1]/p'
                desc = driver.find_element_by_xpath(xpath_desc).text
                kamus['Deskripsi'] = jdl + ':' + desc
            except:
                kamus['Deskripsi'] = ''
                ada_peta = False

            if ada_peta == False:
                # Judul Deskripsi/Deskripsi Kalau tidak ada peta
                try:
                    xpath_jdl = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/h2'
                    jdl = driver.find_element_by_xpath(xpath_jdl).text
                except:
                    jdl = ''

                try:
                    xpath_desc = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[1]/div[1]/p'
                    desc = driver.find_element_by_xpath(xpath_desc).text
                    kamus['Deskripsi'] = jdl + ':' + desc
                except:
                    kamus['Deskripsi'] = ''


            ## Klik Menampilkan Lebih banyak untuk kolom detil/info properti
            keklik = False
            ada_fasilitas = False
            cobaklik = 0
            while keklik == False and cobaklik < 20:
                try:
                    button = driver.find_element_by_xpath(
                      '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/span')
                #         '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/span')
                    button.click()
                    print("Berhasil menampilkan lebih banyak KOLOM PROPERTI")
                    keklik = True
                except:
                    cobaklik += 1

            if keklik == False:
                cobaklik = 0
                while keklik == False and cobaklik < 20:
                    try:
                        button = driver.find_element_by_xpath(
            #               '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[2]/span')
                        '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div/div/div[2]/span')
                        button.click()
                        print("Berhasil menampilkan lebih banyak KOLOM PROPERTI")
                        keklik = True
#                         ada_fasilitas = True
                    except:
                        cobaklik += 1

            if keklik == False:
                print("Gagal menampilkan lebih banyak KOLOM PROPERTI atau button memang tidak ada")
            
            if ada_fasilitas == False:
                try:
                    xpath_nama_fasilitas = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div/div[2]'
                    nama_fasilitas = driver.find_element_by_xpath(xpath_nama_fasilitas).text
                except:
                    nama_fasilitas = ''
                if nama_fasilitas == 'Fasilitas':
                    ada_fasilitas = True
            
            ## Detil Properti
            if ada_fasilitas == True:
                for i in range(1,15):
                    try:
                        xpath_nama_info = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/div['+str(i)+']/p[1]'
                        nama_info = driver.find_element_by_xpath(xpath_nama_info).text
                        xpath_info = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/div['+str(i)+']/p[2]'
                        info = driver.find_element_by_xpath(xpath_info).text
                        kamus[nama_info] = info
                    except:
                        break

                klik_fasilitas = False
                cobaklik = 0
                while klik_fasilitas == False and cobaklik < 20:
                    try:
                        button = driver.find_element_by_xpath('//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div/div[2]')
                        button.click()
                        print("Berhasil menampilkan KOLOM FASILITAS")
                        klik_fasilitas = True
                    except:
                        cobaklik += 1
                if klik_fasilitas == True:
                    try:
                        xpath_nama_fasilitas = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[1]/div/div/div[2]'
                        nama_fasilitas = driver.find_element_by_xpath(xpath_nama_fasilitas).text
                        xpath_fasilitas = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div/div[2]/div/p'
                        fasilitas = driver.find_element_by_xpath(xpath_fasilitas).text
                        kamus[nama_fasilitas] = fasilitas
                    except:
                        print('Tidak ada Fasilitas')
            else:
                for i in range(1,15):
                    try:
                        xpath_nama_info = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div/div['+str(i)+']/p[1]'
                        nama_info = driver.find_element_by_xpath(xpath_nama_info).text
                        xpath_info = '//*[@id="99-root-app"]/div/div/div[2]/div[2]/div[3]/div/div/div[2]/div/div[2]/div[1]/div/div/div['+str(i)+']/p[2]'
                        info = driver.find_element_by_xpath(xpath_info).text
                        kamus[nama_info] = info
                    except:
                        break

            print('Done')
            data[link] = kamus
            data_part.append(data)
            print(kamus)
            print("\n")
            driver.quit()
    
# Create JSON file
with open("data_rumah123.json", "w") as file:
    json.dump(data_part, file)
print("Data collected") 
runtime = time.time() - start_time
print('Run time :', runtime/3600)