import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')

df_clean = df[['일자', '통합 분류1']].dropna()

pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)

daily_total_articles = pivot_df.sum(axis=1) #날짜 기사합산 시리즈

average_daily_articles = daily_total_articles.mean() # 평균

print("=== [콘솔 확인] 하루 평균 기사 발행량 ===")
print(f"분석 기간: 총 {len(pivot_df)}일")
print(f"★ 하루 평균 기사 수: {average_daily_articles:.2f}건")
print("====================================================\n")

"""
   데이터프레임의 날짜를 순회하면서 
   ‘하루 평균 기사 수’에 미치지 못하는 날들을 다음 날과 계속해서 
   누적 결합하는 로직
"""



combined_data = {}  # {결합된_맨앞_날짜: 합산된_기사수}를 담을 딕셔너리
current_group_start = None
current_sum = 0

print("=== [콘솔 확인] 날짜 결합 및 시리즈 생성 진행 ===")

for date, count in daily_total_articles.items():
    # 새로운 그룹의 시작점 지정
    if current_group_start is None:
        current_group_start = date
        
    current_sum += count
    
    # 더하고 있는 값이 평균보다 커지면, 만약 마지막의 기사수가 평균보다 작은 경우는 
    # 아래 if식으로 처리하고 있음
    if current_sum >= average_daily_articles:
        combined_data[current_group_start] = current_sum
        # 딕셔너리의 날짜를 index로, 합산된 기사수를 value로 넣어준다.
        # 그리고 다음 작업을 위해 초기화
        current_group_start = None
        current_sum = 0

# 자투리 날짜 처리 index는 저장상태임, value는 아직 저장되지 않은 상태이므로, 마지막에 한 번 더 처리
if current_group_start is not None:
   combined_data[current_group_start] = current_sum


combined_series = pd.Series(combined_data, name="결합_기사수")
combined_series.index.name = "결합_일자"

print("====================================================\n")
print("=== 🎉 최종 생성된 결합 날짜별 기사 수 시리즈 ===")
print(combined_series)
print("====================================================")
print(f"데이터 타입: {type(combined_series)}")