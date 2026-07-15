# Git Flow 및 커밋 정책

- 상태: accepted
- 최종 검토일: 2026-07-15
- 적용 범위: Orchestration, Backend, Frontend, AI server 저장소

## 1. 기본 원칙

- `main`은 배포 가능한 릴리스 이력, `develop`은 다음 릴리스의 통합 기준으로 사용한다.
- `main` 변경은 항상 `release/*` 또는 `hotfix/*` PR을 거친다.
- 동작에 영향을 주지 않는 작은 변경은 `develop`에 직접 커밋할 수 있다.
- 검토가 필요한 변경은 `feature/*` 브랜치와 PR을 사용한다.
- 브랜치명에는 사람, AI 모델 또는 도구 이름을 넣지 않는다.
- 커밋은 하나의 논리적 변경만 포함하고 언제든 검토하거나 되돌릴 수 있어야 한다.

## 2. 브랜치 구조

| 브랜치 | 기준 브랜치 | 병합 대상 | 용도 | 수명 |
| --- | --- | --- | --- | --- |
| `main` | - | - | 운영 릴리스 이력 | 영구 |
| `develop` | `main` | - | 다음 릴리스 통합 | 영구 |
| `feature/*` | `develop` | `develop` | 기능 개발과 검토가 필요한 변경 | 임시 |
| `release/*` | `develop` | `main`, `develop` | 릴리스 안정화와 버전 준비 | 임시 |
| `hotfix/*` | `main` | `main`, `develop` | 운영 버전 긴급 수정 | 임시 |

`develop`을 `main`에 직접 병합하지 않는다. 정식 배포는 `release/*`, 긴급 배포는 `hotfix/*`를 사용한다.

## 3. 직접 커밋과 PR 선택 기준

### `develop` 직접 커밋

다음 조건을 모두 만족하면 `develop`에 직접 커밋할 수 있다.

- README, 오탈자, 주석, 문구, 단순 계획 문서처럼 동작에 영향을 주지 않는 변경
- API, 데이터 구조, 보안, 의존성, 빌드, CI/CD와 인프라에 영향이 없는 변경
- 하나의 작은 목적만 포함하고 다른 팀원의 검토가 필요하지 않은 변경
- 사용자가 PR을 요청하지 않은 변경

### PR 필수

다음 중 하나라도 해당하면 작업 브랜치와 PR을 사용한다.

- 소스 코드의 동작이나 사용자 기능 변경
- API·이벤트 계약, 데이터 구조와 마이그레이션 변경
- 인증·인가, 개인정보와 보안 관련 변경
- 의존성, 빌드, 배포, CI/CD와 인프라 변경
- 여러 서비스 또는 여러 문서의 팀 정책에 영향을 주는 변경
- 호환성을 깨거나 되돌리기 어려운 변경
- 사용자가 PR 또는 리뷰를 요청한 변경

PR 필요 여부가 모호하면 작업 전에 사용자에게 확인한다.

## 4. 브랜치 이름

```text
feature/<issue-number>-<short-description>
release/<semantic-version>
hotfix/<semantic-version>
```

이슈가 없으면 번호를 생략할 수 있다.

```text
feature/123-reading-history
feature/update-api-contract
release/1.2.0
hotfix/1.2.1
```

- 영문 소문자, 숫자와 하이픈을 사용한다.
- 설명은 짧은 kebab-case로 작성한다.
- `codex/`, `claude/`, `gemini/`, `ai/` 또는 개인 이름처럼 작업 주체를 나타내는 접두사는 사용하지 않는다.
- 브랜치 하나에는 하나의 목적만 둔다.

## 5. `develop` 직접 커밋 절차

1. 최신 `develop`을 `git pull --ff-only`로 동기화한다.
2. 변경 범위가 직접 커밋 허용 기준에 맞는지 확인한다.
3. 하나의 원자적 커밋으로 작성한다.
4. `develop`에 push하고 원격 반영 여부를 확인한다.
5. 하네스·문서 변경은 `harness-validation` 결과를 확인한다.

소스 테스트·빌드·린트·정적 분석은 사용자가 명시적으로 요청한 경우에만 실행한다.

## 6. 작업 브랜치 절차

### 기능 개발

1. 최신 `develop`에서 `feature/*` 브랜치를 만든다.
2. 작고 논리적인 단위로 커밋한다.
3. 필요한 경우 개인 작업 브랜치에서 최신 `develop`을 rebase한다.
4. `develop` 대상 PR을 만들고 검토를 받는다.
5. squash merge한 뒤 작업 브랜치를 삭제한다.

공유 중인 feature 브랜치는 rebase로 이력을 바꾸기 전에 참여자와 합의한다.

