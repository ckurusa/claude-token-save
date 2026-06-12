---
name: doc-optimizer
description: CLAUDE.md·SOUL.md·README.md의 중복·낡은 내용을 찾아 정리합니다
---

# doc-optimizer

세 문서(`CLAUDE.md`, `SOUL.md`, `README.md`)를 읽고 품질 문제를 진단한 뒤, 수정안을 제시하거나 직접 적용합니다.

## 트리거

- `/doc-optimizer` 입력 시
- "문서 정리해줘", "CLAUDE.md 최적화", "문서 중복 확인" 같은 요청

## 점검 기준

| 원칙 | 확인 항목 |
|------|---------|
| **SSOT** | 같은 정보가 두 파일 이상에 쓰여 있는가? |
| **Minimum** | 파일을 30초 안에 읽을 수 있는가? 불필요한 설명은 없는가? |
| **Freshness** | 실제 코드/구조와 맞지 않는 낡은 내용은 없는가? |

## 실행 순서

### 1단계 — 세 문서 읽기

`CLAUDE.md`, `SOUL.md`, `README.md`를 모두 읽는다.

### 2단계 — 문제 목록 작성

다음 형식으로 진단 결과를 보여준다:

```
[SSOT]      README.md 3행 ↔ CLAUDE.md 7행 — 데이터 소스 설명 중복
[Minimum]   SOUL.md — "존재 이유" 섹션 2문장으로 줄일 수 있음
[Freshness] CLAUDE.md — issue-writer·issue-runner 스킬 목록 누락
```

### 3단계 — 수정 적용 (확인 후)

사용자 승인 시 해당 파일을 직접 수정한다.
- 중복 내용: 한 곳만 남기고 나머지는 참조 링크(`→ SOUL.md 참고`)로 대체
- 낡은 내용: 삭제 또는 현재 상태로 업데이트
- 과도한 설명: 핵심만 남기고 압축

### 4단계 — 결과 보고

수정된 파일 목록과 변경 요약을 전달한다.
