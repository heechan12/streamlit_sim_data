import streamlit as st
import pandas as pd
from Utils.utils import read_excel_as_pandas, edit_excel_data, get_result_code
from constant import FIRST_APDU_COMMAND, SECOND_APDU_COMMAND, THIRD_APDU_COMMAND

st.set_page_config(layout="wide")

FIRST_APDU_COMMAND = 'AA82022CA20900A4080C047FFF6F61A281FF00D60000FA'
SECOND_APDU_COMMAND = 'A20900A4080C047FFF6F61A281FF00D600FAFA'
THIRD_APDU_COMMAND = 'A20700A4080C022F30A20700D6000502'

def decimal_to_hex(decimal_number):
    return hex(decimal_number)[2:]

def read_excel_as_pandas(file) -> pd :
    """
    전달받은 엑셀의 2번째 시트 내용을 전달

    :param file : xlsx 파일
    :return: pandas
    """
    try :
        excel_file = pd.read_excel(file, sheet_name=1)
        return excel_file
    except :
        print("파일을 읽을 수 없습니다")
        return

def is_valid_sheet(excel_file: pd.DataFrame) -> bool :
    """
    엑셀 내 시트가 국가 정보 업데이트를 할 수 있는 템플릿의 시트인지 확인

    :param excel_file:
    :return: bool
    """
    df = excel_file

    if df is not None :
        d4_value = df.iloc[2, 3]
        d103_value = df.iloc[101, 3]
        h3_value = df.iloc[1, 7]
        i3_value = df.iloc[1, 8]
        j3_value = df.iloc[1, 9]
    else :
        d4_value = "None"
        d103_value = "None"
        h3_value = "None"
        i3_value = "None"
        j3_value = "None"

    if d4_value == 1 and d103_value == 100 and h3_value == "MCC" and i3_value == "MNC" and j3_value == "AcT":
        return True
    else:
        return False

def edit_excel_data(excel_file: pd) -> str :
    """
    엑셀 내 시트의 데이터로 국가정보 업데이트 로직 수행
    버전 코드는 없음

    :param excel_file:
    :return:
    """
    df = excel_file

    if is_valid_sheet(df) :
        print("valid excel and sheet")

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

        edited_code = FIRST_APDU_COMMAND + first_combined + SECOND_APDU_COMMAND + second_combined + THIRD_APDU_COMMAND

        return edited_code

    else :
        print("invalid excel and sheet")

        return 'invalid'

    # 모든 셀에서 스페이스 제거
def get_result_code(code:str, version) -> str :
    """
    국가 정보 업데이트를 위한 코드에 최종 버전 코드 추가

    :param code:
    :param version:
    :return: 최종 코드
    """
    version_hex = decimal_to_hex(version)

    if code is not None :
        result_code = code + version_hex
        return result_code

    return '오류'


def main():
    st.title("국가정보 업데이트_v0.2")

    uploaded_file = st.file_uploader("엑셀 파일(.xlsx) 추가", type="xlsx")
    version = st.number_input("버전 정보(숫자) 입력", min_value=1, value=1)
    generate_button = st.button("코드 생성")

    if uploaded_file is not None and generate_button:
        if isinstance(version, int) and version > 0:
            excel_pd_file = read_excel_as_pandas(uploaded_file)

            if excel_pd_file is not None :
                code = edit_excel_data(excel_pd_file)
                if code != 'invalid' :
                    result_code = get_result_code(code, version)

                    st.text_area(label="최종 코드", value=result_code, height=300)
                    st.write(f"총 글자 수 : {len(result_code)}")
                else :
                    st.error("엑셀 파일 내 값에 오류가 있습니다.")
            else :
                st.error("엑셀 파일에 오류가 있습니다.")


        else:
            st.error("버전이 올바르지 않습니다.")


if __name__ == "__main__":
    main()
