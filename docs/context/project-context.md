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
- 서비스 저장소와 submodule 구성을 완료했으며 현재 계약 정합화와 Backend·Frontend 구현을 병행한다.
- iRead의 제품 방향은 난독증 또는 읽기곤란 위험이 있는 초등 저학년 아동을 위한 개인화 읽기 훈련 시스템이다.
- 핵심 사용자는 아동이며 보호자, 난독증·문해교육 전문가, 교사와 교육기관이 주요 이해관계자다.
- 해결할 문제와 근거는 [제품 비전과 범위](../product/vision-and-scope.md)와 [문제 및 근거 조사](../product/research-basis.md)에 기록한다.
- 기술 기준선은 [ADR-0002](../decisions/ADR-0002-technology-baseline.md)에 기록되어 있다.
- 주 데이터베이스는 [ADR-0006](../decisions/ADR-0006-mysql-primary-database.md)에 따라 MySQL 8.4.x LTS를 사용한다.
- 현재 산출물은 실제 운영하지 않는 데모 버전이며, 데이터 보관, 로컬·Docker MySQL과 API 보안 범위는 [ADR-0008](../decisions/ADR-0008-demo-data-and-runtime-policy.md)을 따른다.
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
- 단어 발음 평가는 [ADR-0013](../decisions/ADR-0013-azure-speech-pronunciation-assessment.md)에 따라 AI server가 Azure Speech `ko-KR` scripted Pronunciation Assessment를 호출하는 방향으로 전환한다.
- 향후 Git 운영은 [Git Flow 및 커밋 정책](../workflows/git-flow.md)을 따른다.
- 요구사항이나 필수 정보가 모호하면 변경 작업 전에 사용자에게 질문한다.

## 저장소 구현 경계

- 오케스트레이션 루트에는 서비스 실행 코드를 직접 만들지 않는다.
- 서비스 구현, 실행 설정과 의존성은 해당 `services/*` submodule에서 관리한다.

## 미결 사항

- [TBD] MVP 범위와 성공 지표
- [TBD] 각 서비스의 구체적인 책임
- [TBD] 아동 앱의 기술 스택
- [TBD] Redis의 책임(캐시, 세션, 큐, pub/sub 등)
- [TBD] 서비스별 데이터 소유권
- [TBD] 운영 전환 시 MySQL 토폴로지, 백업·복구와 배포 제약
- [TBD] 운영 전환 시 인증·인가, 감사와 개인정보 처리 요구사항
- [TBD] [제품 용어 및 책임 경계](../product/product-responsibility-boundary.md)의 임시 기준을 최종 제품 범위로 채택할지 결정
- [TBD] 아동의 시선·음성 데이터 수집 항목과 별도 동의서에 명시할 데이터셋별 보관 기간

## 갱신 원칙

사용자가 미결 사항을 확정하면 이 문서, 관련 제품/아키텍처 문서와 ADR을 함께 갱신한다.
