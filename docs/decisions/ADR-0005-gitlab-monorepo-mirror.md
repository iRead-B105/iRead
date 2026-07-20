# ADR-0005: GitLab 단일 저장소 통합 미러

- 상태: accepted
- 결정일: 2026-07-20

## 배경

GitHub에서는 오케스트레이션 저장소와 Backend, Frontend, AI server 저장소를 분리하고 Git submodule로 조율한다. 팀은 이 개발 구조를 유지하면서 GitLab 단일 저장소에서도 통합 코드와 원본 커밋 이력을 확인해야 한다.

## 결정

- GitHub의 네 저장소를 개발 기준으로 유지한다.
- GitLab `s15-webmobile2-sub1/S15P11B105`는 읽기 전용 통합 미러로 사용한다.
- GitLab `main`은 오케스트레이션 `develop`이 기록한 submodule commit을 `--squash` 없는 Git subtree로 펼친다.
- GitLab `upstream/<repository>/*`는 각 GitHub 저장소의 branch를 원본 commit SHA로 보존한다.
- tag는 `upstream/<repository>/*` namespace로 보존한다.
- GitLab에는 동기화 계정 외의 직접 push를 허용하지 않는다.
- GitHub PR 메타데이터, review, comment와 check 결과는 이번 미러 범위에서 제외한다.

## 근거

- GitHub에서 사용하는 저장소 소유권과 PR 흐름을 변경하지 않는다.
- GitLab `main` 하나만 clone해도 세 서비스의 실제 파일을 받을 수 있다.
- squash를 사용하지 않아 통합 시점까지의 원본 commit과 merge graph가 `main`에서 도달 가능하다.
- 별도 `upstream/*` ref로 원본 branch와 tag 이름을 충돌 없이 추적할 수 있다.

## 영향

- GitLab `main`의 commit graph에는 네 저장소의 이력이 함께 표시된다.
- GitLab `main`의 서비스 코드는 원본 저장소 최신 HEAD가 아니라 오케스트레이션이 고정한 commit과 일치한다.
- GitLab에서 수정한 내용을 GitHub로 역동기화하지 않는다.
- GitLab token과 자동 동기화 workflow 운영이 필요하다.
- PR 및 issue 이관이 필요하면 GitHub API를 사용하는 별도 결정을 추가해야 한다.

## 대안

### 저장소별 1:1 GitLab mirror

원본 이력을 단순하게 보존할 수 있지만 GitLab 단일 저장소 요구를 만족하지 않는다.

### squash subtree만 사용

`main` 이력은 간결하지만 원본 세부 commit이 `main`에 연결되지 않는다.

### GitHub와 GitLab 양방향 개발

서로 다른 저장소 경계 때문에 branch와 merge 충돌 위험이 커서 채택하지 않는다.
