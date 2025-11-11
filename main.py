import pymysql, dbmanager

def vote_on_item():
    
    current_items = dbmanager.get_all_food_types()
    if not current_items:
        print("투표할 항목을 불러오지 못했습니다. DB 연결 또는 항목을 확인하세요.")
        return
        
    print('\n----- 투표할 음식 종류 -----')
    for num, typename in current_items:
        print(f'{num}. {typename}')
    print('0. 기타(직접입력)')
    print('-' * 28)
    
    choice = input('선택: ')
    
    if choice.isdigit():
        choice_num = int(choice)
        
        if choice_num > 0 and choice_num <= current_items[-1][0]: # current_items의 최대 NUM과 비교
            selected_item = next((item for item in current_items if item[0] == choice_num), None)
            
            if selected_item:
                success, message = dbmanager.process_vote(choice_num, selected_item)
                if success:
                    print(f"'{selected_item[1]}'에 투표했습니다.")
                else:
                    print(message)
            else:
                 print('잘못된 선택입니다.')
                 
        elif choice_num == 0:
            new_typename = input('새로운 음식 종류를 입력해주세요: ')
            if new_typename:
                success, message = dbmanager.process_new_type(new_typename)
                if success:
                    print(message)
                else:
                    print(f"오류가 발생했습니다: {message}")
            else:
                print('입력이 취소되었습니다.')
        else:
            print('잘못된 선택입니다.')
    else:
        print('숫자만 입력할 수 있습니다.')
            
def display_results():
    results = dbmanager.get_all_vote_results()
    if not results:
        print("투표 결과를 불러오지 못했습니다.")
        return

    print('\n--------- 설문 현황 ---------')
    for num, typename, vote in results:
        print(f'{num}. {typename} ===> {vote}표')
    print('-' * 29)

    input('초기로 돌아가려면 아무 문자 입력: ')


def display():
    while True:
        print('\n★ 좋아하는 음식 종류 설문조사 ★')
        print('1.설문 참여하기')
        print('2.설문 현황보기')
        main_choice = input('선택: ')

        if main_choice == '1':
            vote_on_item()
        elif main_choice == '2':
            display_results()
        elif main_choice == '999':
            dbmanager.mysqlreset()
            dbmanager.setup_init_mysql()
        else:
            print('1, 2 중 하나만 선택할 수 있습니다. (999 = 초기화)')

# DB init 실행부분
try:
    dbmanager.setup_init_mysql()
except pymysql.err.OperationalError:
    dbmanager.add_grant_user()

# UI 실행부분
display()