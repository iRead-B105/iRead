---
type: Feature Catalog
title: "기능 카탈로그: teacher"
description: "teacher 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, teacher]
timestamp: 2026-07-27T12:19:48+09:00
---
# 기능 카탈로그: teacher

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| SB-DSP-01 | 교수자 요약 정보 표시 | 현재 교수자의 프로필 사진, 이름과 요약 정보를 표시한다. | server | `get_admin_teacher_info` |
| SB-DSP-02 | 교수자 프로필 정보 표시 | 교수자의 프로필 이미지, 이름, 소속 기관, 이메일, 성별, 연락처와 주소를 표시한다. | server | `get_admin_teacher_info` |
| SB-SAVE-01 | 교수자 프로필 입력값 검증 | 수정한 프로필 이미지와 교수자 정보의 필수 입력 여부 및 허용 형식을 검증한다. | server | `patch_admin_teacher_profile` |
| SB-SAVE-02 | 교수자 프로필 저장 | 검증된 교수자 프로필 수정사항을 저장한다. | server | `patch_admin_teacher_profile` |
| SB-SAVE-03 | 교수자 프로필 저장 성공 처리 | 교수자 프로필 저장이 완료되면 저장 결과를 표시하고 프로필 정보를 갱신한다. | server | `patch_admin_teacher_profile` |
| SB-SAVE-04 | 교수자 프로필 저장 실패 처리 | 교수자 프로필 저장에 실패하면 실패 사유를 표시하고 다시 시도할 수 있도록 한다. | server | `patch_admin_teacher_profile` |
| SB-SAVE-05 | 교수자 프로필 수정 취소 처리 | 저장하지 않은 교수자 프로필 수정사항을 취소하고 기존 값으로 되돌린다. | server | `patch_admin_teacher_profile` |
| SB-SEL-01 | 교수자 프로필 이미지 선택 | 교수자 프로필에 사용할 이미지를 선택하거나 변경한다. | server | `get_admin_teacher_info` |
| SB-SEL-02 | 교수자 프로필 정보 수정 입력 | 교수자의 이름, 소속 기관, 이메일, 성별, 연락처와 주소를 입력하거나 수정한다. | server | `get_admin_teacher_info` |
| SB-SEL-03 | 아동 변경 메뉴 표시 | 현재 아동 요약을 선택하면 최근 본 아동과 전체 아동 목록을 표시한다. | server | `get_admin_teacher_info` |
| SB-SEL-04 | 아동 변경 목록 검색 | 아동 변경 메뉴에서 이름을 입력해 전환할 아동을 검색한다. | server | `get_admin_teacher_info` |
| SB-SEL-05 | 현재 아동 변경 | 아동 변경 목록에서 다른 아동을 선택해 현재 관리 대상을 변경한다. | server | `get_admin_teacher_info` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
