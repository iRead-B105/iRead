# iRead orchestration

`iRead`는 확정된 서비스명이며, 이 디렉터리는 iRead의 오케스트레이션 저장소입니다.

이 디렉터리는 서비스 기획, 시스템 경계, 저장소 간 계약, 의사결정과 실행 계획을 관리하는 오케스트레이션 저장소입니다. Spring Boot 백엔드, Vue 프런트엔드, FastAPI AI 서버는 각각 별도 저장소로 만들고 이후 Git submodule로 연결합니다.

현재 단계에서는 서비스 소스 코드, Git 저장소, 원격 저장소, submodule을 만들지 않습니다.

## 시작 순서

1. [프로젝트 컨텍스트](docs/context/project-context.md)에서 확정 사항과 미결 사항을 확인합니다.
2. [제품 비전과 범위](docs/product/vision-and-scope.md)를 작성합니다.
3. [용어집](docs/context/glossary.md)과 [요구사항](docs/product/requirements.md)을 함께 갱신합니다.
4. 중요한 선택은 [ADR](docs/decisions/README.md)로 기록합니다.
5. 구현 가능한 작업은 [백로그](docs/planning/backlog.md)와 `plans/`의 실행 계획으로 구체화합니다.

## 현재 기술 기준선

| 영역 | 기준선 |
| --- | --- |
| Backend | Spring Boot 3, Java 21, Gradle Kotlin DSL |
| Frontend | Vue 3, TypeScript, Vite, pnpm |
| AI server | FastAPI, Python 3.12, uv |
| Cache / messaging candidate | Redis, Docker Compose |

Redis의 구체적 책임과 주 데이터베이스는 아직 결정하지 않았습니다.

## AI 하네스

- `AGENTS.md`: AI 모델이나 도구에 관계없이 사용하는 단일 범용 지침
- `PLANS.md`: 긴 작업의 실행 계획 작성 규약
- `docs/workflows/ai-development.md`: 탐색부터 컨텍스트 갱신까지의 작업 루프
- `tools/validate_harness.py`: 필수 문서와 내부 Markdown 링크 검증
- `.github/pull_request_template.md`: 내부 팀용 Pull Request 작성 기준

AI 도구가 `AGENTS.md`를 자동으로 읽지 않는 경우에는 세션을 시작할 때 이 파일을 컨텍스트로 제공한다. 모델별 지침 파일은 별도로 관리하지 않는다.

## 검증

Python 3.12 이상에서 다음 명령을 실행합니다.

```bash
python tools/validate_harness.py
```

GitHub Actions는 모든 Pull Request와 `main`, `develop` push에서 문서 구조와 링크 검증만 자동 실행합니다. 브랜치 보호의 필수 status check 이름은 `harness-validation`입니다. 소스 테스트·빌드·린트·정적 분석은 포함하지 않습니다.
