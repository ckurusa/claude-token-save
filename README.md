# Claude Token Save

Claude Code 세션의 토큰 사용량과 비용을 모니터링하는 도구입니다.

## 설치

Python 3.10+, [GitHub CLI](https://cli.github.com/) 설치 후:

```bash
git clone https://github.com/ckurusa/claude-token-save.git
cd claude-token-save
```

## 사용법

### 터미널 리포트

```bash
python token_report.py                   # 최근 세션 자동 탐색
python token_report.py --threshold 2.0  # 임계치 $2 지정
```

### HTML 대시보드

`token_report.html`을 브라우저로 열고, `~/.claude/projects/<slug>/<session>.jsonl` 파일을 드래그하거나 선택합니다.

### 슬래시 커맨드

Claude Code 세션 안에서:

| 커맨드 | 동작 |
|--------|------|
| `/token-report` | 현재 세션 비용 리포트 |
| `/issue-writer` | 약점 분석 → GitHub 이슈 등록 |
| `/issue-runner` | 열린 이슈 처리 → 닫기 |
| `/doc-optimizer` | CLAUDE·SOUL·README 중복·낡은 내용 정리 |

## 파일 구조

```
token_report.py        # CLI 리포트 스크립트
token_report.html      # 브라우저 대시보드
CLAUDE.md              # 에이전트 운영 지침
SOUL.md                # 프로젝트 원칙
.claude/skills/        # 슬래시 커맨드 스킬 정의
```

## 세션 파일 위치

```
~/.claude/projects/<slug>/<session-id>.jsonl
```

`<slug>` = 프로젝트 절대경로에서 영숫자 외 모든 문자를 `-`로 치환한 값
