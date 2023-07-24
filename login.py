import time

def login_prompt():
    while True:
        user_input = input("입력창에 'People' 또는 'Admin'을 입력하세요: ")
        if user_input.lower() == 'people' or user_input.lower() == 'admin':
            print("로그인 되었습니다!!")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

    time.sleep(19)  # 19초 대기

    # start.py 파일 불러오기
    try:
        import start
    except ModuleNotFoundError:
        print("start.py 파일을 찾을 수 없습니다. 깃허브 저장소에 있는지 확인하세요.")

if __name__ == "__main__":
    login_prompt()
