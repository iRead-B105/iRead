# 빌드 및 배포

이 문서는 GitLab 저장소를 받은 직후 전체 데모 환경을 재현하는 절차를 설명한다. 기본 실행 방식은 저장소 루트의 `compose.yml`을 사용하는 Docker Compose다.

## 1. 저장소 구조

| 경로 | 역할 |
| --- | --- |
| `services/backend` | Spring Boot Backend API |
| `services/frontend-web` | 교수자용 Vue 웹 애플리케이션 |
| `services/frontend-app` | 아동용 Vue 웹 애플리케이션 |
| `services/ai` | 이야기·훈련 생성과 음성 처리를 담당하는 FastAPI 서비스 |
| `services/eyetracking` | Windows에서 Tobii 장치와 브라우저를 연결하는 로컬 브리지 |
| `contracts` | API·DB·시선 데이터 계약과 ERD |
| `compose.yml` | MySQL부터 두 Frontend까지 통합 실행하는 Compose 파일 |
| `.env.example` | 통합 실행에 필요한 환경변수 예시 |

## 2. 확인된 개발·실행 환경

| 구분 | 제품과 버전 | 설정 또는 용도 |
| --- | --- | --- |
| OS | Windows 11 x64 | Tobii native bridge 필수 환경 |
| Git | 2.52.0.windows.1 | 저장소 clone과 변경 이력 관리 |
| IDE | Visual Studio Code 1.132.0 x64 | 문서·Frontend·Python·Java 소스 확인에 사용한 IDE |
| Native IDE | Visual Studio 2022 Build Tools | `Desktop development with C++` workload, Tobii bridge 빌드 시에만 필요 |
| Container runtime | Docker 29.2.1, Docker Compose 5.1.0 | 전체 데모 환경 실행 |
| JVM | Eclipse Temurin 21 JDK | `backend` 컨테이너의 빌드·실행 JVM |
| Backend | Spring Boot 4.0.7, Gradle 9.5.1 | `./gradlew bootRun` |
| WAS | Embedded Apache Tomcat 11.0.22 | Spring Boot가 관리하는 내장 Servlet container |
| Database | MySQL 8.4 | UTF-8 `utf8mb4`, 기본 DB `iread_demo` |
| Cache | Redis 7.4 Alpine | append-only mode |
| 교수자 Frontend | Node.js 24, pnpm 11.9.0, Vue 3.5, Vite 8 | 개발 서버 포트 5173 |
| 아동 Frontend | Node.js 24, npm, Vue 3.5, Vite 8 | 개발 서버 포트 5174 |
| AI 서비스 | Python 3.12, uv 0.11.32, FastAPI | 컨테이너 포트 8080, 호스트 포트 8081 |
| 메일 테스트 | Mailpit 1.27 | SMTP 1025, 웹 UI 8025 |
| 시선 추적 | Python FastAPI, C++, Tobii Game Integration SDK 9.0.4.26 | 로컬 브리지 포트 8765 |

버전 기준 파일은 `services/backend/build.gradle`, `services/backend/gradle/wrapper/gradle-wrapper.properties`, 두 Frontend의 `package.json`과 lock 파일, `services/ai/pyproject.toml`, `services/ai/Dockerfile`, `services/eyetracking/requirements.txt`, `compose.yml`이다.

## 3. 사전 준비

필수 항목:

1. Git
2. Docker Desktop 또는 Docker Engine과 Compose plugin
3. 모든 서비스 컨테이너를 실행할 수 있는 충분한 메모리와 디스크 공간
4. 컨테이너 이미지와 의존성을 받을 수 있는 네트워크

Tobii를 실제로 사용할 때만 추가한다.

1. Windows PC
2. Tobii Eye Tracker 5
3. Tobii Experience와 장치 드라이버
4. Tobii Game Integration SDK 9.0.4.26
5. Visual Studio 2022 Build Tools의 C++ workload

## 4. 환경변수 준비

### 4.1 통합 환경 `.env`

```powershell
Copy-Item .env.example .env
```

```bash
cp .env.example .env
```

주요 값은 다음과 같다.

