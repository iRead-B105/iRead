# iRead 포팅 매뉴얼

이 디렉터리는 GitLab `S15P11B105` 저장소를 clone한 뒤 iRead 데모 환경을 빌드하고 실행하는 데 필요한 자료를 모은다. 저장소에는 Backend, 교수자 웹, 아동 앱, AI 서비스와 시선 추적 브리지의 전체 소스가 포함되어 있으므로 별도 소스 다운로드가 필요하지 않다.

## 문서 구성

| 문서 | 내용 |
| --- | --- |
| [빌드 및 배포](01-build-and-deploy.md) | 실행 환경, 버전, 환경변수, 서비스별 빌드·실행·종료와 주의사항 |
| [외부 서비스](02-external-services.md) | Azure Speech, AI 생성 공급자, SMTP와 Tobii SDK 설정 |
| [데이터베이스](03-database.md) | MySQL 접속, ERD·migration 위치, 덤프 생성·복원과 검증 |
| [시연 시나리오](04-demo-scenario.md) | 교수자·아동 화면별 클릭 순서와 예상 결과 |
| [최신 데모 DB 덤프](database/iread_demo.sql) | 실제 개인정보와 비밀값을 제외한 시연용 MySQL 데이터 |

## 가장 빠른 실행 순서

### 1. 저장소 받기

```bash
git clone https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105.git
cd S15P11B105
```

### 2. 로컬 설정 만들기

Windows PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item services/ai/.env.example services/ai/.env
```

macOS 또는 Linux:

```bash
cp .env.example .env
cp services/ai/.env.example services/ai/.env
```

`.env`의 `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD`, `AUTH_JWT_SECRET`을 로컬 값으로 바꾼다. 실제 Azure 또는 생성형 AI 기능을 사용할 때만 `services/ai/.env`에서 사용할 공급자의 키와 provider를 설정한다. 키와 비밀번호가 들어간 두 `.env` 파일은 Git에 올리지 않는다.

### 3. 서비스 실행

Windows에서 Docker 서비스와 로컬 시선 추적 브리지를 함께 실행한다.

```powershell
.\start-all-local.bat
```

시선 추적 장치 없이 Docker 서비스만 실행하거나 macOS·Linux에서 실행한다.

```bash
docker compose up -d --build
```

### 4. 실행 확인

```bash
docker compose ps
```

| 대상 | 주소 |
| --- | --- |
| 교수자 앱 | `http://localhost:5173` |
| 아동 앱 | `http://localhost:5174` |
| Backend API | `http://localhost:8080` |
| AI 서비스 | `http://localhost:8081` |
| Mailpit | `http://localhost:8025` |
| MySQL | `localhost:3307` |
| Redis | `localhost:6379` |
| 로컬 시선 추적 브리지 | `http://localhost:8765` |

### 5. 시연 시작

- 교수자 계정: `test@test.com` / `qwer1234`
- 시연 아동: 김도윤, 이서연, 박지호
- 상세 순서: [시연 시나리오](04-demo-scenario.md)

위 계정과 아동 정보는 시연을 위해 만든 가상 데이터다. 실제 사용자 개인정보, 실제 음성 원본, API 키와 운영 비밀번호를 제출용 데이터베이스나 문서에 추가하지 않는다.

## 종료와 초기화

데이터를 보존하고 종료한다.

```bash
docker compose down
```

시연 데이터를 정해진 초기 상태로 되돌린다.

```powershell
.\reset-qa-demo.bat
```

```bash
./reset-qa-demo.sh
```

DB 볼륨 삭제는 복구할 필요가 없는 로컬 데이터인지 확인한 뒤에만 수행한다. 자세한 절차는 [데이터베이스 문서](03-database.md)를 따른다.
