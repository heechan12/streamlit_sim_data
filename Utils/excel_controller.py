from typing import final

import pandas as pd
from Utils.util import *
from constant import FIRST_APDU_COMMAND, SECOND_APDU_COMMAND, THIRD_APDU_COMMAND

# 엑셀 파일 경로 지정
file_path = '/Users/yangheechan/PycharmProjects/pythonProject/sim_test/test_file/test_file_1.xlsx'

# 엑셀 파일을 읽고 두 번째 시트를 데이터프레임으로 로드
df = pd.read_excel(file_path, sheet_name=1)  # sheet_name=1은 두 번째 시트를 의미합니다.

# 모든 셀에서 스페이스 제거
df = df.applymap(lambda x: str(x).replace(' ', '') if pd.notnull(x) else x)

# H4:J103 범위의 값을 추출
data = df.iloc[2:102, 7:10].astype(str).values  # 값을 문자열로 변환

# 3글자가 아닌 값에 'F'를 붙여서 3글자로 만듦
formatted_data = [[cell.ljust(3, 'F') if cell != 'nan' else 'nan' for cell in row] for row in data]

print("formatted_data : ")
print(formatted_data)

# NaN 값을 조건에 맞게 변경
for row in formatted_data:
    for idx, cell in enumerate(row):
        if cell == 'nan':
            if idx == 2:  # 세 번째 열의 NaN 값
                row[idx] = 'AAAA'
            else:  # 첫 번째와 두 번째 열의 NaN 값
                row[idx] = 'AAA'

# 각 행을 10개의 열로 분리
expanded_data = [list(''.join(row)) for row in formatted_data]

# 열 순서를 바꿀 인덱스 지정 (0-based index)
new_column_order = [1, 0, 5, 2, 4, 3]  # 새로운 열 순서

# 각 행의 열 순서를 재배치하고, 7~10번째 열은 그대로 유지
reordered_data = [
    [row[i] for i in new_column_order] + row[6:] for row in expanded_data
]

# 각 행의 열 값을 하나의 문자열로 합침
combined_data = [''.join(row) for row in reordered_data]

# 1부터 50행까지를 하나의 문자열로 결합
first_combined = ''.join(combined_data[:50])

# 51부터 100행까지를 하나의 문자열로 결합
second_combined = ''.join(combined_data[50:])

version = decimal_to_hex(10088)
final_code = FIRST_APDU_COMMAND + first_combined + SECOND_APDU_COMMAND + second_combined + THIRD_APDU_COMMAND + version

print(final_code)