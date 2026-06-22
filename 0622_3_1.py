import matplotlib.pyplot as plt
from itertools import cycle
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
#결합일자를 기준으로 다시 카테고리별 합산 결과 테이블



# ====================================================
# 2. 전체 카테고리 데이터 비율 변환
# ====================================================
# 합산 결과 테이블의 카테고리별대로 합산시 가장 많은 것부터 차례대로 이름을 나열 내림차순으로 진행
all_categories = compressed_df.sum().sort_values(ascending=False).index.tolist()
df_absolute = compressed_df[all_categories].copy()

# ====================================================
# 3. Matplotlib + Seaborn 시각화 (실제 기사 건수 기준)
# ====================================================
plt.figure(figsize=(16, 9))

# 누적 막대그래프 초기화
bottom_data = pd.Series(0, index=df_absolute.index)

# 🎨 [단색 단순 처리] Matplotlib의 가장 기본적이고 명확한 10가지 단색 배열 (tab10)
# 카테고리가 10개가 넘어가면 다시 첫 번째 색상으로 돌아가서 단순 반복됩니다.
base_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']  # 기본 10색 
color_cycler = cycle(base_colors)

# 실제 기사 건수를 바닥(bottom)에서부터 차곡차곡 쌓아 올립니다.
for category in all_categories:
    current_color = next(color_cycler)  # 순서대로 단색 하나씩 꺼내기
    
    # edgecolor='white'로 경계선을 주어 색상이 겹치더라도 명확히 구분
    plt.bar(df_absolute.index, df_absolute[category], 
            bottom=bottom_data, label=category, color=current_color, 
            width=0.6, edgecolor='white', linewidth=0.6)
    bottom_data += df_absolute[category]

# 📊 텍스트 추가: 각 막대 위에 '총 개수' 노출
for idx, total_val in bottom_data.items():
    if total_val > 0: 
        plt.text(x=idx, 
                 y=total_val + (bottom_data.max() * 0.01), 
                 s=f'{int(total_val):,}', 
                 ha='center', 
                 va='bottom', 
                 fontsize=10, 
                 weight='bold')

# 그래프 디테일 설정
plt.title('날짜 구간별 세부 카테고리별 실제 기사 발행량 추이 (30개 구간 축약)', fontsize=16, pad=20)
plt.xlabel('날짜 구간 (시작일)', fontsize=12)
plt.ylabel('기사 발행 건수 (건)', fontsize=12)
plt.xticks(rotation=45, ha='right')

plt.grid(axis='y', linestyle='--', alpha=0.5)

# 범례가 많을 테니 2열(ncol=2)로 나누어 깔끔하게 정렬
plt.legend(title="통합 분류1 (전체)", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9, ncol=2)

# Y축 상단 글자 잘림 방지 여유 공간
plt.ylim(0, bottom_data.max() * 1.1)

plt.tight_layout()
plt.show()