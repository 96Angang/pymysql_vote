# pymysql_vote
```text
                  +---------------------+
                  |       MySQL DB      |
                  |  (VOTE_FOOD 데이터) |
                  +----------^----------+
                             |
                             | (DB_HOST, DB_USER 사용) // 현재 testuser와 DB 및 테이블이 존재하지 않을 경우 초기 SQL이 넣어지게 작동하게 해두었음
                             |                         // 예외 발생이 있다면 testuser의 비밀번호가 다를 시에 접속 에러 발생
                  +----------v----------+
                  |    dbmanager.py     |
                  |  (DB 연결 및 CRUD)  |
                  +----------^----------+
                             |
                             | (함수 호출: get_all_food_types, process_vote 등) // 핵심 코드
                             |
                  +----------v----------+
                  |       main.py       |
                  | (UI, Logic, Input/Output)
                  +----------^----------+
                             |
                             | (print, input) // 단순 입력/출력 부분, dbmanager 호출하여 핵심코드 작동
                             |
                  +----------v----------+
                  |     사용자 (User)    |
                  +---------------------+

main.py 주요 함수 : display(), display_results(), vote_on_item()
      // 실행 시 DB Manager의 DB 초기 설정 부분 작동, 이후 무한루프 디스플레이 실행
      // display()에서 1번은 투표 참여 기능, 2번은 설문 현황 보기, 999번은 DB 초기화(이후 초기설정 입력)
      // db관련은 관리목적 상 분리하여 dbmanager.py에 되어있음.

dbmanager.py 주요 함수 : setup_init_mysql(), add_grant_user(), mysqlreset() // DB 초기 설정 및 초기화 부분
                        db_connect() // 동일한 구조의 DB 접속 정보 통합용 함수
                        get_all_food_types() // 2번 설문 현황 보기 실행 시 컬럼 조회 정보 출력
                        process_vote(선택된번호[숫자], 참조정보[튜플]) // 1번 투표 참여 시 입력한 번호 조회 후 컬럼 확인 후 투표 반영, return값은 성공여부 및 메시지 출력
                        process_new_type(추가할음식[문자]) // 1번 투표 참여 시 0번을 입력했을 때 컬럼 조회한 후 비교, return값은 process_vote와 동일
                        
