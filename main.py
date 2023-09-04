import streamlit as st
from Utils import util
from Utils.sim_data import SimData
from constant import *

# test_code = '''0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123'''

if __name__ == '__main__':
    st.title('SIM Data Decoder')

    # 1. SIM Data 입력
    st.subheader('1. SIM Data 입력')
    test_code = st.text_area(":red[0x를 제외한 500자 Hex Code] 를 입력하세요", placeholder='0x를 제외한 500자 Hex Code를 입력하세요', height=200)
    list_test_code = []

    if st.button('Code 확인', type="primary"):
        if not util.isCorrectLength(test_code, CODE_LENGTH) or not util.isHex(test_code):
            if not util.isCorrectLength(test_code, CODE_LENGTH) :
                st.warning(f'''코드 길이가 :red[{CODE_LENGTH}자]가 아닙니다. (:red[{len(test_code)} 자])''', icon="⚠️")
            if not util.isHex(test_code):
                st.warning('코드가 :red[Hex Code]가 아닙니다.', icon="⚠️")
            # exit(0)
        # elif not util.isHex(test_code):
        #     st.warning('코드가 :red[Hex Code]가 아닙니다.', icon="⚠️")
            # exit(0)
        else:
            st.success('코드가 정상입니다.', icon="👍")
            # st.balloons()
            # Todo : split_code_to_datalist 로 변경 필요
            # Todo : 그런데 코드 구분이 정해진 숫자일지??? (담당자 확인 필요)
            list_test_code = util.split10(test_code)

            sim_data = SimData(list_test_code)
            print(sim_data.code0)
            print(sim_data.code1)
            print(sim_data.code2)
            print(sim_data.code3)

            # 2. SIM Data 출력
            st.subheader('2. SIM Data 출력')
            st.write(list_test_code)

    test_code_2 = '''0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'''

    split_list = SimData.split_code_to_data_list(code=test_code_2, split_length_list=CODE_DIVISION_LENGTH_LIST)

    for i, split in enumerate(split_list, start=1):
        print(f"{i}: {split}")

    test_data = SimData(split_list)
    print(test_data.code0)
    print(test_data.code1)
    print(test_data.code2)
    print(test_data.code3)

    # Todo : 각 구분된 코드 별로 디코딩 하기
