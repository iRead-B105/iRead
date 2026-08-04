# 문서 업데이트 로그

## 2026-08-05

* **교수자 이야기 시선 판정 계약**: Backend가 `story-gaze-word-v1`로 동일 단어 응시 구간, 체류·건너뜀·되돌아보기를 판정하고 `wordMetrics`와 `replay.events`를 반환하도록 확정했다. 동일 token sample 공백은 최대 250ms, 방문 tail은 80ms, 최초 확인 시점은 페이지 첫 유효 token sample 기준 상대 시간으로 통일했다.
* **이동 경로·히트맵 책임 분리**: 교수자 Frontend는 Backend event를 700ms 간격으로 재생하고 마지막 event에서 페이지 상대 체류 히트맵으로 전환한다. raw 좌표 재생·판정과 page metric 단어 균등 분배는 사용하지 않는다.

## 2026-07-31

* **Flyway V1·V2 기준선 통합 검증**: 최종 스키마를 V1, 전체 데모 데이터를 V2로 통합하고 공식 MySQL Community Server 8.4.11의 빈 DB에서 Flyway·Hibernate mapping·제약조건·동시성·데모 seed 테스트 8건을 최신 `develop` 병합 전후 모두 통과했다.

## 2026-07-29

* **훈련 입력 계약**: 34개 훈련 템플릿과 생성 문항에 `requiredInputs`를 추가해 `VOICE`, `GAZE` 사용 여부를 명시했다.
* **입력 완료 검증**: 음성 문항은 문항당 최종 발음 녹음 한 건, 시선 훈련은 원시 데이터가 있는 완료 시선 세션 한 건을 완료 조건으로 확정했다.
* **센서 실패 처리**: 음성·시선 인식 실패는 오답이나 시도 횟수로 저장하지 않고 성공 입력만 완료 근거로 사용한다.
* **문장 발음 평가**: 30초 미만 문장 녹음을 Azure Speech에 한 번 전달하고 단어별 점수·오류·음성 구간을 문항 토큰에 정렬해 저장하도록 Backend–AI 계약과 구현을 확장했다.
* **누락·삽입 정책**: `Omission`은 발음 0점·건너뛰기, `Insertion`은 부모 분석 결과의 개수로 처리하며 단어 정렬 실패 시 전체 저장을 취소한다.
* **아동 훈련 목록**: 인증된 아동이 본인의 현재 진행 가능한 커리큘럼과 훈련 순서·영역·이름·상태를 조회하는 App API를 추가했다.

