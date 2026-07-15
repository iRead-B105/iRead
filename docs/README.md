# Documentation map

이 문서는 필요한 컨텍스트만 빠르게 찾기 위한 라우터다. 상태 표기는 `draft`, `proposed`, `accepted`, `deprecated`를 사용한다.

| 질문 | 먼저 읽을 문서 | 함께 갱신할 문서 |
| --- | --- | --- |
| 지금 확정된 사실은 무엇인가? | [프로젝트 컨텍스트](context/project-context.md) | 관련 ADR |
| 어떤 문제를 누구를 위해 푸는가? | [비전과 범위](product/vision-and-scope.md) | [요구사항](product/requirements.md) |
| 용어가 무엇을 뜻하는가? | [용어집](context/glossary.md) | 관련 제품 문서 |
| 시스템과 저장소 경계는 무엇인가? | [시스템 컨텍스트](architecture/system-context.md) | [저장소 전략](architecture/repository-strategy.md) |
| 서비스는 어떻게 통신하는가? | [인터페이스 원칙](architecture/interface-principles.md) | 요구사항, ADR |
| 왜 이렇게 결정했는가? | [ADR 인덱스](decisions/README.md) | 프로젝트 컨텍스트 |
| 다음에 무엇을 하는가? | [백로그](planning/backlog.md) | [로드맵](planning/roadmap.md) |
| 작업을 시작/완료할 수 있는가? | [Definition of Ready](planning/definition-of-ready.md) | [Definition of Done](planning/definition-of-done.md) |
| AI 에이전트는 어떻게 작업하는가? | [AI 개발 워크플로](workflows/ai-development.md) | `AGENTS.md`, `PLANS.md` |
| 브랜치와 커밋을 어떻게 관리하는가? | [Git Flow 및 커밋 정책](workflows/git-flow.md) | 저장소 전략, 관련 ADR |

## 문서 갱신 원칙

- 확정된 사실과 미결 사항을 섞지 않는다.
- 중요한 결정은 ADR을 만들고 관련 문서에서 링크한다.
- 제품 요구사항 변경이 시스템 경계에 영향을 주면 제품·아키텍처 문서를 같은 작업에서 갱신한다.
- 사용자의 확인 없이 `[ASSUMPTION]`을 삭제하거나 확정 사항으로 바꾸지 않는다.
