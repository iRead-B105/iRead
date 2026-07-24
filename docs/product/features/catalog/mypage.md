---
type: Feature Catalog
title: "기능 카탈로그: mypage"
description: "mypage 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, mypage]
timestamp: 2026-07-24T17:47:15+09:00
---
# 기능 카탈로그: mypage

| 기능 ID | 기능 | 설명 | API operationId |
| --- | --- | --- | --- |
| GR-CHAR-01 | 대표 캐릭터 표시 | 현재 대표 캐릭터의 이미지와 이름을 표시한다. | `patch_app_mypage_character_representative` |
| GR-CHAR-02 | 획득 캐릭터 목록 표시 | 학습자가 획득한 캐릭터와 캐릭터가 등장한 이야기 영역을 표시한다. | `get_app_mypage_character` |
| GR-COM-02 | 성장 정보 조회 상태 표시 | 조회 중, 조회 실패, 데이터 없음 상태를 화면에 표시한다. | `get_app_mypage_growth_status` |
| GR-STAT-01 | 성장 영역 카드 표시 | 음운 인식, 파닉스, 단어, 유창성, 긴글 영역을 카드 형태로 표시한다. | `get_app_mypage_growth_statistics` |
| GR-STAT-02 | 영역별 성취 현황 표시 | 소리 조각, 완성 객차, 획득 열매 등 영역별 성취 수치를 표시한다. | `get_app_mypage_growth_statistics` |
| GR-STAT-03 | 영역별 성장 콘텐츠 표시 | 영역의 학습 성과를 꽃, 기차, 나무 등의 시각적 콘텐츠로 표시한다. | `get_app_mypage_growth_statistics` |
| GR-STAT-04 | 영역별 성장률 표시 | 각 학습 영역의 성장률을 백분율과 진행 막대로 표시한다. | `get_app_mypage_growth_statistics` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
