# Git Flow 및 커밋 정책

- Status: accepted
- Last reviewed: 2026-07-15
- Applies to: Orchestration, Backend, Frontend, AI server repositories

## 1. 기본 원칙

- 정통 Git Flow의 `main`과 `develop` 장기 브랜치를 사용한다.
- 모든 변경은 목적에 맞는 작업 브랜치와 Pull Request를 거친다.
- 브랜치명에는 작업 종류만 표현한다. 사람, AI 모델 또는 도구의 이름을 넣지 않는다.
- 커밋은 하나의 논리적 변경만 포함하고 언제든 검토하거나 되돌릴 수 있어야 한다.
- `main`은 항상 배포 가능한 상태, `develop`은 다음 릴리스의 통합 상태를 유지한다.
- 이 정책은 Git 저장소를 실제로 초기화한 뒤 적용한다. 현재 문서화만으로 Git 작업을 시작하지 않는다.

## 2. 브랜치 구조

| Branch | Base | Merge target | Purpose | Lifetime |
| --- | --- | --- | --- | --- |
| `main` | - | - | 운영에 배포된 릴리스 이력 | permanent |
| `develop` | `main` | - | 다음 릴리스의 통합 기준 | permanent |
| `feature/*` | `develop` | `develop` | 기능, 일반 버그 수정, 문서 및 리팩터링 | temporary |
| `release/*` | `develop` | `main`, `develop` | 릴리스 안정화와 버전 준비 | temporary |
| `hotfix/*` | `main` | `main`, `develop` | 운영 버전의 긴급 수정 | temporary |

`develop`을 `main`에 직접 병합하지 않는다. 정식 배포는 `release/*`, 긴급 배포는 `hotfix/*`를 통한다.

## 3. 브랜치 이름 규칙

### 허용 형식

```text
feature/<issue-number>-<short-description>
release/<semantic-version>
hotfix/<semantic-version>
```

예시:

```text
feature/123-reading-history
feature/148-update-api-contract
release/1.2.0
hotfix/1.2.1
```

### 작성 규칙

- 영문 소문자, 숫자와 하이픈만 사용한다.
- 설명은 짧은 kebab-case로 작성한다.
- 이슈가 있으면 번호를 반드시 포함한다.
- `feature`, `release`, `hotfix` 외 접두사는 팀 합의와 정책 개정 없이 추가하지 않는다.
- `codex/`, `claude/`, `gemini/`, `ai/`, 개인 이름 등 작업 주체를 나타내는 접두사는 사용하지 않는다.
- 브랜치 하나에는 하나의 목적만 둔다.

## 4. 브랜치별 작업 흐름

### Feature

1. 최신 `develop`에서 `feature/*` 브랜치를 만든다.
2. 작고 논리적인 단위로 커밋한다.
3. 작업 중 최신 `develop`이 필요하면 개인 작업 브랜치에서 rebase한다.
4. `harness-validation`과 사용자가 명시적으로 요청한 검증을 통과한 뒤 `develop` 대상으로 Pull Request를 만든다.
5. 기본적으로 squash merge하고 작업 브랜치를 삭제한다.

공유 중인 feature 브랜치는 다른 작업자의 커밋을 다시 쓰지 않도록 rebase 전에 합의한다.

### Release

1. 릴리스할 `develop`에서 `release/<version>`을 만든다.
2. 버전, 문서, 설정과 릴리스 차단 버그만 수정한다. 새 기능은 추가하지 않는다.
3. 필수 `harness-validation`과 사용자가 명시적으로 요청한 검증 후 `main`에 `--no-ff` merge commit으로 병합한다.
4. `main`의 병합 결과에 `v<version>` annotated tag를 만든다.
5. 같은 release 브랜치를 `develop`에도 `--no-ff`로 병합하여 안정화 변경을 되돌려 보낸다.
6. 검증과 tag 확인 후 release 브랜치를 삭제한다.

### Hotfix

1. 운영 중인 최신 `main`에서 `hotfix/<version>`을 만든다.
2. 긴급 문제에 필요한 최소 변경과 회귀 테스트만 포함한다.
3. 필수 `harness-validation`과 사용자가 명시적으로 요청한 검증 후 `main`에 `--no-ff` merge하고 `v<version>` tag를 만든다.
4. 같은 hotfix 브랜치를 `develop`에도 `--no-ff`로 병합한다.
5. 활성 release 브랜치가 있다면 해당 수정의 반영 여부도 확인한다.
6. 배포 및 역병합 확인 후 hotfix 브랜치를 삭제한다.

## 5. Squash merge와 merge commit

### Squash merge

작업 브랜치의 여러 커밋을 대상 브랜치의 하나의 커밋으로 합친다.

- 장점: `develop` 이력이 기능 단위로 단순해지고 중간 수정·WIP 커밋이 남지 않는다.
- 단점: 작업 브랜치의 세부 커밋 경계와 원래 commit SHA가 대상 브랜치에 유지되지 않는다.
- 적합한 경우: 짧은 feature 브랜치, 일반 기능·문서·리팩터링 PR.

### Merge commit (`--no-ff`)

작업 브랜치의 개별 커밋과 분기 구조를 유지하면서 별도의 병합 커밋을 만든다.

- 장점: 언제 어떤 release/hotfix 분기가 병합되었는지 추적하기 쉽고 전체 커밋 이력을 보존한다.
- 단점: 작은 PR까지 사용하면 그래프와 로그가 불필요하게 복잡해진다.
- 적합한 경우: release, hotfix처럼 분기 자체가 중요한 작업.

### 권장 정책

