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

plt.rc('font', family='Malgun Gothic')
sns.set(font="Malgun Gothic", style="whitegrid")
plt.rcParams['axes.unicode_minus'] = False
plt.rc('font', family = 'Malgun Gothic')

travel_agency_df=pd.read_csv('travel_agency.csv', encoding='CP949').drop(columns='Unnamed: 0')
tourist_df=pd.read_csv('tourist.csv', encoding='CP949').drop(columns='Unnamed: 0')
food_df=pd.read_csv('food.csv', encoding='CP949').drop(columns='Unnamed: 0')
festival_df=pd.read_csv('festival.csv', encoding='CP949').drop(columns='Unnamed: 0')
culture_df=pd.read_csv('culture.csv', encoding='CP949').drop(columns='Unnamed: 0')
sleep_df=pd.read_csv('sleep.csv', encoding='CP949').drop(columns='Unnamed: 0')
comparison_df=pd.read_csv('comparison.csv', encoding='cp949').set_index('Unnamed: 0')
comparison_df.index.name=None

dfs=[travel_agency_df, tourist_df, food_df, festival_df, culture_df, sleep_df]
def filter_by_region(region, dfs):
    filtered_dfs=[df[df['시도명']==region] for df in dfs]
    return filtered_dfs

# comparison_df 정규화
scaler=StandardScaler()
comparison_df_scaled=pd.DataFrame(scaler.fit_transform(comparison_df),
columns=comparison_df.columns, index=comparison_df.index)

# 제목
st.title('광역지자체별 관광 인프라 분석')

region=st.selectbox('시도명을 선택하세요.', list(comparison_df.index), placeholder='시도명 선택')
st.write(f'선택된 광역지자체: {region}')
# tourist=[comparison_df.index==region]['방문자수']
# st.write(f'{region}에는 {tourist}명이 방문했습니다. (2023년 기준)')

# 선택된 시도의 데이터 필터링
filetered_data=comparison_df.index==region
filetered_tourist=tourist_df[tourist_df['시도명']==region]
# print(filetered_tourist)

# 시도 관련 정보 표시
tourist_list=filetered_tourist['관광지명'].tolist()

if len(tourist_list) > 5:
    displayed=', '.join(tourist_list[:5])
    st.markdown(f"- **주요 관광지**: {displayed} 외 {len(tourist_df)-5}개 더 있습니다.")
else:
    displayed=', '.join(tourist_list)
    st.markdown(f"- **주요 관광지**: {displayed}")

st.markdown('---')

st.subheader(f"{region}의 문화 및 관광서비스업체 개수")
chart_data=comparison_df.drop('방문자수', axis=1)
st.bar_chart(chart_data.loc[region])

filtered_results=filter_by_region(region, dfs)
st.subheader(f"{region}의 문화 및 관광서비스")
for i, result in enumerate(filtered_results, 1):
    st.write(f"{i}. ")
    st.dataframe(result.iloc[:5, :2])

st.markdown('---')

# 지도시각화
st.subheader(f"문화 및 관광서비스업체 분포 시각화")
categories=['문화시설', '관광숙박업', '음식업체', '축제', '종합여행업', '관광지']
select_categories=st.selectbox('시각화할 항목을 선택하세요.', categories)

if select_categories=='문화시설':
    with open('culture_map.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)
elif select_categories=='관광숙박업':
    with open('sleep_map.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)
elif select_categories=='음식업체':
    with open('food_map1.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)
elif select_categories=='측제':
    with open('festival_map.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)
elif select_categories=='종합여행업':
    with open('travel_agency_map.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)
else:
    with open('tourist_map.html', 'r', encoding='utf-8') as f:
        html_content=f.read()
        st.components.v1.html(html_content, height=600)


st.markdown('---')
st.header('데이터 분석_상관관계')

st.subheader('관광지수와 관광 인프라의 상관관계 1번')
# 상관관계 분석_관광지수-인프라
total_corr=comparison_df_scaled.drop(columns='방문자수').corr()
total_mask=np.zeros_like(total_corr, dtype=np.bool_)
total_mask[np.triu_indices_from(total_mask)]=True
max_total_corr=total_corr[total_corr>=0.5].columns

#sns.heatmap(total_corr, annot=True, cmap='coolwarm')
ax=sns.heatmap(total_corr, annot=True, cmap='coolwarm', mask=total_mask)
st.pyplot(plt)
st.markdown('모든 변수와 양의 상관관계를 가집니다.')

st.subheader('관광지수와 관광 인프라의 상관관계 2번')
total_corr_values=total_corr['관광지수'].drop('관광지수')
st.bar_chart(total_corr_values)

st.subheader('방문자수와 관광 인프라의 상관관계')
# 상관관계 분석_방문자수-관광인프라(관광지수 포함함)
# 상관관계지수
tour_corr=comparison_df_scaled.corr()

# 상관계수 바 차트 시각화
tour_corr_values=tour_corr['방문자수'].drop('방문자수')
st.bar_chart(tour_corr_values)

