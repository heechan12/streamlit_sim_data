import streamlit as st
from Utils import util
from Utils.sim_data import SimData
from constant import *

# test_code = '''0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123'''

if __name__ == '__main__':

    st.title('PLMN update tool')

    # 1. SIM Data 입력
    st.header('1. 기존 SIM Data 입력')
    input_old_code = st.text_area(label=":red[0x를 제외한 500자 Hex Code] 를 입력하세요",
                                  placeholder='0x를 제외한 500자 Hex Code를 입력하세요',
                                  height=200)
    list_test_code = []

    if st.button('Code 확인', type="primary"):
        if not util.isCorrectLength(input_old_code, CODE_LENGTH) or not util.isHex(input_old_code):
            if not util.isCorrectLength(input_old_code, CODE_LENGTH):
                st.warning(f'''코드 길이가 :red[{CODE_LENGTH}자]가 아닙니다. (:red[{len(input_old_code)} 자])''', icon="⚠️")
            if not util.isHex(input_old_code):
                st.warning('코드가 :red[Hex Code]가 아닙니다.', icon="⚠️")
        else:
            st.success('코드가 정상입니다.', icon="👍")
            old_code = input_old_code
            # st.balloons()
            # Todo : split_code_to_data_list 로 변경 필요
            # Todo : 그런데 코드 구분이 정해진 숫자일지??? (담당자 확인 필요)
            list_test_code = util.split10(input_old_code)

            # sim_data = SimData(list_test_code)
            # print(sim_data.code0)
            # print(sim_data.code1)
            # print(sim_data.code2)
            # print(sim_data.code3)

    # 2. SIM Data 출력
    st.header('2. 기존 정보 및 업데이트')
    tab1, tab2 = st.tabs(['기존 정보', '업데이트 정보 입력'])
    tab1.write(list_test_code)

    mcc = tab2.text_input(label="MCC", value="123", max_chars=3)
    mnc = tab2.text_input(label="MNC", value="456", max_chars=3)
    print("mcc : " + mcc)
    print("mnc : " + mnc)
    # col1, col2 = st.columns(2)
    # col1.subheader('기존 정보')
    # col1.write(list_test_code)
    #
    # col2.subheader('업데이트 정보 입력')
    # # col2_1, col2_2 = col2.columns(2)
    # # col2_1.write('col2_1')
    # # col2_2.write('col2_2')
    #
    # with col2.container():
    #     col2.write('This is inside a container')
    #     col2_1, col2_2 = col2.columns(2)
    #     col2_1.text('MCC')
    #     col2_2.text_input(label="MCC", value="123", max_chars=3)
    #
    # with col2.container():
    #     col2.write('This is inside a container')
    #     col2_1, col2_2 = col2.columns(2)
    #     col2_1.text('MCC')
    #     col2_2.text_input(label="MCC", value="123", max_chars=3)

    # st.write(list_test_code)

    # test_code_2 = '''0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'''
    #
    # split_list = SimData.split_code_to_data_list(code=test_code_2, split_length_list=CODE_DIVISION_LENGTH_LIST)
    #
    # for i, split in enumerate(split_list, start=1):
    #     print(f"{i}: {split}")
    #
    # test_data = SimData(split_list)
    # print(test_data.code0)
    # print(test_data.code1)
    # print(test_data.code2)
    # print(test_data.code3)

    # Todo : 각 구분된 코드 별로 디코딩 하기
