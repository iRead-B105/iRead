# iRead

iRead는 난독증 또는 읽기곤란 위험이 있는 초등 저학년 아동을 위한 개인화 읽기 훈련 시스템입니다.

아동이 자신의 읽기 특성과 변화 속도에 맞춰 꾸준히 훈련할 수 있도록 돕고, 보호자와 전문가는 훈련 과정과 변화를 함께 살펴볼 수 있도록 하는 것을 목표로 합니다. 현재는 실제 운영을 목적으로 하지 않는 데모 버전을 개발하고 있습니다.

> iRead는 의료적 진단이나 전문가의 판단을 대체하지 않습니다. 아동의 안전과 존엄성, 개인정보 보호를 우선하며 전문가의 읽기 교육과 지원을 보조하는 도구를 지향합니다.

## 이 저장소의 역할

이 저장소는 여러 iRead 서비스가 하나의 제품으로 일관되게 개발되도록 조율하는 오케스트레이션 저장소입니다.

제품 요구사항, 시스템 구조, 서비스 간 API·데이터 계약, 주요 기술 결정과 공통 작업 방식을 이곳에서 관리합니다. 실제 서비스 코드는 독립된 저장소에서 개발하며 `services/` 아래에 Git submodule로 연결합니다.

| 영역 | 역할 | 저장소 |
| --- | --- | --- |
| Backend | 도메인, API와 데이터베이스 | [iRead-backend](https://github.com/iRead-B105/iRead-backend) |
| Frontend | 웹 사용자 인터페이스 | [iRead-frontend-web](https://github.com/iRead-B105/iRead-frontend-web) |
| 아동 앱 | 아동용 읽기 훈련 애플리케이션 | [iRead-frontend-app](https://github.com/iRead-B105/iRead-frontend-app) |
| AI server | AI 기능 서비스 | [iRead-ai](https://github.com/iRead-B105/iRead-ai) |
| 시선 추적 | Tobii 기반 시선 수집·보정 프로토타입 | [iRead-eyetracking](https://github.com/iRead-B105/iRead-eyetracking) |

## 저장소 받기

서비스 저장소까지 한 번에 받으려면 `--recurse-submodules` 옵션을 사용합니다.

```bash
git clone --recurse-submodules https://github.com/iRead-B105/iRead.git
cd iRead
```

이미 이 저장소만 clone했다면 submodule을 별도로 초기화합니다.

```bash
git submodule update --init --recursive
```

각 서비스의 실행 방법과 개발 환경은 해당 서비스 디렉터리의 README를 확인해 주세요.

## 통합 데모 환경

Backend, 데이터베이스, 개발 인프라와 두 Frontend를 하나의 Docker 네트워크에서 실행합니다.

```bash
docker compose up -d
```

| 서비스 | 주소 |
| --- | --- |
| 교수자 앱 (`frontend-web`) | `http://localhost:5173` |
| 아동 앱 (`frontend-app`) | `http://localhost:5174` |
| Backend API | `http://localhost:8080` |
| MySQL | `localhost:3307` |
| Redis | `localhost:6379` |
| AI Mock | `http://localhost:8081` |
| Mailpit | `http://localhost:8025` |

모든 컨테이너는 `iread-network`에 연결됩니다. 종료할 때는 데이터 볼륨을 보존하는
`docker compose down`을 사용합니다.

## 프로젝트 문서

| 알고 싶은 내용 | 문서 |
| --- | --- |
| 제품 목표와 대상 사용자 | [제품 비전과 범위](docs/product/vision-and-scope.md) |
| 기능 요구사항 | [제품 요구사항](docs/product/requirements.md) |
| 전체 시스템 구성 | [시스템 컨텍스트](docs/architecture/system-context.md) |
| 기능·API·데이터베이스 명세 | [계약 카탈로그](contracts/catalog.md) |
| 주요 기술 결정과 배경 | [ADR 목록](docs/decisions/index.md) |
| Backend·Frontend 작업 목록 | [구현 백로그](docs/planning/implementation-backlog.md) |
| 전체 문서 탐색 | [문서 인덱스](docs/index.md) |

## 기술 구성

| 영역 | 기술 |
| --- | --- |
| Backend | Spring Boot 4.0.7, Java 21, Gradle |
| Frontend | Vue 3, TypeScript, Vite, pnpm |
| AI server | FastAPI, Python 3.12, uv |
| Database | MySQL 8.4 LTS |
| Infrastructure | Redis, Docker Compose |
| 시선 추적 | FastAPI, JavaScript, C++, Tobii Game Integration SDK |

아동 앱의 기술 스택과 일부 인프라 역할은 제품 범위에 맞춰 확정할 예정입니다.

## 함께 개발하기

- 서비스 구현은 해당 `services/*` 저장소에서 작업합니다.
- 공통 요구사항, API·데이터 계약과 주요 결정은 이 저장소에서 관리합니다.
- 브랜치와 커밋은 [Git 작업 방식](docs/workflows/git-flow.md)을 따릅니다.
- submodule 갱신 방법은 [submodule 운영 가이드](docs/workflows/submodules.md)를 확인합니다.
- AI 에이전트는 [AGENTS.md](AGENTS.md)의 저장소 지침을 따릅니다.

문서와 서비스 간 계약을 변경했다면 다음 검사를 실행합니다.

```bash
python tools/validate_harness.py
python tools/validate_contracts.py
```
