---
type: Execution Plan
title: "데모 Flyway 기준선 통합"
description: "재생성 가능한 데모 migration을 V1·V2 기준선에 통합하고 다음 신규 migration이 V3부터 시작하도록 정리합니다."
tags: [plan, backend, flyway, mysql, demo, migration]
timestamp: 2026-07-30T00:00:00+09:00
---
# 데모 Flyway 기준선 통합

- 상태: completed
- 작성일: 2026-07-30
- 수정일: 2026-07-30
- 대상: `services/backend`

## 범위

- `db/demo/V3~V10`의 최종 데이터를 `V2__demo_seed.sql`에 통합한다.
- 기존 V11의 시선 분석 상세 컬럼은 빈 DB 스키마 기준선인 V1에 통합한다.
- 빈 MySQL에서 V1과 V2만으로 데모 Flyway가 성공하도록 선행 템플릿 참조를 해소한다.
- 데모 기준선을 다시 압축할 수 있는 조건과 기존 DB 재생성 요구사항을 문서화한다.
- 애플리케이션 런타임 초기화 로직은 변경하지 않는다.

## 작업

- [x] V3~V11의 순서와 데이터·스키마 의존성을 확인한다.
- [x] V2에 필요한 무음성 훈련 템플릿을 선행 배치한다.
- [x] V3~V10을 V2에, V11의 스키마를 V1에 통합하고 개별 migration 파일을 제거한다.
- [x] 빈 MySQL에서 Flyway, Hibernate와 데모 seed를 검증한다.
- [x] 기존 데모 DB 재생성 조건과 다음 V3 규칙을 문서화한다.

## 검증

- Backend 전체 테스트
- MySQL 8.4 `MySqlFlywayIntegrationTest`
- MySQL 8.4 `MySqlDemoSeedIntegrationTest`
- 계약·ERD·문서 하네스와 `git diff --check`

## 롤백

- Backend 커밋을 되돌리고 빈 데모 DB를 다시 생성한다.
- 이미 적용한 공유 DB의 Flyway 이력은 직접 수정하지 않는다.

## 미결 사항

- 없음

## 완료 기록

- 데모 데이터 Flyway 파일을 `V2__demo_seed.sql` 하나로 통합했다.
- V11의 시선 분석 상세 JSON 컬럼은 `V1__baseline_schema.sql`에 통합했다.
- 기존 V9가 Flyway 이후 초기화에 의존하던 템플릿 4, 5, 7, 8, 11을 V2에서 선행 생성하도록 수정했다.
- 빈 MySQL 8.4에서 V1, V2 적용, `MySqlFlywayIntegrationTest`,
  `MySqlDemoSeedIntegrationTest`와 H2 `DemoSeedIntegrationTest`를 검증했다.
- 기존 V3~V11 적용 DB는 삭제 후 재생성하고 다음 신규 migration은 V3부터 사용하도록 운영 규칙을 기록했다.
