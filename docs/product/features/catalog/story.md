---
type: Feature Catalog
title: "기능 카탈로그: story"
description: "story 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, story]
timestamp: 2026-07-29T11:17:47+09:00
---
# 기능 카탈로그: story

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| ST-BRANCH-01 | 이야기 분기 입력 화면 표시 | AI 이야기 분기점에 도달하면 질문, 선택지 3개와 마이크 입력 화면을 표시한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-BRANCH-02 | 이야기 분기 질문·선택지 표시 | `content`의 분기 질문과 `branchPrompt`의 AI 생성 버튼 선택지 3개를 표시한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-BRANCH-03 | 이야기 분기 음성 STT 처리 | 아동의 음성을 업로드하고 STT로 분기 의도를 나타내는 텍스트를 추출한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-BRANCH-04 | 진행률 기반 AI 이야기 분기 생성 요청 | Backend가 `stories.progress`와 음성 또는 버튼으로 확정한 분기 텍스트를 AI 요청에 포함하여 현재 진행률에 적합한 다음 이야기를 생성한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-BRANCH-05 | AI 생성 분기 장면 저장 및 이동 | 최종 STT 텍스트 또는 선택한 AI 선택지 문구와 생성 장면을 저장한다. 같은 분기 대사의 재시도에는 최초 저장 결과를 변경하지 않고 반환한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-DTL-01 | 이야기 상세 정보 조회 | 선택한 이야기의 표지, 제목, 설명, 예상 시간, 장면 수와 등장인물을 조회한다. | server | `get_app_story_by_studentId_by_storyTemplateId` |
| ST-DTL-02 | 이야기 상세 정보 표시 | 조회한 이야기 정보를 상세 화면에 표시한다. | server | `get_app_story_by_studentId_by_storyTemplateId` |
| ST-DTL-03 | 이야기 책장 화면 이동 | 책장으로 버튼을 선택하면 이야기 목록 화면으로 이동한다. | server | `get_app_story_by_studentId_by_storyTemplateId` |
| ST-DTL-04 | 신규 이야기 생성 | 읽기 시작 버튼 선택 시 해당 이야기의 읽기 세션을 생성한다. | server | `post_app_story_by_studentId_by_storyTemplateId_sessions` |
| ST-DTL-05 | 이야기 읽기 진입 경로 결정 | 최초 읽기이면 조작 안내 화면으로, 기존 기록이 있으면 저장된 장면으로 이동한다. | server | `get_app_story_by_studentId_by_storyTemplateId` |
| ST-DTL-06 | 이야기 읽기 세션 재개 | 저장된 마지막 장면부터 이야기를 다시 시작한다. | server | `get_app_story_by_studentId_by_storyId_resume` |
| ST-DTL-07 | 이어보기 | 이전의 보던 책의 마지막으로 읽은 대사의 화면으로 이동한다. | server | `get_app_story_by_studentId_by_storyId_resume` |
| ST-GUIDE-01 | 이야기 조작 방법 표시 | 장면 이동, 음성 재생, 음성 분기 답변과 목차 사용 방법을 표시한다. | client | - |
| ST-GUIDE-02 | 이야기 조작 안내 완료 처리 | 이제 읽어 볼게요 버튼 선택 시 조작 안내 확인 상태를 저장한다. | client | - |
| ST-GUIDE-03 | 이야기 진행 화면 이동 | 조작 안내 완료 후 첫 번째 이야기 장면으로 이동한다. | client | - |
| ST-LIB-01 | 이야기 목록 조회 | 학습자가 열람할 수 있는 이야기와 진행 상태를 조회한다. | server | `get_app_story_by_studentId` |
| ST-LIB-02 | 이야기 카드 표시 | 이야기 표지, 제목, 예상 시간과 진행 정보를 카드로 표시한다. | server | `get_app_story_by_studentId` |
| ST-LIB-03 | 이야기 카드 진행 상태 표시 | 새 이야기, 읽는 중, 읽음 상태를 표시한다. | server | `get_app_story_by_studentId` |
| ST-LIB-04 | 이야기 진행률 표시 | 읽는 중인 이야기의 현재 장면과 전체 장면 수를 표시한다. | server | `get_app_story_by_studentId` |
| ST-LIB-05 | 이야기 상세 화면 이동 | 선택 가능한 이야기 카드를 선택하면 해당 이야기의 상세 화면으로 이동한다. | server | `get_app_story_by_studentId` |
| ST-LIB-06 | 이야기 선택 안내 표시 | 대표 캐릭터를 통해 학습자가 읽을 이야기를 선택할 수 있도록 안내 문구를 표시한다. | server | `get_app_story_by_studentId` |
| ST-LIB-07 | 내 책장 | 삭제되지 않은 진행 중·완료 이야기 목록을 확인한다. | server | `get_app_story_by_studentId` |
| ST-LIB-08 | 이야기 상태 탭 분류 | 진행 중 이야기와 완료 이야기를 별도 탭으로 구분해 표시한다. | client | `get_app_story_by_studentId` |
| ST-LIB-09 | 진행 중 이야기 보관 제한 | 완료·삭제 이야기를 제외하고 아동별 진행 중 이야기를 최대 15권까지 생성한다. | server | `post_app_story_by_studentId_by_storyTemplateId_sessions` |
| ST-LIB-10 | 진행 중 이야기 삭제 | 제목과 진행률을 확인한 뒤 진행 중 이야기 상태를 `DELETED`로 변경해 아동·교사 책장에서 제외한다. | server | `delete_app_story_session` |
| ST-LIB-11 | 이야기 진입 이미지 준비 | 책장 조회 시 진행 중 이야기는 첫 미열람 장면, 완료 이야기는 첫 장면 이미지를 제공해 독서 화면 진입 전에 미리 로딩한다. | server | `get_app_story_by_studentId` |
| ST-LIB-11 | 이야기 진입 이미지 사전 로딩 | 아동 선택 직후 책장 응답의 진입 장면 이미지를 미리 로딩하고, 실제 이미지가 준비된 뒤 독서 화면을 표시한다. | client | `get_app_story_by_studentId` |
| ST-READ-01 | 이야기 장면 조회 | 현재 장면의 이미지, 제목, 본문, 음성과 음성 분기 입력 필요 여부를 조회한다. | server | `get_app_story_by_studentId_by_storyId_lines_by_lineId` |
| ST-READ-02 | 이야기 장면 표시 | 현재 장면의 이미지와 본문을 화면에 표시한다. | server | `get_app_story_by_studentId_by_storyId_lines_by_lineId` |
| ST-READ-03 | 이야기 장면 진행 상태 표시 | 현재 장면 번호와 전체 장면 수를 표시한다. | server | `get_app_story_by_studentId_by_storyId_lines_by_lineId` |
| ST-READ-04 | 이전 이야기 장면 이동 | 이전 장면이 존재하면 이전 장면으로 이동한다. | server | `get_app_story_by_studentId_by_storyId_lines_by_lineId` |
| ST-READ-05 | 다음 이야기 장면 이동 | 다음 장면이 존재하면 다음 이야기 장면으로 이동한다. | server | `get_app_story_by_studentId_by_storyId_lines_by_lineId` |
| ST-READ-06 | 이야기 목차 표시 | 목차 버튼을 선택하면 읽은 장면과 이동 가능한 장면을 목록으로 표시한다. | server | `get_app_story_by_studentId_by_storyId_lines` |
| ST-READ-07 | 목차 장면 이동 | 목차에서 선택한 읽기 완료 장면으로 이동한다. | server | `get_app_story_by_studentId_by_storyId_lines` |
| ST-READ-08 | 이야기 진행 상태 저장 | 현재 장면과 마지막 읽기 시각을 이야기 읽기 세션에 저장한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-READ-09 | 이야기 완료 처리 | 마지막 장면까지 읽으면 이야기 읽기 세션을 완료 상태로 변경하고 완료 시각을 저장한다. | server | `post_app_story_by_studentId_by_storyId_lines_by_lineId_branches` |
| ST-STT-01 | 마이크 사용 권한 확인 | 소리 내어 읽기 시작 전에 마이크 권한과 장치 사용 가능 여부를 확인한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-02 | 이야기 문장 음성 입력 시작 | 학습자가 현재 읽기 대상 문장을 소리 내어 읽을 수 있도록 음성 입력을 시작한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-03 | 이야기 문장 음성 입력 종료 | 사용자의 읽기 완료 요청 또는 제한 시간 도달 시 음성 입력을 종료한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-04 | 이야기 문장 음성 인식 | 입력된 음성을 STT로 변환하여 인식된 문장을 생성한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-05 | 이야기 문장 읽기 결과 검증 | STT 인식 문장과 현재 읽기 대상 문장을 비교하여 읽기 결과를 검증한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-06 | 이야기 문장 읽기 상태 표시 | 음성 입력 대기, 듣는 중, 인식 중, 완료와 재시도 상태를 표시한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-07 | 이야기 문장 읽기 결과 저장 | 인식 결과, 읽기 시간, 재시도 횟수와 대상 문장 정보를 이야기 읽기 세션에 저장한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-STT-08 | 이야기 문장 읽기 실패 처리 | 음성이 감지되지 않거나 STT 인식에 실패하면 오류를 안내하고 다시 읽을 수 있도록 한다. | server | `post_app_story_by_studentId_by_storyId_speech` |
| ST-TTS-01 | 이야기 본문 TTS 음성 조회 | 현재 장면 본문에 대응하는 TTS 음성을 조회하며, 생성된 음성이 없으면 음성 생성을 요청한다. | server | `post_app_story_by_studentId_by_storyId_tts` |
| ST-TTS-02 | 이야기 음성 재생 | 재생 버튼을 선택하면 현재 장면의 TTS 음성을 재생하고, 재생이 완료된 뒤 같은 버튼을 다시 선택하면 처음부터 다시 재생한다. | server | `post_app_story_by_studentId_by_storyId_tts` |
| ST-TTS-03 | 이야기 음성 재생 상태 제어 | 음성 재생, 일시 정지, 종료와 중복 재생을 제어한다. | server | `post_app_story_by_studentId_by_storyId_tts` |
| ST-TTS-04 | 이야기 음성 재생 완료 처리 | 현재 장면의 TTS 음성 재생이 끝나면 재생 상태를 완료로 변경하고 동일한 재생 버튼을 다시 사용할 수 있도록 한다. | server | `post_app_story_by_studentId_by_storyId_tts` |
| ST-TTS-05 | 이야기 음성 재생 실패 처리 | TTS 음성을 불러오거나 재생하지 못한 경우 오류를 안내하고 다시 시도할 수 있도록 한다. | server | `post_app_story_by_studentId_by_storyId_tts` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
