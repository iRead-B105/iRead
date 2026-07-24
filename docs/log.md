# 문서 업데이트 로그

## 2026-07-24

* **전환**: 저장소 관리 문서를 Open Knowledge Format v0.1 구조로 전환했다.
* **결정**: [MySQL 채택](decisions/ADR-0006-mysql-primary-database.md)과 [명세 기준 원본](decisions/ADR-0007-okf-and-specification-sources.md)을 기록했다.
* **추가**: [명세 관리 워크플로](workflows/specification-management.md), [데이터 모델](architecture/data-model.md)과 [계약 카탈로그](../contracts/catalog.md)를 추가했다.
* **이전**: Notion의 활성 API 115건을 App·Admin·Auth OpenAPI로, 기능 334건을 도메인별 OKF 카탈로그로 이전했다.
* **정합화**: 별도 이야기 진행률 저장·완료 API를 보관하고 해당 기능을 음성 분기 생성 API로 통합했다.
* **정합화**: MySQL 스키마의 임시·오탈자 컬럼을 바로잡고 외래 키, 유일성, 값 범위와 다형 콘텐츠 제약을 추가했다.
* **결정**: 운영 안정성을 위해 데이터베이스 버전을 MySQL 8.4.x LTS로 확정했다.
* **검증**: 기능–API 추적 데이터와 계약 검증 워크플로를 추가했다.
