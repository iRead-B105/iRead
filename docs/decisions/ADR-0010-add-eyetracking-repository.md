---
type: Architecture Decision
title: "ADR-0010: 시선 추적 저장소 추가"
description: "Tobii 기반 시선 추적 프로토타입 저장소와 submodule 경로를 추가한 결정입니다."
tags: [architecture, repository, submodule, eyetracking, tobii, adr]
timestamp: 2026-07-25T00:00:00+09:00
---
# ADR-0010: 시선 추적 저장소 추가

- 상태: accepted
- 결정일: 2026-07-25
- 결정자: 사용자
- 대체 대상: 없음

## 배경

Tobii Eye Tracker 5의 시선 데이터를 읽기 활동에 연결하는 프로토타입은 기존 Backend, Frontend, AI server와 다른 실행 환경과 장치 의존성을 가진다. 독립 저장소의 개발 이력을 유지하면서 orchestration이 검증한 commit을 GitLab 통합 미러에 포함하려면 정식 submodule 경로가 필요하다.

## 결정 기준

- 시선 추적 프로토타입의 Python, 브라우저와 native C++ 코드를 독립적으로 관리한다.
- orchestration에서 서비스 조합에 포함할 정확한 commit을 기록한다.
- 기존 서비스와 같은 clone, 갱신과 GitLab 동기화 절차를 적용한다.

## 검토한 대안

1. GitLab 단일 저장소에만 시선 추적 코드를 유지한다.
2. Frontend 또는 AI server 저장소로 즉시 병합한다.
3. `iRead-eyetracking`을 독립 저장소와 orchestration submodule로 관리한다.

## 결정

- 공개 저장소 `iRead-B105/iRead-eyetracking`을 시선 추적 프로토타입의 기준 저장소로 사용한다.
- orchestration의 `services/eyetracking`에 `develop` 추적 submodule로 연결한다.
- GitLab 통합 미러에서는 같은 gitlink commit을 `services/eyetracking`의 실제 코드로 펼친다.
- 본 서비스로 이전할 최종 Backend·Frontend 책임과 API 계약은 별도 결정으로 남긴다.

## 영향

### 긍정적 영향

- 장치 의존 프로토타입의 이력과 실행 환경을 독립적으로 관리할 수 있다.
- orchestration과 GitLab 미러가 동일한 시선 추적 commit을 추적할 수 있다.

### 부정적 영향과 트레이드오프

- 저장소와 submodule 참조를 하나 더 관리해야 한다.
- 프로토타입 기능을 본 서비스에 병합할 때 중복 구현과 데이터 계약을 정리해야 한다.

## 검증 및 재검토 조건

- `services/eyetracking`이 원격 `develop`에 존재하는 commit을 가리켜야 한다.
- `git clone --recurse-submodules`로 시선 추적 저장소까지 받을 수 있어야 한다.
- 시선 추적 기능을 Backend 또는 Frontend에 완전히 이전하면 저장소 유지 여부를 새 ADR로 재검토한다.
