import pandas as pd


df1 = pd.read_csv('lamudi/csv_(agak)bersih.csv')
df2 = pd.read_csv('olx/csv_(agak)bersih.csv')
df3 = pd.read_csv('rumah123/Stage_1_Data_Munging/munged_data_rumah123.csv')
df3 = df3[['kamar_mandi','kamar','lb','lt','tipe_property','price','sertifikat','deskripsi',
     'lokasi','ada_garasi','pool','taman','electricity','floors_total','gym']]
df4 = pd.read_csv('lamudi/extra/csv_(agak)bersih.csv')
data = pd.concat([df1,df2,df3,df4],axis=0)
data.to_csv('data.csv')

