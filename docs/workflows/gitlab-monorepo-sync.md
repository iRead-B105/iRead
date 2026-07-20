# GitLab 단일 저장소 동기화 가이드

- 상태: accepted
- 최종 검토일: 2026-07-20

## 저장소 역할

- GitHub `iRead-B105/iRead`와 세 서비스 저장소는 개발 기준이다.
- GitLab `s15-webmobile2-sub1/S15P11B105`는 읽기 전용 통합 미러다.
- GitLab에서 직접 개발하거나 GitHub로 역동기화하지 않는다.

## GitLab branch 구성

| branch | 역할 |
| --- | --- |
| `main` | 오케스트레이션이 고정한 세 서비스 commit의 통합 코드 |
| `upstream/orchestration/*` | 오케스트레이션 원본 branch |
| `upstream/backend/*` | Backend 원본 branch |
| `upstream/frontend/*` | Frontend 원본 branch |
| `upstream/ai/*` | AI server 원본 branch |

원본 tag는 `upstream/<repository>/*` namespace로 저장한다. 원본에서 삭제된 branch는 감사 이력을 위해 GitLab에서 자동 삭제하지 않는다.

## 동기화 시점

`.github/workflows/sync-gitlab-monorepo.yml`은 다음 조건에서 실행한다.

- 오케스트레이션 `develop` push
- 수동 `workflow_dispatch`
- 6시간 간격 보정 실행

서비스 저장소의 변경은 오케스트레이션이 submodule 참조를 갱신한 뒤 GitLab `main`에 반영한다. 보정 실행은 `upstream/*` branch와 tag를 최신 상태로 유지한다.

## GitHub secret

오케스트레이션 저장소의 Actions secret에 다음 값을 등록한다.

| 이름 | 값 |
| --- | --- |
| `GITLAB_PUSH_TOKEN` | GitLab `S15P11B105`에 push할 수 있는 project 또는 personal access token |

token은 최소 `write_repository` 범위와 만료일을 사용한다. token을 문서, workflow 또는 Git remote URL에 직접 기록하지 않는다.

## 최초 적용

빈 GitLab 프로젝트에는 Owner 또는 Maintainer가 기본 `main` branch를 먼저 생성해야 한다. 초기 subtree 통합 이력을 push한 뒤 GitHub Actions의 `GitLab Monorepo Sync` workflow를 수동 실행한다.

## 실패 처리

- submodule 참조가 원본 branch에서 확인되지 않으면 동기화를 중단한다.
- 기존 고정 commit의 조상이 아닌 commit으로 이동하면 이력 재작성 또는 rollback으로 보고 동기화를 중단한다.
- GitLab push가 실패하면 GitHub 원본 저장소에는 변경을 가하지 않는다.
- token 만료 또는 권한 오류가 발생하면 secret을 교체한 뒤 수동 실행한다.
