# 데이터베이스

iRead의 주 데이터베이스는 MySQL 8.4 LTS다. 문자 집합은 `utf8mb4`, collation은 `utf8mb4_unicode_ci`, 기본 DB 이름은 `iread_demo`다.

## 1. 관련 파일

| 파일 | 역할 |
| --- | --- |
| [database/iread_demo.sql](database/iread_demo.sql) | 제출용 최신 비식별 데모 DB dump |
| `contracts/database/erd.png` | 승인된 ERD 이미지 |
| `contracts/database/erd.md` | ERD 설명 |
| `contracts/database/schema.sql` | 계약 기준 schema |
| `services/backend/src/main/resources/db/migration/` | 공통 Flyway schema와 migration |
| `services/backend/src/main/resources/db/demo/` | `demo` profile 전용 seed migration |
| `services/backend/src/main/resources/db/demo-data/` | QA 시연 데이터 초기화 SQL |

실행 시점의 최종 schema 기준은 Backend의 Flyway migration이다. `contracts/database/schema.sql`은 서비스 간 계약 검토용 기준이며, DB를 실행할 때 임의로 Flyway 대신 적용하지 않는다.

## 2. 기본 접속 정보

Compose 내부:

```text
host=mysql
port=3306
database=iread_demo
username=iread
password=<루트 .env의 MYSQL_PASSWORD>
```

호스트 PC:

```text
host=127.0.0.1
port=3307
database=iread_demo
username=iread
password=<루트 .env의 MYSQL_PASSWORD>
```

Backend JDBC URL:

```text
jdbc:mysql://mysql:3306/iread_demo?serverTimezone=Asia/Seoul&characterEncoding=UTF-8
```

실제 비밀번호는 `.env`에서 관리하며 문서, SQL dump와 commit에 넣지 않는다.

## 3. DB 생성 방식

새 DB에서 Backend를 `demo` profile로 처음 실행하면 다음 순서로 데이터가 구성된다.

1. Flyway가 `db/migration`과 `db/demo`의 versioned migration을 순서대로 적용한다.
2. 기준 훈련 template과 읽기 feature가 준비된다.
3. 교수자 화면용 비식별 showcase와 persona 데이터가 적용된다.
4. QA 데이터셋이 교수자 `1001`과 시연 아동 `2001`, `2002`, `2103`의 상태를 재구성한다.
5. `qa_demo_dataset_deployments`에 데이터셋 tag가 기록된다.

`IREAD_QA_DEMO_DATASET_DEPLOY_TAG`가 바뀐 경우에만 QA 데이터셋을 다시 설치한다.

## 4. 제출용 dump의 데이터 범위

`iread_demo.sql`은 빈 DB가 아니다. 화면과 기능을 바로 확인할 수 있도록 다음 가상 데이터를 포함한다.

- 교수자 계정 `test@test.com`
- 가상 아동 김도윤, 이서연, 박지호와 추가 분석 persona
- 과거 훈련·검사·이야기·보고서 이력
- 다음 시연용 커리큘럼과 문항
- 시선·발음 분석 화면을 확인하기 위한 비식별 fixture metadata
- `flyway_schema_history`

제외 대상:

- 실제 사용자 이름·연락처·주소·이메일
- 실제 아동의 음성·시선 원본
- MySQL root 비밀번호와 운영 계정 비밀번호
- Azure, GMS, OpenAI, Gemini, SMTP key
- 로컬 PC의 SDK·파일 경로

SQL에 포함된 연락처, 주소와 보호자 정보는 `010-0000-*`, `demo@demo*.com`, `가상시`처럼 시연용으로 만든 값이다. 교수자 비밀번호는 알려진 데모 비밀번호의 단방향 hash만 저장한다.

### 4.1 DB 밖에 저장되는 시연 에셋

SQL dump에는 이미지나 원시 JSON의 바이너리 내용이 아니라 파일 URL, 분석 결과와 metadata만 들어간다. 실제 시연 에셋은 전체 GitLab 저장소의 Backend 소스에 포함되어 있으므로 `exec/` 아래에 같은 파일을 중복 저장하지 않는다.

에셋 목록의 기준은 [`manifest.json`](../services/backend/src/main/resources/assets/qa-demo/manifest.json)이다.

