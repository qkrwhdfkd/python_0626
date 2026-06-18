import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv'  # 파일명을 여기에 적어주세요.


df = pd.read_csv(file_path, encoding='cp949')



# 🛠️ 통합 분류 집계 시각화


plt.rcParams["font.family"] = "Malgun Gothic"  
plt.rcParams["axes.unicode_minus"] = False  


##### 여기서 부터 커스터마이징 #####

'''
LLM 프롬프트 명령어
  범례를 추가해서 x축 뭐라하지???? 막대명칭???? 상징화하기
  -> 사용자의 의도 가독성을 높이기 위한  범례로 막대 명칭 상징화하기
'''

"""
=========================================
[시각화 관점] 언론사별 뉴스 발행량 비교
- X축 글자를 지우고 범례(Legend)로 상징화
=========================================
"""

# 1. 언론사별 뉴스 발행량 시리즈 생성
media_counts = df["언론사"].value_counts()

# 2. 반드시 콘솔에 시리즈 구조와 데이터 확인
print("=== [콘솔 확인] 언론사별 뉴스 발행량 시리즈 ===")
print(media_counts)
print("Type:", type(media_counts))
print("============================================\n")

# 3. 그래픽 도화지 준비
plt.figure(figsize=(10, 6))

# 3. 바 차트 그리기 (hue를 '언론사'로 지정하여 색상 다채롭게 + 범례 활성화)
# legend=True를 명시하고, 각 막대를 상징할 색상 팔레트(set2, pastel 등)를 씁니다.
ax = sns.barplot(
    x=media_counts.index,
    y=media_counts.values,
    hue=media_counts.index,
    palette="Set2",
    legend=True,
)

# 4. ★핵심: X축의 텍스트 레이블을 제거하여 범례로 시선 집중시키기
ax.set_xticklabels([])  # X축 막대 밑의 글자를 숨김
plt.xlabel("언론사 고유 색상 (범례 참조)", fontsize=11, labelpad=10)
plt.ylabel("뉴스 발행 건수 (건)", fontsize=12, labelpad=10)

# 5. 차트 제목 설정
plt.title(
    "주요 언론사별 뉴스 발행량 비교 (상징화 패턴)",
    fontsize=16,
    fontweight="bold",
    pad=20,
)

# 6. 막대 위에 데이터 값(숫자) 표시
for i, value in enumerate(media_counts.values):
    plt.text(i, value + 0.1, str(value), ha="center", va="bottom", fontsize=11)

# 7. 범례(Legend) 위치 및 스타일 이쁘게 다듬기
plt.legend(
    title="언론사 명칭",
    loc="upper right",
    bbox_to_anchor=(1.15, 1),
    frameon=True,
    shadow=True,
)

# 그래프 출력
plt.tight_layout()
plt.show()