| 그룹 | 변수 | 설명 |
| --- | --- | --- |
| Compose | `COMPOSE_PROJECT_NAME`, `IREAD_CONTAINER_PREFIX`, `IREAD_VOLUME_PREFIX`, `IREAD_NETWORK_NAME` | 컨테이너·볼륨·네트워크 이름 |
| Database | `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_ROOT_PASSWORD`, `MYSQL_PORT` | MySQL DB와 접속 정보 |
| Runtime | `BACKEND_PORT`, `AI_PORT`, `FRONTEND_WEB_PORT`, `FRONTEND_APP_PORT` | 호스트 공개 포트 |
| Infrastructure | `REDIS_PORT`, `SMTP_PORT`, `MAILPIT_WEB_PORT` | Redis와 로컬 메일 포트 |
| Authentication | `AUTH_JWT_SECRET`, `AUTH_COOKIE_SECURE` | JWT 서명과 cookie 보안 설정 |
| Dataset | `IREAD_QA_DEMO_DATASET_ENABLED`, `IREAD_QA_DEMO_DATASET_DEPLOY_TAG` | 비식별 QA 데모 데이터 설치 여부와 버전 태그 |
| Backend-AI | `AI_API_KEY`, `AI_READ_TIMEOUT` | Backend와 AI 서비스 사이의 공유 키와 timeout |
| Mock switch | `AI_MOCK_GENERATE`, `AI_MOCK_STORY`, `AI_MOCK_IMAGE`, `AI_MOCK_EVALUATE`, `AI_MOCK_SPEECH`, `AI_MOCK_PRONUNCIATION`, `AI_MOCK_TRANSCRIBE`, `AI_MOCK_TTS` | AI 기능별 실제 공급자 호출 여부 |
| Eye tracking | `VITE_GAZE_WS_URL`, `VITE_GAZE_MODE_URL` | 아동 앱이 연결할 로컬 브리지 주소 |

다음 값은 예시 그대로 외부에 배포하면 안 된다.

- `MYSQL_PASSWORD`
- `MYSQL_ROOT_PASSWORD`
- `AUTH_JWT_SECRET`
- `AI_API_KEY`

`AUTH_JWT_SECRET`은 32바이트 이상의 임의 문자열을 사용한다. HTTPS 배포에서는 `AUTH_COOKIE_SECURE=true`로 바꾸고 실제 Frontend origin을 Backend CORS 설정에 추가한다.

### 4.2 AI 서비스 `services/ai/.env`

```powershell
Copy-Item services/ai/.env.example services/ai/.env
```

```bash
cp services/ai/.env.example services/ai/.env
```

`AI_INTERNAL_API_KEY`는 루트 `.env`의 `AI_API_KEY`와 같아야 한다. 실제로 사용할 공급자 하나만 선택하고 해당 키를 입력한다. 공급자별 설정은 [외부 서비스 문서](02-external-services.md)를 따른다.

### 4.3 시선 추적 `services/eyetracking/config.json`

Tobii native bridge를 직접 실행할 때만 만든다.

```powershell
Copy-Item services/eyetracking/config.example.json services/eyetracking/config.json
```

`nativeBridge.exePath`와 필요하면 `nativeBridge.sdkDir`을 현재 PC 경로에 맞춘다. `config.json`에는 개인 PC 경로가 포함될 수 있으므로 Git에 올리지 않는다.

## 5. 전체 서비스 실행

### 5.1 Windows 통합 실행

```powershell
.\start-all-local.bat
```

이 스크립트는 다음 순서로 동작한다.

1. Docker Compose 서비스 빌드 및 실행
2. `services/eyetracking/.venv`가 없으면 Python 가상환경과 의존성 준비
3. 로컬 시선 추적 브리지를 `0.0.0.0:8765`에서 실행

### 5.2 Docker 서비스만 실행

```bash
docker compose up -d --build
```

서비스 의존 순서는 `mysql`, `redis`, `ai`, `mailpit`의 health check가 성공한 뒤 `backend`와 두 Frontend를 시작하는 구조다.

### 5.3 상태 확인

```bash
docker compose ps
docker compose logs --tail=100 backend
docker compose logs --tail=100 ai
```

```bash
curl http://localhost:8080/actuator/health
curl http://localhost:8081/health
```

정상 판정:

- `mysql`, `redis`, `ai`가 `healthy`
- `backend`, `frontend-web`, `frontend-app`, `mailpit`가 `running`
- Backend health 응답의 `status`가 `UP`
- AI health 요청이 HTTP 200

## 6. 서비스별 빌드와 실행

통합 Compose가 아닌 개별 개발이나 오류 분석 때 사용한다.

### 6.1 Backend

요구사항: JDK 21, 로컬 MySQL과 Redis

```powershell
cd services/backend
.\gradlew.bat test
.\gradlew.bat bootRun --args="--spring.profiles.active=demo"
```

```bash
cd services/backend
./gradlew test
./gradlew bootRun --args="--spring.profiles.active=demo"
```

### 6.2 교수자 Frontend

```bash
cd services/frontend-web
corepack enable
pnpm install --frozen-lockfile
pnpm test
pnpm build
pnpm dev
```

개발 서버는 `/api`와 `/uploads`를 Backend로 proxy한다. 별도 배포에서는 reverse proxy가 두 경로를 Backend로 전달해야 한다.

### 6.3 아동 Frontend

```bash
cd services/frontend-app
npm ci
npm test
npm run build
npm run dev -- --port 5174
```

API 실행에 필요한 값:

```text
VITE_LEARNER_DATA_SOURCE=api
VITE_API_BASE_URL=
VITE_BACKEND_URL=http://127.0.0.1:8080
VITE_GAZE_WS_URL=ws://127.0.0.1:8765/gaze
VITE_GAZE_MODE_URL=http://127.0.0.1:8765/api/mode
```

