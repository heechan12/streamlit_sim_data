import random


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


def get_random_hex(length):
    '''
    테스트를 위한 함수 \n
    입력받은 길이만큼의 랜덤한 Hex Code 를 반환
    :param length:
    :return:
    '''
    # 랜덤한 Hex 코드를 저장할 변수
    hex_code = ""

    # Hex 코드는 0부터 F까지의 문자로 이루어져 있으므로, 가능한 문자들을 리스트로 저장
    hex_characters = "0123456789ABCDEF"

    # 입력받은 길이만큼 랜덤한 Hex 문자를 생성하여 hex_code에 추가
    for _ in range(length):
        hex_code += random.choice(hex_characters)

    return hex_code


def change_value(old_data, new_data) :
    temp_list = list(old_data)
    for i in range(len(new_data)):
        temp_list[i] = new_data[i]

    return ''.join(temp_list)

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


def decimal_to_hex(decimal_number):
    return hex(decimal_number)[2:]



version = '2768'
