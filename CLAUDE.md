# TOKEN SAVE — Claude Code 토큰 절약 실습

Claude Code 세션의 토큰 사용량을 측정·모니터링하는 스킬 실습 프로젝트입니다.

## 핵심 파일

| 파일 | 역할 |
|------|------|
| `token_report.py` | 세션 JSONL 파싱 → 토큰/비용 집계 리포트 |
| `.claude/skills/token-report.md` | `/token-report` 스킬 정의 |

## 빠른 사용

```bash
# 현재 세션 리포트 (자동 탐색)
python token_report.py

# 임계치 지정 ($2)
python token_report.py --threshold 2.0
```

## 데이터 소스

세션 데이터: `~/.claude/projects/<slug>/<session-id>.jsonl`
- `type == "assistant"` 라인의 `message.usage` 필드에서 읽음
- 입력/출력/캐시 읽기/캐시 생성 토큰 전부 기록됨

## 스킬 사용

세션 중 언제든지 `/token-report` 를 입력하면 현재까지 사용량을 확인할 수 있다.
