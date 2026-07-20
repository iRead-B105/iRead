# GitLab 단일 저장소 동기화

- 상태: active
- 담당: iRead 팀
- 작성일: 2026-07-20
- 수정일: 2026-07-20

## 기대 결과

GitHub의 오케스트레이션 및 세 서비스 저장소를 개발 기준으로 유지하면서 GitLab `S15P11B105`의 `main`에서 현재 통합 코드를 조회하고 빌드할 수 있다. GitLab `main`은 원본 커밋과 merge graph를 연결하고, `upstream/*` 브랜치는 저장소별 원본 브랜치를 보존한다.

## 배경

- GitHub `iRead-B105/iRead`는 세 서비스 저장소를 Git submodule로 연결한다.
- GitHub의 네 저장소와 기존 개발·PR 흐름은 변경하지 않는다.
- GitLab `s15-webmobile2-sub1/S15P11B105`는 단일 통합 저장소로 사용한다.
- 세부 결정은 [ADR-0005](../docs/decisions/ADR-0005-gitlab-monorepo-mirror.md)를 따른다.

## 확인이 필요한 사항

- [BLOCKED] GitLab Owner 또는 Maintainer가 빈 프로젝트의 기본 `main` 브랜치를 최초 생성해야 한다.
- [BLOCKED] GitHub 오케스트레이션 저장소에 `GITLAB_PUSH_TOKEN` secret을 등록해야 한다.

## 작업 단계

- [x] GitHub 저장소와 submodule 경로 및 고정 커밋 확인
- [x] squash 없는 subtree 방식으로 초기 GitLab 통합 이력 생성
- [ ] GitLab 기본 `main` 브랜치 생성 후 초기 통합 이력 push
- [x] 저장소별 `upstream/*` ref 동기화 스크립트 작성
- [x] GitHub Actions 자동 동기화 workflow 작성
- [ ] 작업 브랜치 PR 검토 및 병합
- [ ] GitHub secret 등록 후 수동 동기화 성공 확인

## 검증

- `python tools/validate_harness.py`
- `git diff --check`
- GitLab `main`에서 세 서비스 경로가 mode `040000 tree`인지 확인
- 각 고정 commit이 GitLab `main`의 조상인지 `git merge-base --is-ancestor`로 확인
- GitLab `upstream/<repository>/main`, `upstream/<repository>/develop` ref 확인
- 테스트·빌드·린트·정적 분석은 사용자 요청이 없으므로 실행하지 않는다.

## 진행 기록

- 2026-07-20: 오케스트레이션 기본 브랜치와 submodule 추적 브랜치가 모두 `develop`임을 확인했다.
- 2026-07-20: Backend `3d1125c`, Frontend `74ecda4`, AI server `f4167a2`를 기준으로 초기 subtree 통합 이력을 로컬에 생성했다.
- 2026-07-20: 현재 인증 계정으로 빈 GitLab 프로젝트의 기본 브랜치를 생성할 권한이 없어 최초 push가 거부됨을 확인했다.

## 결정 및 변경 사항

- GitHub 네 저장소를 개발 기준으로 유지한다.
- GitLab `main`에는 `--squash` 없는 subtree를 사용해 원본 커밋 이력을 연결한다.
- GitLab `upstream/*`에는 저장소별 원본 branch와 tag를 이름 충돌 없이 보존한다.
- 오케스트레이션이 기록한 submodule commit만 GitLab `main`의 서비스 코드로 반영한다.

## 남은 위험

- GitHub PR의 제목, 본문, 댓글, 리뷰 및 check 결과는 Git ref가 아니므로 자동 보존하지 않는다.
- 삭제된 원본 branch는 GitLab에서 자동 삭제하지 않아 보관용 ref가 누적될 수 있다.
- GitLab token 만료 시 동기화 workflow가 실패한다.
