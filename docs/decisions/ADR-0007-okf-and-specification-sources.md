---
type: Architecture Decision
title: "ADR-0007: OKF 문서 체계와 명세 기준 원본"
description: 문서를 OKF로 관리하고 기능·API·데이터베이스 명세의 기준 원본과 파생 관계를 정의한 결정입니다.
tags: [documentation, okf, api, database, contracts, adr]
timestamp: 2026-07-24T00:00:00+09:00
---
# ADR-0007: OKF 문서 체계와 명세 기준 원본

- 상태: accepted
- 결정일: 2026-07-24
- 결정자: 사용자
- 대체 대상: [저장소 전략](../architecture/repository-strategy.md)의 계약 원본 미결 항목

## 배경

기능 명세와 API 명세는 Notion에서 관리되고 SQL은 오케스트레이션 저장소에 존재한다. 같은 내용을 여러 위치에서 수동 편집하면 승인된 계약과 구현이 서로 달라질 수 있다. 사람과 AI 에이전트가 동일한 문서를 탐색하고 변경 이력을 검토할 수 있는 형식도 필요하다.

## 결정 기준

- 문서는 사람과 AI 에이전트가 별도 도구 없이 읽을 수 있어야 한다.
- 명세마다 하나의 기준 원본과 명시적인 파생 방향이 있어야 한다.
- 계약은 Git diff와 PR로 검토할 수 있어야 한다.
- OpenAPI와 SQL 같은 도메인 형식을 일반 문서 형식으로 대체하지 않아야 한다.

## 검토한 대안

1. Notion, Markdown과 SQL을 각각 독립된 기준 원본으로 유지한다.
2. 별도 OKF 복사본을 생성해 기존 문서와 병행한다.
3. 기존 Markdown을 OKF 개념 문서로 전환하고 도메인 계약을 연결한다.

## 결정

- `docs/`를 Open Knowledge Format v0.1 지식 번들로 관리한다.
- 저장소가 관리하는 Markdown 개념 문서는 `type`, `title`, `description`, `tags`, `timestamp` frontmatter를 갖는다.
- `index.md`와 `log.md`는 OKF 예약 파일로 사용한다.
- 기능 명세의 승인 기준선은 `docs/product/features/`에 저장한다.
- 서비스 간 HTTP API 계약의 목표 기준 원본은 `contracts/openapi/`의 OpenAPI 문서다.
- MySQL 실행 스키마의 기준 원본은 Backend migration이며, `contracts/database/schema.sql`은 검토용 스냅샷이다.
- Notion은 초안 작성과 탐색에 사용한다. 저장소 기준선으로 이전된 명세는 저장소에서 먼저 변경한 뒤 Notion을 동기화한다.
- Notion의 활성 API는 OpenAPI로 내보내며 `x-notion-*` 확장 필드로 원본과 기능 관계를 추적한다.
- 의미 검토가 남은 operation은 `x-review-status: needs-review`로 표시하고 Notion 원본과 함께 검토한다.
- Backend–AI 내부 API는 실제 경로와 인증 방식이 확정되기 전까지 `[TBD]`로 유지한다.

## 영향

### 긍정적 영향

- 문서와 계약을 Git으로 함께 검토할 수 있다.
- AI 에이전트가 frontmatter와 인덱스를 이용해 필요한 지식만 탐색할 수 있다.
- 기능, API와 데이터 모델 사이의 추적 관계를 명시할 수 있다.

### 부정적 영향과 트레이드오프

- Notion과 생성된 OpenAPI·기능 카탈로그의 동기화 도구를 유지해야 한다.
- 저장소와 Notion 동기화 절차가 필요하다.
- OKF v0.1이 초안이므로 규격 변경을 추적해야 한다.

## 검증 및 재검토 조건

- 하네스 검증은 저장소 관리 개념 문서의 frontmatter와 예약 파일 구조를 확인한다.
- OpenAPI, migration과 교차 추적 검증은 하네스 구조 검사와 분리한다.
- OKF의 호환되지 않는 새 버전을 채택할 때 새 ADR로 이 결정을 대체한다.

# Citations

[1] [Open Knowledge Format v0.1 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
