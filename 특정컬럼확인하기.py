"""
=========================================
[시각화 관점] 통합 분류1(카테고리) 뉴스 비중 분석
- 상위 10개 카테고리 추출 및 데이터 검증
=========================================
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

file_path = './원본/한국언론진흥재단_뉴스빅데이터_메타데이터_노인_20011231.csv'  # 파일명을 여기에 적어주세요.


df = pd.read_csv(file_path, encoding='cp949')

# 1. '통합 분류1' 컬럼의 빈도수를 계산하여 시리즈 생성
category_counts = df["통합 분류1"].value_counts().head(10)  # 상위 10개 카테고리만 추출

# 2. ★반드시 콘솔에 시리즈 구조와 데이터 확인
print("=== [콘솔 확인] 통합 분류1  카테고리 시리즈 ===")
print(category_counts)
print("데이터 타입:", type(category_counts))
print("====================================================\n")