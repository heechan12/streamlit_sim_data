import streamlit as st
from Utils.utils import read_excel_as_pandas, edit_excel_data, get_result_code

st.set_page_config(layout="wide")

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
            st.error("Please enter a valid version number.")


if __name__ == "__main__":
    main()
