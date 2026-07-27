---
type: Architecture Decision
title: "ADR-0011: 확정 ERD를 단일 V1 기준선으로 채택"
description: "ERDCloud에서 확정한 23개 테이블 설계를 MySQL 계약과 Flyway 단일 V1의 기준선으로 채택한 결정입니다."
tags: [architecture, database, mysql, erd, flyway]
timestamp: 2026-07-27T00:00:00+09:00
---
# ADR-0011: 확정 ERD를 단일 V1 기준선으로 채택

- 상태: accepted
- 결정일: 2026-07-27
- 결정자: 사용자
- 대체 대상: 2026-07-27 이전의 미적용 MySQL V1 초안

## 배경

Backend 구현과 API 검토 과정에서 기존 ERD에 없는 테이블·컬럼과 명칭 변경이 V1 초안에 포함됐다. 실제 DB에는 아직 스키마와 데이터가 적용되지 않았으므로 증분 V2보다 확정 ERD를 기준으로 V1을 다시 구성할 수 있다.

사용자는 기존 명칭과 단수·복수형을 최대한 유지하고 필수 MySQL 타입·제약조건만 실행 DDL에 반영한 ERD를 확정했다.

## 결정

- [확정 ERD 이미지](../../contracts/database/erd.png)의 23개 테이블과 관계를 현재 데이터 모델로 채택한다.
- 실행 기준 원본은 Backend Flyway `V1__baseline_schema.sql` 하나로 유지한다.
- `contracts/database/schema.sql`은 V1과 동일한 계약 미러로 관리한다.
- ERDCloud가 COMMENT로 표현한 `AUTO_INCREMENT`, `UNIQUE`, `DEFAULT`, `CHECK`는 실행 DDL의 실제 속성·제약조건으로 변환한다.
- ERD 관계선은 외래 키로 변환하고 FK에 복사된 `AUTO_INCREMENT` 메타데이터는 적용하지 않는다.
- `training_datas`, `train_id`, `test_datas`, `tests`, `story_lines.has_choices` 명칭을 유지한다.
- `teachers.email`을 유일한 교사 로그인 식별자로 사용하고 인증 테이블은 `auth_refresh_sessions`만 사용한다.
- 실제 DB에 적용하기 전이므로 V2를 만들지 않고 V1을 교체한다.

## 영향

- `story_scenes`, `story_choices`, `test_curriculums`가 기준선에 포함된다.
- 이전 초안의 `student_study_progresses`, `student_word_stats`, 파일 메타데이터 테이블과 `character.is_representative`는 기준선에서 제외된다.
- 검사, 이야기, 캐릭터, 보고서와 시선 엔티티는 새 계약에 맞춘 Backend 정합화가 필요하다.
- 대표 캐릭터 상태는 서버에 저장하지 않고 관련 API를 제거하며, 필요한 표시 상태는 클라이언트가 관리한다.
- `story_choices`에는 분기 대사별 최종 STT 텍스트 한 건을 저장하고 `story_line_id`를 UNIQUE로 보호한다.

## 후속 결정

- 2026-07-27: 대표 캐릭터 서버 API를 제거하고 관련 표시 상태를 클라이언트 책임으로 변경했다.
- 2026-07-27: `story_choices`는 분기 대사별 최종 STT 텍스트 한 건을 저장하며 `story_line_id`를 UNIQUE로 보호한다.
- 2026-07-27: 성장 정보는 별도 컬럼 없이 완료된 훈련을 학생·훈련 템플릿별로 실시간 집계하고 꽃 성장 단계는 클라이언트가 계산한다.
- 2026-07-27: 꽃은 훈련 템플릿별 완료 1회마다 한 단계 성장하고 총 5회에 만개하며 이후 만개 상태를 유지한다.
- 2026-07-27: 같은 이야기 분기 대사의 네트워크 재시도는 최초 저장 결과를 `200 OK`로 반환하고 `replayed`로 재사용 여부를 알린다.

## 검증

- 계약 스키마와 Flyway V1의 동일성을 검사한다.
- 생성 ERD가 23개 테이블과 31개 외래 키를 포함하는지 검사한다.
- Backend 정합화 후 빈 MySQL 8.4 실행과 Hibernate schema validation을 수행한다.
