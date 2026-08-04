---
type: Execution Plan
---
# 이야기 책장 보관·삭제 정책

- 상태: completed
- 수정일: 2026-08-04

## 범위

- 아동별 진행 중 이야기(`IN_PROGRESS`)를 최대 15권까지 보관한다.
- 완료 이야기(`COMPLETED`)는 15권 한도에서 제외하고 읽던 책 화면의 별도 탭으로 제공한다.
- 같은 이야기 템플릿의 여러 세션을 동시에 진행할 수 있다.
- 아동은 진행 중 이야기만 확인 후 소프트 삭제할 수 있으며 삭제 즉시 아동·교사 책장에서 제외한다.
- 이야기 템플릿과 표지는 삭제하지 않고 같은 종류의 새 이야기를 다시 시작할 수 있다.
- 기존 책장 카드와 페이지네이션의 시각 개선을 유지하고 카드 그림자가 목록 경계에서 잘리지 않도록 수정한다.

## 작업

- [x] 제품 기능 명세와 App OpenAPI 계약에 보관·삭제 정책을 반영한다.
- [x] Backend에 15권 시작 제한과 진행 중 이야기 소프트 삭제 API를 구현한다.
- [x] Frontend에 진행 중·완료 탭, 삭제 확인 팝업과 즉시 목록 갱신을 구현한다.
- [x] 책장 카드 그림자와 페이지네이션 UI를 브라우저에서 시각 검증한다.
- [x] 관련 테스트, 빌드와 계약·하네스 검증을 실행한다.

## 검증

- `services/backend`: Story 서비스·컨트롤러 테스트와 전체 테스트
- `services/frontend-app`: 이야기 repository·책장 화면 테스트, 타입 검사, 빌드
- 루트: `python tools/validate_contracts.py`, `python tools/validate_harness.py`
- 브라우저: 진행 중·완료 탭, 삭제 확인·취소·완료, 카드 그림자와 페이지네이션 상태 확인

## 미결 사항

- 없음

## 검증 결과

- Story 서비스 단위 테스트와 Frontend 이야기 repository 테스트 통과
- Frontend 타입 검사와 production build 통과
- 계약 및 하네스 검증 통과
- 브라우저에서 상태 탭, 삭제 팝업, 카드 그림자와 페이지네이션 확인
- 전체 테스트는 기존 환경 문제로 미통과: Frontend `localStorage` 초기화 및 음성 활동 비동기 테스트 2건, Backend 테스트 런타임의 광범위한 `NoClassDefFoundError`
