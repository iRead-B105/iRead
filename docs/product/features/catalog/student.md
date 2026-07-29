---
type: Feature Catalog
title: "기능 카탈로그: student"
description: "student 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, student]
timestamp: 2026-07-29T11:17:47+09:00
---
# 기능 카탈로그: student

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| DB-COM-01 | 아동 등록 화면 이동 | 새 아동과 보호자 정보를 입력하는 아동 등록 화면으로 이동한다. | client | - |
| DB-COM-02 | 아동 행 관리 메뉴 표시 | 아동 행에서 아동 상세, 정보 수정과 아동 삭제 메뉴를 표시한다. | client | - |
| DB-DSP-01 | 아동 목록 표시 | 현재 교수자가 담당하는 아동의 이름, 학교, 나이, 현재 학습, 최근 학습일, 이번 주 참여 상태와 누적 학습 시간을 목록으로 표시한다. | server | `get_admin_student_list` |
| DB-DSP-02 | 아동 목록 페이지 이동 | 아동 목록이 여러 페이지인 경우 이전, 다음 또는 페이지 번호를 선택해 목록을 이동한다. | client | - |
| DB-DSP-03 | 아동 목록 빈 상태 표시 | 검색·필터 조건에 맞는 아동이 없으면 결과 없음 안내를 표시한다. | client | - |
| DB-FLT-01 | 아동 이름·학교 검색 | 입력한 이름 또는 학교명을 기준으로 담당 아동 목록을 필터링한다. | server | `get_admin_student_list` |
| DB-FLT-02 | 아동 나이 필터 | 전체 또는 6세부터 12세까지의 나이를 선택해 아동 목록을 필터링한다. | server | `get_admin_student_list` |
| DB-FLT-03 | 최근 학습 기간 필터 | 전체 기간, 최근 7일 또는 최근 30일을 선택해 아동 목록을 필터링한다. | server | `get_admin_student_list` |
| DB-SEL-01 | 아동 선택 | 아동 목록에서 관리할 아동을 선택한다. | client | - |
| DB-SEL-02 | 아동 선택 성공 처리 | 아동이 선택되면 해당 아동의 메인 홈 화면으로 이동한다. | client | - |
| DB-SEL-03 | 아동 선택 실패 처리 | 아동을 선택할 수 없으면 오류를 표시하고 다시 선택할 수 있도록 한다. | client | - |
| DB-STAT-01 | 전체 아동 수 표시 | 현재 교수자가 담당하는 전체 아동 수를 표시한다. | server | `get_admin_student_summary` |
| DB-STAT-02 | 오늘 학습 예정 수 표시 | 오늘 학습 일정이 예약된 아동 수를 표시한다. | server | `get_admin_student_summary` |
| GR-COM-01 | 성장 정보 조회 | 완료된 훈련 횟수를 학습자·훈련 템플릿별로 실시간 집계하여 조회한다. | server | `get_app_student_by_studentId_growth` |
| GR-COM-02 | 성장 정보 조회 상태 표시 | 조회 중, 조회 실패와 데이터 없음 상태를 클라이언트에서 표시한다. | client | - |
| GR-STAT-01 | 훈련 템플릿별 성장 카드 표시 | 훈련 템플릿 이름과 완료 횟수를 성장 카드에 표시한다. | server | `get_app_student_by_studentId_growth` |
| GR-STAT-02 | 훈련 완료 횟수 표시 | 같은 훈련 템플릿을 완료할 때마다 1회씩 증가한 완료 횟수를 표시한다. | server | `get_app_student_by_studentId_growth` |
| GR-STAT-03 | 꽃 성장 콘텐츠 표시 | 훈련 완료 0회부터 5회까지 매회 꽃을 한 단계씩 성장시키고 5회 이상이면 만개 상태로 표시한다. | client | - |
| GR-STAT-04 | 성장 단계 표시 | 클라이언트가 min(completedCount, 5)로 현재 성장 단계를 계산한다. | client | - |
| MH-DSP-01 | 학습 기록 표시 | 선택한 아동의 학습 날짜, 학습 종류, 분류와 성취도를 표시한다. | server | `get_admin_student_by_studentId_training_history` |
| MH-DSP-02 | 학습 상태 요약 표시 | 선택한 아동의 현재 단계, 최근 학습일과 확인이 필요한 학습 이벤트 수를 표시한다. | server | `get_admin_student_by_studentId_learning_summary` |
| MH-DSP-03 | 다음 권장 훈련 표시 | 아동의 최근 결과를 바탕으로 다음 권장 훈련과 권장 시간·횟수를 표시한다. | server | `get_admin_student_by_studentId_learning_events` |
| MH-DSP-04 | 학습 이벤트 상세 표시 | 선택한 최근 학습 기록의 발생 정보, 문제 구간, 재시도와 시스템 대응을 표시한다. | server | `get_admin_student_by_studentId_learning_events` |
| MH-SAVE-01 | 교수자 내부 메모 저장 | 아동의 단일 교수 메모를 students.teacher_memo에 저장한다. 별도 메모 목록이나 이력은 생성하지 않는다. | server | `patch_admin_student_by_studentId` |
| MH-SAVE-02 | 교수자 내부 메모 입력값 검증 | students.teacher_memo에 저장할 선택 입력값의 허용 길이와 형식을 검증한다. | server | `patch_admin_student_by_studentId` |
| MH-SAVE-03 | 교수자 내부 메모 저장 성공 처리 | students.teacher_memo 갱신이 완료되면 저장 성공 결과를 표시한다. | server | `patch_admin_student_by_studentId` |
| MH-SAVE-04 | 교수자 내부 메모 저장 실패 처리 | students.teacher_memo 갱신에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_student_by_studentId` |
| MH-SAVE-05 | 학습 이벤트 내용을 교수 메모에 추가 | 선택한 학습 이벤트 내용을 현재 teacher_memo 입력값에 추가한 뒤 단일 교수 메모로 저장한다. | server | `patch_admin_student_by_studentId` |
| MH-SAVE-07 | 교수자 내부 메모 수정 | 기존 students.teacher_memo 값을 수정한다. | server | `patch_admin_student_by_studentId` |
| MH-STAT-01 | 읽기 정확도 추이 표시 | 최근 6주의 읽기 정확도 변화, 변화폭과 해석을 차트로 표시한다. | server | `get_admin_student_by_studentId_accuracy_trend` |
| SM-DSP-01 | 아동 상세 정보 표시 | 아동 정보 수정 화면에서 선택한 아동의 기본 정보와 보호자 정보를 표시한다. | server | `get_admin_student_by_studentId` |
| SM-SAVE-01 | 아동 등록 처리 | 입력한 아동 정보를 저장하고 현재 교수자의 담당 아동으로 등록한다. | server | `post_admin_student` |
| SM-SAVE-02 | 아동 삭제 처리 | 삭제를 확인한 아동의 정보를 삭제한다. | server | `delete_admin_student_by_studentId` |
| SM-SAVE-03 | 아동 정보 수정 입력 | 아동 정보와 보호자 정보를 입력하거나 수정한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-04 | 아동 등록 입력값 검증 | 아동과 보호자 등록 정보의 필수 입력 여부와 허용 형식을 검증한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-05 | 아동 정보 수정 저장 | 현재 입력한 아동 정보 수정사항의 저장을 요청한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-06 | 아동 정보 수정 취소 처리 | 저장하지 않은 아동 정보 수정사항을 취소하고 기존 값으로 되돌린다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-07 | 아동 등록 성공 처리 | 아동 등록이 완료되면 등록 결과를 표시하고 아동 정보를 갱신한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-08 | 아동 등록 실패 처리 | 아동 등록에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-09 | 아동 삭제 성공 처리 | 아동 삭제가 완료되면 삭제 결과를 표시하고 아동 목록을 갱신한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-10 | 아동 삭제 실패 처리 | 아동 삭제에 실패하면 실패 사유를 표시하고 삭제를 중단한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-11 | 아동 정보 수정 입력값 검증 | 수정한 아동과 보호자 정보의 필수 입력 여부와 허용 형식을 검증한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-12 | 아동 정보 수정 성공 처리 | 아동 정보 수정이 완료되면 수정 결과를 표시하고 상세 정보를 갱신한다. | server | `patch_admin_student_by_studentId` |
| SM-SAVE-13 | 아동 정보 수정 실패 처리 | 아동 정보 수정에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_student_by_studentId` |
| SM-SEL-01 | 아동 관리 하위 화면 이동 | 메인 홈, 커리큘럼, 훈련 이력, 테스트 이력 또는 보고서 화면으로 이동한다. | server | `get_admin_student_by_studentId` |
| SM-SEL-02 | 아동 등록 정보 입력 | 새 아동과 보호자의 등록 정보를 입력한다. | server | `get_admin_student_by_studentId` |
| SM-SEL-03 | 아동 삭제 확인 | 선택한 아동의 삭제 여부를 확인한다. | server | `get_admin_student_by_studentId` |
| SM-SEL-04 | 아동 프로필 이미지 선택 | 아동 등록 또는 수정 화면에서 JPG·PNG 형식의 5MB 이하 프로필 이미지를 선택한다. | server | `get_admin_student_by_studentId` |
| TH-FLT-01 | 훈련 이력 조회 기간 선택 | 최근 30일 또는 최근 3개월을 선택해 훈련 이력 조회 범위를 변경한다. | server | `get_admin_student_by_studentId_training_history` |
| TI-STAT-03 | 아동 테스트 평균 추이 표시 | 선택한 아동의 날짜별 테스트 평균값 추이를 테스트 비교 막대그래프와 함께 꺾은선 그래프로 표시한다. | server | `get_admin_student_by_studentId_accuracy_trend` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
