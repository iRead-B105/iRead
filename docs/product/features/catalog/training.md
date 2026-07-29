---
type: Feature Catalog
title: "기능 카탈로그: training"
description: "training 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, training]
timestamp: 2026-07-29T11:17:47+09:00
---
# 기능 카탈로그: training

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| CU-DSP-01 | 훈련 목록 표시 | 교수자에게 전체 훈련 카탈로그를 표시하고, 인증된 아동에게 현재 커리큘럼의 훈련 순서·영역·이름·상태를 표시한다. | server | `get_admin_training_by_studentId`, `get_app_training_by_studentId` |
| CU-DSP-02 | 차회 커리큘럼 표시 | 선택한 학습자가 다음 회차에 수행할 커리큘럼을 표시한다. | server | `get_admin_training_by_studentId_by_curriculumId` |
| CU-DSP-03 | 교안 학습 자료 목록 표시 | 선택한 훈련 교안의 학습 자료 목록과 배치 순서를 표시한다. | server | `get_admin_training_by_studentId_by_trainingId_expected_word` |
| CU-DSP-04 | 선택 훈련 상세 표시 | 선택한 훈련의 정확도, 학습 판단, 권장 시간과 학습 목표를 표시한다. | server | `get_admin_training_by_studentId_by_trainingId_detail` |
| CU-DSP-05 | 아동 화면 미리보기 표시 | 편집 중인 교안이 아동 화면에 표시될 모습을 미리보기로 표시한다. | server | `get_admin_training_by_studentId_by_trainingId_detail` |
| CU-SAVE-01 | 차회 커리큘럼 저장 | 수정한 차회 커리큘럼을 저장한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-02 | 교안 학습 자료 추가 | 입력한 자료를 선택한 훈련의 아동별 교안에 추가한다. | server | `post_admin_training_by_studentId_by_trainingId_expected_word` |
| CU-SAVE-03 | 교안 학습 자료 삭제 | 선택한 훈련 교안의 학습 자료를 삭제한다. | server | `delete_admin_training_by_studentId_by_trainingId_expected_word_by_wordId` |
| CU-SAVE-04 | 차회 커리큘럼 입력값 검증 | 수정한 차회 커리큘럼의 훈련 구성과 순서를 검증한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-05 | 차회 커리큘럼 저장 성공 처리 | 차회 커리큘럼 저장이 완료되면 저장 결과를 표시하고 커리큘럼을 갱신한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-06 | 차회 커리큘럼 저장 실패 처리 | 차회 커리큘럼 저장에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-07 | 교안 학습 자료 입력값 검증 | 학습 자료의 유형, 활동 이름, 제시 내용과 배치 순서 등 필수 입력값을 검증한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-08 | 교안 학습 자료 추가 성공 처리 | 학습 자료 추가가 완료되면 결과를 표시하고 교안 자료 목록과 미리보기를 갱신한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-09 | 교안 학습 자료 추가 실패 처리 | 학습 자료 추가에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-10 | 교안 학습 자료 삭제 성공 처리 | 학습 자료 삭제가 완료되면 결과를 표시하고 교안 자료 목록과 미리보기를 갱신한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-11 | 교안 학습 자료 삭제 실패 처리 | 학습 자료 삭제에 실패하면 실패 사유를 표시하고 삭제를 중단한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-12 | 다음 회차 훈련 추가 | 선택한 훈련을 학생의 다음 회차 커리큘럼에 추가한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-13 | 다음 회차 훈련 횟수 조정 | 다음 회차에 포함된 훈련의 시행 횟수를 늘리거나 줄인다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-14 | 다음 회차 훈련 순서 변경 | 편집 모드에서 훈련을 끌어 다음 회차 순서를 변경한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-15 | 다음 회차 훈련 삭제 | 다음 회차 커리큘럼에서 선택한 훈련을 제외한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SAVE-16 | 아동별 교안 기본 정보 수정 | 선택한 아동에게 적용할 훈련명과 영역을 수정하고 저장한다. | server | `patch_admin_training_by_studentId_by_curriculumId` |
| CU-SEL-01 | 차회 커리큘럼 수정 입력 | 선택한 학습자의 차회 커리큘럼에 포함할 훈련과 순서를 수정한다. | server | `get_admin_training_by_studentId_by_curriculumId` |
| CU-SEL-02 | 교안 학습 자료 입력 | 선택한 훈련 교안에 추가할 자료 유형, 활동 이름, 제시 내용, 정답 기준과 힌트를 입력한다. | server | `get_admin_training_by_studentId_by_curriculumId` |
| CU-SEL-03 | 교안 학습 자료 삭제 확인 | 선택한 교안 학습 자료의 삭제 여부를 확인한다. | server | `get_admin_training_by_studentId_by_curriculumId` |
| CU-SEL-04 | 아동별 교안 편집 화면 표시 | 다음 회차 훈련의 교안 편집 화면을 열어 기본 정보와 학습 자료를 표시한다. | server | `get_admin_training_by_studentId_by_curriculumId` |
| TH-DSP-01 | 훈련 기록 목록 표시 | 선택한 아동의 학습일, 훈련명, 결과와 학습 판단을 훈련 기록 목록으로 표시한다. | server | `get_admin_training_by_studentId_curriculum_log` |
| TH-DSP-02 | 훈련 이력 표시 | 선택한 커리큘럼 로그에 포함된 훈련 이력을 표시한다. | server | `get_admin_training_by_studentId_by_curriculumId_training_log` |
| TH-DSP-03 | 선택 훈련 세부 결과 표시 | 선택한 훈련의 요약과 세부 활동별 문항 수, 학습 시간, 점수와 학습 판단을 표시한다. | server | `get_admin_training_by_studentId_by_trainingId_detail` |
| TH-EXP-01 | 훈련 결과 CSV 저장 | 선택한 훈련의 결과 데이터를 CSV 형식으로 저장한다. | server | `post_admin_training_by_studentId_by_trainingId_export` |
| TH-EXP-02 | 훈련 결과 JSON 저장 | 선택한 훈련의 결과 데이터를 JSON 형식으로 저장한다. | server | `post_admin_training_by_studentId_by_trainingId_export` |
| TH-GAZE-01 | 훈련 시선 분석 결과 표시 | 교수자가 훈련 이력 화면에서 훈련별 시선 분석 결과와 읽기 어려움이 나타난 영역을 확인할 수 있도록 표시한다. | server | `get_admin_training_by_studentId_by_trainingId_gaze_analysis` |
| TH-SEL-01 | 훈련 기록 선택 | 세부 결과와 읽기 속도 통계를 확인할 개별 훈련 기록을 선택한다. | client | - |
| TH-STAT-01 | 읽기 속도 추이 표시 | 조회 기간의 분당 정확하게 읽은 단어 수와 기간 시작 대비 변화율을 차트로 표시한다. | server | `get_admin_training_by_studentId_by_curriculumId_statistics` |
| TR-AUD-01 | 문제 음성 재생 | 재생 버튼을 선택하면 현재 문항에 등록된 음성을 재생한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-AUD-02 | 문제 음성 다시 듣기 처리 | 현재 문항의 발음을 다시 들을 수 있게 한다 | client | - |
| TR-AUD-03 | 문제 음성 재생 상태 제어 | 훈련 문제 음성의 재생, 일시 정지, 종료 및 중복 재생 방지 상태를 제어한다. | client | - |
| TR-COM-01 | 훈련 문항 조회 | 현재 문항 번호, 전체 문항 수, 읽기 단어와 진행 상태를 조회한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-COM-02 | 훈련 진행 상태 표시 | 현재 문항과 전체 문항을 표시하고 진행률 바를 갱신한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-COM-03 | 다음 버튼 상태 제어 | 현재 문항의 응답 완료 조건에 따라 다음 버튼의 활성 상태를 제어한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-COM-04 | 다음 문항 이동 | 정답인 선택지를 골랐거나 녹음 결과가 정상적으로 저장되면 다음 버튼을 활성화하고 다음 문항으로 이동한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-COMP-01 | 훈련 완료 처리 | 현재 훈련 세션의 상태를 완료로 변경하고 완료 시각을 기록한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-DSP-01 | 읽기 단어 표시 | 현재 문항의 읽기 대상 단어를 화면에 표시한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-DSP-02 | 문제 이미지 표시 | 현재 문항에 등록된 대상 이미지를 표시한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-DSP-03 | 읽기 문장 표시 | 현재 문항의 전체 문장을 읽기 순서에 맞게 표시한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-DSP-04 | 목표 어절 강조 | 분석 또는 평가 대상이 되는 특정 단어·어절을 문장 안에서 시각적으로 강조한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-GUIDE-01 | 훈련 방법 안내 표시 | 듣고 고르기, 보고 읽기, 천천히 진행하기 등 현재 훈련의 훈련방법을 표시한다 | server | `get_app_training_by_studentId_by_trainingId_intro` |
| TR-GUIDE-02 | 훈련 세션 상태 초기화 | 새 훈련 시작 전에 이전 문항 위치와 응답 상태를 초기화한다. | server | `post_app_training_by_studentId_by_trainingId_session_reset` |
| TR-GUIDE-03 | 훈련 세션 시작 | 초기화된 상태로 훈련 세션을 시작하고 첫 문항을 표시한다. | server | `post_app_training_by_studentId_by_trainingId_start` |
| TR-INTRO-01 | 훈련 기본 정보 표시 | 훈련 시작 전에 예상 소요 시간과 해당 훈련 문항 수를 표시한다. | server | `get_app_training_by_studentId_by_trainingId_intro` |
| TR-INTRO-02 | 훈련 방법 안내 화면 이동 | 사용자가 학습 시작 버튼을 선택하면 훈련 방법 안내 화면으로 이동한다 | server | `get_app_training_by_studentId_by_trainingId_intro` |
| TR-REC-01 | 마이크 사용 권한 확인 | 훈련 음성 녹음 전에 브라우저의 마이크 사용 권한을 확인한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-02 | 음성 녹음 시작 | 녹음 시작 버튼 선택 시 마이크 입력을 받아 녹음을 시작한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-03 | 녹음 상태 표시 | 녹음 준비, 녹음 중, 녹음 완료 상태를 표시한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-04 | 녹음 시간 표시 | 녹음 경과 시간을 표시한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-05 | 음성 입력 파형 표시 | 훈련 녹음 중 입력되는 음성 신호를 파형으로 표시한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-06 | 음성 녹음 종료 | 사용자의 종료 요청 또는 최대 녹음 시간 도달 시 녹음을 종료한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-07 | 음성 재녹음 처리 | 기존 녹음 결과를 초기화하고 동일한 훈련 문항의 음성 녹음을 다시 시작할 수 있도록 한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-08 | 녹음 결과 검증 | 최소 녹음 시간과 음성 감지 여부를 확인하고 유효하지 않으면 재녹음을 안내한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-REC-09 | 훈련 음성 응답 저장 | 유효한 음성 데이터를 현재 훈련 문항의 응답으로 저장한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_recordings` |
| TR-SAVE-01 | 훈련 응답 최종 저장 | 훈련에서 생성된 선택 응답이나 음성 응답을 하나의 훈련 세션 결과로 최종 저장한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-SAVE-02 | 훈련 응답 저장 중 입력 잠금 | 훈련 응답 최종 저장 중에는 선택, 녹음, 화면 이동 등 학습자 입력을 제한한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-SAVE-03 | 훈련 응답 저장 상태 표시 | 훈련 응답을 최종 저장하는 동안 진행 상태를 표시한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-SAVE-04 | 훈련 응답 저장 실패 처리 | 훈련 응답 최종 저장에 실패하면 오류를 표시하고 다시 시도할 수 있도록 한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-SAVE-05 | 훈련 완료 화면 자동 이동 | 훈련 응답 저장이 완료되면 훈련 완료 화면으로 자동 이동한다. | server | `post_app_training_by_studentId_by_trainingId_complete` |
| TR-SEL-01 | 선택지 표시 | 문항에 설정된 선택지를 정해진 순서로 표시한다. | server | `get_app_training_by_studentId_by_trainingId_questions_by_questionNumber` |
| TR-SEL-02 | 단일 선택 처리 | 사용자가 선택지 중 하나만 선택할 수 있도록 처리하며, 다른 선택지를 누르면 기존 선택을 변경한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_responses` |
| TR-SEL-03 | 선택 상태 표시 | 사용자가 선택한 선택지를 테두리, 배경 등의 시각적 효과로 구분한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_responses` |
| TR-SEL-04 | 선택 응답 저장 | 선택한 항목의 식별값과 응답 시각을 현재 문항의 응답으로 저장한다. | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_responses` |
| TR-SEL-05 | 정답 확인 버튼 | 현재 학습자가 선택한 선택지가 정답인지 확인할 수 있도록 한다 | server | `post_app_training_by_studentId_by_trainingId_questions_by_questionNumber_responses` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