| 구분 | 파일 수 | 저장소 안의 원본 위치 | DB와의 관계 | 실행 시 위치 |
| --- | ---: | --- | --- | --- |
| 이야기·훈련 이미지 | 39 | `services/backend/src/main/resources/assets/qa-demo/images/` | `/uploads/images/<파일명>` URL 저장 | `backend-images` volume의 `/data/uploads/images` |
| 원시 시선 JSON | 66 | `services/backend/src/main/resources/assets/qa-demo/gaze/` | 시연 아동 `2001`, `2002`, `2103`의 `gaze_sessions.data_url`과 연결 | `backend-gaze` volume의 `/data/gaze` |
| 발음 분석 JSON | 36 | `services/backend/src/main/resources/assets/qa-demo/pronunciation/` | 검사 결과 JSON의 `rawAssetPath`와 연결 | Backend classpath에서 유효성 확인 및 참조 |
| 기본 아동 profile 이미지 | 2 | 두 Frontend의 `public/images/` | `/images/student-profile-boy.png`, `/images/student-profile-girl.png` | Frontend 정적 파일로 제공 |
| QA 음성 원본 | 0 | 제출용 에셋에 포함하지 않음 | DB dump에 음성 파일 경로 없음 | 새 녹음·TTS가 필요한 경우 실행 중 생성 |

Backend의 `QaDemoAssetInstaller`는 위 manifest를 읽고 이미지와 시선 JSON을 named volume에 복사한다. `reset-qa-demo.bat` 또는 `reset-qa-demo.sh`를 실행하면 DB 상태와 함께 이 에셋도 다시 설치된다.

추가 분석 persona `2101`~`2111`은 교수자 화면에서 집계 결과를 확인하기 위한 가상 레코드다. 이 persona의 `gaze_analysis_results`는 DB에 포함되지만 원시 시선 JSON은 제출용 manifest 범위에 포함하지 않는다. 원시 시선 재생·재분석을 포함한 시연은 manifest가 관리하는 `2001`, `2002`, `2103`으로 진행한다.

중요한 복원 조건:

- `iread_demo.sql`만 별도로 전달하면 이미지와 시선 파일은 복원되지 않는다.
- 전체 GitLab 저장소를 clone한 상태에서 복원해야 한다.
- dump에 QA 배포 tag가 이미 기록되어 있으면 Backend 기동 시 자동 설치가 생략될 수 있으므로, dump 복원 후 반드시 `reset-qa-demo`를 한 번 실행한다.
- 실제 사용자 음성 원본은 개인정보 보호를 위해 제출하지 않는다. 발음 시연 이력은 비식별 발음 분석 JSON과 DB 결과를 사용한다.

## 5. 최신 dump 정보

| 항목 | 값 |
| --- | --- |
| 파일 | `exec/database/iread_demo.sql` |
| 생성 기준 | 현재 Backend Flyway migration과 QA 데모 데이터셋 |
| 생성일 | 2026-08-10 |
| SHA-256 | `1BC86DBFDB93038DD00F4FA7ACD3DEE4F8D4ADAF0AB27882FE5BE5038AD289E0` |

덤프를 빈 MySQL 데이터 디렉터리에 복원하고 같은 Backend를 재기동해 아래 항목을 검증했다.

- [x] 빈 MySQL에 오류 없이 복원된다.
- [x] `flyway_schema_history`와 성공한 migration 15개가 포함된다.
- [x] 교수자 2명, 아동 13명과 시연 아동 `2001`, `2002`, `2103`이 조회된다.
- [x] 교육과정 108개, 훈련 627개, 검사 81개, 이야기 27개, 보고서 28개가 조회된다.
- [x] `test@test.com` 교수자 계정과 시연 아동의 인증 정보가 포함된다.
- [x] 저장소의 데모 초기화 코드에 정의된 비밀값·개인정보 금지 패턴이 없다.
- [x] 복원 후 Backend가 Flyway schema version `15`를 확인하고 정상 기동한다.
- [x] SQL의 핵심 시연 에셋 참조가 manifest의 이미지 39개, 시선 JSON 66개, 발음 분석 JSON 36개와 모두 일치한다.

덤프는 로컬의 격리된 MySQL 8.0.45 환경에서 생성·복원 검증했다. 제출 실행 환경은 `compose.yml`에 고정된 MySQL 8.4이며, SQL은 DB 생성문과 `utf8mb4` 설정을 포함한다. 최종 제출 전에는 제출 PC의 Docker 환경에서도 한 번 더 복원 절차를 실행한다.

## 6. dump 복원

### 6.1 기존 DB 백업

현재 DB가 필요하면 복원 전에 별도 dump를 만든다.

```bash
docker compose exec -T mysql sh -lc 'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --databases "$MYSQL_DATABASE" --single-transaction --routines --triggers --events --set-gtid-purged=OFF --default-character-set=utf8mb4' > iread_before_restore.sql
```

### 6.2 Backend 중지

