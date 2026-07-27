# 문서 업데이트 로그

## 2026-07-27

* **결정**: [확정 ERD를 단일 V1 기준선으로 채택](decisions/ADR-0011-adopt-approved-erd-baseline.md)하고 기존 미적용 스키마 초안을 대체했다.
* **정합화**: MySQL 계약, Flyway V1, 확정 ERD 이미지와 생성 ERD를 23개 테이블·31개 외래 키 기준으로 동기화했다.
* **상태 변경**: 새 ERD와 Backend 엔티티의 차이가 남아 `BE-001`을 `in-progress`로 변경했다.
* **API 정합화**: 대표 캐릭터 서버 API 제거, 훈련 템플릿별 완료 횟수 조회, 음성 분기의 최종 STT 텍스트 저장 계약을 확정했다.
* **재시도·성장 정책**: 꽃은 완료 1회마다 성장해 총 5회에 만개하며, 같은 이야기 분기의 네트워크 재시도에는 최초 결과를 반환하도록 확정했다.

## 2026-07-24

* **전환**: 저장소 관리 문서를 Open Knowledge Format v0.1 구조로 전환했다.
* **결정**: [MySQL 채택](decisions/ADR-0006-mysql-primary-database.md)과 [명세 기준 원본](decisions/ADR-0007-okf-and-specification-sources.md)을 기록했다.
* **추가**: [명세 관리 워크플로](workflows/specification-management.md), [데이터 모델](architecture/data-model.md)과 [계약 카탈로그](../contracts/catalog.md)를 추가했다.
* **이전**: Notion의 활성 API 115건을 App·Admin·Auth OpenAPI로, 기능 334건을 도메인별 OKF 카탈로그로 이전했다.
* **정합화**: 별도 이야기 진행률 저장·완료 API를 보관하고 해당 기능을 음성 분기 생성 API로 통합했다.
* **정합화**: MySQL 스키마의 임시·오탈자 컬럼을 바로잡고 외래 키, 유일성, 값 범위와 다형 콘텐츠 제약을 추가했다.
* **결정**: 운영 안정성을 위해 데이터베이스 버전을 MySQL 8.4.x LTS로 확정했다.
* **검증**: 기능–API 추적 데이터와 계약 검증 워크플로를 추가했다.
