import streamlit as st
from Utils import util
from Utils.sim_data import SimData
from constant import *

# test_code_2
test_code = util.get_random_hex(CODE_LENGTH)
print(test_code)

# 전역 변수 라인
# 향후 SIM Data 가 변경되었을 때 비교를 위해
if 'OLD_SIM_DATA' not in st.session_state:
    st.session_state.OLD_SIM_DATA = None

if 'NEW_SIM_DATA' not in st.session_state:
    st.session_state.NEW_SIM_DATA = None

# Session 1 처리 확인 용도
if 'is_session_1_done' not in st.session_state:
    st.session_state.is_session_1_done = False

# Session 2 처리 확인 용도
if 'is_session_2_done' not in st.session_state:
    st.session_state.is_session_2_done = False


if __name__ == '__main__':

    st.title('SIM Data update tool? 📱')

    # 1. SIM Data 입력
    st.header('1. 기존 SIM Data 입력')
    input_old_code = st.text_area(label=":red[0x를 제외한 500자 Hex Code] 를 입력하세요",
                                  placeholder='0x를 제외한 500자 Hex Code를 입력하세요',
                                  height=200)
    # 띄어쓰기, 개행문자 제거
    input_old_code = input_old_code.replace(" ", "").replace("\n", "")

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
            st.toast('다음 단계로 넘어갑니다!', icon="👍")
            st.session_state.is_session_1_done = True  # Session 1 확인
            # Todo : split_code_to_data_list 로 변경 필요
            # Todo : 그런데 코드 구분이 정해진 숫자일지??? (담당자 확인 필요)
            list_test_code = util.split10(input_old_code)

            st.session_state.OLD_SIM_DATA = SimData(list_test_code)
            st.session_state.NEW_SIM_DATA = SimData(list_test_code)

    # 2. SIM Data 출력
    # 1번 세션에서 Code 확인 버튼을 눌렀을 때만 출력
    if st.session_state.is_session_1_done is True:
        st.header('2. 기존 정보 및 업데이트')

    # Todo : Hex -> 무언가의 데이터로의 전환이 필요

    # 데이터 전환 이후 처리하는 부분
    if st.session_state.NEW_SIM_DATA is not None:
        st.sidebar.subheader('기존 정보')
        st.sidebar.write('이곳에는 디코딩 된 Input Code 값을 출력할 예정')
        st.sidebar.write(st.session_state.OLD_SIM_DATA.list)

        mcc = st.text_input(label="MCC", value=st.session_state.NEW_SIM_DATA.code0[:3], max_chars=3,
                            on_change=None)
        mnc = st.text_input(label="MNC", value=st.session_state.NEW_SIM_DATA.code1[:3], max_chars=3,
                            on_change=None)

        if st.button('업데이트 정보 입력', type="primary"):
            st.toast('값이 업데이트 되었습니다!', icon="🎉")
            st.toast('다음 단계로 넘어갑니다!', icon="👍")
            st.write(f"mcc : {mcc}")
            st.write(f"mnc : {mnc}")

            st.session_state.is_session_2_done = True  # Session 2 확인

    # Session 3
    # 최종 수정된 데이터 확인 및 출력
    if st.session_state.is_session_2_done is True:
        st.header('3. 변경된 정보 확인')

    # # 탭 방식
    # tab1, tab2 = st.tabs(['기존 정보', '업데이트 정보 입력'])
    # tab1.write(list_test_code)
    #
    # # 1번 세션에서 Code 확인 버튼을 눌렀을 때만 출력
    # if SIM_DATA is not None:
    #     mcc = tab2.text_input(label="MCC", value=SIM_DATA.code0, max_chars=3)
    #     mnc = tab2.text_input(label="MNC", value=SIM_DATA.code1, max_chars=3)
    #     print("mcc : " + mcc)
    #     print("mnc : " + mnc)

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
