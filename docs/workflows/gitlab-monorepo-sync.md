---
type: Workflow
title: "GitLab 단일 저장소 동기화"
description: "GitHub orchestration과 submodule을 GitLab 단일 저장소로 동기화하는 절차입니다."
tags: [workflow, git, github-actions, gitlab, submodule, subtree, mirror]
timestamp: 2026-07-25T00:00:00+09:00
---
# GitLab 단일 저장소 동기화

- 상태: accepted
- 최종 검토일: 2026-07-27
- 대상: `https://lab.ssafy.com/s15-webmobile2-sub1/S15P11B105`

## 구조

GitHub는 독립 저장소와 submodule 구조를 유지한다. GitLab `main`은 다음 통합 구조를 사용한다.

```text
S15P11B105/
├── orchestration 파일
└── services/
    ├── backend/
    ├── frontend-web/
    ├── ai/
    ├── frontend-app/
    └── eyetracking/
```

GitLab에는 `.gitmodules`와 gitlink를 복사하지 않는다. 각 `services/*`에는 orchestration `develop`이 가리키는 실제 서비스 commit의 파일을 넣는다.

## 사전 설정

GitLab 프로젝트에서 push 권한이 있는 access token을 만든다. 토큰 값을 채팅, 문서와 저장소에 기록하지 않고 GitHub `iRead` 저장소의 `Settings → Secrets and variables → Actions`에 다음 이름으로 등록한다.

```text
GITLAB_PUSH_TOKEN
```

GitLab `main`과 `upstream/*`에 push할 수 있는 권한이 필요하다.
동기화 스크립트는 GitLab HTTPS 인증 프롬프트에 username `oauth2`와 Repository Secret의 token을 `GIT_ASKPASS`로 전달한다. token을 URL, 로그 또는 Git 설정에 기록하지 않는다.

## 개발과 동기화

1. 서비스 저장소의 작업 브랜치를 해당 서비스 `develop`에 병합한다.
2. 서비스 담당자가 orchestration에서 해당 submodule gitlink를 갱신한다.
3. 포인터 변경 브랜치를 push하고 orchestration `develop` 대상 PR을 생성한다.
4. 필수 리뷰 인원 0명 정책에 따라 서비스 조합을 확인한 뒤 PR을 병합한다.
5. `Harness Validation`이 포인터 commit을 검증한다.
6. 검증이 성공하면 `GitLab Monorepo Sync`가 같은 commit을 자동으로 동기화한다.
7. GitLab 재동기화가 필요하면 `GitLab Monorepo Sync`를 수동 실행한다.

서비스 저장소에 push한 것만으로 GitLab 통합 코드가 바뀌지 않는다.
포인터 PR을 orchestration `develop`에 병합해야 해당 조합이
GitLab `main`에 반영된다.
GitLab `main`의 `services/*`는 mirror 결과이므로 직접 수정하지 않는다. 직접 수정한 파일은 다음 동기화에서 GitHub 서비스 commit의 스냅샷으로 교체된다.

`Contract Validation`은 계약 관련 파일이 바뀐 push와 PR에서 기존 경로 필터에 따라 별도로 실행한다. GitLab 동기화 workflow는 기존 검증 workflow를 수정하거나 중복 등록하지 않는다.

## 이력 보존

- GitLab `main`에는 GitHub 작업 commit을 monorepo 경로로 1:1 투영한다.
- 투영 commit은 원본의 메시지, 작성자 이름과 작성 시각을 유지한다.
- `156529176+2hnK@users.noreply.github.com` 작성자 이메일은 GitLab 프로필 연결을 위해 `kimgh921@gmail.com`으로 투영한다.
- `.gitmodules`나 gitlink만 바꿔 GitLab 파일 차이가 없는 원본 commit도 빈 projection commit으로 보존한다.
- 파일 경로와 부모가 달라지므로 투영 commit SHA는 원본과 다르다.
- `chore(mirror)` 전용 commit은 생성하지 않는다.
- 원본 branch는 `upstream/<repository>/<branch>`로 보존한다.
- 원본 tag는 `upstream/<repository>/<tag>`로 보존한다.
- 원본 SHA와 투영 SHA의 대응은 `refs/notes/iread-source-map`에 기록한다.
- 동기화 상태는 `refs/notes/iread-source-state`에 기록한다.
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

## upstream ref 정합화

GitHub 원본 branch의 이력이 변경되어 GitLab `upstream/<repository>/<branch>` push가
non-fast-forward로 거부되면 원본과 GitLab의 이력을 검토한 뒤 `GitLab Monorepo Sync`를
수동 실행한다. `reconcile_upstream_refs`에는 정합화할 대상을
`repository/branch` 형식으로 입력하며 여러 대상은 쉼표로 구분한다.

```text
backend/feat/example-one,backend/feat/example-two
```

수동 정합화는 입력한 ref에만 적용된다. 실행 시점의 GitLab SHA를 lease로 확인한 뒤
해당 ref를 현재 GitHub 원본 branch로 갱신하므로, 검토 이후 GitLab ref가 다시 바뀌면
덮어쓰지 않고 실패한다. `GitLab main`과 입력하지 않은 upstream ref에는 force push하지
않는다. 이 작업에는 projection 이력을 교체하는 `rebuild_history`를 사용하지 않는다.

## 이력 재구성

기존 mirror 이력에서 projection 이력으로 전환할 때만 GitHub Actions의 수동 실행에서 `rebuild_history`를 활성화한다. 이 실행은 현재 GitLab `main`을 원본 작업 commit의 1:1 projection 이력으로 교체한다. 일반 자동·예약·수동 실행은 force push하지 않고 기존 projection 이력에 새 작업 commit만 fast-forward로 추가한다.

projection 상태 note가 없는 동안 일반 실행은 GitLab `main`을 변경하지 않고 성공 종료한다. 따라서 이력 교체는 `rebuild_history`를 명시한 수동 실행에서만 발생한다.

## 장애 처리

- `GITLAB_PUSH_TOKEN is required`: GitHub Actions secret 등록 여부를 확인한다.
- `HTTP Basic: Access denied`: token 만료 여부와 `write_repository` scope를 확인한다.
- `Requested orchestration commit is not on develop`: 검증 이후 branch 이력이 변경됐는지 확인한다.
- push 권한 오류: GitLab token 역할과 보호 branch 허용 대상을 확인한다.
- `Expected submodule gitlink`: 해당 서비스가 orchestration `develop`에 submodule로 병합됐는지 확인한다.
- `moved non-fast-forward`: upstream force push 또는 gitlink 되돌림을 확인하고 자동 동기화를 재개하기 전에 이력을 검토한다.
- upstream ref push의 `fetch first`: GitHub와 GitLab 이력을 검토한 뒤 수동 실행의
  `reconcile_upstream_refs`에 충돌한 ref만 지정한다.
- `Projection state is absent`: 수동 실행에서 `rebuild_history`를 활성화해 최초 projection 이력을 생성한다.
- 포인터 PR 누락: 서비스 `develop`을 병합한 담당자가 orchestration
  submodule 참조 갱신과 PR 생성을 완료했는지 확인한다.
- GitLab `main` 직접 변경: 원본 GitHub 저장소로 옮기고 orchestration gitlink를 갱신한다.
