class SimData:
    # 외부에서 list 를 받아서
    # 1. 10자리씩 나누고
    # 2. 각 항목을 멤버 변수에 할당
    def __init__(self, input_list):
        self.list = input_list
        self.code0 = input_list[0]
        self.code1 = input_list[1]
        self.code2 = input_list[2]
        self.code3 = input_list[3]

    def split_code_to_data_list(code: str, split_length_list) -> list:
        '''
        500자로 된 코드를 입력받아서
        정해진 길이로 나누어서 리스트로 반환하는 함수
        :param code : String
        :param split_length_list : List
        :return: list
        '''
        result = []
        start = 0
        for length in split_length_list:
            if start + length <= len(code):
                result.append(code[start:start + length])
                start += length
            else:
                result.append(code[start:])
                break
        return result
