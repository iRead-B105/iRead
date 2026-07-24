---
type: Contract Review Queue
title: "API 계약 검토 목록"
description: "Notion에서 OpenAPI로 이전했지만 추가 의미 검토가 필요한 API를 정리합니다."
tags: [contracts, openapi, review]
timestamp: 2026-07-24T17:47:15+09:00
---
# API 계약 검토 목록

활성 API 115건 가운데 52건에 추가 검토 표시가 남아 있다.

권장 처리는 기존 ERD와 정식 도메인 API를 우선하고, 화면 이동·선택·재생 상태는 클라이언트 책임으로 분리한 결과다.

| API | 분류 | 권장 처리 | 검토 사유 | Notion |
| --- | --- | --- | --- | --- |
| `GET /api/admin/navigation/sidebar` | 클라이언트 화면 상태 | 권한 정보로 클라이언트가 메뉴를 구성하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-navigation-sidebar-3a6027df905381389a02c0774dc1e399) |
| `GET /api/admin/report/selection` | 클라이언트 화면 상태 | 학생 목록 조회 결과를 사용하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-report-selection-3a6027df9053810b8b14c89c4cce8aa8) |
| `GET /api/admin/student/actions` | 클라이언트 화면 상태 | 권한과 학생 상태로 버튼을 구성하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-actions-3a6027df9053819f915fc3b8bf8bf055) |
| `GET /api/admin/student/filter` | 기존 API 통합 | 학생 목록의 query parameter로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-filter-3a6027df905381769e20fa7f7f3dea58) |
| `GET /api/admin/student/list-state` | 클라이언트 화면 상태 | 학생 목록 응답과 클라이언트 상태로 대체 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-list-state-3a6027df90538120873de10550e8bf60) |
| `GET /api/admin/student/selection` | 클라이언트 화면 상태 | 클라이언트 선택 상태로 전환하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-selection-3a6027df905381f792a5d9e57a0b8850) |
| `GET /api/admin/student/summary` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-summary-3a6027df905381c2b972d54d7016f7b4) |
| `GET /api/admin/student/{studentId}/form` | 기존 API 통합 | GET /api/admin/student/{studentId}로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-studentId-form-3a6027df905381d190a9e85b3a716e0b) |
| `PATCH /api/admin/student/{studentId}/form-submit` | 기존 API 통합 | PATCH /api/admin/student/{studentId}로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-studentId-form-submit-3a6027df90538183bf50d761e4717afb) |
| `GET /api/admin/student/{studentId}/learning-events` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-studentId-learning-events-3a6027df90538187839fccedc173f001) |
| `GET /api/admin/student/{studentId}/reading-accuracy-trend` | 기존 API 통합 | GET /api/admin/student/{studentId}/accuracy-trend로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-student-studentId-reading-accuracy-trend-3a6027df905381d7ad43d10048c7404e) |
| `GET /api/admin/teacher/profile/edit` | 기존 API 통합 | GET /api/admin/teacher/info로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-teacher-profile-edit-3a6027df905381009526f27411a2b0be) |
| `PATCH /api/admin/teacher/profile/save-state` | 경로 정규화 | PATCH /api/admin/teacher/info로 이름과 계약을 정규화 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-teacher-profile-save-state-3a6027df9053816ba11bde7d6ad251d2) |
| `GET /api/admin/teacher/profile/view` | 기존 API 통합 | GET /api/admin/teacher/info로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-teacher-profile-view-3a6027df90538192bb9fd7cebab96054) |
| `GET /api/admin/test/{studentId}/comparison-selection` | 기존 API 통합 | GET /api/admin/test/{studentId}/compare의 query parameter로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-test-studentId-comparison-selection-3a6027df9053810ab3dcfdbb5542bf2b) |
| `GET /api/admin/test/{studentId}/statistics` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-test-studentId-statistics-3a6027df90538112bc47f9286440c334) |
| `GET /api/admin/test/{studentId}/{testId}/summary` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-test-studentId-testId-summary-3a6027df905381b9afdedda8a8a782aa) |
| `GET /api/admin/training/{studentId}/history/filter` | 기존 API 통합 | 훈련 이력 조회의 query parameter로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-history-filter-3a6027df9053818aaa1dc1350096ba40) |
| `GET /api/admin/training/{studentId}/history/selection` | 클라이언트 화면 상태 | 클라이언트 선택 상태로 전환하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-history-selection-3a6027df90538173a701d01f2a2df923) |
| `PATCH /api/admin/training/{studentId}/{curriculumId}/curriculum-editor` | 기존 API 통합 | PATCH /api/admin/training/{studentId}/{curriculumId}로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-curriculumId-curriculum-editor-3a6027df905381cbafdef7ef208a678e) |
| `GET /api/admin/training/{studentId}/{curriculumId}/editor-selection` | 기존 API 통합 | GET /api/admin/training/{studentId}/{curriculumId}로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-curriculumId-editor-selection-3a6027df905381d79a47f3ac4c59bb7b) |
| `GET /api/admin/training/{studentId}/{trainingId}/detail` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-trainingId-detail-3a6027df905381e2944bfba2a0f3d467) |
| `POST /api/admin/training/{studentId}/{trainingId}/export` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-trainingId-export-3a6027df905381828e0ae5c2b3154b0d) |
| `GET /api/admin/training/{studentId}/{trainingId}/result-detail` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-admin-training-studentId-trainingId-result-detail-3a6027df905381cd8fd4d3f2dc10fe2a) |
| `PATCH /api/app/mypage/character/representative` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-mypage-character-representative-3a6027df905381f79e00efe43504032d) |
| `GET /api/app/mypage/growth/statistics` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-mypage-growth-statistics-3a6027df9053816db133e5a2da089985) |
| `GET /api/app/mypage/growth/status` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-mypage-growth-status-3a6027df905381248246e8ae43fec5aa) |
| `GET /api/app/story/{studentId}/library` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-library-3a6027df9053811385edf7176c1d605b) |
| `POST /api/app/story/{studentId}/{storyId}/gaze-analysis` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyId-gaze-analysis-3a6027df90538193b8dde16cf514d049) |
| `GET /api/app/story/{studentId}/{storyId}/guide` | 클라이언트 화면 상태 | 사용 안내는 앱 정적 자원으로 관리하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyId-guide-3a6027df90538132a298e7d085852057) |
| `GET /api/app/story/{studentId}/{storyId}/navigation` | 기존 API 통합 | 이야기 장면 조회 응답으로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyId-navigation-3a6027df9053813c9486f856352f0d08) |
| `POST /api/app/story/{studentId}/{storyId}/speech` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyId-speech-3a6027df905381b9b153c7645fd71bbf) |
| `POST /api/app/story/{studentId}/{storyId}/tts` | 서버 계약 상세화 | ERD 필드와 요청·응답 의미를 대조한 뒤 유지 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyId-tts-3a6027df905381df826ff422d6aa1691) |
| `GET /api/app/story/{studentId}/{storyTemplateId}/detail-state` | 기존 API 통합 | GET /api/app/story/{studentId}/{storyTemplateId}로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-story-studentId-storyTemplateId-detail-state-3a6027df905381e59326eb66e34ba13b) |
| `GET /api/app/test/{studentId}/audio-state` | 클라이언트 화면 상태 | 문항 응답의 음성 URL과 클라이언트 재생 상태로 대체 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-audio-state-3a6027df905381d0b656f421dcb8290e) |
| `GET /api/app/test/{studentId}/intro-navigation` | 기존 API 통합 | 해당 학습의 intro 조회 응답으로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-intro-navigation-3a6027df9053818e9e4ed26cd2345cf7) |
| `PATCH /api/app/test/{studentId}/question-navigation` | 기존 API 통합 | 문항 번호 기반 GET 문항 조회로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-question-navigation-3a6027df905381cea81feea129d41ef1) |
| `GET /api/app/test/{studentId}/questions/display-state` | 기존 API 통합 | 문항 번호 기반 GET 문항 조회로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-questions-display-state-3a6027df905381f59245edd340a09147) |
| `POST /api/app/test/{studentId}/recording-state` | 기존 API 통합 | 문항별 recordings 업로드 API로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-recording-state-3a6027df905381c1ae6bec3b440f3649) |
| `PATCH /api/app/test/{studentId}/selection-state` | 기존 API 통합 | 문항별 responses 저장 API로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-selection-state-3a6027df905381198ec9c408e9dbda74) |
| `POST /api/app/test/{studentId}/session-reset` | 세션 계약 정리 | start의 재시작 의미 또는 별도 reset 필요성을 결정 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-session-reset-3a6027df905381a7ad55f42d31500dab) |
| `POST /api/app/test/{studentId}/submission-status` | 경로 정규화 | 상태 조회형 이름 대신 submit 또는 complete 명령으로 정규화 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-test-studentId-submission-status-3a6027df9053814c8252ea0fa6cd5154) |
| `GET /api/app/training/{studentId}/{trainingId}/audio-state` | 클라이언트 화면 상태 | 문항 응답의 음성 URL과 클라이언트 재생 상태로 대체 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-audio-state-3a6027df9053816ab94bcc55e008fdbc) |
| `GET /api/app/training/{studentId}/{trainingId}/intro-navigation` | 기존 API 통합 | 해당 학습의 intro 조회 응답으로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-intro-navigation-3a6027df90538150ac18f31803e68283) |
| `PATCH /api/app/training/{studentId}/{trainingId}/question-navigation` | 기존 API 통합 | 문항 번호 기반 GET 문항 조회로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-question-navigation-3a6027df9053818b9ff9e3e994c96693) |
| `GET /api/app/training/{studentId}/{trainingId}/questions/display-state` | 기존 API 통합 | 문항 번호 기반 GET 문항 조회로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-questions-display-state-3a6027df90538155a5cbc08b969df7d7) |
| `POST /api/app/training/{studentId}/{trainingId}/recording-state` | 기존 API 통합 | 문항별 recordings 업로드 API로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-recording-state-3a6027df9053818c9318d546a124f428) |
| `PATCH /api/app/training/{studentId}/{trainingId}/selection-state` | 기존 API 통합 | 문항별 responses 저장 API로 통합 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-selection-state-3a6027df90538133af60c672a7fb1f0e) |
| `POST /api/app/training/{studentId}/{trainingId}/session-reset` | 세션 계약 정리 | start의 재시작 의미 또는 별도 reset 필요성을 결정 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-session-reset-3a6027df90538199af99ddb00a8c29e7) |
| `POST /api/app/training/{studentId}/{trainingId}/submission-status` | 경로 정규화 | 상태 조회형 이름 대신 submit 또는 complete 명령으로 정규화 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-training-studentId-trainingId-submission-status-3a6027df905381139407d384d15f679d) |
| `GET /api/app/user/home-navigation` | 클라이언트 화면 상태 | 인증 사용자 정보로 앱이 이동을 결정하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-user-home-navigation-3a6027df9053812980a7d8662036b275) |
| `PATCH /api/app/user/session-navigation` | 클라이언트 화면 상태 | 세션·화면 이동 상태를 클라이언트로 이전하고 API는 제거 | Notion 주석에 검수 필요 표시 | [원본](https://app.notion.com/p/api-app-user-session-navigation-3a6027df905381649e45f7c12fad55e4) |

## 별도 미결 사항

- [TBD] Backend–AI 내부 API의 실제 경로와 인증 방식
- [TBD] Backend MySQL migration 도입 시점
