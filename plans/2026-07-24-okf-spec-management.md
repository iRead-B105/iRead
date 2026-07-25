---
type: Execution Plan
title: OKF·명세 관리 체계 도입
description: 저장소 문서를 OKF로 전환하고 MySQL과 계약 기준 원본을 정리하는 실행 계획입니다.
tags: [plan, okf, documentation, contracts, mysql]
timestamp: 2026-07-24T00:00:00+09:00
---
# OKF·명세 관리 체계 도입

- 상태: completed
- 담당: Codex
- 작성일: 2026-07-24
- 수정일: 2026-07-24

## 기대 결과

저장소 관리 문서가 OKF v0.1로 탐색 가능하고, 기능·API·MySQL 명세의 기준 원본과 전환 상태가 명확하다.

## 작업 단계

- [x] OKF v0.1 규격 확인
- [x] MySQL과 명세 관리 ADR 작성
- [x] 기존 문서에 OKF frontmatter 적용
- [x] 인덱스와 로그 구성
- [x] 하네스 검증 확장
- [x] 하네스 검증 실행

## 검증

- `python tools/validate_harness.py`
- 내부 링크, OKF frontmatter와 예약 파일 구조 확인

## 진행 기록

- 2026-07-24: 사용자가 MySQL과 권장 명세 관리안을 승인했다.
- 2026-07-24: OKF v0.1 공식 규격을 확인했다.
- 2026-07-24: 39개 OKF 개념 문서와 예약 인덱스·로그 검증을 완료했다.

## 결정 및 변경 사항

- [ADR-0006](../docs/decisions/ADR-0006-mysql-primary-database.md)
- [ADR-0007](../docs/decisions/ADR-0007-okf-and-specification-sources.md)

## 남은 위험

- Notion API의 저장소 OpenAPI 이전과 Backend Flyway V1 도입은 후속 계획에서 완료했다.
- Notion은 이관 출처로 보존하며 별도 요청 없이 Git 계약을 역동기화하지 않는다.
