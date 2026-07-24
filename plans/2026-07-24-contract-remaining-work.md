---
type: Execution Plan
title: "기능·API·MySQL 계약 후속 작업"
description: "Notion에서 이전한 기능·API 계약과 MySQL 스키마를 구현 가능한 상태로 마무리하기 위한 남은 작업을 정리합니다."
tags: [plan, contracts, notion, openapi, mysql]
timestamp: 2026-07-24T00:00:00+09:00
---
# 기능·API·MySQL 계약 후속 작업

- 상태: active
- 담당: [TBD]
- 작성일: 2026-07-24
- 수정일: 2026-07-24

## 기대 결과

검수 대기 API가 서버 계약, 기존 API 통합 또는 클라이언트 책임으로 확정되고 Backend–AI 계약과 MySQL migration이 실행 가능한 기준 원본으로 관리된다.

## 현재 상태

- Notion 활성 API 115건과 기능 334건을 저장소로 이전했다.
- 계약 검증 기준으로 API 63건은 검토 완료, 52건은 의미 검토가 필요하다.
- MySQL 8.4.x LTS 스키마는 테이블 24개와 외래 키 25개를 포함한다.
- 별도 이야기 진행률·완료 API는 음성 분기 생성 API로 통합했다.
- `우선순위`와 `구현여부` Notion 속성은 동기화 범위에서 제외한다.

## 필수 작업

### 구현 전

- [ ] 기존 API와 중복된 22건을 정식 도메인 API로 통합한다.
- [ ] 화면 이동·선택·재생 상태 등 클라이언트 책임 API 11건을 활성 서버 계약에서 제거한다.
- [ ] 서버 계약 상세화 대상 14건의 요청·응답, 타입, 필수 여부, 오류 코드를 ERD와 대조한다.
- [ ] 경로 정규화 대상 3건을 REST 명령 의미에 맞게 수정한다.
- [ ] 검사·훈련의 초기화와 제출 계약 2건을 정리한다.
- [ ] 변경한 Notion 기능 관계, OpenAPI와 추적 데이터를 다시 생성하고 검증한다.
- [ ] STT, 이야기 생성, 진행률 반환, TTS와 시선 분석을 포함하는 Backend–AI 내부 API를 정의한다.
- [ ] 현재 스키마를 Backend의 Flyway 또는 Liquibase migration으로 이전한다.
- [ ] MySQL 8.4.x에서 migration과 제약조건을 실제 실행 검증한다.

### 운영 배포 전

- [ ] EC2 음성 파일의 보관 기간, 삭제 정책과 경로 접근 권한을 확정한다.
- [ ] 개인정보와 보고서 스냅샷 보존 기간을 확정한다.
- [ ] MySQL 백업·복구와 운영 토폴로지를 확정한다.
- [ ] API 권한 검증과 로그 개인정보 제거 기준을 확정한다.

## 선택 작업

- [ ] SQL 테이블 명칭과 `training_datas`, `test_datas` 명칭을 일관되게 개선한다.
- [ ] OpenAPI 공통 스키마를 `components`로 추출한다.
- [ ] ERD 이미지와 문서 사이트를 자동 생성한다.
- [ ] Notion 정기 동기화와 API 호환성 검사를 자동화한다.
- [ ] Redis 역할과 아동 앱 기술 스택을 확정한다.
- [ ] 음성 파일을 EC2 로컬 디스크에서 객체 스토리지로 이전하는 방안을 검토한다.

## 확인이 필요한 사항

- 33건의 API 통합·제거는 [API 검토 목록](../contracts/review-queue.md)의 권장안을 적용한다.
- 나머지 19건에서 ERD만으로 결정할 수 없는 제품 동작이 발견될 때만 사용자에게 질문한다.
- migration 도구는 Backend 초기 구조와 함께 Flyway와 Liquibase 중 하나를 선택한다.

## 예상 소요

- 기능·API·SQL 명세 완료: 6~10시간
- Backend migration 작성과 MySQL 실행 검증: 추가 1~2일
- 운영·보안 정책 문서화: 추가 0.5~1일

## 검증

- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- `git diff --check`
- MySQL migration 도입 후 MySQL 8.4.x 임시 환경에서 전체 migration 실행

## 진행 기록

- 2026-07-24: 기능 334건, 활성 API 115건과 MySQL 스키마 기준선을 확립했다.
- 2026-07-24: 검수 대기 API 52건을 처리 성격별로 분류했다.

## 결정 및 변경 사항

- [ADR-0006](../docs/decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용한다.
- [ADR-0007](../docs/decisions/ADR-0007-okf-and-specification-sources.md)에 따라 저장소 계약을 구현 기준 원본으로 관리한다.

## 남은 위험

- Backend–AI 내부 API의 경로, 인증, 타임아웃과 재시도 정책이 아직 정의되지 않았다.
- 실제 MySQL 실행 검증 전에는 DDL의 환경별 호환성을 보장할 수 없다.
- 운영 보존 정책이 확정되지 않아 개인정보와 음성 데이터 삭제 기준이 미정이다.
