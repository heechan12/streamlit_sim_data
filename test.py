import streamlit as st
import pandas as pd

FIRST_APDU_COMMAND = 'AA82022CA20900A4080C047FFF6F61A281FF00D60000FA'
SECOND_APDU_COMMAND = 'A20900A4080C047FFF6F61A281FF00D600FAFA'
THIRD_APDU_COMMAND = 'A20700A4080C022F30A20700D6000502'

def decimal_to_hex(decimal_number):
    return hex(decimal_number)[2:]

def process_excel(file, version):
    # 엑셀 파일을 읽고 두 번째 시트를 데이터프레임으로 로드
    df = pd.read_excel(file, sheet_name=1)  # sheet_name=1은 두 번째 시트를 의미합니다.

    # 모든 셀에서 스페이스 제거
    df = df.applymap(lambda x: str(x).replace(' ', '') if pd.notnull(x) else x)

    # H4:J103 범위의 값을 추출
    data = df.iloc[2:102, 7:10].astype(str).values  # 값을 문자열로 변환

    # 3글자가 아닌 값에 'F'를 붙여서 3글자로 만듦
    formatted_data = [[cell.ljust(3, 'F') if cell != 'nan' else 'nan' for cell in row] for row in data]

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

    version_hex = decimal_to_hex(version)
    final_code = FIRST_APDU_COMMAND + first_combined + SECOND_APDU_COMMAND + second_combined + THIRD_APDU_COMMAND + version_hex

    return final_code

def main():
    st.title("국가정보 업데이트")

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
    version = st.number_input("Enter Version (as an integer)", min_value=0, value=10088)

    if uploaded_file is not None:
        final_code = process_excel(uploaded_file, version)
        st.text_area("Final Code", final_code)

if __name__ == "__main__":
    main()
