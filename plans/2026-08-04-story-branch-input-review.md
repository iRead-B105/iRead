---
type: Execution Plan
---
# 이야기 음성 분기 입력 경량 LLM 검토

- 상태: completed
- 수정일: 2026-08-04

## 범위

- STT 원문을 자동 교정하지 않고 현재 분기 질문에 대한 관련성과 아동 안전성을 경량 LLM으로 판정한다.
- `ALLOW`, `CONFIRM`, `RETRY`, `BLOCK`의 구조화된 판정과 제한된 사유 코드를 Backend–AI 및 App 계약에 추가한다.
- `BLOCK` 입력은 이야기 생성과 최종 선택 저장에서 제외하고, 아동에게 중립적인 재녹음 또는 기존 버튼 선택지를 제공한다.
- 별도 STT 신뢰도·길이 기반 비즈니스 검증 단계는 제거하되, 요청 크기·필수값·API 스키마 같은 기술적 계약 검증은 유지한다.
- 교사 알림, 자동 신고, STT 문장 교정과 차단 원문의 별도 저장은 이번 범위에서 제외한다.

## 작업

- [x] 제품 기능 명세와 App·Backend–AI OpenAPI 계약을 갱신한다.
- [x] AI server에 최소 입력·구조화 출력 기반 분기 입력 검토 기능을 추가한다.
- [x] Backend가 STT 직후 검토를 호출하고 허용된 원문만 최종 분기로 제출하도록 보호한다.
- [x] 아동 App이 판정별로 확인·재녹음·버튼 선택 UX를 제공하도록 갱신한다.
- [x] 관련 서비스 테스트와 계약·하네스 검증을 실행한다.

## 검증

- `services/ai`: 분기 입력 판정 단위·API 테스트
- `services/backend`: Story 서비스·컨트롤러 및 AI client 관련 테스트
- `services/frontend-app`: 이야기 repository·화면 관련 테스트, 타입 검사 또는 빌드
- 루트: `python tools/validate_contracts.py`, `python tools/validate_harness.py`

## 미결 사항

- [TBD] 반복적인 자해·위협 발화의 교사 알림과 보호자·기관 연계 정책은 동의, 보관과 오탐 대응 기준이 정해질 때까지 보류한다.
