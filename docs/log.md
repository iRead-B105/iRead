# 문서 업데이트 로그

## 2026-07-29

* **훈련 입력 계약**: 34개 훈련 템플릿과 생성 문항에 `requiredInputs`를 추가해 `VOICE`, `GAZE` 사용 여부를 명시했다.
* **입력 완료 검증**: 음성 문항은 문항당 최종 발음 녹음 한 건, 시선 훈련은 원시 데이터가 있는 완료 시선 세션 한 건을 완료 조건으로 확정했다.
* **센서 실패 처리**: 음성·시선 인식 실패는 오답이나 시도 횟수로 저장하지 않고 성공 입력만 완료 근거로 사용한다.
* **문장 발음 평가**: 30초 미만 문장 녹음을 Azure Speech에 한 번 전달하고 단어별 점수·오류·음성 구간을 문항 토큰에 정렬해 저장하도록 Backend–AI 계약과 구현을 확장했다.
* **누락·삽입 정책**: `Omission`은 발음 0점·건너뛰기, `Insertion`은 부모 분석 결과의 개수로 처리하며 단어 정렬 실패 시 전체 저장을 취소한다.

## 2026-07-28

* **결정**: [Azure Speech 단어 단위 발음 평가](decisions/ADR-0013-azure-speech-pronunciation-assessment.md)를 채택하고 App → Backend → AI server → Azure 경계와 음성·자격증명 정책을 확정했다.
* **ERD 정합화**: `word_attempt_logs`에서 `has_gaze_data`, `recognized_text`를 제거하고 발음 정확도, 문항·대상·토큰 위치와 최종 시도 컬럼을 MySQL 계약·Backend에 반영했다.
* **점수 분리**: Azure `AccuracyScore`는 `pronunciation_accuracy_score`에 저장하고 `total_score`는 발음·시선·읽기 수행 종합 점수로 유지했다.
* **API 전환**: 검사·훈련 녹음 API가 클라이언트 인식 문자열·점수 대신 multipart 음성을 받고 서버 분석 결과를 반환하도록 계약을 갱신했다.
* **계획**: [Azure Speech 연동 실행 계획](../plans/2026-07-28-azure-speech-pronunciation-assessment.md)에 AI adapter, 단어 배열 정렬, 오류·비용·보안 검증과 미결 점수 정책을 기록했다.

## 2026-07-27

* **정책 경량화**: [ADR-0012](decisions/ADR-0012-lightweight-harness-policy.md)에 따라 위험 기반 계획·검증, 기록 문서 중심 메타데이터와 Git 추적 파일 기반 하네스 검증을 채택했다.
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
