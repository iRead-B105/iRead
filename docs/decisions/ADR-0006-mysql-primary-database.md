---
type: Architecture Decision
title: "ADR-0006: 주 데이터베이스로 MySQL 채택"
description: iRead의 영구 관계형 데이터 저장소로 MySQL을 채택한 결정입니다.
tags: [architecture, database, mysql, adr]
timestamp: 2026-07-24T00:00:00+09:00
---
# ADR-0006: 주 데이터베이스로 MySQL 채택

- 상태: accepted
- 결정일: 2026-07-24
- 결정자: 사용자
- 대체 대상: [ADR-0002](ADR-0002-technology-baseline.md)의 주 데이터베이스 미결 범위

## 배경

기능 명세와 API 명세를 ERD에 맞춰 검토하려면 SQL 방언과 실행 기준을 확정해야 한다. 기존 문서는 주 데이터베이스를 미결 상태로 유지했으나, 사용자가 MySQL 채택을 확정했다.

## 결정 기준

- 관계형 학습·보고서·이야기 데이터를 일관되게 저장할 수 있어야 한다.
- Backend의 migration으로 재현 가능한 스키마 변경 이력을 관리할 수 있어야 한다.
- 개발·검증 환경에서 동일한 DDL을 실행할 수 있어야 한다.

## 검토한 대안

1. 데이터베이스 결정을 계속 미룬다.
2. MySQL 8.4.x LTS를 주 데이터베이스로 채택한다.

## 결정

- 주 데이터베이스로 MySQL 8.4.x LTS를 채택하고 배포 시점의 최신 8.4 패치 버전을 사용한다.
- 운영 토폴로지는 `[TBD]`로 유지한다.
- Backend 구현이 시작되면 `services/backend`의 migration을 실행 가능한 스키마 기준 원본으로 사용한다.
- 오케스트레이션 저장소의 SQL은 migration에서 생성하거나 검토 시점에 고정한 스키마 스냅샷으로 관리한다.

## 영향

### 긍정적 영향

- SQL 문법과 데이터 타입 검증 기준이 명확해진다.
- API와 ERD의 필드 매핑을 일관되게 검토할 수 있다.
- migration 기반 배포와 롤백 계획을 수립할 수 있다.

### 부정적 영향과 트레이드오프

- MySQL에 종속된 DDL과 제약조건을 관리해야 한다.
- 8.4 LTS에서 제거되거나 변경된 8.0 기능이 있는지 migration 도입 시 검토해야 한다.

## 검증 및 재검토 조건

- 임시 MySQL 환경에서 모든 migration이 순서대로 실행되어야 한다.
- 다른 데이터베이스로 변경하려면 새 ADR로 이 결정을 대체한다.

# Citations

- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/)
- [MySQL LTS와 Innovation 릴리스 정책](https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html)
