# -*- coding: utf-8 -*-
"""Tugas Kelompok Ketiga.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CaHHZJElUuVICcIDTSoM1gx0zOj1k-JV

Mengimport library yang dibutuhkan dan menautkan Google Drive
"""

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from google.colab import drive
drive.mount('/content/drive')

"""Membuka dan memproses dataset"""

data = pd.read_excel('/content/drive/My Drive/DatasetBDA/SampleSuperstores.xlsx')
data.head()

"""Mengeksplorasi kolom pada dataset"""

data.columns

"""Mengeksplorasi kota yang unik di setiap transaksinya"""

data.City.unique()

"""Data cleaning"""

# Menghapus spasi tambahan pada kategori dan sub-kategori
data['Category'] = data['Category'].str.strip()
data['Sub-Category'] = data['Sub-Category'].str.strip()
  
# Menghapus baris yang tidak terdapat nomor invoice
data.dropna(axis = 0, subset =['Postal Code'], inplace = True)
data['Postal Code'] = data['Postal Code'].astype('str')

"""Splitting data berdasarkan kota asal transaksi *diambil contoh 4 kota


"""

# Transaksi yang dilakukan di Los Angeles
basket_LA = (data[data['City'] =="Los Angeles"]
		.groupby(['Postal Code', 'Category'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('Postal Code'))

# Transaksi yang dilakukan di Fort Lauderdale
basket_FL = (data[data['City'] =="Fort Lauderdale"]
		.groupby(['Postal Code', 'Category'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('Postal Code'))

# Transaksi yang dilakukan di New York City
basket_NYC = (data[data['City'] =="New York City"]
		.groupby(['Postal Code', 'Category'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('Postal Code'))

# Transaksi yang dilakukan di San Francisco
basket_SF = (data[data['City'] =="San Francisco"]
		.groupby(['Postal Code', 'Category'])['Quantity']
		.sum().unstack().reset_index().fillna(0)
		.set_index('Postal Code'))

"""Data encoding"""

# Membuat hot encode untuk menyesuaikan dengan library yang digunakan
def hot_encode(x):
	if(x<= 0):
		return 0
	if(x>= 1):
		return 1

# Encoding dataset
basket_encoded = basket_LA.applymap(hot_encode)
basket_LA = basket_encoded

basket_encoded = basket_FL.applymap(hot_encode)
basket_FL = basket_encoded

basket_encoded = basket_NYC.applymap(hot_encode)
basket_NYC = basket_encoded

basket_encoded = basket_SF.applymap(hot_encode)
basket_SF = basket_encoded

"""Membuat model dan analisa hasil

Los Angeles
"""

# Bentuk model
frq_items = apriori(basket_LA, min_support = 0.05, use_colnames = True)
  
# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Fort Lauderdale"""

# Bentuk model
frq_items = apriori(basket_FL, min_support = 0.05, use_colnames = True)
  
# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""New York City"""

# Bentuk model
frq_items = apriori(basket_NYC, min_support = 0.05, use_colnames = True)
  
# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""San Francisco"""

# Bentuk model
frq_items = apriori(basket_SF, min_support = 0.05, use_colnames = True)
  
# Mengumpulkan data pada sebuah dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())

"""Setelah menganalisis keempat contoh model diatas, dapat disimpulkan bahwa pada keempat kota diatas, jenis barang yang sering dibeli adalah kebutuhan kantor, furnitur, dan teknologi"""