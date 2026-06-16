import pandas as pd

# CSV 파일 경로 지정

# 이것은 판다스(pandas)가 CSV 파일을 기본값인 UTF-8 방식으로 읽으려고 시도했으나, 
# 파일 안에 한글(텍스트) 인코딩 방식(주로 엑셀의 CP949)이 달라서 파일을 해석못해 발생한 대표적인 오류

# 기존 코드: df = pd.read_csv(file_path)
# 변경 코드: 뒤에 encoding='cp949'를 추가

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv'  # 파일명을 여기에 적어주세요.

# CSV 파일을 읽어서 데이터프레임으로 변환
df = pd.read_csv(file_path, encoding='cp949')

# 상위 5개 데이터 확인
print(df.head())

df.info()

# 🛠️ 지역별 기사 개수 추출 및 시각화 코드

import matplotlib.pyplot as plt


# 1. 한글 폰트 설정 (그래프에서 한글 깨짐 방지)
plt.rcParams["font.family"] = "Malgun Gothic"  # 윈도우 기본 맑은 고딕
plt.rcParams["axes.unicode_minus"] = False  # 마이너스 부호 깨짐 방지
# 그래프에 마이너스 기호( - )가 네모 상자(□)나 깨진 글자로 나오는 현상을 막아주는 설정




# 3. '통합 분류1'에서 지역 정보 분리 및 필터링
# 결측치(빈 칸) 제거 후, 하이픈(-)을 기준으로 대분류와 소분류를 분리합니다.
df = df.dropna(subset=["통합 분류1"]) 
# 가변인자 지우면 첫번째 인자로 오해, subset(부분집합의 뜻)은 특정 열을 기준으로 결측치를 제거하는 옵션입니다.
# 통합분류에 결측치가 있는 경우 해당 행 전체를 제거하겠다는 의미입니다.

df["대분류"] = df["통합 분류1"].apply(lambda x: x.split("-")[0].strip())
df["세부지역"] = df["통합 분류1"].apply(
    lambda x: x.split("-")[1].strip() if "-" in x else "기타"
)

# [ 기존 df ] 
# 일자       | 언론사   | 통합 분류1  | 제목
# 06-16    | 중도일보 | 지역-강원   | 민원 일회 방문...

# 👇 코드 실행 후 (새로운 컬럼 2개가 우측에 붙음)

# [ 새로운 df ]
# 일자       | 언론사   | 통합 분류1  | 제목            | 대분류  | 세부지역
# 06-16    | 중도일보 | 지역-강원   | 민원 일회 방문... | 지역   | 강원

# 대분류가 '지역'인 데이터만 골라냅니다.
region_df = df[df["대분류"] == "지역"]
# df에서 '대분류'가 '지역'인 행(Row)들을 통째로 가져와서 저장하는 것

# 4. 지역별 기사 개수 추출 (집계)
region_counts = region_df["세부지역"].value_counts()
# region_counts는 데이터프레임이 아니라 시리즈(Series)입니다.
# 세부지역 컬럼만 추출해서 각 지역별로 몇 건의 기사가 있는지 세어서 저장하는 것
# 키와 값을 구분해서 저장하는 형태로, 예를 들어 '강원': 10, '서울': 15 이런 식으로 저장됩니다.
# 리스트보다는 딕션너리와 유사한 형태입니다.

print("=== 지역별 기사 개수 ===")
print(region_counts)

# 5. 시각화 (막대그래프)
plt.figure(figsize=(10, 6))
region_counts.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title("지역별 노인 관련 기사 개수", fontsize=16, fontweight="bold", pad=15)
plt.xlabel("지역", fontsize=12)
plt.ylabel("기사 개수 (건)", fontsize=12)
plt.xticks(rotation=45)  # 글자가 겹치지 않도록 회전
plt.grid(axis="y", linestyle="--", alpha=0.7)  # y축 기준 점선 배경

# 그래프 상단에 숫자(건수) 표시하기
for i, v in enumerate(region_counts):
    plt.text(i, v + 0.1, str(v), ha="center", va="bottom", fontsize=10)

#plt.tight_layout()  # 여백 조정
plt.show()




