# 교수자 Web–아동 App 실시간 연동 Vue Frontend 인수

- 상태: ready
- 담당 저장소: `services/frontend-web`, `services/frontend-app`
- 기술 기준: Vue 3, TypeScript, Pinia, Vue Router, Vite
- 기준 브랜치: 두 Frontend 저장소의 최신 `develop`
- 관련 작업: [실시간 데이터 연동 TODO](realtime-data-sync-todo.md)
- 관련 계획: [교수자 Web–아동 App 실시간 데이터 연동](../../plans/2026-07-31-teacher-learner-data-linkage.md)

## 결론

Backend, OpenAPI, SSE 클라이언트, 이벤트별 선택 재조회, 화면 복귀 재조회와 3초 안전 재검증은 구현되어 있다. Vue 담당자는 기존 동기화 코드를 다시 작성하지 않고 다음 세 결과를 완성한다.

1. 교수자 화면에서 3초 이상 최신화에 실패했을 때만 데이터가 오래되었음을 알리고 수동 재시도를 제공한다.
2. 교수자 보고서 화면에 생성 시점의 완료 데이터 스냅샷이라는 점을 표시한다.
3. 교수자 Web과 아동 App을 실제 브라우저로 동시에 열어 주요 데이터 흐름이 새로고침 없이 3초 이내 반영되는지 검증한다.

## 시작 기준

- orchestration: `develop`의 최신 커밋
- Backend: `develop`의 최신 커밋
- 교수자 Web: `develop`의 최신 커밋
- 아동 App: `develop`의 최신 커밋
- 데모 계정: `demo@iread.local` / `demo1234`
- 기본 학생: 샛별, `studentId=2001`
- 기본 교육과정: `curriculumId=190001`
- 훈련 ID는 고정하지 않고 현재 교육과정 API에서 조회한다.

```powershell
docker compose up -d
node tools/verify_realtime_demo.mjs
```

## 이미 구현된 범위

### 교수자 Web

- `/api/admin/realtime/events` 인증 SSE 연결
- 연결 종료 후 1초 간격 자동 재연결
- 학생별 이벤트 버전 중복 제거
- 학생 목록·요약과 현재 열린 학생 화면의 선택 재조회
- `visibilitychange`로 화면 복귀 시 강제 재조회
- 활성 화면의 3초 안전 재검증
- 보고서 화면의 실시간 재조회 제외

주요 파일:

- `services/frontend-web/src/lib/realtime/realtimeClient.ts`
- `services/frontend-web/src/realtime/installTeacherRealtimeSync.ts`
- `services/frontend-web/src/main.ts`

### 아동 App

- `/api/app/realtime/events` 인증 SSE 연결과 자동 재연결
- 현재 학생의 이벤트만 반영하고 버전 중복 제거
- 교수자 학생 정보 변경 시 세션 프로필 재조회
- 교육과정·훈련 변경 시 현재 교육과정 재조회
- 화면 복귀와 교육과정 화면의 3초 안전 재검증
- 기존 34개 `trainingType` 기반 훈련 화면 매핑
- 지원하지 않는 훈련 유형의 계약 오류 노출

주요 파일:

- `services/frontend-app/src/lib/realtime/realtimeClient.ts`
- `services/frontend-app/src/realtime/installLearnerRealtimeSync.ts`
- `services/frontend-app/src/features/learner/content/trainingTemplateMapping.ts`
- `services/frontend-app/src/main.ts`

## 구현할 Frontend 범위

### 1. 교수자 데이터 최신성 안내

상시 연결 아이콘이나 `SSE connected` 같은 기술 상태는 표시하지 않는다.

- 정상 상태와 3초 이내 일시적 재연결은 아무 메시지 없이 처리한다.
- SSE 재연결 여부가 아니라 마지막 관련 API 재조회 성공 시각으로 최신성을 판단한다.
- 관련 API 재조회가 3초 이상 성공하지 못하면 다음 수준의 안내를 표시한다.

```text
연결이 불안정하여 최신 정보가 아닐 수 있습니다. [다시 시도]
```

- `다시 시도`는 현재 라우트에 필요한 조회만 실행한다.
- 재조회 성공 시 경고를 즉시 제거한다.
- 마지막 갱신 시각은 경고가 표시된 동안에만 보조 정보로 표시한다.
- 학생 전환과 로그아웃 시 이전 학생의 실패 상태를 제거한다.
- 보고서 화면은 생성 시점 스냅샷임을 유지하며 실시간 최신성 경고 대상에서 제외한다.

권장 수정 위치:

- `services/frontend-web/src/realtime/installTeacherRealtimeSync.ts`
- `services/frontend-web/src/lib/realtime/realtimeClient.ts`
- `services/frontend-web/src/layouts/TeacherLayout.vue`
- 필요하면 실시간 최신성만 담당하는 작은 store 또는 composable을 추가한다.

