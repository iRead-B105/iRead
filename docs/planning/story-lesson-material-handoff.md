# 이야기 분기·교안 편집 작업 인계

## 결론

현재는 공유·운영 데이터가 없는 로컬 데모 개발 단계다. Backend 계약은 예상 단어 전용 API를 폐기하고 생성된 교안 전체 편집과 음성·버튼 이야기 분기를 제공한다. Vue와 AI server 담당자는 아래 기준 원본을 유지하면서 각 소비자 구현을 갱신한다.

| 대상 | 기준 원본 |
| --- | --- |
| 교수자 교안 편집 API | [Admin OpenAPI](../../contracts/openapi/admin-api.yaml) |
| 아동 이야기 음성·버튼 분기 API | [App OpenAPI](../../contracts/openapi/app-api.yaml) |
| Backend–AI 생성 계약 | [Backend–AI OpenAPI](../../contracts/openapi/ai-api.yaml) |
| 이야기 제품 정책 | [AI 이야기 분기 기능 명세](../product/features/story-branch.md) |
| 서비스 인증·재시도·보안 | [인터페이스 원칙](../architecture/interface-principles.md) |

## Vue 담당자 인계

### 변경 목적

교수자가 예상 단어를 별도로 입력하는 UI를 제거하고, AI가 생성한 교안 문항을 조회·편집·정렬·제거한 뒤 전체 목록으로 저장한다.

### 구현 작업

- `ExpectedWord` 모델과 `getExpectedWords`, `addExpectedWord`, `deleteExpectedWord` API·repository·store·mock을 제거한다.
- `StudentCurriculumView`와 `LessonMaterialEditor`의 예상 단어 입력·삭제 UI와 관련 상태를 제거한다.
- 훈련 선택 시 `GET /api/admin/training/{studentId}/{trainingId}/lesson-material`을 호출한다.
- 화면 상태에 `materials`, `revision`, `editable`을 보관한다.
- `presentation`, `content`, `answer`를 편집하고 배열 순서로 문항 배치를 표현한다.
- 자료 제거는 삭제할 항목을 배열에서 제외하고, `PUT /api/admin/training/{studentId}/{trainingId}/lesson-material`로 남은 전체 목록을 저장한다.
- PUT에는 GET으로 받은 `revision`과 1~5개의 `questionNo`, `questionType`, `presentation`, `content`, `answer`를 보낸다. `questionType`은 변경하지 않는다.
- 저장 성공 시 응답의 `revision`과 `materials`로 화면 상태를 교체한다.
- 교안 재생성 성공 후에는 lesson-material을 다시 조회한다.
- `CONTENT_UPDATED` 실시간 이벤트를 받으면 편집 중이 아닐 때 최신 교안을 다시 조회한다. 편집 중이면 원격 변경 안내 후 사용자가 새로고침하도록 한다.

### 오류 처리

- `409 LESSON_MATERIAL_REVISION_CONFLICT`: 최신 revision을 다시 조회하도록 안내한다.
- `409 TRAINING_NOT_EDITABLE`: 진행 중이거나 완료된 훈련은 읽기 전용으로 전환한다.
- `422 LESSON_MATERIAL_VALIDATION_FAILED`: `details.errors[].path`, `reason`, `message`를 해당 편집 필드에 표시한다.
- `materials`가 0개가 되지 않도록 마지막 자료 제거를 막는다.
- 네트워크 실패 시 마지막으로 서버가 확인한 revision과 자료를 유지한다.

### 완료 기준

- Frontend 소스와 테스트에 `/expected-word`, `ExpectedWord`, `expectedWords` 참조가 없다.
- GET 응답 매핑, 전체 PUT 저장, 재정렬·제거, 409·422 처리 테스트가 있다.
- mock repository도 실제 API와 같은 revision 증가 및 전체 목록 교체 규칙을 따른다.
- `pnpm test`, `pnpm lint`, `pnpm build`가 통과한다.

## AI server 담당자 인계

### 확정 정책

