# TOKEN SAVE — Claude Code 토큰 절약 실습

Claude Code 세션의 토큰 사용량을 측정·모니터링하는 스킬 실습 프로젝트입니다.
프로젝트 원칙 → [SOUL.md](SOUL.md)

## 핵심 파일

| 파일 | 역할 |
|------|------|
| `token_report.py` | 세션 JSONL 파싱 → 토큰/비용 집계 리포트 |
| `token_report.html` | 브라우저 대시보드 (파일 선택형) |

## 빠른 사용

```bash
python token_report.py                   # 현재 세션 자동 탐색
python token_report.py --threshold 2.0  # 임계치 $2 지정
```

## 데이터 소스

세션 데이터: `~/.claude/projects/<slug>/<session-id>.jsonl`
- `type == "assistant"` 라인의 `message.usage` 필드에서 읽음
- slug = 프로젝트 경로의 영숫자 외 문자를 `-`로 치환한 값

## 스킬 목록

| 커맨드 | 동작 |
|--------|------|
| `/token-report` | 현재 세션 비용 리포트 |
| `/issue-writer` | 약점 분석 → GitHub 이슈 등록 |
| `/issue-runner` | 열린 이슈 처리 → 닫기 |
| `/doc-optimizer` | 문서 중복·낡은 내용 정리 |
