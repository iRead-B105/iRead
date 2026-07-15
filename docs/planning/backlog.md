# Product discovery backlog

- Status: active
- Last reviewed: 2026-07-15

작업 순서는 선행 결정을 반영한다. 상태는 `todo`, `in-progress`, `blocked`, `done`을 사용한다.

| ID | Priority | Work item | Depends on | Status |
| --- | --- | --- | --- | --- |
| TASK-001 | P0 | 해결할 사용자 문제와 근거 정의 | 사용자 입력 | todo |
| TASK-002 | P0 | 핵심 사용자와 이해관계자 정의 | TASK-001 | blocked |
| TASK-003 | P0 | MVP 범위와 성공 지표 정의 | TASK-001, TASK-002 | blocked |
| TASK-004 | P0 | 핵심 사용자 여정과 요구사항 작성 | TASK-003 | blocked |
| TASK-005 | P1 | Backend·Frontend·AI server 책임 경계 정의 | TASK-004 | blocked |
| TASK-006 | P1 | 데이터 소유권, 주 데이터베이스, Redis 역할 결정 | TASK-005 | blocked |
| TASK-007 | P1 | 인증·인가·개인정보 요구사항 정의 | TASK-002, TASK-004 | blocked |
| TASK-008 | P1 | 서비스 간 API/이벤트 계약 초안 작성 | TASK-005, TASK-006 | blocked |
| TASK-009 | P2 | 각 서비스 저장소명과 submodule 경로 결정 | TASK-005 | blocked |
| TASK-010 | P2 | 배포 환경, 관측성과 운영 목표 정의 | TASK-005 | blocked |
| TASK-011 | P2 | Git 저장소 및 submodule 구성 | TASK-009 | blocked |

## Next clarification

다음 작업을 시작하려면 TASK-001에 필요한 아래 정보를 사용자에게 질문한다.

- 주 사용자는 누구인가?
- 사용자가 현재 겪는 가장 중요한 문제는 무엇인가?
- 서비스가 제공해야 할 핵심 결과는 무엇인가?
- 문제와 사용자에 대해 이미 확보한 조사나 제약이 있는가?
