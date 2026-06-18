"""
=========================================
[시각화 관점] 주요 언론사별 뉴스 발행량 TOP 10
- 상위 10개 언론사만 추출하여 범례 상징화
=========================================
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv'  # 파일명을 여기에 적어주세요.


df = pd.read_csv(file_path, encoding='cp949')

# 1. 시각화를 위한 시리즈(Series) 생성 + TOP 10 제한
# value_counts()는 기본적으로 내림차순 정렬되므로, .head(10)을 붙이면 상위 10개만 남습니다.
media_counts_top10 = df["언론사"].value_counts().head(10)

# 2. 반드시 콘솔에 상위 10개 시리즈 구조와 데이터 확인
print("=== [콘솔 확인] TOP 10 언론사별 뉴스 발행량 시리즈 ===")
print(media_counts_top10)
print("개수:", len(media_counts_top10))
print("==================================================\n")


# 3. 한글 폰트 및 마이너스 깨짐 설정
plt.rcParams["font.family"] = "Malgun Gothic"  # Mac은 'AppleGothic'
plt.rcParams["axes.unicode_minus"] = False

# 4. 그래픽 도화지 준비
plt.figure(figsize=(12, 6))  # 10개를 보여줘야 하므로 가로를 살짝 넓혔습니다.

# 5. 바 차트 그리기 (상위 10개 데이터만 투입)
ax = sns.barplot(
    x=media_counts_top10.index,
    y=media_counts_top10.values,
    hue=media_counts_top10.index,
    palette="Set2",
    legend=True,
)

# 6. X축의 텍스트 레이블을 제거하여 범례로 시선 집중시키기
ax.set_xticklabels([])
plt.xlabel("언론사 고유 색상 (우측 범례 참조)", fontsize=11, labelpad=10)
plt.ylabel("뉴스 발행 건수 (건)", fontsize=12, labelpad=10)

# 7. 차트 제목 설정
plt.title(
    "주요 언론사별 뉴스 발행량 순위 TOP 10", fontsize=16, fontweight="bold", pad=20
)

# 8. 막대 위에 데이터 값(숫자) 표시
for i, value in enumerate(media_counts_top10.values):
    plt.text(i, value + 0.1, str(value), ha="center", va="bottom", fontsize=11)

# 9. 범례(Legend) 위치 및 스타일 조정
plt.legend(
    title="언론사 TOP 10",
    loc="upper right",
    bbox_to_anchor=(1.20, 1),  # 범례가 그래프와 겹치지 않게 살짝 오른쪽으로 이동
    frameon=True,
    shadow=True,
)

# 그래프 출력
plt.tight_layout()
plt.show()