### 6.4 AI 서비스

```bash
cd services/ai
uv sync --frozen
uv run pytest
uv run uvicorn iread_ai.app:app --host 0.0.0.0 --port 8081
```

Docker 이미지 단독 빌드:

```bash
docker build -t iread-ai:local services/ai
```

### 6.5 시선 추적 브리지

```powershell
cd services/eyetracking
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\run_server.bat
```

Tobii native bridge 빌드:

```powershell
cd services/eyetracking\native
.\build_native_with_vs2022.bat C:\path\to\tobii_gameintegration_9.0.4.26
```

## 7. 포트와 데이터 경로

| 서비스 | 컨테이너 포트 | 기본 호스트 포트 | 영속 데이터 |
| --- | ---: | ---: | --- |
| MySQL | 3306 | 3307 | `iread-demo-mysql-data` volume |
| Redis | 6379 | 6379 | `iread-demo-redis-data` volume |
| Backend | 8080 | 8080 | 이미지·음성·시선용 named volume |
| AI | 8080 | 8081 | 필요 시 `AI_TRAINING_ITEM_DB_PATH`로 별도 지정 |
| 교수자 Frontend | 5173 | 5173 | 소스 mount, node_modules volume |
| 아동 Frontend | 5174 | 5174 | 소스 mount, node_modules volume |
| Mailpit SMTP | 1025 | 1025 | 로컬 테스트 메일 |
| Mailpit UI | 8025 | 8025 | 브라우저 메일함 |
| 시선 추적 브리지 | 해당 없음 | 8765 | 로컬 Windows 프로세스 |

## 8. 배포 시 주의사항

1. `.env`와 `services/ai/.env`를 commit하지 않는다.
2. 외부 배포에서는 예시 비밀번호·JWT·내부 AI 키를 새 값으로 교체한다.
3. HTTPS에서는 secure cookie, HTTPS API와 `wss://` gaze 연결을 사용한다. HTTPS 페이지에서 `http://`·`ws://`를 호출하면 브라우저가 mixed content로 차단할 수 있다.
4. 교수자 Frontend의 `/api`, `/uploads`와 아동 Frontend의 `/api`를 Backend로 전달하는 same-origin reverse proxy를 둔다.
5. `CORS_ALLOWED_ORIGINS`에는 실제 Frontend origin만 등록한다.
6. MySQL, 업로드 이미지, 음성, 시선 파일은 서로 다른 volume에 있으므로 DB만 백업하면 파일 자료가 복구되지 않는다.
7. Tobii 장치는 브라우저가 직접 접근하지 않는다. Windows 로컬 브리지와 native executable이 먼저 실행돼야 한다.
8. 시연용 `demo` profile과 QA 데이터셋을 실제 사용자 데이터가 있는 운영 DB에 적용하지 않는다.
9. AI 실제 호출은 공급자 비용과 quota를 사용한다. 시연 전 quota와 region을 확인한다.

## 9. 종료와 재시작

데이터를 보존하고 종료한다.

```bash
docker compose down
```

코드와 설정을 다시 반영한다.

```bash
docker compose up -d --build
```

Backend만 다시 컴파일한다.

```bash
docker compose up -d --build backend
```

시연 데이터를 초기 상태로 되돌린다.

```powershell
.\reset-qa-demo.bat
```

```bash
./reset-qa-demo.sh
```

다음 명령은 로컬 DB 전체를 삭제한다. DB 덤프가 있거나 삭제해도 되는 데이터임을 확인한 경우에만 실행한다.

```bash
docker compose down
docker volume rm iread-demo-mysql-data
docker compose up -d
```

## 10. 주요 설정 파일 목록

| 파일 | 내용 |
| --- | --- |
| `.env.example` | 통합 Compose 환경변수 예시 |
| `compose.yml` | 컨테이너, 포트, health check, volume, 서비스 의존 순서 |
| `services/backend/src/main/resources/application.properties` | Backend 공통 설정과 환경변수 연결 |
| `services/backend/src/main/resources/application-demo.properties` | 데모 profile과 AI mock 정책 |
| `services/backend/src/main/resources/db/migration/` | 운영 기준 Flyway schema와 migration |
| `services/backend/src/main/resources/db/demo/` | 데모 profile 전용 Flyway 데이터 |
| `services/ai/.env.example` | 생성·이미지·음성 공급자 설정 예시 |
| `services/ai/pyproject.toml`, `uv.lock` | Python과 AI 의존성 버전 |
| `services/frontend-web/package.json`, `pnpm-lock.yaml` | 교수자 Frontend 버전과 빌드 명령 |
| `services/frontend-app/package.json`, `package-lock.json` | 아동 Frontend 버전과 빌드 명령 |
| `services/eyetracking/config.example.json` | Tobii executable, SDK와 Backend 연결 예시 |
| `contracts/database/erd.png`, `erd.md`, `schema.sql` | 승인된 ERD와 기준 schema |
