# 필요한 라이브러리 임포트
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# import folium
# from streamlit_folium import st_folium
import warnings
warnings.filterwarnings('ignore')

plt.rc('font', family='NanumBarunGothic')
sns.set(font="NanumGothic", style="whitegrid")
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family = 'NanumGothic')

travel_agency_df=pd.read_csv('travel_agency.csv', encoding='CP949').drop(columns='Unnamed: 0')
tourist_df=pd.read_csv('tourist.csv', encoding='CP949').drop(columns='Unnamed: 0')
food_df=pd.read_csv('food.csv', encoding='CP949').drop(columns='Unnamed: 0')
festival_df=pd.read_csv('festival.csv', encoding='CP949').drop(columns='Unnamed: 0')
culture_df=pd.read_csv('culture.csv', encoding='CP949').drop(columns='Unnamed: 0')
sleep_df=pd.read_csv('sleep.csv', encoding='CP949').drop(columns='Unnamed: 0')
comparison_df=pd.read_csv('comparison.csv', encoding='cp949').set_index('Unnamed: 0')
comparison_df.index.name=None

print(comparison_df.index.dtype)
print(list(comparison_df.index))
print(comparison_df.head())
print(comparison_df.columns)