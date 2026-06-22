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
# 3. Matplotlib + Seaborn 시각화 (실제 기사 건수 기준)
# ====================================================
plt.figure(figsize=(16, 9))

# 1️⃣ 세부 카테고리명에서 '대분류' 추출 후, 고유한 대분류 리스트 생성
# 예: '사회_복지', '사회_노동' -> '사회' 추출 (구분자가 다르면 '_'를 변경하세요)
macro_df = compressed_df.copy()
macro_names = list(dict.fromkeys(col.split('-')[0] for col in compressed_df.columns))

# 2. 대괄호([]) 인덱싱과 sum을 활용해 한 줄로 합산 처리!
# 각 대분류로 시작하는 컬럼들만 compressed_df[...]로 쏙 골라내서 더해줍니다.
macro_df = pd.DataFrame({
    macro: compressed_df[[col for col in compressed_df.columns if col.startswith(f"{macro}-")]].sum(axis=1)
    for macro in macro_names
})

print(macro_names, macro_df)


# [정렬] 발행량이 많은 대분류 순서대로 컬럼 정렬 (시각적으로 안정감을 줍니다)
all_macro_categories = macro_df.sum().sort_values(ascending=False).index.tolist()
df_visual = macro_df[all_macro_categories].copy()

# ====================================================
# 2️⃣ 대분류 통합 시각화 (단색 처리 & 총 건수 노출)
# ====================================================
plt.figure(figsize=(16, 9))

# 누적 막대그래프용 바닥 정보 초기화
bottom_data = pd.Series(0, index=df_visual.index)

# 🎨 [단색 구분] Matplotlib 기본 제공 10색(tab10) 사용
# 그라데이션이 전혀 없는 뚜렷한 독립된 원색/단색 계열입니다.
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 대분류를 하나씩 쌓아 올립니다.
for i, category in enumerate(all_macro_categories):
    current_color = colors[i % len(colors)]
    
    # 💡 edgecolor와 linewidth를 주어 동일 막대 안에서도 단색 블록 간 경계를 명확히 분리합니다.
    plt.bar(df_visual.index, df_visual[category], 
            bottom=bottom_data, label=category, color=current_color, 
            width=0.6, edgecolor='white', linewidth=0.8)
    
    bottom_data += df_visual[category]

# 📊 [막대 위 총 기사 건수 노출]
# 최종 합산된 bottom_data 값을 활용하여 막대 꼭대기에 숫자를 넣습니다.
for idx, total_val in bottom_data.items():
    if total_val > 0:  # 0건인 날짜 구간은 텍스트 표시 생략
        plt.text(x=idx, 
                 y=total_val + (bottom_data.max() * 0.01),  # 막대 윗부분 여백
                 s=f'{int(total_val):,}',                    # 천단위 콤마 표기 (예: 1,234)
                 ha='center', 
                 va='bottom', 
                 fontsize=11, 
                 weight='bold',
                 color='black')

# 그래프 스타일 설정
plt.title('날짜 구간별 대분류 통합 실제 기사 발행량 추이', fontsize=16, pad=20, weight='bold')
plt.xlabel('날짜 구간 (시작일)', fontsize=12)
plt.ylabel('총 기사 발행 건수 (건)', fontsize=12)

# X축 라벨 45도 회전 및 우측 정렬
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)

# Y축에만 투명도 있는 그리드 추가
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 💡 대분류만 존재하므로 범례를 깔끔하게 우측 상단에 1열로 배치
plt.legend(title="대분류", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=11, title_fontsize=12)

# Y축 상단 여유 공간 확보 (수치가 그래프 테두리에 잘리지 않도록 함)
plt.ylim(0, bottom_data.max() * 1.12)

plt.tight_layout()
plt.show()