| Merge path | Method | Reason |
| --- | --- | --- |
| `feature/*` → `develop` | Squash merge | 기능 단위의 깨끗한 통합 이력 |
| `release/*` → `main`, `develop` | Merge commit (`--no-ff`) | 릴리스 경계와 역병합 이력 보존 |
| `hotfix/*` → `main`, `develop` | Merge commit (`--no-ff`) | 긴급 수정의 배포 및 역병합 추적 |

이 혼합 방식이 Git Flow의 분기 이력을 보존하면서 일상 개발 이력을 간결하게 유지하는 기본 정책이다.

## 6. 커밋 메시지 규칙

[Conventional Commits](https://www.conventionalcommits.org/) 형식을 사용하고 제목과 본문은 한국어로 작성한다.

```text
<type>(<scope>): <한국어 제목>

<선택: 변경 이유와 주의사항>

<선택: 이슈, breaking change 등의 footer>
```

### Type

| Type | Use |
| --- | --- |
| `feat` | 사용자에게 제공되는 기능 추가 |
| `fix` | 결함 수정 |
| `docs` | 문서만 변경 |
| `refactor` | 동작 변경 없는 구조 개선 |
| `test` | 테스트 추가 또는 수정 |
| `perf` | 성능 개선 |
| `style` | 의미 없는 서식 변경 |
| `build` | 빌드 시스템 또는 외부 의존성 변경 |
| `ci` | CI/CD 설정 변경 |
| `chore` | 위 유형에 속하지 않는 유지보수 |
| `revert` | 이전 커밋 되돌리기 |

### Scope

- 선택 사항이며 변경 영역이 명확할 때만 사용한다.
- 예: `orchestration`, `backend`, `frontend`, `ai`, `api`, `auth`, `submodule`.
- 각 서비스 저장소에서는 실제 모듈이나 도메인 이름을 우선 사용한다.

### 제목과 본문

- 제목은 명확한 개조식 표현으로 작성하고 마침표를 붙이지 않는다.
- 제목은 가능하면 50자 이내로 작성한다.
- `수정`, `변경`만 쓰지 말고 무엇이 어떻게 달라졌는지 표현한다.
- 본문에는 코드 자체로 알 수 없는 변경 이유와 트레이드오프를 기록한다.
- 관련 이슈는 footer에 `Refs: #123`, 완료되는 이슈는 `Closes: #123`으로 연결한다.
- 호환성을 깨는 변경은 `BREAKING CHANGE: <한국어 설명>`을 footer에 기록한다.

예시:

```text
feat(api): 독서 기록 조회 기능 추가
fix(ai): 빈 입력 처리 중 발생하는 오류 수정
docs(orchestration): Git Flow 정책 문서화
chore(submodule): backend v1.2.0 참조 반영
```

## 7. 커밋 단위

- 커밋 하나에는 하나의 변경 이유만 포함한다.
- 기능 코드, 무관한 리팩터링과 대규모 서식 변경을 한 커밋에 섞지 않는다.
- 각 커밋은 가능한 한 빌드 및 테스트 가능한 상태여야 한다.
- 비밀값, 생성물, 로컬 환경 설정과 대용량 바이너리를 커밋하지 않는다.
- `WIP`, `temp`, `fix again` 같은 임시 메시지는 최종 대상 브랜치에 남기지 않는다.
- feature 브랜치의 정리가 필요하면 PR 병합 전에 interactive rebase를 사용할 수 있지만 공유 브랜치의 이력은 다시 쓰지 않는다.

## 8. Pull Request 정책

- 모든 PR은 [저장소 PR 템플릿](../../.github/pull_request_template.md)을 사용한다.
- PR 하나는 하나의 목적과 추적 가능한 이슈를 가진다.
- PR 제목은 squash 결과로 사용할 수 있도록 Conventional Commits 형식의 한국어 제목으로 작성한다.
- 본문에는 목적, 주요 변경, 비범위, 검증 결과, 위험과 롤백 방법을 기록한다.
- 필수 `harness-validation`과 사용자가 명시적으로 요청한 검증이 성공하고 최소 한 명의 리뷰 승인을 받은 뒤 병합한다.
- 작성자는 자신의 diff와 민감정보 포함 여부를 먼저 검토한다.
- 리뷰 중 추가된 변경의 테스트·빌드·린트·정적 분석은 사용자가 다시 명시적으로 요청한 경우에만 실행한다.
- merge 후 임시 브랜치를 삭제한다.

## 9. 금지 사항

- `main`, `develop`, `release/*`, `hotfix/*` 직접 push
- 보호 브랜치 force push 또는 이력 재작성
- 검증 실패나 필수 리뷰를 우회한 병합
- `develop`에서 `main`으로의 직접 병합
- tag 이동 또는 배포된 tag 재사용
- 서로 무관한 변경을 하나의 PR이나 커밋에 혼합
- AI 도구나 작업자 이름을 브랜치 접두사로 사용

## 10. 저장소 보호 권장 설정

Git 호스팅을 설정할 때 `main`과 `develop`에 다음 규칙을 적용한다.

- Pull Request를 통한 변경만 허용
- 필수 CI status check 통과
- 필수 status check로 `harness-validation` 지정
- 소스 테스트·빌드·린트·정적 분석 workflow는 사용자의 명시적 요청 없이 추가하지 않음
- 최소 1명 승인 및 변경 후 승인 무효화
- force push와 branch deletion 금지
- 대화가 해결되지 않은 PR의 병합 금지
- `main`의 릴리스 tag는 `vMAJOR.MINOR.PATCH` 형식으로 보호
