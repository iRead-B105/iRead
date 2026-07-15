# ADR-0002: Technology baseline

- Status: accepted
- Date: 2026-07-15

## Context

서비스 저장소를 만들기 전에 각 영역의 초기 기술 기준선을 기록할 필요가 있다.

## Decision

- Backend: Spring Boot 3, Java 21, Gradle Kotlin DSL
- Frontend: Vue 3, TypeScript, Vite, pnpm
- AI server: FastAPI, Python 3.12, uv
- Redis: Docker Compose로 실행할 예정

## Boundaries of this decision

- Spring Boot와 Vue의 정확한 minor/patch 버전은 저장소 생성 시 결정한다.
- Redis의 책임과 배포 토폴로지는 결정하지 않는다.
- 주 데이터베이스, AI 모델 제공자와 클라우드/배포 플랫폼은 결정하지 않는다.

## Consequences

- 서비스별 초기 scaffold와 검증 도구를 선택할 기준이 생긴다.
- 버전 및 라이브러리 선택은 각 저장소 생성 시 호환성을 확인해야 한다.

