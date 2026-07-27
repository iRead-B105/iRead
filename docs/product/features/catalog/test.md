---
type: Feature Catalog
title: "기능 카탈로그: test"
description: "test 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, test]
timestamp: 2026-07-27T12:19:48+09:00
---
# 기능 카탈로그: test

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| TE-AUD-01 | 문제 음성 재생 | 재생 버튼을 선택하면 현재 문항에 등록된 음성을 재생한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-AUD-02 | 음성 재생 횟수 제한 | 문항별 최대 재생 횟수를 적용하고 현재 재생 횟수를 1/2 형태로 표시한다. | client | - |
| TE-AUD-03 | 재생 버튼 상태 제어 | 음성 재생 중에는 중복 재생을 방지하며, 최대 재생 횟수에 도달하면 다시 듣기 기능을 비활성화한다. | client | - |
| TE-COM-01 | 테스트 문항 조회 | 현재 문항 번호, 전체 문항 수, 읽기 단어와 진행 상태를 조회한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-COM-02 | 테스트 진행 상태 표시 | 현재 문항과 전체 문항을 표시하고 진행률 바를 갱신한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-COM-03 | 다음 버튼 상태 제어 | 현재 문항의 응답 완료 조건에 따라 다음 버튼의 활성 상태를 제어한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-COM-04 | 다음 문항 이동 | 현재 문항의 응답이 완료된 상태에서 다음 버튼을 선택하면 응답을 저장하고 다음 문항을 조회하여 표시한다. 마지막 문항인 경우 응답 정리 화면으로 이동한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-COMP-01 | 테스트 완료 처리 | 현재 테스트 세션의 상태를 완료로 변경하고 완료 시각을 기록한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_complete` |
| TE-DSP-01 | 읽기 단어 표시 | 현재 문항의 읽기 대상 단어를 화면에 표시한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-DSP-02 | 문제 이미지 표시 | 현재 문항에 등록된 대상 이미지를 표시한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-DSP-03 | 읽기 문장 표시 | 현재 문항의 전체 문장을 읽기 순서에 맞게 표시한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-DSP-04 | 목표 어절 강조 | 분석 또는 평가 대상이 되는 특정 단어·어절을 문장 안에서 시각적으로 강조한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-GUIDE-01 | 테스트 방법 안내 표시 | 듣고 고르기, 보고 읽기, 천천히 진행하기 등 테스트 수행 방법을 순서대로 표시한다. | server | `get_app_test_by_studentId_intro` |
| TE-GUIDE-02 | 테스트 세션 상태 초기화 | 새로운 테스트를 시작하는 경우 현재 문항, 응답 기록 및 진행 상태를 초기값으로 설정한다. | server | `post_app_test_by_studentId_session_reset` |
| TE-GUIDE-03 | 테스트 세션 시작 | 사용자가 준비됐어요 버튼을 선택하면 테스트 세션을 시작하고 첫 번째 테스트 문항으로 이동한다. | server | `post_app_test_by_studentId_start` |
| TE-INTRO-01 | 테스트 기본 정보 표시 | 테스트 시작 전에 예상 소요 시간과 전체 진행 단계 수를 표시한다. | server | `get_app_test_by_studentId_intro` |
| TE-INTRO-02 | 테스트 방법 안내 화면 이동 | 사용자가 테스트 시작 버튼을 선택하면 테스트 방법 안내 화면으로 이동한다 | server | `get_app_test_by_studentId_intro` |
| TE-REC-01 | 마이크 사용 권한 확인 | 테스트 음성 녹음 전에 브라우저의 마이크 사용 권한을 확인한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-02 | 음성 녹음 시작 | 녹음 시작 버튼 선택 시 마이크 입력을 받아 녹음을 시작한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-03 | 녹음 상태 표시 | 녹음 준비, 녹음 중, 녹음 완료 상태를 표시한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-04 | 녹음 시간 표시 | 녹음 경과 시간을 표시한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-05 | 음성 입력 파형 표시 | 테스트 녹음 중 입력되는 음성 신호를 파형으로 표시한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-06 | 음성 녹음 종료 | 사용자의 종료 요청 또는 최대 녹음 시간 도달 시 녹음을 종료한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-07 | 녹음 결과 검증 | 최소 녹음 시간과 음성 감지 여부를 확인하고 유효하지 않으면 재녹음을 안내한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-REC-08 | 테스트 음성 응답 저장 | 유효한 음성 데이터를 현재 테스트 문항의 응답으로 저장한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_recordings` |
| TE-SAVE-01 | 테스트 응답 최종 저장 | 테스트에서 생성된 선택 응답과 음성 응답을 하나의 테스트 세션 결과로 최종 저장한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_complete` |
| TE-SAVE-02 | 테스트 응답 저장 중 입력 잠금 | 테스트 응답 최종 저장 중에는 선택, 녹음, 화면 이동 등 학습자 입력을 제한한다. | server | `post_app_test_by_studentId_complete` |
| TE-SAVE-03 | 테스트 응답 저장 상태 표시 | 테스트 응답을 최종 저장하는 동안 진행 상태를 표시한다. | server | `post_app_test_by_studentId_complete` |
| TE-SAVE-04 | 테스트 응답 저장 실패 처리 | 테스트 응답 최종 저장에 실패하면 오류를 표시하고 다시 시도할 수 있도록 한다. | server | `post_app_test_by_studentId_complete` |
| TE-SAVE-05 | 테스트 완료 화면 자동 이동 | 테스트 응답 저장이 완료되면 테스트 완료 화면으로 자동 이동한다. | server | `post_app_test_by_studentId_complete` |
| TE-SEL-01 | 선택지 표시 | 문항에 설정된 선택지를 정해진 순서로 표시한다. | server | `get_app_test_by_studentId_questions_by_questionNumber` |
| TE-SEL-02 | 단일 선택 처리 | 사용자가 선택지 중 하나만 선택할 수 있도록 처리하며, 다른 선택지를 누르면 기존 선택을 변경한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_responses` |
| TE-SEL-03 | 선택 상태 표시 | 사용자가 선택한 선택지를 테두리, 배경 등의 시각적 효과로 구분한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_responses` |
| TE-SEL-04 | 선택 응답 저장 | 선택한 항목의 식별값과 응답 시각을 현재 문항의 응답으로 저장한다. | server | `post_app_test_by_studentId_questions_by_questionNumber_responses` |
| TI-DSP-01 | 테스트 날짜 선택 항목 표시 | 선택 검사 1건과 비교 검사 최대 2건의 날짜 입력 항목을 표시한다. | server | `get_admin_test_by_studentId_list` |
| TI-DSP-02 | 선택 검사 종합 표시 | 선택 검사의 총점, 이전 대비 변화, 강점·보완 영역, 권장 과정과 다음 검사 시점을 표시한다. | server | `get_admin_test_by_studentId_compare` |
| TI-GAZE-01 | 테스트 시선 분석 결과 표시 | 교수자가 테스트 이력 화면에서 아동의 시선 체류 시간, 되돌아보기 횟수와 읽기 이탈 구간을 확인할 수 있도록 표시한다. | server | `get_admin_test_by_studentId_by_testId_gaze_analysis` |
| TI-SEL-01 | 테스트 비교 대상 선택 | 기준이 되는 선택 검사 1건과 비교 검사 최대 2건을 날짜 기준으로 선택한다. | server | `get_admin_test_by_studentId_compare` |
| TI-SEL-02 | 테스트 비교 대상 선택 해제 | 선택한 비교 검사 날짜를 해제한다. | server | `get_admin_test_by_studentId_compare` |
| TI-SEL-03 | 테스트 기록 비교 | 선택 검사 1건과 비교 검사 최대 2건의 영역별 결과 비교를 실행한다. | server | `get_admin_test_by_studentId_compare` |
| TI-SEL-04 | 테스트 비교 대상 선택 제한 처리 | 비교 검사 두 건을 이미 추가한 상태에서는 추가 버튼을 비활성화하고 선택 제한을 안내한다. | server | `get_admin_test_by_studentId_compare` |
| TI-STAT-01 | 테스트 결과 비교 차트 표시 | 선택 검사와 비교 검사들의 영역별 환산 점수를 차트로 비교하여 표시한다. | server | `get_admin_test_by_studentId_compare` |
| TI-STAT-02 | 테스트 영역별 통계 표시 | 선택한 두 테스트의 읽기 시간, 정답률, 문제 풀이 시간과 시선 관련 통계를 표시한다. | server | `get_admin_test_by_studentId_compare` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
