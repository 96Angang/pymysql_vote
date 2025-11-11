import pymysql

DB_HOST = 'localhost'
DB_USER = 'testuser'
DB_PASS = 'test1234'
DB_NAME = 'VOTE_FOOD'
TABLE_NAME = 'FOODTYPE'

ROOT_USER = 'root'
ROOT_PASS = 'MYROOTPASSWORD' # 변경 필요

TARGET_HOST = '%'

def setup_init_mysql():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        with conn.cursor() as cur:
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            cur.execute(create_db_query)
            # print(f"데이터베이스 '{DB_NAME}' 확인/생성 완료.")
            
            cur.execute(f"USE {DB_NAME}")
            
            create_table_if_not_exists_query = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                NUM INT NOT NULL, 
                TYPENAME VARCHAR(50) NOT NULL UNIQUE, 
                VOTE INT NOT NULL 
            )
            """
            cur.execute(create_table_if_not_exists_query)

            default_items = [
                (1, '한식', 0), (2, '중식', 0), (3, '일식', 0), (4, '양식', 0)
            ]
            
            cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            if cur.fetchone()[0] == 0:
                # print('초기 기본 항목을 삽입합니다.')
                for num, name, vote in default_items:
                    cur.execute(f"INSERT IGNORE INTO {TABLE_NAME} (NUM, TYPENAME, VOTE) VALUES (%s, %s, %s)", (num, name, vote))
                
            
            conn.commit()
            # print(f"테이블 '{TABLE_NAME}'이 성공적으로 생성되었습니다.")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류가 발생했습니다: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.open:
            conn.close()
            # print("데이터베이스 연결이 종료되었습니다.")

def add_grant_user():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=ROOT_USER,
            password=ROOT_PASS
        )
        with conn.cursor() as cur:
            create_user_query = (
                f"CREATE USER IF NOT EXISTS '{DB_USER}'@'{TARGET_HOST}' "
                f"IDENTIFIED BY '{DB_PASS}'"
            )
            # print(f"Executing: {create_user_query}")
            cur.execute(create_user_query)
            # print(f"사용자 '{DB_USER}' 확인/생성 완료.")
            
            grant_query = (
                f"GRANT ALL PRIVILEGES ON {DB_NAME}.* "
                f"TO '{DB_USER}'@'{TARGET_HOST}'"
            )
            # print(f"Executing: {grant_query}")
            cur.execute(grant_query)
            
            flush_query = "FLUSH PRIVILEGES"
            # print(f"Executing: {flush_query}")
            cur.execute(flush_query)
            
            conn.commit()
            # print(f"성공: 사용자 '{DB_USER}'에게 '{DB_NAME}' 데이터베이스에 대한 모든 권한이 부여되었습니다. (접속 허용 호스트: {TARGET_HOST})")
    except pymysql.MySQLError as e:
        print(f"MySQL 오류가 발생했습니다: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn and conn.open:
            conn.close()
            # print("데이터베이스 연결이 종료되었습니다.")

def mysqlreset():
    conn = None
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS
        )
        
        with conn.cursor() as cur:
            cur.execute(f"USE {DB_NAME}")
            drop_table_query = f"DROP TABLE IF EXISTS {TABLE_NAME}"
            cur.execute(drop_table_query)
            print(f"기존 테이블 '{TABLE_NAME}' 삭제 완료.")
            
            create_table_query = f"""
            CREATE TABLE {TABLE_NAME} (
                NUM INT NOT NULL,
                TYPENAME VARCHAR(50) NOT NULL UNIQUE,
                VOTE INT NOT NULL
            )
            """
            cur.execute(create_table_query)
            
            conn.commit()
            print(f"테이블 '{TABLE_NAME}'이 성공적으로 초기화되었습니다.")

    except pymysql.MySQLError as e:
        print(f"MySQL 오류가 발생했습니다: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn and conn.open:
            conn.close()
            # print("데이터베이스 연결이 종료되었습니다.")