```bash
docker compose stop backend
docker compose up -d mysql
```

### 6.3 dump를 MySQL 컨테이너로 복사

```bash
docker compose cp exec/database/iread_demo.sql mysql:/tmp/iread_demo.sql
```

### 6.4 복원

`iread_demo.sql`은 DB 생성문을 포함하므로 root 계정으로 전체 파일을 적용한다.

```bash
docker compose exec mysql sh -lc 'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" < /tmp/iread_demo.sql'
```

### 6.5 Backend 재시작

```bash
docker compose up -d backend
docker compose logs --tail=100 backend
```

Flyway validation 오류 없이 Backend health가 `UP`이면 schema 이력이 정상 복원된 것이다.

### 6.6 QA 에셋과 시연 상태 복원

dump에는 `qa_demo_dataset_deployments`의 배포 tag도 들어 있다. 같은 tag로 Backend를 시작하면 초기 설치가 이미 끝난 것으로 판단해 에셋 복사를 생략할 수 있으므로 다음 명령을 반드시 실행한다.

Windows PowerShell 또는 명령 프롬프트:

```powershell
.\reset-qa-demo.bat
```

macOS 또는 Linux:

```bash
./reset-qa-demo.sh
```

이 명령은 Backend의 `qaDemoReset` 작업을 실행해 QA DB 상태를 다시 맞추고 manifest가 관리하는 이미지와 시선 JSON을 named volume에 복사한다.

## 7. 복원 결과 확인

MySQL shell:

```bash
docker compose exec mysql sh -lc 'mysql -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"'
```

확인 query:

```sql
SELECT version, description, success
FROM flyway_schema_history
ORDER BY installed_rank;

SELECT id, email, name, organization
FROM teachers
WHERE email = 'test@test.com';

SELECT id, name, school
FROM students
WHERE id IN (2001, 2002, 2103)
ORDER BY id;

SELECT COUNT(*) AS curriculum_count FROM daily_curriculums;
SELECT COUNT(*) AS training_count FROM trainings;
SELECT COUNT(*) AS test_count FROM tests;
SELECT COUNT(*) AS story_count FROM stories;
SELECT COUNT(*) AS report_count FROM reports;
```

에셋 설치 확인:

```bash
docker compose exec backend sh -lc 'find /data/uploads/images -type f | wc -l'
docker compose exec backend sh -lc 'find /data/gaze -type f | wc -l'
docker compose exec backend sh -lc 'find /workspace/src/main/resources/assets/qa-demo/pronunciation -type f | wc -l'
```

새 volume에서 복원했다면 순서대로 이미지 `39`, 시선 JSON `66`, 발음 분석 JSON `36`이 조회된다. 기존 volume에 실행 중 생성된 파일이 남아 있으면 첫 번째와 두 번째 값은 더 클 수 있다.

세 아동의 이름과 각 이력 count가 조회되면 문서의 [시연 시나리오](04-demo-scenario.md)를 진행한다.

## 8. 시연 상태 초기화

전체 DB를 삭제하지 않고 QA 아동의 시연 상태만 초기화한다.

```powershell
.\reset-qa-demo.bat
```

```bash
./reset-qa-demo.sh
```

이 명령은 세 아동의 QA 데이터와 패키지에 포함된 이미지·시선 fixture를 정해진 상태로 복원한다.

## 9. 완전 초기화

다음 명령은 로컬 MySQL volume 전체를 삭제한다. 제출용 dump와 필요한 로컬 데이터를 백업한 뒤에만 실행한다.

```bash
docker compose down
docker volume rm iread-demo-mysql-data
docker compose up -d
```

일상적인 시연 복구에는 volume 삭제 대신 `reset-qa-demo`를 사용한다.

## 10. dump 재생성

최종 schema 또는 시연 데이터가 변경된 경우에만 재생성한다.

1. 새 MySQL volume에서 Backend `demo` profile을 시작한다.
2. `reset-qa-demo`를 실행한다.
3. 화면과 DB count를 확인한다.
4. 다음 명령으로 dump를 덮어쓴다.

```bash
docker compose exec -T mysql sh -lc 'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --databases "$MYSQL_DATABASE" --single-transaction --routines --triggers --events --set-gtid-purged=OFF --default-character-set=utf8mb4' > exec/database/iread_demo.sql
```

5. SHA-256을 다시 계산해 이 문서의 dump 정보를 갱신한다.

Windows PowerShell:

```powershell
Get-FileHash exec/database/iread_demo.sql -Algorithm SHA256
```

macOS 또는 Linux:

```bash
sha256sum exec/database/iread_demo.sql
```
