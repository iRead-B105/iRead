---
type: Feature Catalog
title: "기능 카탈로그: report"
description: "report 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, report]
timestamp: 2026-07-25T01:00:44+09:00
---
# 기능 카탈로그: report

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| RP-DSP-01 | 보고서 상세 조회 | 선택한 저장 보고서의 상세 내용을 조회한다. | server | `get_admin_report_by_reportId` |
| RP-DSP-02 | 보고서 교수자 의견 입력 | 보고서에서만 사용하는 보호자 전달용 학습 결과와 다음 지도 계획을 교수자 의견으로 직접 입력한다. 학습 현황의 교수자 내부 메모와 연동하지 않는다. | server | `patch_admin_report_by_reportId_teacher_memo` |
| RP-DSP-03 | 보고서 상세 미리보기 표시 | 선택 기간의 학습 분석 결과와 교수자 의견을 저장된 보고서 상세 화면에 표시한다. | server | `get_admin_report_by_reportId` |
| RP-DSP-04 | 보고서 상세 표시 | 동기 생성되어 저장된 보고서의 분석 결과와 교수자 메모를 표시한다. | server | `get_admin_report_by_reportId` |
| RP-DSP-05 | 보고서 조회 실패 처리 | 보고서를 조회할 수 없으면 오류를 표시하고 다시 선택할 수 있도록 한다. | server | `get_admin_report_by_reportId` |
| RP-DSP-07 | 보고서 생성일 표시 | reports.created_at을 보고서 생성일로 표시한다. 발행 버전은 사용하지 않는다. | server | `get_admin_report_by_reportId` |
| RP-GAZE-01 | 시선 분석 결과 보고서 반영 | 저장된 시선 분석 결과를 보고서 작성 화면에 반영하여 아동의 읽기 패턴을 참고할 수 있도록 한다. | server | `post_admin_report_by_reportId_gaze_analysis` |
| RP-GEN-01 | 보고서 분석 결과 자동 생성 | 선택한 기간의 학습 데이터를 동기 처리하여 보고서 분석 결과를 생성하고 reports.snapshot_data에 저장한다. | server | `post_admin_report` |
| RP-GEN-02 | 보고서 분석 결과 생성 성공 처리 | 동기 보고서 생성이 완료되면 저장된 보고서 상세와 교수자 메모 입력 화면을 표시한다. | server | `post_admin_report` |
| RP-GEN-03 | 보고서 분석 결과 생성 실패 처리 | 동기 보고서 생성에 실패하면 저장하지 않고 오류를 표시한 뒤 다시 시도할 수 있도록 한다. | server | `post_admin_report` |
| RP-SAVE-01 | 보고서 저장 | 선택 기간의 동기 분석 결과, 기간과 교수자 의견을 reports에 저장하고 created_at을 보고서 작성 일시로 사용한다. | server | `post_admin_report` |
| RP-SEL-01 | 보고서 기간 선택 | 보고서 작성에 사용할 시작일과 종료일을 선택한다. | client | - |
| RP-SEL-02 | 보고서 선택 | 저장된 보고서 목록에서 발행일-v번호 형식의 보고서를 선택해 상세 내용을 확인한다. | client | - |
| RP-SEL-03 | 보고서 기간 입력값 검증 | 보고서 시작일과 종료일의 필수 입력 여부와 기간 순서를 검증한다. | client | - |
| RP-SEL-04 | 보고서 기간 다시 설정 | 보고서 미리보기에서 기간 설정 단계로 돌아가 시작일과 종료일을 다시 선택한다. | client | - |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
