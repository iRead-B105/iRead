---
type: Project Context
title: "프로젝트 컨텍스트"
description: "iRead의 확정 사실, 현재 범위와 미결 사항을 관리하는 기준 문서입니다."
tags: [context, project, source-of-truth]
timestamp: 2026-07-24T00:00:00+09:00
---
# 프로젝트 컨텍스트

- 상태: draft
- 최종 검토일: 2026-07-24
- 서비스명: `iRead`

## 저장소 목적

서비스 기획부터 구현 준비까지의 공통 컨텍스트를 관리하고, 독립적인 Backend·Frontend·AI server·아동 앱·시선 추적 저장소를 조율한다.

## 확정 사항

- 서비스명과 오케스트레이션 저장소명은 `iRead`다.
- 현재 디렉터리는 오케스트레이션 저장소로 사용한다.
- Backend, Frontend, AI server, 아동 앱, 시선 추적 프로토타입은 각각 별도 저장소로 관리하고 Git submodule로 연결한다.
- 서비스 저장소와 submodule 구성까지 완료했으며 다음 단계는 제품 탐색이다.
- iRead의 제품 방향은 난독증 또는 읽기곤란 위험이 있는 초등 저학년 아동을 위한 개인화 읽기 훈련 시스템이다.
- 핵심 사용자는 아동이며 보호자, 난독증·문해교육 전문가, 교사와 교육기관이 주요 이해관계자다.
- 해결할 문제와 근거는 [제품 비전과 범위](../product/vision-and-scope.md)와 [문제 및 근거 조사](../product/research-basis.md)에 기록한다.
- 기술 기준선은 [ADR-0002](../decisions/ADR-0002-technology-baseline.md)에 기록되어 있다.
- 주 데이터베이스는 [ADR-0006](../decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용하며 운영 토폴로지는 미정이다.
- 문서와 명세 기준 원본은 [ADR-0007](../decisions/ADR-0007-okf-and-specification-sources.md)과 [명세 관리 워크플로](../workflows/specification-management.md)를 따른다.
- GitHub `iRead-B105/iRead` 저장소에 `main`, `develop` 브랜치가 구성되어 있으며 기본 브랜치는 `develop`이다.
- 여섯 저장소는 모두 공개 상태이며 서비스 저장소의 기본 브랜치도 `develop`이다.
- 공개 범위와 보호 정책은 [ADR-0003](../decisions/ADR-0003-public-repositories.md)에 기록되어 있다.
- 기존 서비스 저장소명과 submodule 경로는 [ADR-0004](../decisions/ADR-0004-service-repository-layout.md), 아동 앱 추가 결정은 [ADR-0005](../decisions/ADR-0005-add-child-app-repository.md), 시선 추적 저장소 추가 결정은 [ADR-0010](../decisions/ADR-0010-add-eyetracking-repository.md)에 기록되어 있다.
- Backend는 `iRead-B105/iRead-backend`를 `services/backend`에 연결한다.
- Frontend는 `iRead-B105/iRead-frontend`를 `services/frontend`에 연결한다.
- AI server는 `iRead-B105/iRead-ai`를 `services/ai`에 연결한다.
- 아동 앱은 `iRead-B105/iRead-app`을 `services/app`에 연결한다.
- 시선 추적 프로토타입은 `iRead-B105/iRead-eyetracking`을 `services/eyetracking`에 연결한다.
- 향후 Git 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 따른다.
- 요구사항이나 필수 정보가 모호하면 변경 작업 전에 사용자에게 질문한다.

## 현재 단계에서 하지 않는 일

- 서비스 실행 코드 생성
- Docker Compose 파일 생성
- 패키지 및 의존성 설치

## 미결 사항

- [TBD] MVP 범위와 성공 지표
- [TBD] 각 서비스의 구체적인 책임
- [TBD] 아동 앱의 기술 스택
- [TBD] Redis의 책임(캐시, 세션, 큐, pub/sub 등)
- [TBD] 데이터 소유권과 MySQL 운영 토폴로지
- [TBD] 인증·인가 및 개인정보 처리 요구사항
- [TBD] 배포 환경과 운영 제약
- [TBD] [제품 용어 및 책임 경계](../product/product-responsibility-boundary.md)의 임시 기준을 최종 제품 범위로 채택할지 결정
- [TBD] 아동의 시선·음성 데이터 수집 목적, 법정대리인 동의와 보관·삭제 기준

## 갱신 원칙

사용자가 미결 사항을 확정하면 이 문서, 관련 제품/아키텍처 문서와 ADR을 함께 갱신한다.
