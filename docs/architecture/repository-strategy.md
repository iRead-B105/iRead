# 저장소 및 submodule 전략

- 상태: proposed
- 최종 검토일: 2026-07-15

## 채택 방향

[ADR-0001](../decisions/ADR-0001-separate-service-repositories.md)에 따라 오케스트레이션 저장소와 세 개의 서비스 저장소를 분리한다.

| 저장소 역할 | 내용 | 기술 스택 | 경로 / URL |
| --- | --- | --- | --- |
| Orchestration | 공통 문서, 계약, ADR, 통합 구성 | Markdown, Docker Compose 예정 | 현재 디렉터리 |
| Backend | 도메인/API 구현과 자체 테스트 | Spring Boot 3, Java 21, Gradle Kotlin DSL | [TBD] |
| Frontend | UI 구현과 자체 테스트 | Vue 3, TypeScript, Vite, pnpm | [TBD] |
| AI server | AI 기능 구현과 자체 테스트 | FastAPI, Python 3.12, uv | [TBD] |

## 소유권 원칙

- 서비스 내부 구현과 단위 테스트는 해당 서비스 저장소가 소유한다.
- 서비스 간 API/이벤트 계약, 호환성 정책과 통합 실행 방법은 오케스트레이션 저장소가 소유한다.
- 계약 원본의 위치와 생성 방식은 서비스 경계가 확정될 때 ADR로 결정한다.
- submodule 경로와 URL은 각 서비스 저장소명이 확정되기 전에는 만들지 않는다.
- 모든 저장소의 브랜치와 커밋 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 공통 기준으로 사용한다.

## 저장소 구성 현황

- [x] 서비스명과 오케스트레이션 저장소명 `iRead` 확정
- [x] 오케스트레이션 저장소 Git 초기화 및 원격 연결
- [x] `main`, `develop` 브랜치 구성
- [ ] Backend, Frontend, AI server 저장소명 확정
- [ ] submodule 디렉터리 배치 확정
- [ ] 각 저장소 생성 및 기본 브랜치 정책 확정
- [ ] submodule 연결
- [ ] clone, update, 통합 검증 절차 문서화
