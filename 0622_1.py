"""
카테고리 빈도수 차이가 나는 날짜들만 선별하기
-> 트랜드 조사이므로 동일한 빈도수의 카테고리들은 제외하고, 차이가 나는 카테고리들만 추출하기
-> 원본데이터를 시각화를 위한 데이블재구성 pivot_table 활용
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')




df_clean = df[['일자', '통합 분류1']].dropna()

# 피벗 테이블  (통합 분류1의 값이 컬럼이 됨) 없는 겂은 0으로 채움
pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)

print(pivot_df.head())  # 피벗 테이블 구조 확인
