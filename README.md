# iRead

iRead의 제품 기획, 시스템 아키텍처, 서비스 간 계약과 주요 의사결정을 관리하는 오케스트레이션 저장소입니다.

Backend, Frontend, AI server는 별도 저장소로 관리하고 Git submodule로 연결합니다.

## 주요 문서

| 목적 | 문서 |
| --- | --- |
| 프로젝트 현황 | [프로젝트 컨텍스트](docs/context/project-context.md) |
| 제품 목표와 범위 | [제품 비전과 범위](docs/product/vision-and-scope.md) |
| 요구사항 | [제품 요구사항](docs/product/requirements.md) |
| 시스템 구조 | [시스템 컨텍스트](docs/architecture/system-context.md) |
| 주요 의사결정 | [ADR](docs/decisions/README.md) |
| 작업 계획 | [백로그](docs/planning/backlog.md), [실행 계획](plans/README.md) |

## 기술 스택

| 영역 | 기준선 |
| --- | --- |
| Backend | Spring Boot 3, Java 21, Gradle Kotlin DSL |
| Frontend | Vue 3, TypeScript, Vite, pnpm |
| AI server | FastAPI, Python 3.12, uv |
| Infrastructure | Redis, Docker Compose |

## 개발 가이드

- `AGENTS.md`: AI 모델이나 도구에 관계없이 사용하는 단일 범용 지침
- `PLANS.md`: 긴 작업의 실행 계획 작성 규약
- `docs/workflows/ai-development.md`: 탐색부터 컨텍스트 갱신까지의 작업 루프
- `docs/workflows/git-flow.md`: 브랜치, 커밋과 병합 정책
- `docs/workflows/documentation-style.md`: 문서 어투와 표현 원칙
- `tools/validate_harness.py`: 필수 문서와 내부 Markdown 링크 검증
- `.github/pull_request_template.md`: 내부 팀용 PR 작성 기준

## 하네스 검증

Python 3.12 이상에서 다음 명령을 실행합니다.

```bash
python tools/validate_harness.py
```

PR과 `main`, `develop` push에서는 GitHub Actions가 같은 검증을 실행합니다.
