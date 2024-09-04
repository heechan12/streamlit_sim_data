import streamlit as st
from streamlit import divider

from Utils.utils import read_excel_as_pandas, generate_update_code, get_final_result_code

st.set_page_config(layout="wide")

def main():
    st.title("국가정보 업데이트 v0.3")
    st.container(height=30, border=False)
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("_엑셀 파일(.xlsx) 추가_", divider="gray")
        uploaded_file = st.file_uploader(".xlsx 파일만 선택 가능합니다", type="xlsx", label_visibility="collapsed")

    with col2:
        st.subheader("_버전 입력_", divider="gray")
        version = st.number_input("숫자만 입력 가능합니다", min_value=1, value=1, label_visibility="collapsed")


    generate_button = st.button("코드 생성")


    if uploaded_file is not None and generate_button:
        st.divider()
        st.subheader(":red[_결과_]", divider="red")

        if isinstance(version, int) and version > 0:
            excel_pd_file = read_excel_as_pandas(uploaded_file)

            if excel_pd_file is not None :
                usim_code, esim_code = generate_update_code(excel_pd_file)
                with st.container(border=True):
                    if usim_code != 'invalid' :
                        usim_result_code = get_final_result_code(usim_code, version)
                        st.markdown(":orange-background[:red[*USIM Code*]]")
                        st.text_area(label="USIM 코드", value=usim_result_code, height=300, label_visibility="collapsed")
                        st.write(f"총 글자 수 : {len(usim_result_code)}")

                    else :
                        st.error("엑셀 파일 내 값에 오류가 있습니다.")

                with st.container(border=True):
                    if esim_code != 'invalid' :
                        esim_result_code = get_final_result_code(esim_code, version)
                        st.markdown(":orange-background[:red[*ESIM Code*]]")
                        st.text_area(label="ESIM 코드", value=esim_result_code, height=300, label_visibility="collapsed")
                        st.write(f"총 글자 수 : {len(esim_result_code)}")

                    else :
                        st.error("엑셀 파일 내 값에 오류가 있습니다.")
            else :
                st.error("엑셀 파일에 오류가 있습니다.")


        else:
            st.error("버전이 올바르지 않습니다.")


if __name__ == "__main__":
    main()