### 2. 보고서 스냅샷 안내

보고서 화면은 실시간 이벤트를 구독하거나 자동 재생성하지 않는다.

- 생성 시각 또는 보고서 기준 기간과 함께 `완료된 학습 데이터를 기준으로 생성된 보고서입니다.` 수준의 안내를 표시한다.
- 교수자 메모 수정과 사용자가 직접 요청하는 시선 추이 갱신은 기존 동작을 유지한다.
- 최신성 경고와 수동 재시도 UI를 보고서 화면에는 표시하지 않는다.
- SSE 이벤트를 받았다는 이유로 보고서 조회 또는 생성 API를 다시 호출하지 않는다.

권장 수정 위치:

- `services/frontend-web/src/views/students/StudentReportView.vue`
- 실제 보고서 화면 경로가 다르면 라우터에서 연결된 현재 컴포넌트를 기준으로 적용한다.

### 3. 실제 브라우저 교차 앱 E2E

다음 시나리오를 교수자 Web `http://localhost:5173`과 아동 App `http://localhost:5174`에서 검증한다.

- 교수자 교육과정·훈련 편집 → 아동 목록·상세 자동 반영
- 교수자 편집 반영 시 아동에게 팝업·배너·알림이 나타나지 않음
- 아동 훈련 시작 → 교수자 활성 교육과정에 `IN_PROGRESS` 반영
- 아동 훈련 완료 → 교수자 이력·요약·통계에 같은 `trainingId`와 결과 반영
- 아동 검사 완료 → 교수자 검사 목록·비교·상세 반영
- 아동 이야기 진행·완료 → 교수자 이야기 이력·상세 반영
- 아동 시선 분석 `AVAILABLE`, `NO_DATA`, `FAILED` → 교수자 분석 화면 반영
- SSE를 끊었다가 복구했을 때 화면 복귀·3초 재검증으로 누락 데이터 복구
- 다른 교수자·학생 데이터가 화면에 섞이지 않음

각 시나리오는 Backend 저장 완료부터 상대 화면 표시 완료까지 시간을 측정하고 3초 이하임을 기록한다.

## 명시적 제외 범위

- 아동 App에는 연결 상태, 마지막 갱신 시각, 재시도 버튼을 추가하지 않는다.
- 교수자 Web에도 정상 연결 중인 `SSE connected` 아이콘이나 상시 연결 상태를 표시하지 않는다.
- 진행 중인 훈련의 교수자 편집 알림, 팝업 또는 배너를 아동 App에 추가하지 않는다.
- 보고서를 실시간으로 재생성하거나 이미 생성된 보고서 내용을 자동 변경하지 않는다.
- SSE 이벤트 본문을 화면 데이터로 직접 렌더링하지 않는다.

## 변경하지 않을 계약

- 한 학생에게 `IN_PROGRESS` 최대 1건과 `NOT_STARTED` 최대 1건을 허용한다.
- 활성 교육과정은 `IN_PROGRESS` 다음 `NOT_STARTED` 순서로 선택한다.
- 교수자는 `NOT_STARTED` 교육과정만 편집한다.
- 진행 중인 훈련에는 교수자 편집 알림을 보내지 않는다.
- 보고서는 완료 데이터 기반 생성 시점 스냅샷이며 자동 재작성하지 않는다.
- 앱은 `trainingType`을 화면 선택 기준으로 사용하고 숫자 템플릿 ID는 이전 응답 호환 fallback으로만 사용한다.
- Frontend는 SSE 이벤트 본문을 화면 데이터로 사용하지 않고 관련 REST API를 다시 조회한다.

## 검증 명령

```powershell
pnpm.cmd --dir services/frontend-web test
$env:VITE_AUTH_SOURCE='api'
$env:VITE_DATA_SOURCE='api'
pnpm.cmd --dir services/frontend-web build

npm.cmd --prefix services/frontend-app test -- --run
npm.cmd --prefix services/frontend-app run build

node tools/verify_realtime_demo.mjs
```

## 완료 조건

- 정상 연결 중에는 불필요한 상태 표시가 없다.
- 3초 이상 최신화 실패 시에만 경고, 마지막 성공 시각과 `다시 시도`가 나타난다.
- 복구 성공 후 경고가 사라지고 최신 데이터가 표시된다.
- 보고서 화면에 완료 데이터 기반 생성 시점 스냅샷 안내가 표시되고 실시간 재조회는 발생하지 않는다.
- 아동 App에는 연결 상태나 교수자 편집 알림 UI가 추가되지 않는다.
- 위 교차 앱 시나리오가 새로고침 없이 3초 이내 통과한다.
- Frontend 단위 테스트와 프로덕션 빌드가 통과한다.
- 측정 결과와 실패한 시나리오를 [실시간 데이터 연동 TODO](realtime-data-sync-todo.md)에 반영한다.
