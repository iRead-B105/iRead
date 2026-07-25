# MySQL 스키마 계약

* [스키마 계약](schema.sql) - Backend Flyway migration 누적 결과와 동일하게 유지하는 MySQL DDL이며 PK, FK, UNIQUE, CHECK 제약을 포함한다.
* [MySQL ERD](erd.md) - `schema.sql`의 테이블과 외래 키에서 자동 생성한 Mermaid 관계도
* [Backend 정합화](backend-alignment.md) - 최신 엔티티와 스키마의 차이, Flyway 적용 결과와 기존 DB 적용 경계
* [데이터 모델](../../docs/architecture/data-model.md) - 소유권과 변경 규칙
* [ADR-0006](../../docs/decisions/ADR-0006-mysql-primary-database.md) - MySQL 채택 결정

ERD는 `python tools/generate_erd.py`로 갱신하고 `python tools/generate_erd.py --check`로 스키마와의 동기화 상태를 확인한다.
