import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')

df_clean = df[['일자', '통합 분류1']].dropna()
#'일자'가 비어있거나(NaN), '통합 분류1'이 비어있거나, 둘 다 비어있는 행은 무조건 통째로 버림

pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)


# 1. 날짜별로 모든 카테고리의 기사 수를 합산 (하루 총 기사 건수 시리즈 생성)
daily_total_articles = pivot_df.sum(axis=1)

# 2. 날짜별 합산 값들의 평균 계산
average_daily_articles = daily_total_articles.mean()

print("=== [콘솔 확인] 하루 평균 기사 발행량 ===")
print(f"분석 기간: 총 {len(pivot_df)}일")
print(f"★ 하루 평균 기사 수: {average_daily_articles:.2f}건")
print("====================================================\n")
