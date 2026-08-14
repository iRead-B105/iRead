# iRead 문서

이 디렉터리는 iRead의 제품, 아키텍처, 결정과 계획을 연결하는 문서 모음이다. ADR, 실행 계획과 승인 기능 명세처럼 추적이 필요한 기록 문서만 `type` frontmatter를 강제한다.

필요한 문서를 빠르게 찾을 수 있도록 문서별 역할과 변경 영향이 있을 때 확인할 문서를 정리한다. 상태가 필요한 기록은 `draft`, `proposed`, `accepted`, `deprecated`로 표시한다.

| 질문 | 먼저 읽을 문서 | 영향 시 확인할 문서 |
| --- | --- | --- |
| 지금 확정된 사실은 무엇인가? | [프로젝트 컨텍스트](context/project-context.md) | 관련 ADR |
| 어떤 문제를 누구를 위해 푸는가? | [비전과 범위](product/vision-and-scope.md) | [요구사항](product/requirements.md) |
| 문제의 근거와 검증할 가설은 무엇인가? | [문제 및 근거 조사](product/research-basis.md) | 비전과 범위, 백로그 |
| 문제 가설을 어떻게 검증하는가? | [문제 가설 검증 계획](product/problem-validation-plan.md) | 문제 및 근거 조사, 백로그 |
| 진단·선별·훈련·치료를 어떻게 구분하는가? | [제품 용어 및 책임 경계](product/product-responsibility-boundary.md) | 비전과 범위, 용어집 |
| 아동용 앱 화면과 리소스는 어떤 기준으로 만드는가? | [아이리드 앱 디자인 가이드](product/iread-app-design-guide.md) | 아동 앱 구현, 제품 요구사항 |
| 앱 리소스를 어떤 화풍·파일·상태로 제작하는가? | [아이리드 앱 리소스 가이드](product/iread-app-resource-guide.md) | [Frontend 리소스 정비 계획](planning/frontend-resource-plan.md), `frontend-app` |
| 현재 frontend 에셋은 무엇이고 어떤 조치가 필요한가? | [Frontend 에셋 인벤토리](product/frontend-asset-inventory.md) | 앱 리소스 가이드, Frontend 리소스 정비 계획 |
| 아동용 앱의 세부 디자인 정책을 어떻게 결정하는가? | [아이리드 앱 디자인 정책 의사결정 질문서](product/iread-app-design-decision-questionnaire.md) | 앱 디자인 가이드, `frontend-app` 구현 |
| 용어가 무엇을 뜻하는가? | [용어집](context/glossary.md) | 관련 제품 문서 |
| 시스템과 저장소 경계는 무엇인가? | [시스템 컨텍스트](architecture/system-context.md) | [저장소 전략](architecture/repository-strategy.md) |
| 5개 서브모듈 통합 작업을 하려면? | [시스템 통합 작업용 하네스](architecture/system-integration-harness.md) | 시스템 컨텍스트, 인터페이스 원칙, 계약 카탈로그 |
| 서비스는 어떻게 통신하는가? | [인터페이스 원칙](architecture/interface-principles.md) | 요구사항, ADR |
| 왜 이렇게 결정했는가? | [ADR 인덱스](decisions/index.md) | 프로젝트 컨텍스트 |
| 다음에 무엇을 하는가? | [제품 탐색 백로그](planning/backlog.md), [Backend·Frontend 구현 백로그](planning/implementation-backlog.md), [실시간 데이터 연동 TODO](planning/realtime-data-sync-todo.md) | [로드맵](planning/roadmap.md) |
| 작업을 시작/완료할 수 있는가? | [시작 준비 기준](planning/definition-of-ready.md) | [완료 기준](planning/definition-of-done.md) |
| AI 에이전트는 어떻게 작업하는가? | [AI 개발 워크플로](workflows/ai-development.md) | `AGENTS.md`, `PLANS.md` |
| 브랜치와 커밋을 어떻게 관리하는가? | [Git Flow 및 커밋 정책](workflows/git-flow.md) | 저장소 전략, 관련 ADR |
| submodule을 어떻게 받거나 갱신하는가? | [submodule 운영 가이드](workflows/submodules.md) | 저장소 전략 |
| GitLab 단일 저장소를 어떻게 갱신하는가? | [GitLab 단일 저장소 동기화](workflows/gitlab-monorepo-sync.md) | [ADR-0009](decisions/ADR-0009-gitlab-monorepo-mirror.md) |
| Jira 작업 자동화를 검토하려면? | [Jira 작업 관리 자동화 제안](workflows/jira-automation-proposal.md) | `AGENTS.md`, 구현 백로그 |
| 문서는 어떤 어투로 작성하는가? | [문서 작성 원칙](workflows/documentation-style.md) | `AGENTS.md`, 문서 템플릿 |
| 기능·API·SQL 명세는 어디서 관리하는가? | [명세 관리 워크플로](workflows/specification-management.md) | [계약 카탈로그](../contracts/catalog.md), 관련 ADR |

## 디렉터리

* [컨텍스트](context/) - 현재 사실과 공통 용어
* [제품](product/) - 제품 범위, 요구사항과 기능 명세
* [아키텍처](architecture/) - 시스템 경계, 인터페이스와 데이터 모델
* [결정](decisions/) - ADR
* [계획](planning/) - 백로그, 로드맵과 완료 기준
* [워크플로](workflows/) - 문서, Git, AI 작업과 명세 관리 절차
* [템플릿](templates/) - 기능 명세와 작업 문서 템플릿
* [검토 보고서](reviews/) - 구현 간 정합성, 통합 준비도와 잔여 위험 점검

## 문서 갱신 원칙

- 확정된 사실과 미결 사항을 섞지 않는다.
- 되돌리기 어렵거나 여러 팀에 영향을 주는 결정은 ADR을 만들고 관련 문서에서 링크한다.
- 제품 요구사항 변경이 시스템 경계에 영향을 줄 때만 제품·아키텍처 문서를 함께 갱신한다.
- 사용자의 확인 없이 `[ASSUMPTION]`을 삭제하거나 확정 사항으로 바꾸지 않는다.
- 문서 추가·삭제·이름 변경 때 관련 인덱스를 갱신하고, 관계는 일반 Markdown 링크로 표현한다.
