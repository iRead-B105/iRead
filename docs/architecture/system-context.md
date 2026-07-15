# 시스템 컨텍스트

- 상태: proposed
- 최종 검토일: 2026-07-15

현재 다이어그램은 확정된 저장소 분리 원칙만 표현한다. 서비스 책임, 호출 방향, 외부 시스템과 저장소 경로는 결정하지 않았다.

```mermaid
flowchart LR
    U["사용자 / 이해관계자 [TBD]"]
    F["Frontend 저장소<br/>Vue 3 + TypeScript"]
    B["Backend 저장소<br/>Spring Boot 3 + Java 21"]
    A["AI server 저장소<br/>FastAPI + Python 3.12"]
    R["Redis<br/>역할 [TBD]"]
    O["Orchestration 저장소<br/>기획 · 계약 · 결정 · 통합 구성"]

    U -. "사용 흐름 [TBD]" .-> F
    F -. "API 계약 [TBD]" .-> B
    B -. "AI 호출 계약 [TBD]" .-> A
    B -. "사용 목적 [TBD]" .-> R
    A -. "사용 목적 [TBD]" .-> R
    O -. "submodule / 계약" .-> F
    O -. "submodule / 계약" .-> B
    O -. "submodule / 계약" .-> A
```

## 미결 경계

- 인증과 사용자 데이터의 소유 서비스
- 동기 HTTP, 비동기 메시징 등 서비스 간 통신 방식
- AI 작업의 요청·상태·결과 저장 방식
- Redis를 사용하는 서비스와 장애 시 동작
- 외부 AI 모델, 스토리지, 관측 도구와 배포 환경
