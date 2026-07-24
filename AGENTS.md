---
type: Agent Instructions
title: "범용 AI 개발 지침"
description: "iRead 저장소에서 AI 에이전트가 따라야 할 범위, 절차, 검증과 문서 관리 규칙입니다."
tags: [agents, governance, workflow, harness]
timestamp: 2026-07-24T00:00:00+09:00
---
# 범용 AI 개발 지침

이 파일은 특정 AI 모델이나 제품에 종속되지 않는 저장소 공통 지침이다. 모든 AI 에이전트는 별도의 모델별 지침을 만들지 않고 이 파일을 최우선 기준으로 사용한다.

## 저장소 목적

이 저장소는 여러 서비스 저장소를 조율하는 기획 및 아키텍처 허브다. 제품 컨텍스트, 서비스 경계, 저장소 간 계약, 의사결정과 실행 계획을 일관되게 유지한다.

## 문서 확인 순서

작업을 시작할 때 필요한 범위만 다음 순서로 읽는다.

1. `docs/context/project-context.md`
2. 작업과 직접 관련된 `docs/product/` 또는 `docs/architecture/` 문서
3. `docs/decisions/index.md`에서 관련 ADR
4. 복잡한 작업이면 `PLANS.md`와 활성 실행 계획

모든 문서를 무조건 읽지 말고 `docs/index.md`의 안내표에서 필요한 문서를 찾는다.

## 작업 전 확인

- 요구사항이 모호하거나 필수 정보가 없고 여러 타당한 선택지가 남으면 변경 작업 전에 사용자에게 질문한다.
- 특히 제품 범위, 사용자 데이터, 서비스 경계, API 계약, 저장소/submodule 경로, 새 의존성, 외부 시스템, 보안·권한, 파괴적 작업은 추측하지 않는다.
- 읽기 전용 탐색으로 사실을 확인할 수 있으면 먼저 확인해도 된다. 탐색 후에도 선택이 필요하면 변경하지 말고 질문한다.
- 임시 가정이 필요하면 문서에 `[ASSUMPTION]`으로 표시하고 사용자 승인을 받기 전에는 확정 사실처럼 사용하지 않는다.
- 미결 항목은 `[TBD]`, 외부 결정을 기다리는 항목은 `[BLOCKED]`로 표시한다.

## 현재 범위

- 확정된 서비스명과 오케스트레이션 저장소명은 `iRead`다.
- 이 저장소에는 서비스 구현 코드를 만들지 않는다.
- Backend, Frontend, AI server, 아동 앱은 각각 `iRead-backend`, `iRead-frontend`, `iRead-ai`, `iRead-app` 공개 저장소로 관리한다.
- 서비스 저장소는 각각 `services/backend`, `services/frontend`, `services/ai`, `services/app`에 Git submodule로 연결한다.
- 오케스트레이션 저장소는 GitHub `iRead-B105/iRead`와 연결되어 있으며 `main`, `develop` 브랜치를 사용한다.
- 다섯 저장소는 모두 공개 저장소이며 `main`, `develop` 브랜치를 사용하고 기본 브랜치는 `develop`이다.
- `main`은 PR과 승인 1명이 필요하며, `develop`은 직접 push를 허용하되 두 브랜치 모두 force push와 삭제를 금지한다.
- 사용자가 요청하기 전에는 새로운 서비스 저장소나 submodule을 추가하지 않는다.

## 기술 기준선

- Backend: Spring Boot 3, Java 21, Gradle Kotlin DSL
- Frontend: Vue 3, TypeScript, Vite, pnpm
- AI server: FastAPI, Python 3.12, uv
- 아동 앱: [TBD]
- Redis: Docker Compose로 구동할 예정이나 역할은 미정
- 주 데이터베이스: MySQL 8.4.x LTS, 운영 토폴로지는 [TBD]

## 기준 문서

- 확정된 현재 사실: `docs/context/project-context.md`
- 제품 목표와 범위: `docs/product/vision-and-scope.md`
- 도메인 언어: `docs/context/glossary.md`
- 요구사항: `docs/product/requirements.md`
- 시스템 및 저장소 경계: `docs/architecture/`
- 중요한 결정과 근거: `docs/decisions/`
- 우선순위와 진행 상태: `docs/planning/`
- 장기 작업의 상세 진행 기록: `plans/`
- Git 브랜치, 커밋과 병합 정책: `docs/workflows/git-flow.md`
- submodule clone, 갱신과 참조 관리: `docs/workflows/submodules.md`
- 문서 어투와 표현 원칙: `docs/workflows/documentation-style.md`
- 기능·API·데이터베이스 명세 관리: `docs/workflows/specification-management.md`
- 계약 기준 원본과 이전 상태: `contracts/catalog.md`

