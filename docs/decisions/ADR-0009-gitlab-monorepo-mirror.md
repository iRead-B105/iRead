---
type: Architecture Decision
title: "ADR-0009: GitLab 단일 저장소 미러"
description: "GitHub submodule 구조를 유지하면서 GitLab에 전체 이력과 실제 코드를 포함한 단일 저장소를 생성하는 결정입니다."
tags: [architecture, git, github, gitlab, submodule, subtree, mirror, adr]
timestamp: 2026-07-25T00:00:00+09:00
---
# ADR-0009: GitLab 단일 저장소 미러

- 상태: accepted
- 결정일: 2026-07-25
- 결정자: 사용자
- 대체 대상: 없음

## 배경

GitHub에서는 orchestration 저장소와 Backend, Frontend, AI server, 아동 앱, 시선 추적 저장소를 독립적으로 개발한다. 제출·검토용 GitLab `S15P11B105`에서는 submodule 추가 작업 없이 전체 코드를 한 번에 받을 수 있어야 하며 각 원본 저장소의 커밋, 브랜치와 태그 이력도 보존해야 한다.

## 결정 기준

- GitHub 저장소별 개발·PR 흐름을 변경하지 않는다.
- GitLab `main`은 orchestration과 모든 서비스의 실제 코드를 포함한다.
- 서비스 원본 커밋을 squash하지 않는다.
- 서로 충돌하는 브랜치와 태그 이름을 모두 보존한다.
- orchestration이 승인한 submodule commit만 GitLab 통합 코드에 반영한다.

## 검토한 대안

1. GitLab에도 submodule 구조를 그대로 복제한다.
2. 서비스 코드를 파일 복사로 합치고 이력은 보존하지 않는다.
3. GitHub에서는 submodule을 유지하고 GitLab에서는 squash 없는 subtree와 이름공간 ref로 통합한다.

## 결정

- GitHub `iRead`를 개발과 계약의 기준 저장소로 유지한다.
- 서비스는 `services/backend`, `services/frontend`, `services/ai`, `services/app`, `services/eyetracking` submodule로 관리한다.
- GitHub Actions는 orchestration `develop`의 gitlink가 가리키는 commit을 GitLab `services/*`에 squash 없는 subtree로 반영한다.
- orchestration과 서비스의 모든 원본 브랜치는 GitLab `upstream/<repository>/*`, 태그는 `upstream/<repository>/*` 이름공간으로 push한다.
- GitLab `main`에는 통합 merge commit이 추가되지만 원본 commit의 메시지, 작성자, 시각과 SHA를 변경하지 않는다.
- GitLab은 읽기 전용 통합 미러로 사용하고 직접 개발하거나 이력을 재작성하지 않는다.

## 영향

### 긍정적 영향

- GitLab에서 submodule 초기화 없이 전체 프로젝트를 받을 수 있다.
- 저장소별 동일 브랜치명과 태그가 충돌하지 않는다.
- GitHub의 독립 저장소 이력과 orchestration이 검증한 서비스 조합을 함께 추적할 수 있다.

### 부정적 영향과 트레이드오프

- GitLab `main`의 first-parent 보기에는 통합 merge commit이 중심으로 보인다.
- 원본 feature branch의 commit은 해당 branch가 통합되기 전까지 `upstream/*`에서 확인해야 한다.
- GitHub 저장소의 PR, issue, review와 Actions 실행 기록은 Git 이력이 아니므로 미러링되지 않는다.

## 검증 및 재검토 조건

- 첫 실행 후 GitLab 루트에 orchestration 파일과 다섯 `services/*` 디렉터리가 있어야 한다.
- `.gitlab-source-revisions.json`의 commit과 orchestration gitlink가 일치해야 한다.
- 원본 branch와 tag가 GitLab `upstream/*`에 존재해야 한다.
- upstream 이력이 non-fast-forward로 변경되면 자동 동기화를 중단하고 수동으로 검토한다.
