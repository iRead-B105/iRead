# 제품 탐색 백로그

- 상태: active
- 최종 검토일: 2026-07-15

작업 순서는 선행 결정을 반영한다. 상태는 `todo`, `in-progress`, `blocked`, `done`을 사용한다.

| ID | 우선순위 | 작업 | 선행 조건 | 상태 |
| --- | --- | --- | --- | --- |
| TASK-001 | P0 | 해결할 사용자 문제와 근거 정의 | 사용자 입력 | done |
| TASK-002 | P0 | 핵심 사용자와 이해관계자 정의 | TASK-001 | done |
| TASK-003 | P0 | MVP 범위와 성공 지표 정의 | TASK-001, TASK-002, 내부 기능 회의 | blocked |
| TASK-004 | P0 | 핵심 사용자 여정과 요구사항 작성 | TASK-003 | blocked |
| TASK-005 | P1 | Backend·Frontend·AI server 책임 경계 정의 | TASK-004 | blocked |
| TASK-006 | P1 | 데이터 소유권, 주 데이터베이스, Redis 역할 결정 | TASK-005 | blocked |
| TASK-007 | P1 | 인증·인가, 법정대리인 동의와 아동 개인정보 요구사항 정의 | TASK-002, TASK-004 | blocked |
| TASK-008 | P1 | 서비스 간 API/이벤트 계약 초안 작성 | TASK-005, TASK-006 | blocked |
| TASK-009 | P2 | 각 서비스 저장소명과 submodule 경로 결정 | 사용자 결정 | done |
| TASK-010 | P2 | 배포 환경, 관측성과 운영 목표 정의 | TASK-005 | blocked |
| TASK-011 | P2 | Git 저장소 및 submodule 구성 | TASK-009 | done |
| TASK-012 | P0 | 전문가·보호자 인터뷰로 문제 가설 검증 | TASK-001 | todo |
| TASK-013 | P0 | 진단·선별·훈련·치료 용어와 제품 책임 범위 검토 | TASK-001 | todo |

## 다음 확인 사항

내부 기능 회의와 별개로 TASK-012와 TASK-013을 진행할 수 있다. TASK-003을 시작하려면 아래 사항을 결정해야 한다.

- 첫 번째 MVP에서 검증할 사용자와 사용 환경
- 포함할 핵심 기능과 제외할 기능
- 구매자·운영자와 전문가의 개입 방식
- 효과, 참여도와 업무 절감 중 우선할 성공 지표
- `진단`, `선별`, `훈련`, `치료` 가운데 서비스가 책임질 범위