문서가 충돌하면 추측으로 정리하지 말고 사용자에게 확인한다. 확인 후 관련 문서와 ADR을 같은 변경에서 함께 갱신한다.

## 작업 절차

1. 요청을 목표, 컨텍스트, 제약, 완료 조건으로 재구성한다.
2. 작업 전 확인 항목을 점검한다.
3. 변경 범위를 작게 계획한다. 여러 세션이 필요한 작업은 실행 계획을 만든다.
4. 가장 가까운 기준 문서를 먼저 수정하고 파생 문서를 동기화한다.
5. 하네스·문서 변경에는 `python tools/validate_harness.py`를 실행한다. 소스 코드 검증은 아래 정책을 따른다.
6. 완료 시 변경 내용, 실행한 검증, 실행하지 않은 검증과 남은 `[TBD]`를 보고한다.

## 소스 검증 정책

- 소스 코드나 기능을 수정한 뒤 테스트, 빌드, 린트, 타입 검사와 정적 분석을 자동으로 실행하지 않는다.
- 위 검증은 사용자가 현재 요청에서 명시적으로 실행을 요청한 경우에만 수행한다. 계획, 템플릿 또는 기존 문서에 검증 명령이 있다는 사실은 실행 권한으로 보지 않는다.
- `test`, `build`, `check`, `lint`, `typecheck`, 정적 분석을 직접 또는 다른 명령을 통해 간접 실행하지 않는다.
- 사용자가 단순히 "검증"이라고만 요청해 범위가 모호하면 어떤 검증을 원하는지 먼저 질문한다.
- 테스트 코드 작성이 요청 범위에 포함되어도 테스트 실행은 별도의 명시적 요청이 있어야 한다.
- 읽기 전용 파일 확인과 diff 검토는 가능하지만 컴파일러, 테스트 러너, 린터 또는 분석기를 실행하지 않는다.
- `python tools/validate_harness.py`와 GitHub의 `harness-validation`은 소스 검증이 아니라 문서 구조와 내부 링크를 확인하므로 자동 실행 정책을 유지한다.
- 소스 검증을 요청받지 않았다면 최종 보고에 `테스트/빌드/린트/정적 분석 미실행(사용자 요청 없음)`이라고 명시한다.

## Git 작업 정책

- 사용자가 Git 작업을 요청하면 먼저 `docs/workflows/git-flow.md`를 읽는다.
- 브랜치는 Git Flow 표준 접두사만 사용하며 `codex/` 등 AI 도구명이나 개인 식별자 접두사를 사용하지 않는다.
- 커밋 메시지는 Conventional Commits 형식을 따르고 제목과 본문은 한국어로 작성한다.
- `main`에는 직접 커밋하거나 push하지 않는다.
- 단순 문서 수정처럼 동작에 영향을 주지 않는 작은 변경은 `develop`에 직접 커밋할 수 있다.
- 소스 동작, API, 데이터, 보안, 의존성, CI/CD, 인프라 또는 여러 서비스에 영향을 주는 변경은 작업 브랜치와 PR을 사용한다.
- 사용자가 PR을 요청했거나 PR 필요 여부가 모호하면 작업 전에 확인한다.
- 공유 브랜치에 강제 push하거나 이미 공유된 이력을 다시 쓰지 않는다.

## 문서 작성 규칙

- 문서를 작성하거나 수정할 때 `docs/workflows/documentation-style.md`를 따른다.
- 저장소 관리 Markdown 개념 문서는 OKF v0.1 frontmatter의 `type`, `title`, `description`, `tags`, `timestamp`를 유지한다.
- `index.md`와 `log.md`는 OKF 예약 파일이므로 일반 개념 문서 frontmatter 규칙을 적용하지 않는다.
- 문서는 기본적으로 한국어로 작성하고 코드 식별자와 표준 기술명은 원문을 유지한다.
- 날짜는 `YYYY-MM-DD`, 식별자는 `REQ-###`, `ADR-####`, `TASK-###` 형식을 사용한다.
- 요구사항은 검증 가능한 문장으로 쓰고 수용 기준을 포함한다.
- 결정된 내용과 제안, 가정을 명확히 구분한다.
- 같은 사실을 여러 문서에 복제하기보다 기준 문서로 연결한다.
- 새로운 주요 결정은 ADR로 남기며 기존 ADR을 덮어쓰지 않는다.

## 완료 기준

- 요청된 산출물이 기준 문서에 반영되어 있다.
- 관련 링크, 상태, 식별자와 용어가 일치한다.
- 중요한 결정에는 근거와 영향이 기록되어 있다.
- 하네스·문서 변경은 하네스 검증 스크립트가 성공한다.
- 소스 검증은 사용자가 명시적으로 요청한 항목만 성공 여부를 확인하며, 요청하지 않은 항목은 미실행으로 보고한다.
- 남은 모호성이나 미결 사항이 명시되어 있다.
