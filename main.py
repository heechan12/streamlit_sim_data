import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

from Utils.utils import read_excel_as_pandas, generate_update_code, get_final_result_code
from constant import ERROR_EXCEL_VALUE, ERROR_EXCEL_FILE, ERROR_VERSION_VALUE, TITLE, APP_VERSION

st.set_page_config(layout="wide")

def main():
    st.title(TITLE + " " + str(APP_VERSION))
    st.container(height=30, border=False)
    col1, col2, col3 = st.columns([1, 1, 0.5], gap="large")

    with col1:
        st.subheader("_엑셀 파일(.xlsx) 추가_", divider="gray")
        uploaded_file = st.file_uploader(".xlsx 파일만 선택 가능합니다", type="xlsx", label_visibility="collapsed")

    with col2:
        st.subheader("_버전 입력_", divider="gray")
        version = st.number_input("숫자만 입력 가능합니다", min_value=1, value=1, label_visibility="collapsed")

    with col3 :
        st.subheader("_코드 생성_", divider="gray")
        generate_button = st.button("코드 생성")


    if uploaded_file is not None and generate_button:
        st.divider()
        st.subheader(":red[_결과_]", divider="red")

        if isinstance(version, int) and version > 0:
            excel_pd_file = read_excel_as_pandas(uploaded_file)

            if excel_pd_file is not None :
                usim_code, esim_code = generate_update_code(excel_pd_file)

                """
                정상 성공 후 결과 화면
                """
                with st.container(border=True):
                    st.toast("👍🏻 코드 생성에 성공하였습니다.")
                    if usim_code != 'invalid' :
                        usim_result_code = get_final_result_code(usim_code, version)
                        st.markdown(":orange-background[:red[*USIM Code*]]")
                        st.text_area(label="USIM 코드", value=usim_result_code, height=300, label_visibility="collapsed")
                        st.write(f"총 글자 수 : {len(usim_result_code)}")
                        # st_copy_to_clipboard(text = usim_result_code, before_copy_label="클립보드에 복사하기")

                    else :
                        st.error(ERROR_EXCEL_VALUE)

                with st.container(border=True):
                    if esim_code != 'invalid' :
                        esim_result_code = get_final_result_code(esim_code, version)
                        st.markdown(":orange-background[:red[*ESIM Code*]]")
                        st.text_area(label="ESIM 코드", value=esim_result_code, height=300, label_visibility="collapsed")
                        st.write(f"총 글자 수 : {len(esim_result_code)}")
                        # st_copy_to_clipboard(text=esim_result_code, before_copy_label="클립보드에 복사하기")

                    else :
                        st.error(ERROR_EXCEL_VALUE)
            else :
                st.error(ERROR_EXCEL_FILE)


        else:
            st.error(ERROR_VERSION_VALUE)


if __name__ == "__main__":
    main()
