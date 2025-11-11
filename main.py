import pymysql, dbmanager
from dbmanager import DB_HOST, DB_USER, DB_PASS, DB_NAME, TABLE_NAME

def db_connect():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"데이터베이스 연결 오류: {e}")
        return None

def vote_on_item():
    conn = db_connect()
        
    current_items = []
    try:
        with conn.cursor() as cur:
            select_query = f"SELECT NUM, TYPENAME FROM {TABLE_NAME} ORDER BY NUM"
            cur.execute(select_query)
            current_items = cur.fetchall()

            print('\n----- 투표할 음식 종류 -----')
            for num, typename in current_items:
                print(f'{num}. {typename}')
            print('0. 기타(직접입력)')
            print('-' * 28)
            
            choice = input('선택: ')
            
            if choice.isdigit():
                choice_num = int(choice)
                
                if choice_num > 0 and choice_num <= len(current_items):
                    selected_item = next((item for item in current_items if item[0] == choice_num), None)
                    
                    if selected_item: # 선택한 것이 값이 존재할 경우
                        update_query = f"UPDATE {TABLE_NAME} SET VOTE = VOTE + 1 WHERE NUM = %s"
                        cur.execute(update_query, (choice_num,))
                        conn.commit()
                        print(f"'{selected_item[1]}'에 투표했습니다.")
                    else: # Next에서 None 반환
                         print('잘못된 선택입니다.')
                         
                elif choice_num == 0:
                    new_typename = input('새로운 음식 종류를 입력해주세요: ')
                    if new_typename:
                        check_query = f"SELECT NUM FROM {TABLE_NAME} WHERE TYPENAME = %s"
                        cur.execute(check_query, (new_typename,))
                        existing_item = cur.fetchone()
                        
                        if existing_item:
                            update_query = f"UPDATE {TABLE_NAME} SET VOTE = VOTE + 1 WHERE TYPENAME = %s"
                            cur.execute(update_query, (new_typename,))
                            conn.commit()
                            print(f"'{new_typename}'에 투표했습니다.")
                        else:
                            cur.execute(f"SELECT MAX(NUM) FROM {TABLE_NAME}")
                            max_num = cur.fetchone()[0] or 0 # 예외처리(오류 방지)
                            new_num = max_num + 1

                            insert_query = f"INSERT INTO {TABLE_NAME} (NUM, TYPENAME, VOTE) VALUES (%s, %s, 1)"
                            cur.execute(insert_query, (new_num, new_typename))
                            conn.commit()
                            print(f"새로운 종류 '{new_typename}'이(가) 추가되고 투표했습니다.")
                    else:
                        print('입력이 취소되었습니다.')
                else:
                    print('잘못된 선택입니다.')
            else:
                print('숫자만 입력할 수 있습니다.')
                
    except pymysql.MySQLError as e:
        print(f"투표 처리 중 MySQL 오류 발생: {e}")
        conn.rollback()
    finally:
        if conn and conn.open:
            conn.close()

def display_results():
    conn = db_connect()
    if not conn:
        return

    results = []
    try:
        with conn.cursor() as cur:

            select_query = f"SELECT NUM, TYPENAME, VOTE FROM {TABLE_NAME} ORDER BY VOTE DESC, NUM ASC"
            cur.execute(select_query)
            results = cur.fetchall()

            print('\n--------- 설문 현황 ---------')
            for num, typename, vote in results:
                print(f'{num}. {typename} ===> {vote}표')
            print('-' * 29)

    except pymysql.MySQLError as e:
        print(f"결과 조회 중 MySQL 오류 발생: {e}")
    finally:
        if conn and conn.open:
            conn.close()

    choice = input('초기로 돌아가려면 아무 문자 입력: ')


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