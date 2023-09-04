def isCorrectLength(code, length) -> bool:
    '''
    입력 받은 code 의 글자 수가 500자 인지 아닌지를 반환하는 함수
    :param code: String
    :param length: int
    :return: true or false
    '''
    if len(code) == length:
        return True
    else:
        return False


# 입력받은 String 을 hex 로 변환하여 반환하는 함수
def isHex(code) -> bool:
    '''
    입력 받은 code 가 hex 인지 아닌지를 반환하는 함수
    :param code: String
    :return: true or false
    '''
    try:
        int(code, 16)
        return True
    except ValueError:
        return False


# 문자열을 hex 로 변환하는 함수
def str2hex(s):
    return s.encode('utf-8').hex()


# 입력받은 문자열을 10 개씩 잘라서 리스트로 반환하는 함수
def split10(s):
    return [s[i:i + 10] for i in range(0, len(s), 10)]

# SimData class 로 이동
# def split_text(code, split_length_list) -> list:
#     result = []
#     start = 0
#     for length in split_length_list:
#         if start + length <= len(code):
#             result.append(code[start:start + length])
#             start += length
#         else:
#             result.append(code[start:])
#             break
#     return result
