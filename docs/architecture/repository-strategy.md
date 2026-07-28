---
type: Architecture
title: "저장소 및 submodule 전략"
description: "오케스트레이션 저장소와 서비스 저장소의 경계, 소유권과 submodule 구성을 정의합니다."
tags: [architecture, repository, submodule, ownership]
timestamp: 2026-07-24T00:00:00+09:00
---
# 저장소 및 submodule 전략

- 상태: accepted
- 최종 검토일: 2026-07-24

## 채택 방향

[ADR-0001](../decisions/ADR-0001-separate-service-repositories.md), [ADR-0004](../decisions/ADR-0004-service-repository-layout.md), [ADR-0005](../decisions/ADR-0005-add-child-app-repository.md), [ADR-0010](../decisions/ADR-0010-add-eyetracking-repository.md)에 따라 오케스트레이션 저장소와 다섯 개의 서비스 저장소를 분리하고 `services/` 아래에 연결한다. 계약 원본은 [ADR-0007](../decisions/ADR-0007-okf-and-specification-sources.md)을 따른다.

| 저장소 역할 | 내용 | 기술 스택 | 경로 / URL |
| --- | --- | --- | --- |
| Orchestration | 공통 문서, 계약, ADR, 통합 구성 | Markdown, Docker Compose 예정 | 현재 디렉터리 |
| Backend | 도메인/API 구현과 자체 테스트 | Spring Boot 4.0.7, Java 21, Gradle Groovy DSL | `services/backend` / [iRead-backend](https://github.com/iRead-B105/iRead-backend) |
| Frontend | UI 구현과 자체 테스트 | Vue 3, TypeScript, Vite, pnpm | `services/frontend-web` / [iRead-frontend-web](https://github.com/iRead-B105/iRead-frontend-web) |
| AI server | AI 기능 구현과 자체 테스트 | FastAPI, Python 3.12, uv | `services/ai` / [iRead-ai](https://github.com/iRead-B105/iRead-ai) |
| 아동 앱 | 아동용 애플리케이션 구현과 자체 테스트 | [TBD] | `services/frontend-app` / [iRead-frontend-app](https://github.com/iRead-B105/iRead-frontend-app) |
| 시선 추적 | Tobii 기반 시선 수집·보정 프로토타입 | FastAPI, HTML/CSS/JavaScript, C++ | `services/eyetracking` / [iRead-eyetracking](https://github.com/iRead-B105/iRead-eyetracking) |

## 소유권 원칙

- 서비스 내부 구현과 단위 테스트는 해당 서비스 저장소가 소유한다.
- 서비스 간 API/이벤트 계약, 호환성 정책과 통합 실행 방법은 오케스트레이션 저장소가 소유한다.
- 승인 기능 명세와 서비스 간 계약은 오케스트레이션 저장소가 소유하고 [계약 카탈로그](../../contracts/catalog.md)에서 기준 원본과 이전 상태를 관리한다.
- Backend migration은 실행 가능한 MySQL 스키마를 소유하고 오케스트레이션 저장소에는 검토용 스냅샷을 둔다.
- submodule clone과 참조 갱신은 [submodule 운영 가이드](../workflows/submodules.md)를 따른다.
- 모든 저장소의 브랜치와 커밋 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 공통 기준으로 사용한다.

## 저장소 구성 현황

- [x] 서비스명과 오케스트레이션 저장소명 `iRead` 확정
- [x] 오케스트레이션 저장소 Git 초기화 및 원격 연결
- [x] `main`, `develop` 브랜치 구성
- [x] Backend, Frontend, AI server, 아동 앱, 시선 추적 저장소명 확정
- [x] submodule 디렉터리 배치 확정
- [x] 각 저장소 생성 및 기본 브랜치 정책 확정
- [x] submodule 연결
- [x] clone, update, 통합 검증 절차 문서화
