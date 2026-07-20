# 저장소 및 submodule 전략

- 상태: accepted
- 최종 검토일: 2026-07-15

## 채택 방향

[ADR-0001](../decisions/ADR-0001-separate-service-repositories.md)과 [ADR-0004](../decisions/ADR-0004-service-repository-layout.md)에 따라 오케스트레이션 저장소와 세 개의 서비스 저장소를 분리하고 `services/` 아래에 연결한다.

| 저장소 역할 | 내용 | 기술 스택 | 경로 / URL |
| --- | --- | --- | --- |
| Orchestration | 공통 문서, 계약, ADR, 통합 구성 | Markdown, Docker Compose 예정 | 현재 디렉터리 |
| Backend | 도메인/API 구현과 자체 테스트 | Spring Boot 3, Java 21, Gradle Kotlin DSL | `services/backend` / [iRead-backend](https://github.com/iRead-B105/iRead-backend) |
| Frontend | UI 구현과 자체 테스트 | Vue 3, TypeScript, Vite, pnpm | `services/frontend` / [iRead-frontend](https://github.com/iRead-B105/iRead-frontend) |
| AI server | AI 기능 구현과 자체 테스트 | FastAPI, Python 3.12, uv | `services/ai` / [iRead-ai](https://github.com/iRead-B105/iRead-ai) |

## 소유권 원칙

- 서비스 내부 구현과 단위 테스트는 해당 서비스 저장소가 소유한다.
- 서비스 간 API/이벤트 계약, 호환성 정책과 통합 실행 방법은 오케스트레이션 저장소가 소유한다.
- 계약 원본의 위치와 생성 방식은 서비스 경계가 확정될 때 ADR로 결정한다.
- submodule clone과 참조 갱신은 [submodule 운영 가이드](../workflows/submodules.md)를 따른다.
- 모든 저장소의 브랜치와 커밋 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 공통 기준으로 사용한다.

## GitLab 통합 미러

- GitHub의 네 저장소를 개발 기준으로 유지한다.
- GitLab [`S15P11B105`](https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105)는 단일 통합 미러로 사용한다.
- GitLab `main`에는 오케스트레이션이 고정한 서비스 commit을 squash 없는 subtree로 통합한다.
- 저장소별 원본 branch와 tag는 GitLab `upstream/*` namespace에 보존한다.
- 세부 결정과 운영 절차는 [ADR-0005](../decisions/ADR-0005-gitlab-monorepo-mirror.md)와 [GitLab 단일 저장소 동기화 가이드](../workflows/gitlab-monorepo-sync.md)를 따른다.

## 저장소 구성 현황

- [x] 서비스명과 오케스트레이션 저장소명 `iRead` 확정
- [x] 오케스트레이션 저장소 Git 초기화 및 원격 연결
- [x] `main`, `develop` 브랜치 구성
- [x] Backend, Frontend, AI server 저장소명 확정
- [x] submodule 디렉터리 배치 확정
- [x] 각 저장소 생성 및 기본 브랜치 정책 확정
- [x] submodule 연결
- [x] clone, update, 통합 검증 절차 문서화
