import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')

df_clean = df[['일자', '통합 분류1']].dropna()

pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)
# 날짜별 통합 분류1의 값이 같은 것들을 모아 수를 세어서 통합 분류1의 값을 컬럼으로 해서 값을 넣어 표를 만들어라

daily_total_articles = pivot_df.sum(axis=1) #총 기사 수
total_articles = daily_total_articles.sum()  
target_chunks = 30                           


visual_threshold = total_articles / target_chunks
# 이때는 '하루 평균'이 아니라, '전체 기사 수를 30으로 나눈 값'이 새로운 기준 모수가 됩니다.

"""
257 일자를 통해
여전히 압축되지 못한 X축을 가시화를 위해 30개로 
축약하기 위한 평균이 아닌 모수를 찾아줘
"""

print("=== [콘솔 확인] 시각화 축약 모수 ===")
print(f"분석 총 일수: {len(daily_total_articles)}일")
print(f"전체 기사 수: {total_articles}건")
print(f"★ 30개 축약을 위한 구간별 기준 모수: {visual_threshold:.2f}건")
print("====================================================\n")

# ====================================================
# 🏃‍♂️ 새로운 모수(visual_threshold)를 적용한 누적 결합 로직
# ====================================================
combined_data = {}
current_group_start = None
current_sum = 0

for date, count in daily_total_articles.items():
    if current_group_start is None:
        current_group_start = date
        
    current_sum += count
    
    # 계산해둔 새로운 시각화 기준 모수를 적용합니다.
    if current_sum >= visual_threshold:
        combined_data[current_group_start] = current_sum
        current_group_start = None
        current_sum = 0

# 마지막 자투리 날짜 처리
if current_group_start is not None:
    combined_data[current_group_start] = current_sum

# 최종 시각화용 시리즈 생성
chart_series = pd.Series(combined_data, name="기사수")
chart_series.index.name = "날짜구간(시작일)"

print("=== 📊 시각화 준비 완료 (Series) ===")
print(chart_series)
print(f"X축 데이터 개수: {len(chart_series)}개")