### 릴리스

1. 릴리스할 `develop`에서 `release/<version>`을 만든다.
2. 버전, 문서, 설정과 릴리스 차단 버그만 수정한다.
3. `main`에 `--no-ff` merge commit으로 병합한다.
4. 병합 결과에 `v<version>` annotated tag를 만든다.
5. 같은 release 브랜치를 `develop`에도 `--no-ff`로 병합한다.
6. 병합과 tag를 확인한 뒤 release 브랜치를 삭제한다.

### 긴급 수정

1. 최신 `main`에서 `hotfix/<version>`을 만든다.
2. 운영 문제 해결에 필요한 최소 변경만 포함한다.
3. `main`에 `--no-ff` merge하고 `v<version>` tag를 만든다.
4. 같은 hotfix 브랜치를 `develop`에도 `--no-ff`로 병합한다.
5. 활성 release 브랜치가 있으면 반영 여부를 확인한다.
6. 배포와 역병합을 확인한 뒤 hotfix 브랜치를 삭제한다.

## 7. 병합 방식

| 병합 경로 | 방식 | 이유 |
| --- | --- | --- |
| `feature/*` → `develop` | Squash merge | 기능 단위로 통합 이력을 정리한다. |
| `release/*` → `main`, `develop` | Merge commit (`--no-ff`) | 릴리스 경계와 역병합 이력을 보존한다. |
| `hotfix/*` → `main`, `develop` | Merge commit (`--no-ff`) | 긴급 수정의 배포와 역병합을 추적한다. |

## 8. 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 형식을 사용하고 제목과 본문은 한국어로 작성한다.

```text
<type>(<scope>): <한국어 제목>

<선택: 변경 이유와 주의사항>

<선택: 이슈와 호환성 변경 정보>
```

| Type | 용도 |
| --- | --- |
| `feat` | 사용자 기능 추가 |
| `fix` | 결함 수정 |
| `docs` | 문서 변경 |
| `refactor` | 동작 변경 없는 구조 개선 |
| `test` | 테스트 추가 또는 수정 |
| `perf` | 성능 개선 |
| `style` | 의미 없는 서식 변경 |
| `build` | 빌드 시스템 또는 외부 의존성 변경 |
| `ci` | CI/CD 설정 변경 |
| `chore` | 그 밖의 유지보수 |
| `revert` | 이전 커밋 되돌리기 |

- scope는 변경 영역이 명확할 때만 사용한다.
- 제목은 가능하면 50자 이내의 명확한 개조식 표현으로 작성하고 마침표를 붙이지 않는다.
- 본문에는 코드만으로 알 수 없는 변경 이유와 트레이드오프를 기록한다.
- 관련 이슈는 `Refs: #123`, 완료되는 이슈는 `Closes: #123`으로 연결한다.
- 호환성을 깨는 변경은 `BREAKING CHANGE: <한국어 설명>`으로 기록한다.

```text
feat(api): 독서 기록 조회 기능 추가
fix(ai): 빈 입력 처리 오류 수정
docs(readme): 프로젝트 소개 간소화
chore(submodule): backend v1.2.0 참조 반영
```

## 9. PR 작성과 병합

- [저장소 PR 템플릿](../../.github/pull_request_template.md)을 사용한다.
- PR 하나에는 하나의 목적을 담고 관련 이슈가 있으면 연결한다.
- 제목은 Conventional Commits 형식의 한국어로 작성한다.
- 본문에는 변경 목적, 영향, 검증 결과와 주의사항을 기록한다.
- 작성자는 변경 내역과 민감정보 포함 여부를 먼저 확인한다.
- 리뷰 승인과 필요한 `harness-validation`을 확인한 뒤 병합한다.
- 소스 테스트·빌드·린트·정적 분석은 사용자가 명시적으로 요청한 경우에만 실행한다.
- 병합 후 임시 브랜치를 삭제한다.

## 10. 금지 사항

- `main` 직접 커밋 또는 push
- 공유 브랜치 force push와 이력 재작성
- `develop`에서 `main`으로 직접 병합
- 배포된 tag 이동 또는 재사용
- 서로 무관한 변경을 하나의 커밋이나 PR에 혼합
- AI 도구나 작업자 이름을 브랜치 접두사로 사용

## 11. 저장소 보호 설정

모든 iRead 저장소에 다음 설정을 적용한다.

- `main`: PR과 승인 1명을 요구하고 모든 리뷰 대화를 해결해야 하며, force push와 브랜치 삭제를 금지한다.
- `develop`: 직접 push를 허용하고 force push와 브랜치 삭제를 금지한다.
- GitHub Actions 사용 범위가 확정되기 전까지 필수 status check는 지정하지 않는다.