- Backend만 AI server를 호출하며 Frontend와 아동 App은 직접 호출하지 않는다.
- `/api/v1/story/generate`와 `/api/v1/story/continue`는 `requestId`, `schemaVersion`, `nextProgress`, `completed`, `lines` 계약을 유지한다.
- 분기 대사의 `content`는 아동에게 보여 줄 질문이다.
- `requiresBranchInput=true`이면 `branchPrompt.options`에 서로 다른 선택지 3개를 제공한다.
- 선택지 번호는 정확히 `1`, `2`, `3`이고 `label`은 공백을 제거한 1~80자 문구다.
- `requiresBranchInput=false`이면 `branchPrompt`는 `null`이다.
- `continue`의 `branchIntent`는 경량 LLM 검토와 아동 확인을 통과한 STT 원문 또는 버튼 선택 결과를 Backend가 확정한 문자열이다. 이야기 생성 AI는 입력 출처를 구분하지 않는다.
- AI server는 `/api/v1/story/branch-input/review`에서 현재 질문·버튼 선택지·STT 원문만 받아 `ALLOW`, `CONFIRM`, `RETRY`, `BLOCK`과 제한된 사유 코드를 구조화해 반환한다.
- 검토 모델은 STT 원문을 교정·재작성하지 않으며 자유 형식 설명을 반환하지 않는다.
- 교수자 예상 단어는 AI 입력이 아니다. 교수자 교안 편집은 Backend의 `lesson-material` API와 `training_datas.generated_data`가 소유한다.
- 이미지 생성은 현재 동기 응답으로 `imageUrl`만 반환한다. 비동기 작업을 도입하기 전에는 생성 상태값을 추가하지 않는다.

### 실제 연동 작업

- [TBD] 실제 생성 provider, model과 자격증명·요청 한도는 팀 결정 후 환경 설정으로 연결한다. 이 결정 전에도 provider adapter와 계약 검증은 구현할 수 있다.
- 결정적 이야기 Mock을 실제 생성 provider 호출로 교체하되 OpenAPI 응답 구조는 변경하지 않는다.
- 아동 연령과 이야기 템플릿에 맞는 안전한 분기 질문과 상호 배타적인 선택지 3개를 생성한다.
- provider 응답을 내부 모델로 파싱하고 계약 위반 응답은 Backend에 전달하기 전에 거부한다.
- 구조 오류에 대한 제한된 재생성 또는 복구 정책과 최종 실패 응답을 구현한다.
- 같은 `Idempotency-Key` 요청은 같은 결과를 반환하도록 처리한다.
- 요청·응답의 `requestId`, `schemaVersion`을 보존하고 `nextProgress`를 현재 진행률 이상 100 이하로 제한한다.
- 아동 이름·음성·자격증명·전체 프롬프트를 로그에 기록하지 않는다.
- 분기 검토 요청 본문, STT 원문과 차단 사유의 자유 형식 설명을 로그에 기록하지 않는다.

### 완료 기준

- 정상 분기, 일반 대사, 선택지 개수·번호·중복 오류, 진행률 역행, provider 오류 테스트가 있다.
- Backend 계약 테스트 fixture로 실제 AI server 응답을 검증한다.
- 동일 멱등성 키 재요청에서 중복 provider 호출 또는 다른 결과가 발생하지 않는다.
- AI server 테스트와 Backend–AI 통합 테스트가 통과한다.

## Flyway와 MySQL 검증

- 최종 스키마는 `V1__baseline_schema.sql`, 전체 데모 데이터는 `V2__demo_seed.sql`에 둔다.
- 아직 로컬 데모 개발 단계이므로 V1·V2가 바뀌면 기존 로컬 데모 DB나 볼륨을 초기화해도 된다.
- 이후 새 변경은 V3부터 누적하고 V1·V2를 다시 쓰지 않는다.
- 반복 개발 중 모든 코드 수정마다 MySQL 테스트를 실행할 필요는 없다.
- V1·V2 변경을 완료 처리하거나 `develop`에 병합하기 전에는 빈 MySQL 8.4에서 V1 단독, demo 프로필의 V1→V2, Hibernate schema validation을 한 번 이상 통과해야 한다.
- H2·단위 테스트는 MySQL JSON 함수, CHECK·UNIQUE와 Flyway 실행 순서를 완전히 검증하지 못하므로 최종 MySQL 검증을 대체하지 않는다.
