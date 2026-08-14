---
type: Feature Catalog
title: "기능 카탈로그: mypage"
description: "mypage 도메인의 기능 식별자, 설명과 API 관계를 정리합니다."
tags: [feature, catalog, mypage]
timestamp: 2026-07-29T11:17:47+09:00
---
# 기능 카탈로그: mypage

| 기능 ID | 기능 | 설명 | 책임 | API operationId |
| --- | --- | --- | --- | --- |
| GR-CHAR-01 | 대표 캐릭터 표시 | 서버에 대표 상태를 저장하지 않으며 필요한 표시 상태는 클라이언트에서 관리한다. | client | - |
| GR-CHAR-02 | 획득 캐릭터 목록 표시 | 학습자가 획득한 캐릭터와 캐릭터가 등장한 이야기 영역을 표시한다. | server | `get_app_mypage_character` |

# Sources

[Notion 기능 명세](https://app.notion.com/p/de0027df905383e98fb00120c64321fc)
