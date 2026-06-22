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

base_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
color_map = {macro: base_colors[i % len(base_colors)] for i, macro in enumerate(macro_names)}

# 범례 중복 표시를 방지하기 위해 기록용 셋(set) 생성
added_labels = set()

# 날짜 구간별로 누적 바닥(bottom)을 관리할 시리즈 (초기값 0)
bottom_data = pd.Series(0, index=macro_df.index)

# 💡 핵심: 데이터프레임의 모든 열을 한 번에 그리지 않고, 
# 각 날짜(행)별로 '값이 큰 순서대로' 정렬하여 밑바닥부터 쌓아 올립니다.
for date_idx in macro_df.index:
    # 현재 날짜의 대분류 데이터만 가져와서 내림차순(큰 값 -> 작은 값) 정렬
    row_sorted = macro_df.loc[date_idx].sort_values(ascending=False)
    
    current_bottom = 0
    for macro, val in row_sorted.items():
        if val <= 0:
            continue
            
        # 처음 등장하는 대분류만 범례(label)에 등록하고, 이후에는 범례 중복 방지
        label_to_use = macro if macro not in added_labels else ""
        if label_to_use:
            added_labels.add(macro)
            
        # 각 날짜(date_idx) 위치에 해당하는 조각 막대 하나만 그리기
        plt.bar(date_idx, val, bottom=current_bottom, 
                label=label_to_use, color=color_map[macro], 
                width=0.6, edgecolor='white', linewidth=0.8)
        
        # 바닥 높이를 현재 값만큼 누적
        current_bottom += val
        
    # 전체 막대 위 총합 수치 기록을 위해 최종 위치 저장
    bottom_data[date_idx] = current_bottom

# 📊 [막대 위 총 기사 건수 노출]
for idx, total_val in bottom_data.items():
    if total_val > 0: 
        plt.text(x=idx, 
                 y=total_val + (bottom_data.max() * 0.01), 
                 s=f'{int(total_val):,}', 
                 ha='center', 
                 va='bottom', 
                 fontsize=11, 
                 weight='bold',
                 color='black')

# 그래프 스타일 설정
plt.title('날짜 구간별 대분류 통합 실제 기사 발행량 추이 (큰 비중이 아래로 배정)', fontsize=16, pad=20, weight='bold')
plt.xlabel('날짜 구간 (시작일)', fontsize=12)
plt.ylabel('총 기사 발행 건수 (건)', fontsize=12)

plt.xticks(rotation=45, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# 💡 범례 표시 (color_map 순서대로 깔끔하게 노출되도록 핸들 정렬)
handles, labels = plt.gca().get_legend_handles_labels()
# 범례에서 빈 텍스트 제거 및 정렬
by_label = dict(zip(labels, handles))
if "" in by_label: del by_label[""]
plt.legend(by_label.values(), by_label.keys(), title="대분류", bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=11, title_fontsize=12)

# Y축 상단 여유 공간 확보
plt.ylim(0, bottom_data.max() * 1.12)

plt.tight_layout()
plt.show()