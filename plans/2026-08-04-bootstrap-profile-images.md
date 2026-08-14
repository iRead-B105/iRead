---
type: Execution Plan
---
# 학생 선택 프로필 이미지 인증 로딩

- 상태: completed
- 수정일: 2026-08-04

## 범위

연결 아동 소유권을 검증하는 프로필 이미지 조회 API를 추가하고, 학습 앱이 bootstrap 또는 learning access token으로 이미지를 Blob URL로 로딩한다. `/uploads/**` 전체 공개와 데이터베이스 변경은 제외한다.

## 작업

- [x] 인증 주체와 아동 소유권을 검증하는 이미지 API 및 테스트 추가
- [x] OpenAPI와 기능–API 관계 갱신
- [x] 로그인 선택 카드와 학습 헤더에서 인증 이미지 Blob 로딩
- [x] 관련 백엔드·프런트엔드·계약 검증 실행

## 검증

- Backend auth/security 관련 테스트
- Frontend 인증 이미지 resolver 및 로그인 화면 테스트
- Frontend 타입 검사와 프로덕션 빌드
- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- 브라우저에서 엘리스 프로필 이미지 로드 확인

## 미결 사항

- 없음

## 완료 기록

- Backend 서비스·라우팅·인가 통합 테스트 통과
- Frontend resolver·로그인 화면 테스트, 타입 검사와 프로덕션 빌드 통과
- 계약·하네스 검증 통과
- 로컬 백엔드 재기동 및 신규 라우트의 비인증 접근 차단 확인
- 브라우저의 실제 로그인 제출은 자격 증명 전송 확인이 필요해 수행하지 않았으며, bootstrap/learning token 성공 경로는 자동화 통합 테스트로 검증함
