---
type: Architecture Decision
title: "ADR-0013: Azure Speech 단어 단위 발음 평가 채택"
description: "한국어 읽기 음성을 Azure Speech Pronunciation Assessment로 평가하고 단어 정확도 점수를 저장하는 서비스 경계와 데이터 정책을 정의합니다."
tags: [architecture, azure, speech, pronunciation, ai, privacy]
timestamp: 2026-07-28T00:00:00+09:00
---
# ADR-0013: Azure Speech 단어 단위 발음 평가 채택

- 상태: accepted
- 결정일: 2026-07-28
- 결정자: 사용자
- 대체 대상: Backend 결정적 발음 분석 Mock을 운영 분석기로 사용하는 설계

## 배경

일반 STT의 맞춤법 전사 결과만으로는 표기와 실제 발음이 다른 한국어 단어의 발음 정확도를 판정할 수 없다. 기존 `recognized_text`, 예상 발음과 관찰 발음 문자열을 비교하는 방식은 실제 음성 근거를 제공하지 못한다.

Azure Speech Pronunciation Assessment는 `ko-KR`을 지원하고 scripted assessment에서 기준 텍스트에 대한 단어 수준 `AccuracyScore`와 `ErrorType`을 반환한다.

- [Azure Speech 발음 평가 사용](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/how-to-pronunciation-assessment)
- [Azure Speech 발음 평가 지원 언어](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=pronunciation-assessment)

## 결정 기준

- 기준 문장을 읽는 아동의 단어별 정확도 점수를 제공해야 한다.
- Azure 자격증명과 음성 원본을 App에 노출하지 않아야 한다.
- 음성 원본은 분석 요청 동안만 보유하고 성공·실패 후 저장하지 않아야 한다.
- 기존 단어 수행·특징 프로필 모델과 `0~1000` 점수 체계를 유지해야 한다.
- Azure 장애 시 불완전한 수행 근거를 저장하지 않아야 한다.

## 검토한 대안

1. 일반 STT 전사와 기준 텍스트를 문자열로 비교한다.
   - 표기와 실제 발음을 구분하지 못하므로 제외한다.
2. App이 Azure Speech를 직접 호출한다.
   - 자격증명 노출, 요청 위변조와 아동 음성 통제 문제 때문에 제외한다.
3. Backend가 Azure Speech를 직접 호출한다.
   - 구현은 단순하지만 기존 Backend–AI 음성 분석 경계를 중복하므로 제외한다.
4. AI server가 Azure Speech를 호출하고 Backend가 내부 계약으로 결과를 받는다.
   - 기존 서비스 경계를 유지하고 Azure 자격증명을 AI server에 한정할 수 있어 채택한다.

## 결정

- App은 검사·훈련 녹음 파일과 대상 위치만 Backend에 multipart로 전송한다.
- Backend는 소유권, 훈련·검사 상태, 대상 단어와 파일 형식을 검증한 후 AI server의 발음 분석 API를 호출한다.
- AI server는 Azure Speech 자격증명을 보유하고 `ko-KR` scripted Pronunciation Assessment를 실행한다.
- Azure 설정은 `referenceText`, `GradingSystem=HundredMark`, `Granularity=Word`, `EnableMiscue=true`를 기준으로 한다.
- 단어별 `AccuracyScore`는 API에서 `0~100`, MySQL `word_attempt_logs.pronunciation_accuracy_score`에서 반올림한 `0~1000` 정수로 저장한다.
- `word_attempt_logs.total_score`는 발음·시선·읽기 수행을 결합한 종합 단어 점수로 유지하며 Azure 점수를 그대로 대입하는 전용 컬럼으로 사용하지 않는다.
- `recognized_text`, 예상 발음과 관찰 발음 문자열은 단어 수행 근거로 저장하지 않는다.
- Azure 단어 `Offset`과 `Duration`은 100ns 단위에서 ms로 변환해 음성 시작·종료 위치에 저장한다.
- 전체 발화의 `AccuracyScore`, `FluencyScore`, `CompletenessScore`, `PronScore`가 필요하면 `trainings.result` 또는 `tests.result`에 분석 메타데이터로 저장하며 단어 점수 컬럼에 복제하지 않는다.
- 한국어에서는 en-US 전용 음절명·음소명·Prosody 기능을 계약 필수값으로 사용하지 않는다.
- Azure 또는 AI server 호출이 실패하거나 시간 초과되면 단어 시도 행과 최종 시도 상태를 저장하지 않는다.
- `demo` profile은 같은 입력에 같은 점수를 반환하는 Mock adapter를 유지한다.

## 영향

### 긍정적 영향

- 발음 문자열을 추정하지 않고 실제 음성 기반 단어 정확도 점수를 사용한다.
- App이 점수·정오 여부를 제출하지 않아 수행 결과 위변조 범위가 줄어든다.
- 기존 `student_feature_profiles.avg_pronunciation_scor` 집계와 `0~1000` 단위를 유지할 수 있다.

### 부정적 영향과 트레이드오프

- Azure 사용료, 네트워크 지연과 지역 장애에 영향을 받는다.
- AI server에 Azure Speech SDK 또는 REST adapter, 자격증명과 호출 관측성이 필요하다.
- Azure 단어 분리와 Backend 토큰 위치가 달라질 수 있어 기준 텍스트 순서와 오류 유형을 사용한 정렬 검증이 필요하다.
- `Omission`의 단어 정확도 점수는 유효하지 않으므로 제품 정책으로 실패 근거와 점수 환산을 정의해야 한다.

## 미결 정책

- [TBD] Azure `Mispronunciation` 기준과 제품 정답 기준 700점의 최종 관계
- [TBD] `total_score`에서 발음·시선·읽기 시간·정답의 최종 가중치
- [TBD] `Insertion`, `Omission`과 Azure 단어 분리 불일치의 상세 저장 형식

## 검증 및 재검토 조건

- `ko-KR` 아동 음성 fixture로 단어 순서, 점수 범위, 누락·삽입과 offset 변환을 검증한다.
- Azure 자격증명이 App·Backend 응답·로그와 저장소에 포함되지 않는지 검사한다.
- 성공·실패·시간 초과 후 임시 음성 파일이 남지 않는지 검사한다.
- Azure 품질·가격·지원 지역 또는 한국어 지원 기능이 변경되면 이 결정을 재검토한다.
