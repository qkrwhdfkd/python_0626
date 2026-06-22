import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv' 
df = pd.read_csv(file_path, encoding='cp949')

df_clean = df[['일자', '통합 분류1']].dropna()

pivot_df = df_clean.groupby(['일자', '통합 분류1']).size().unstack(fill_value=0)
# 날짜별 통합 분류1의 값이 같은 것들을 모아 수를 세어서 통합 분류1의 값을 컬럼으로 해서 값을 넣어 표를 만들어라

# 한글 깨짐 방지 설정 (Windows 기준, Mac은 'AppleGothic')
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

daily_total_articles = pivot_df.sum(axis=1) #총 기사 수
total_articles = daily_total_articles.sum()  
target_chunks = 30                           


visual_threshold = total_articles / target_chunks


"""
이제 축약된 날짜 X 축으로 시각화를 할 것인데
통합 분류1의 값을 기사 비율로 표현 3위까지만
"""

date_mapping = {}
current_group_start = None
current_sum = 0

for date, count in daily_total_articles.items():
    if current_group_start is None:
        current_group_start = date
    current_sum += count
    date_mapping[date] = current_group_start
    if current_sum >= visual_threshold:
        current_group_start = None
        current_sum = 0



if current_group_start is not None:
    for date in daily_total_articles.index:
        if date not in date_mapping:
            date_mapping[date] = current_group_start

# 원래의 pivot_df 인덱스를 결합 날짜로 바꾼 후 합산
pivot_df['결합_일자'] = pivot_df.index.map(date_mapping)
compressed_df = pivot_df.groupby('결합_일자').sum()

print(pivot_df)

# ====================================================
# 2. 전체 기간 기준 상위 3개 카테고리만 추출 및 비율 변환
# ====================================================
# 전체 기간 동안 가장 많이 기사가 난 상위 3개 카테고리 선정
top_3_categories = compressed_df.sum().nlargest(3).index.tolist()

# 상위 3개 카테고리 데이터만 필터링
df_top3 = compressed_df[top_3_categories].copy()

# 각 날짜 구간별 '총 기사 수'로 나누어 비율(%)로 변환
# (상위 3개만의 비율이 아니라, 그날 전체 기사 대비 3대 카테고리의 비율을 구합니다)
row_totals = compressed_df.sum(axis=1)
df_percentage = df_top3.div(row_totals, axis=0) * 100

# ====================================================
# 3. Matplotlib + Seaborn 시각화 (누적 막대 그래프)
# ====================================================
plt.figure(figsize=(15, 8))

# 누적 막대그래프 그리기 (밑바닥부터 쌓아 올리는 방식)
bottom_data = pd.Series(0, index=df_percentage.index)
colors = sns.color_palette('pastel', 3)

for i, category in enumerate(top_3_categories):
    plt.bar(df_percentage.index, df_percentage[category], 
            bottom=bottom_data, label=category, color=colors[i], width=0.6)
    bottom_data += df_percentage[category]

# 그래프 디테일 설정
plt.title('날짜 구간별 상위 3개 카테고리 기사 비율 변화 (30개 구간 축약)', fontsize=16, pad=20)
plt.xlabel('날짜 구간 (시작일)', fontsize=12)
plt.ylabel('기사 비율 (%)', fontsize=12)
plt.xticks(rotation=45, ha='right') # X축 글자 겹침 방지
plt.ylim(0, 100) # 비율이므로 y축은 0~100
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend(title="통합 분류1 (Top 3)", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()