* **결정**: [Azure Speech 단어 단위 발음 평가](decisions/ADR-0013-azure-speech-pronunciation-assessment.md)를 채택하고 App → Backend → AI server → Azure 경계와 음성·자격증명 정책을 확정했다.
* **ERD 정합화**: `word_attempt_logs`에서 `has_gaze_data`, `recognized_text`를 제거하고 발음 정확도, 문항·대상·토큰 위치와 최종 시도 컬럼을 MySQL 계약·Backend에 반영했다.
* **점수 분리**: Azure `AccuracyScore`는 `pronunciation_accuracy_score`에 저장하고 `total_score`는 발음·시선·읽기 수행 종합 점수로 유지했다.
* **API 전환**: 검사·훈련 녹음 API가 클라이언트 인식 문자열·점수 대신 multipart 음성을 받고 서버 분석 결과를 반환하도록 계약을 갱신했다.
* **계획**: [Azure Speech 연동 실행 계획](../plans/2026-07-28-azure-speech-pronunciation-assessment.md)에 AI adapter, 단어 배열 정렬, 오류·비용·보안 검증과 미결 점수 정책을 기록했다.
* **MySQL 8.4 실제 통합 검증**: 공식 체크섬을 확인한 MySQL Community Server 8.4.11 임시 인스턴스에서 Flyway·JPA 매핑, 제약조건, 동시성 잠금과 데모 seed 통합 테스트 4건을 모두 통과했다.
* **Mailpit 계정 복구 E2E 검증**: Mailpit 1.30.6과 실제 Backend·MySQL을 연결해 메일 수신, 43자 일회용 토큰 링크, 비밀번호 변경, 토큰 재사용 거부, 토큰 원문 비저장, 기존 refresh session 폐기와 변경 비밀번호 로그인을 확인했다.
* **데모 훈련 seed 충돌 수정**: 데모 SQL의 커리큘럼 단원·템플릿 위치를 정식 `training-templates.json` 기준과 맞춰 demo profile 기동 시 `(curriculum_unit_id, sequence_no)` 중복으로 종료되던 문제를 해결하고, MySQL 데모 통합 테스트에서 34개 템플릿 초기화를 검증했다.
* **교수자 Frontend 백로그 현행화**: 라우팅·환경 설정·API/mock 저장소, 인증·학생 관리·훈련·검사·보고서·시선·프로필 화면과 364개 Frontend 테스트, production build·lint 성공을 근거로 `FE-001`~`FE-005`를 `done`으로 변경했다. 아동 앱 범위가 함께 있는 `FE-011`~`FE-012`는 인계 작업이 남아 있어 유지했다.
* **교수자 보고서 계약 정합화**: 보고서 삭제 API를 폐기하고 저장된 분석 스냅샷을 유지하며, 교수자 의견은 생성·수정 모두 최대 2,000자로 통일했다.
* **교수자 프로필 계약 정합화**: 이메일을 읽기 전용 로그인 식별자로 고정하고 연락처·주소를 프로필 범위에서 제외했으며, 프로필 이미지는 실제 JPG·PNG 파일만 최대 5MB까지 허용하도록 검증했다.
* **교수자 계정 복구 전환**: 별도 아이디 찾기와 고정 데모 코드를 폐기하고 [ADR-0014](decisions/ADR-0014-email-password-reset.md)의 10분 만료 일회용 이메일 링크, 토큰 해시 저장, 요청 제한과 refresh session 폐기를 구현했다. 로컬 데모 메일함은 Mailpit을 사용한다.
* **보고서 빈 기간·중복 생성 차단**: 완료된 훈련·검사가 없는 기간은 `REPORT_DATA_NOT_FOUND`로 저장하지 않고, `reports(student_id, start_date, end_date)` UNIQUE와 사전 검사로 동일 기간 중복을 차단해 기존 보고서를 다시 열 수 있도록 했다.
* **교수자 보고서 시선 추이 자동 집계**: body 없는 갱신 요청으로 보고서 기간의 훈련·검사 시선 분석 결과를 Backend가 자동 수집해 시간순 추이, 변화량과 실패 세션 건수를 `snapshot.gazeTrend`에 저장하도록 통일했다.
* **교수자 보고서 상세 응답 정합화**: 저장된 분석 결과를 평면 필드로 변환하지 않고 `studentId`, `snapshot`, `teacherMemo` 구조로 반환하도록 Backend·Frontend·OpenAPI 계약을 통일했다.
* **교수자 보고서 목록 계약 활성화**: Backend에 구현된 `GET /api/admin/report`를 저장소 유래 OpenAPI 계약으로 명시하고, 교수자 Frontend의 임시 목록 차단 로직을 제거했다.
* **교수자 검사 비교 통계 보류**: 종합·영역별 점수와 추천 계산 규칙을 `BE-032`로 기록하고 App 결과 JSON 계약 확정 이후로 연기했다.
* **교수자 검사 목록 응답 정합화**: Frontend가 Backend·OpenAPI의 `testHistory` wrapper를 해제한 뒤 완료 검사를 최신순으로 표시하도록 수정했다.
* **교수자 커리큘럼 이력 기간 정합화**: 30일·3개월 선택을 완료일 기준 `from`·`to` 범위로 변환해 Frontend·OpenAPI·Backend에 적용했다. 기간별 읽기 속도 통계는 음성 분석 작업 범위로 분리했다.
* **교수자 훈련 이력 기간 정합화**: Frontend의 30일·3개월 선택을 Backend 계약의 `from`·`to` 날짜 범위로 변환하고 데모 저장소에도 동일한 달력 경계 규칙을 적용했다.
* **교수자 학습 이벤트 정합화**: 최근 학습 이벤트 목록 API를 추가하고 상세 조회를 `eventType + eventId` 복합 식별 방식으로 통일했다.
* **교수자 학생 목록 정합화**: 이름·학교, 만 나이, 최근 학습 기간 필터와 0-based 페이지 계약을 Frontend·OpenAPI·Backend에 동일하게 적용하고 주간 참여·누적 학습 필드를 실제 응답에 추가했다.
* **계약 출처 표시**: Notion 이관 이후 저장소에서 추가한 API는 `x-contract-origin: repository`로 구분하도록 계약 검증 규칙을 확장했다.

## 2026-07-28

* **App–Backend 비음성 정합화**: 훈련·검사 문항을 `questionType`, `responseType`, `content`, 선택적 `requiredInputs` 표시 계약으로 변환하고 정답·분석 정보를 아동 App에서 숨겼다.
* **서버 판정·멱등성**: App은 원시 응답과 `submissionId`만 보내며 Backend가 저장된 정답으로 평가한다. 훈련 최대 3회·힌트·정답 공개와 검사 최초 제출 원칙을 기존 결과 JSON에서 처리한다.
* **완료 화면 경계**: 훈련 완료 요청 body와 검사 문항별 완료 API를 제거하고, 서버 완료 시각과 칭찬 화면 정보만 아동에게 반환하도록 구현했다.
* **데모 가정**: 필기 분석 모델 연결 전 `TRACE`는 유효한 획 좌표 구조를 제출하면 성공으로 처리한다.

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
