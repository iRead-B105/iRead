---
type: Execution Plan
title: "교수자 앱 보고서·계정 계약 정합화"
description: "교수자 앱의 보고서, 프로필 이미지와 이메일 기반 계정 복구 계약을 Frontend·Backend·OpenAPI·MySQL 기준선에 맞추는 실행 계획입니다."
tags: [plan, frontend-web, backend, report, auth, email, security]
timestamp: 2026-07-29T00:00:00+09:00
---
# 교수자 앱 보고서·계정 계약 정합화

- 상태: completed
- 작성일: 2026-07-29
- 수정일: 2026-07-29

## 범위

### 포함

- 보고서 삭제 API를 제거하고 교수자 의견 길이를 2,000자로 통일한다.
- 교수자 이메일을 읽기 전용 로그인 식별자로 고정하고 프로필 수정 계약에서 제외한다.
- 교수자 연락처와 주소를 현재 프로필 범위에서 제외한다.
- 교수자·아동 프로필 이미지를 JPG·PNG, 최대 5MB로 검증한다.
- 별도 로그인 아이디 찾기 기능을 제거하고 이메일 로그인 용어로 통일한다.
- ADR-0013에 따라 10분 만료·일회용 이메일 링크 비밀번호 재설정을 구현한다.
- 로컬 데모는 Mailpit, 배포 환경은 SMTP 환경변수를 사용한다.
- 관련 기능, OpenAPI, Backend, Frontend와 테스트를 함께 정합화한다.

### 제외

- 학습 앱 Frontend 구현
- 음성 처리 구현
- 다른 팀원이 담당하는 정책 원문 수정
- App 학습 JSON 계약 확정 이후 수행할 BE-032 테스트 비교 통계
- 운영 SMTP 자격 증명과 발신 도메인 발급

## 확정 사항

- 보고서는 삭제 기능을 제공하지 않고 저장된 스냅샷을 유지한다.
- 보고서 교수자 의견은 생성·수정 모두 최대 2,000자다.
- 교수자 이메일은 프로필 화면에서 변경할 수 없다.
- 교수자 프로필은 이름, 소속, 성별과 이미지로 한정한다.
- 프로필 이미지는 JPG 또는 PNG이며 최대 5MB다.
- `teachers.email`이 유일한 로그인 식별자이므로 별도 아이디 찾기를 제공하지 않는다.
- 비밀번호 재설정은 고정 데모 코드가 아닌 이메일 일회용 링크를 사용한다.

## 작업

- [x] 보고서 API·DTO·Frontend 검증과 오류 계약을 정리한다.
- [x] 교수자 프로필 DTO·서비스·Frontend·이미지 검증을 정리한다.
- [x] 아이디 찾기 API와 잔여 계약을 폐기한다.
- [x] 비밀번호 재설정 토큰 저장소, 메일 발송, 요청·확인 API를 구현한다.
- [x] Frontend 비밀번호 재설정 요청·확인 화면을 일회용 링크 흐름으로 변경한다.
- [x] OpenAPI와 기능 카탈로그·백로그를 동기화한다.
- [x] 계약·Backend·Frontend·하네스 검증을 수행한다.

## 검증

- `python tools/generate_contracts.py`
- `python tools/validate_contracts.py`
- `python tools/validate_harness.py`
- `services/backend/gradlew.bat test`
- `pnpm.cmd test -- --run`
- `pnpm.cmd build`
- `pnpm.cmd lint`

## 미결 사항

- 외부 배포 SMTP 호스트·계정·발신 도메인은 운영 환경변수로 주입해야 한다.
- Mailpit은 로컬 데모 기본 구성으로만 추가하며 운영 의존성으로 사용하지 않는다.
