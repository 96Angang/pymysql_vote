import pymysql

DB_HOST = 'localhost'
DB_USER = 'testuser'
DB_PASS = 'test1234'
DB_NAME = 'VOTE_FOOD'
TABLE_NAME = 'FOODTYPE'

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
            print(f"데이터베이스 '{DB_NAME}' 확인/생성 완료.")
            
            cur.execute(f"USE {DB_NAME}")
            
            create_table_if_not_exists_query = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                NUM INT NOT NULL, 
                TYPENAME VARCHAR(50) NOT NULL UNIQUE, 
                VOTE INT NOT NULL 
            )
            """
            cur.execute(create_table_if_not_exists_query)
    finally:
        if conn and conn.open:
            conn.close()
            print("데이터베이스 연결이 종료되었습니다.")
            
setup_init_mysql()