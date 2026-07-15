# Glossary

- Status: draft
- Last reviewed: 2026-07-15

제품과 팀에서 같은 뜻으로 사용해야 하는 용어를 기록한다. 서비스명과 도메인이 정해지기 전에는 기술 용어만 유지한다.

| Term | Definition | Status |
| --- | --- | --- |
| iRead | 이 프로젝트의 확정된 서비스명 | accepted |
| Orchestration repository | 서비스 구현이 아니라 공통 기획, 계약, 의사결정과 통합 구성을 관리하는 저장소 | accepted |
| Backend | Spring Boot 기반의 도메인/API 서비스 저장소. 구체적 책임은 미정 | draft |
| Frontend | Vue 기반의 사용자 인터페이스 저장소. 대상 사용자와 화면 범위는 미정 | draft |
| AI server | FastAPI 기반의 AI 관련 기능 제공 저장소. 모델과 책임은 미정 | draft |
| Redis | 캐시·세션·메시징 후보 인프라. 실제 역할은 미정 | draft |

## 추가 규칙

- 동의어는 대표 용어로 연결한다.
- 기술 구현이 아니라 비즈니스 의미를 우선 설명한다.
- 의미가 바뀌면 영향을 받는 요구사항 식별자를 함께 기록한다.
