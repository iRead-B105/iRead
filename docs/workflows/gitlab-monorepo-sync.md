---
type: Workflow
title: "GitLab 단일 저장소 동기화"
description: "GitHub orchestration과 submodule을 GitLab 단일 저장소로 동기화하는 절차입니다."
tags: [workflow, git, github-actions, gitlab, submodule, subtree, mirror]
timestamp: 2026-07-25T00:00:00+09:00
---
# GitLab 단일 저장소 동기화

- 상태: accepted
- 최종 검토일: 2026-07-25
- 대상: `https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105`

## 구조

GitHub는 독립 저장소와 submodule 구조를 유지한다. GitLab `main`은 다음 통합 구조를 사용한다.

```text
S15P11B105/
├── orchestration 파일
└── services/
    ├── backend/
    ├── frontend/
    ├── ai/
    ├── app/
    └── eyetracking/
```

GitLab에는 `.gitmodules`와 gitlink를 복사하지 않는다. 각 `services/*`에는 orchestration `develop`이 가리키는 실제 서비스 commit의 파일을 subtree로 넣는다.

## 사전 설정

GitLab 프로젝트에서 push 권한이 있는 access token을 만든다. 토큰 값을 채팅, 문서와 저장소에 기록하지 않고 GitHub `iRead` 저장소의 `Settings → Secrets and variables → Actions`에 다음 이름으로 등록한다.

```text
GITLAB_PUSH_TOKEN
```

GitLab `main`과 `upstream/*`에 push할 수 있는 권한이 필요하다.
동기화 스크립트는 GitLab HTTPS 인증 프롬프트에 username `oauth2`와 Repository Secret의 token을 `GIT_ASKPASS`로 전달한다. token을 URL, 로그 또는 Git 설정에 기록하지 않는다.

## 개발과 동기화

1. 서비스 저장소에서 평소와 같이 개발하고 GitHub에 push한다.
2. orchestration에서 반영할 submodule을 해당 commit으로 갱신한다.
3. submodule gitlink 변경을 orchestration `develop`에 반영한다.
4. 기존 `Harness Validation`이 해당 commit을 검증한다.
5. 검증이 성공하면 `GitLab Monorepo Sync`가 같은 commit을 자동으로 동기화한다.
6. 수동 실행이 필요하면 GitHub Actions에서 `Run workflow`를 사용한다.

서비스 저장소에 push한 것만으로 GitLab 통합 코드가 바뀌지 않는다. orchestration gitlink를 갱신해야 해당 조합이 GitLab `main`에 반영된다.
GitLab `main`의 `services/*`는 mirror 결과이므로 직접 수정하지 않는다. 직접 수정한 파일은 다음 동기화에서 GitHub 서비스 commit의 스냅샷으로 교체된다.

`Contract Validation`은 계약 관련 파일이 바뀐 push와 PR에서 기존 경로 필터에 따라 별도로 실행한다. GitLab 동기화 workflow는 기존 검증 workflow를 수정하거나 중복 등록하지 않는다.

## 이력 보존

- 서비스 commit을 squash하지 않고 GitLab `main`의 merge parent로 연결한다.
- 연결한 commit의 파일 스냅샷을 해당 `services/*` 경로에 반영한다.
- 원본 branch는 `upstream/<repository>/<branch>`로 보존한다.
- 원본 tag는 `upstream/<repository>/<tag>`로 보존한다.
- 동기화 상태는 GitLab 루트 `.gitlab-source-revisions.json`에서 확인한다.
- 원본 commit이 non-fast-forward로 이동하면 자동 반영하지 않고 workflow를 실패시킨다.

예시는 다음과 같다.

```text
upstream/orchestration/develop
upstream/backend/develop
upstream/frontend/develop
upstream/ai/develop
upstream/app/develop
upstream/eyetracking/develop
```

## 첫 실행

첫 실행은 기존 GitLab의 `iRead-*` 루트 디렉터리를 orchestration 루트와 `services/*` 구조로 전환하는 일반 commit을 만든다. 기존 GitLab commit을 force push로 덮어쓰지 않는다. 이후 실행부터 manifest의 commit과 최신 gitlink를 비교해 변경된 서비스만 이력을 연결하고 파일 스냅샷을 갱신한다.

## 장애 처리

- `GITLAB_PUSH_TOKEN is required`: GitHub Actions secret 등록 여부를 확인한다.
- `HTTP Basic: Access denied`: token 만료 여부와 `write_repository` scope를 확인한다.
- `Requested orchestration commit is not on develop`: 검증 이후 branch 이력이 변경됐는지 확인한다.
- push 권한 오류: GitLab token 역할과 보호 branch 허용 대상을 확인한다.
- `Expected submodule gitlink`: 해당 서비스가 orchestration `develop`에 submodule로 병합됐는지 확인한다.
- `moved non-fast-forward`: upstream force push 또는 gitlink 되돌림을 확인하고 자동 동기화를 재개하기 전에 이력을 검토한다.
- GitLab `main` 직접 변경: 원본 GitHub 저장소로 옮기고 orchestration gitlink를 갱신한다.
