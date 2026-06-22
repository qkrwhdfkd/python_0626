import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')

df_clean = df[['일자', '통합 분류1']].dropna()

pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)

# 1. 행(날짜) 방향 (axis=1 설정이 핵심!)
# 그날 모든 카테고리의 빈도수가 같다면 표준편차는 0이 됩니다.
daily_std = pivot_df.std(axis=1)

# 2. 표준편차가 0인 날짜들만 필터링하여 리스트로 추출
same_value_days = daily_std[daily_std == 0].index.tolist()

# ---------------------------------------------------------------
# 3. 결과 콘솔 확인 및 검증
# ---------------------------------------------------------------
print("=== [콘솔 확인] 날짜별 표준편차가 0인 날짜 분석 ===")
print(f"전체 {len(pivot_df)}일 중 표준편차가 0인 날: 총 {len(same_value_days)}일")
print(f"해당 날짜 리스트: {same_value_days}\n")

if len(same_value_days) > 0:
    print("--- [데이터 검증] 표준편차가 0인 날들의 실제 카테고리별 빈도수 ---")
    # 실제로 모든 카테고리 수치가 똑같이 생겼는지 눈으로 확인합니다.
    print(pivot_df.loc[same_value_days])
else:
    print("※ 모든 카테고리의 빈도수가 완벽히 일치하여 표준편차가 0이 된 날은 없습니다.")
print("====================================================\n")