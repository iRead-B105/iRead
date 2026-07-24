---
type: Workflow
title: 명세 관리 워크플로
description: 기능, API, MySQL 스키마와 Notion 파생 문서를 일관되게 변경하는 절차입니다.
tags: [workflow, feature-spec, openapi, mysql, notion]
timestamp: 2026-07-24T00:00:00+09:00
---
# 명세 관리 워크플로

- 상태: accepted
- 최종 검토일: 2026-07-24

## 기준 원본

| 대상 | 기준 원본 | 파생 또는 협업 위치 |
| --- | --- | --- |
| 승인된 기능 명세 | `docs/product/features/` | Notion 기능 명세 데이터베이스 |
| HTTP API 계약 | `contracts/openapi/` | Notion API 명세 데이터베이스, 서비스 구현 코드 |
| MySQL 실행 스키마 | `services/backend`의 migration | `contracts/database/schema.sql`, ERD |
| 주요 기술·제품 결정 | `docs/decisions/` | 관련 컨텍스트와 Notion 설명 |
| 계약 상태와 이전 현황 | `contracts/catalog.md` | 각 인덱스 |

OpenAPI로 아직 이전하지 않은 Notion API는 전환 기간의 운영 원본이다. 불완전한 OpenAPI 파일을 기준 원본처럼 만들지 않고, 엔드포인트 단위로 요청·응답·오류·보안 계약을 검토한 뒤 이전한다.

## 기능 변경

1. Notion에서 초안을 작성하거나 기존 기능을 탐색한다.
2. 사용자 결정이 필요한 제품 범위와 데이터 처리를 확인한다.
3. 승인된 내용을 `docs/product/features/`의 기능 명세에 반영한다.
4. 관련 요구사항, API `operationId`, 데이터 자산과 ADR을 연결한다.
5. 저장소 기준선 변경 후 Notion의 기능 설명과 관계를 동기화한다.

## API 변경

1. 제공자, 소비자와 인증 주체를 확인한다.
2. OpenAPI로 이전된 계약은 `contracts/openapi/`를 먼저 변경한다.
3. 요청·응답, 오류, 멱등성, 시간 제한과 호환성 영향을 기록한다.
4. 기능 명세의 API 관계와 서비스 구현 영향을 확인한다.
5. 호환성을 깨는 변경은 전환 및 롤백 계획과 ADR을 작성한다.
6. Notion API 명세는 저장소 계약을 기준으로 동기화한다.

## 데이터베이스 변경

1. 기존 ERD로 API를 충족할 수 있는지 먼저 검토한다.
2. 꼭 필요한 테이블·컬럼·제약조건만 제안하고 데이터 소유자를 확인한다.
3. Backend migration을 작성하고 순서, 롤백과 기존 데이터 변환을 기록한다.
4. migration 실행 결과로 스키마 스냅샷과 ERD를 갱신한다.
5. 관련 API와 기능 명세의 필드 매핑을 동기화한다.

## 변경 추적

기능 문서는 다음 연결을 가능한 범위에서 포함한다.

```text
기능 식별자 → 요구사항 ID → OpenAPI operationId → 소유 서비스 → MySQL 테이블·컬럼
```

폐기 기능은 활성 API와 연결하지 않는다. 삭제 대신 폐기 사유와 대체 계약을 기록해 변경 이력을 유지한다.

## 검증 분리

- `tools/validate_harness.py`: OKF frontmatter, 예약 파일, 필수 문서와 내부 링크
- OpenAPI 검증: 문법, 경로 파라미터, `operationId`, 요청·응답 스키마
- MySQL 검증: 임시 MySQL에서 migration 실행, 제약조건과 스키마 차이
- 추적 검증: 기능 식별자, `operationId`와 데이터 자산 연결

소스 테스트·빌드·린트·정적 분석은 사용자가 현재 요청에서 명시적으로 요청한 경우에만 실행한다. 하네스 검증은 문서 구조 검사이므로 문서 변경 시 실행한다.

## Notion 동기화

Notion API와 기능 명세를 저장소 산출물로 갱신할 때 다음 순서를 사용한다.

```bash
python tools/export_notion_specs.py \
  --token-file <notion-token-file> \
  --output contracts/notion/spec-snapshot.json
python tools/generate_contracts.py
python tools/validate_contracts.py
python tools/validate_harness.py
```

- 확정된 제품 결정을 Notion에 재적용해야 할 때만 `tools/reconcile_notion_decisions.py --token-file <notion-token-file>`을 먼저 실행한다.
- 토큰 값과 토큰 파일은 저장소에 추가하지 않는다.
- 내보내기는 `우선순위`와 `구현여부` 속성을 읽거나 저장하지 않는다.
- 생성된 OpenAPI를 직접 수정하지 않고 Notion 원본 또는 생성 규칙을 수정한 뒤 다시 생성한다.
- `x-review-status: needs-review`인 operation은 [검토 목록](../../contracts/review-queue.md)을 따른다.
