---
type: Architecture Decision
title: "ADR-0004: 서비스 저장소 구성"
description: "서비스 저장소명과 submodule 배치 경로를 정한 결정입니다."
tags: [architecture, repository, submodule, adr]
timestamp: 2026-07-24T00:00:00+09:00
---
# ADR-0004: 서비스 저장소 구성

- 상태: accepted
- 결정일: 2026-07-15

## 배경

독립적으로 생성한 Backend, Frontend, AI server 저장소를 오케스트레이션 저장소에서 일관된 경로로 조율해야 한다.

## 결정

| 서비스 | 저장소 | submodule 경로 |
| --- | --- | --- |
| Backend | `iRead-B105/iRead-backend` | `services/backend` |
| Frontend | `iRead-B105/iRead-frontend-web` | `services/frontend-web` |
| AI server | `iRead-B105/iRead-ai` | `services/ai` |

- 세 submodule은 원격 `develop`을 갱신 기준으로 사용한다.
- 오케스트레이션 저장소는 각 서비스의 검토된 특정 커밋을 기록한다.
- 공통 로컬 통합 구성은 오케스트레이션 저장소가 관리한다.
- 별도 infra 저장소는 배포 환경과 운영 요구사항이 구체화될 때 검토한다.

## 영향

- 서비스 저장소의 독립적인 이력과 개발 주기를 유지할 수 있다.
- `services/` 아래에 외부 저장소를 모아 루트 디렉터리의 역할을 명확하게 유지한다.
- clone과 브랜치 전환 시 submodule 초기화 및 동기화가 필요하다.
- 서비스 커밋과 오케스트레이션의 참조 커밋을 각각 관리해야 한다.

## 검토한 대안

- 루트에 `backend`, `frontend`, `ai`를 바로 배치하는 방식은 저장소 역할이 늘어날수록 루트 구성이 복잡해질 수 있어 채택하지 않았다.
- `submodules/` 경로는 구현 서비스라는 의미보다 Git 관리 방식이 앞에 드러나 채택하지 않았다.
