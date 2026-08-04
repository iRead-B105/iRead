---
type: Feature Catalog
title: "기능 카탈로그: gaze"
description: "gaze 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, gaze]
timestamp: 2026-08-04T19:21:22+09:00
---
# 기능 카탈로그: gaze

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| GZ-GAZE-01 | 시선 추적 장치 연결 상태 확인 | 테스트 시작 전 시선 추적 장치가 정상적으로 연결되어 있는지 확인하고, 연결 상태를 사용자에게 표시한다. | server | `get_app_gaze_device_status` |
| GZ-GAZE-02 | 시선 추적 보정 안내 표시 | 정확한 시선 측정을 위해 학습자에게 화면 응시 위치와 보정 방법을 안내한다. | server | `get_app_gaze_calibration_guide` |
| GZ-GAZE-03 | 시선 추적 실패 처리 | 장치 연결 끊김, 보정 실패, 데이터 수집 오류가 발생한 경우 안내 메시지를 표시하고 대체 흐름을 처리한다. | server | `patch_app_gaze_sessions_by_gazeSessionId_failed` |
| ST-GAZE-01 | 이야기 읽기 시선 데이터 수집 시작 | 이야기 장면을 읽는 동안 학습자의 문장별 시선 위치와 체류 시간 데이터를 수집한다. | server | `post_app_gaze_sessions` |
| ST-GAZE-02 | 이야기 문장별 시선 체류 시간 분석 | Backend가 calculationVersion에 따라 계산한 페이지·단어별 체류·건너뜀·되돌아보기 결과를 표시한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results`, `get_admin_story_by_studentId_by_storyId_gaze_analysis` |
| ST-GAZE-03 | 이야기 시선 분석 결과 저장 | 이야기 읽기 과정에서 분석된 시선 결과를 이야기 진행 기록과 함께 저장한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results`, `get_admin_story_by_studentId_by_storyId_gaze_analysis` |
| ST-GAZE-04 | 이야기 읽기 시선 데이터 수집 종료 | 이야기 장면이 완료되면 해당 이야기에 대한 시선 데이터 수집을 종료한다. | server | `patch_app_gaze_sessions_by_gazeSessionId_end` |
| TE-GAZE-01 | 테스트 시선 데이터 수집 시작 | 테스트 문항이 표시되면 학습자의 시선 위치, 응시 시간, 이동 흐름 등의 데이터 수집을 시작한다. | server | `post_app_gaze_sessions` |
| TE-GAZE-02 | 테스트 시선 데이터 수집 종료 | 테스트 문항 풀이가 종료되면 해당 문항에 대한 시선 데이터 수집을 중단한다. | server | `patch_app_gaze_sessions_by_gazeSessionId_end` |
| TE-GAZE-03 | 문장 영역별 시선 체류 시간 분석 | 학습자가 문장 또는 단어 영역에 머문 시간을 분석하여 오래 응시한 영역을 확인한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results` |
| TE-GAZE-04 | 되돌아보기 횟수 분석 | 학습자가 이미 읽은 문장이나 단어 영역으로 다시 시선을 이동한 횟수를 분석한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results` |
| TE-GAZE-05 | 테스트 시선 분석 결과 저장 | 테스트 중 수집된 시선 데이터를 분석한 결과를 학습 결과와 함께 저장한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results` |
| TR-GAZE-01 | 훈련 시선 데이터 수집 시작 | 훈련 문항 진행 중 학습자의 시선 위치와 응시 흐름 데이터 수집을 시작한다. | server | `post_app_gaze_sessions` |
| TR-GAZE-02 | 훈련 시선 데이터 수집 종료 | 훈련 문항이 완료되면 해당 훈련에 대한 시선 데이터 수집을 종료한다. | server | `patch_app_gaze_sessions_by_gazeSessionId_end` |
| TR-GAZE-03 | 훈련 시선 분석 결과 저장 | 훈련 중 수집된 시선 데이터를 분석하여 훈련 결과와 함께 저장한다. | server | `post_app_gaze_sessions_by_gazeSessionId_analysis_results` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
