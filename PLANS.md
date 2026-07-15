# Execution plans

여러 문서나 서비스 경계를 함께 바꾸거나 한 세션을 넘어갈 수 있는 작업은 `plans/`에 실행 계획을 만든다. 계획은 다른 AI 에이전트가 이전 대화 없이도 이어서 수행할 수 있어야 한다.

## 파일 규칙

- 경로: `plans/YYYY-MM-DD-<short-topic>.md`
- 상태: `draft`, `active`, `blocked`, `completed`, `superseded`
- 계획은 자체 완결적이어야 하며 관련 source of truth를 링크한다.
- 진행 중 발견한 사실과 결정은 대화에만 남기지 말고 계획에 갱신한다.

## 필수 섹션

```md
# <목표>

- Status: draft
- Owner: [TBD]
- Created: YYYY-MM-DD
- Updated: YYYY-MM-DD

## Outcome
완료 후 사용자가 관찰할 수 있는 결과.

## Context
관련 문서, 현재 상태, 제약과 비목표.

## Clarifications required
작업 전에 사용자 결정이 필요한 질문. 없으면 `없음`.

## Steps
- [ ] 독립적으로 검증 가능한 단계

## Validation
각 결과를 확인할 명령 또는 검토 기준. 소스 테스트·빌드·린트·정적 분석은 계획에 적혀 있어도 사용자가 명시적으로 요청한 경우에만 실행한다.

## Progress log
- YYYY-MM-DD: 수행 내용과 발견 사항

## Decisions and changes
계획 중 확정한 결정 및 연결된 ADR.

## Remaining risks
미결 사항, 위험, 후속 작업.
```

## 운영 규칙

- 작업을 시작할 때 `Status`를 `active`로 바꾸고 체크리스트를 최신 상태로 유지한다.
- 막힘은 원인과 해제 조건을 기록한다. 사용자 결정이 필요하면 추측해 우회하지 않는다.
- 완료 시 실행한 검증 증거, 사용자 요청이 없어 실행하지 않은 검증과 남은 위험을 기록한 뒤 `completed`로 바꾼다.
- 범위가 크게 달라지면 기존 계획을 `superseded`로 표시하고 새 계획으로 연결한다.
