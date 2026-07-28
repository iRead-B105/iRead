---
type: Execution Plan
title: "Azure Speech 단어 단위 발음 평가 연동"
description: "AI server가 Azure Speech Pronunciation Assessment를 호출하고 Backend가 단어별 정확도 근거를 저장·집계하도록 전환하는 실행 계획입니다."
tags: [plan, azure, speech, pronunciation, backend, ai, mysql]
timestamp: 2026-07-28T00:00:00+09:00
---
# Azure Speech 단어 단위 발음 평가 연동

- 상태: active
- 작성일: 2026-07-28
- 수정일: 2026-07-28
- 관련 결정: [ADR-0013](../docs/decisions/ADR-0013-azure-speech-pronunciation-assessment.md)
- 대상: `services/backend`, `services/ai`, `services/app`

## 목표

App이 업로드한 한국어 읽기 음성을 AI server가 Azure Speech `ko-KR` scripted Pronunciation Assessment로 분석하고, Backend가 단어별 `AccuracyScore`와 문항 위치를 저장해 종합 점수와 읽기 특징 프로필의 발음 근거로 사용한다.

## 범위

### 포함

- 검사·훈련 multipart 음성 업로드와 Backend 소유권·상태·파일 검증
- Backend–AI 발음 분석 계약의 Azure 단어 정확도 모델 정합화
- AI server의 Azure Speech adapter, 자격증명·timeout·오류 변환
- Azure 단어 결과와 Backend 기준 단어·토큰 위치 정렬
- `word_attempt_logs.pronunciation_accuracy_score`와 문항 위치·최종 시도 저장
- 전체 발화 점수의 부모 `result` JSON 저장 여부와 종합 점수 정책 확정
- Mock·실제 Azure adapter의 계약 테스트

### 제외

- 음성 원본 영구 저장
- App의 Azure 직접 호출과 Azure 자격증명 보유
- 한국어에서 지원하지 않는 음절명·음소명·Prosody 기반 피드백
- Azure 원본 응답 전체의 MySQL 영구 저장

## 확정 계약

- App은 점수·정오 여부·음성 인식 문자열을 제출하지 않는다.
- API의 발음 정확도는 `0~100`, MySQL은 `AccuracyScore × 10`을 반올림한 `0~1000`을 사용한다.
- 단어 점수는 `pronunciation_accuracy_score`, 발음·시선·읽기 수행 종합 점수는 `total_score`에 분리한다.
- `question_no`는 1부터, `target_index`와 `token_index`는 0부터 시작한다.
- 같은 문항·대상·토큰 위치에서는 마지막 성공 시도만 `is_final=true`다.
- Azure 실패 시 새 단어 시도와 이전 최종 시도 변경을 커밋하지 않는다.
- Azure 자격증명은 AI server 런타임 비밀값으로만 주입한다.

## 작업

- [ ] **AZ-SP-001** 확정 ERD의 단어 발음 정확도·문항 위치·최종 시도 컬럼을 MySQL 계약과 Backend 엔티티에 동기화한다.
- [x] **AZ-SP-002** App 녹음 계약에서 `recognizedText`, 예상·관찰 발음 문자열과 클라이언트 제출 점수를 제거한다.
- [ ] **AZ-SP-003** Backend–AI 응답을 전체 발화 결과와 `words[]` 단어 결과로 확장하고 토큰 정렬 오류 계약을 확정한다.
- [ ] **AZ-SP-004** AI server에 Azure Speech SDK 또는 REST adapter와 `ko-KR`, `HundredMark`, `Word`, miscue 설정을 구현한다.
- [ ] **AZ-SP-005** Azure 자격증명, region, endpoint, timeout을 환경변수로 주입하고 로그·응답 노출을 차단한다.
- [ ] **AZ-SP-006** Backend가 Azure `Offset`·`Duration`을 ms로 변환하고 단어별 시도 행을 원자적으로 저장한다.
- [ ] **AZ-SP-007** `Insertion`, `Omission`, 단어 분리 불일치와 낮은 점수의 제품 정책을 확정한다.
- [ ] **AZ-SP-008** 발음·시선·읽기 시간·정답을 결합하는 `total_score` 가중치와 하위 호환 정책을 확정한다.
- [ ] **AZ-SP-009** App 녹음 화면을 새 multipart 요청과 단어별 결과 응답에 연결한다.
- [ ] **AZ-SP-010** 실제 Azure sandbox와 결정적 Mock으로 계약·장애·보안·비용 검증을 완료한다.

## 검증

- Backend 전체 테스트와 MySQL 8.4 Flyway·Hibernate schema validation
- AI server Azure adapter의 한국어 정상·누락·삽입·낮은 점수 fixture
- App–Backend와 Backend–AI OpenAPI 계약 검증
- Azure 401·429·5xx·timeout 시 DB 미저장과 임시 파일 삭제
- Azure `Offset`, `Duration` 100ns→ms 변환과 토큰 순서 검증
- Azure 키·음성 본문·전체 응답이 로그와 API에 노출되지 않는지 검사
- Mock과 실제 adapter가 같은 내부 응답 스키마를 따르는지 검사

## 2026-07-28 준비 변경 검증

- `python tools/validate_contracts.py`: 81 operations, 334 features, 25 MySQL tables, 34 foreign keys 검증 성공
- `python tools/validate_harness.py`: 87 Markdown files와 35 record documents 검증 성공
- Backend `.\gradlew.bat test`: 성공
- MySQL 통합 테스트는 실행 환경이 없어 opt-in 상태로 제외됐다. 실제 MySQL 8.4 Flyway·Hibernate 검증 전까지 `AZ-SP-001`은 완료 처리하지 않는다.

## 미결 사항

- [TBD] Azure `Mispronunciation` 기준과 제품 정답 임계값 700점의 관계
- [TBD] `total_score` 최종 가중치
- [TBD] 전체 발화 점수 중 `AccuracyScore`, `FluencyScore`, `CompletenessScore`, `PronScore`의 저장 범위
- [TBD] Azure 호출 지역과 데모 사용량·비용 상한

## 롤백

- 실제 Azure adapter를 비활성화하고 결정적 Mock adapter로 전환한다.
- Azure 호출 실패 시 기존 최종 단어 시도와 학생 특징 프로필을 유지한다.
- DB 컬럼은 nullable이므로 Azure 비활성 상태에서도 선택형 훈련과 기존 종합 점수 흐름을 유지한다.
