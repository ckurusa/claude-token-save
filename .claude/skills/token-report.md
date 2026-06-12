# token-report

현재 Claude Code 세션의 토큰 사용량과 추정 비용을 리포트합니다.

## 트리거

다음 중 하나를 사용할 때 이 스킬을 사용한다:
- 사용자가 `/token-report` 를 입력할 때
- "토큰 얼마 썼어?", "비용 확인", "토큰 사용량 보여줘" 같은 요청

## 실행 방법

프로젝트 루트의 `token_report.py`를 Bash 툴로 실행한다.

```bash
python token_report.py
```

임계치를 지정하고 싶을 때:
```bash
python token_report.py --threshold 2.0
```

특정 세션 파일을 직접 지정할 때:
```bash
python token_report.py "C:\Users\Admin\.claude\projects\<slug>\<session>.jsonl"
```

## 결과 해석

| 항목 | 설명 |
|------|------|
| 입력 토큰 | 실제 청구되는 입력 (캐시 미적용) |
| 캐시 읽기 | 90% 할인 적용 — 많을수록 절약 |
| 캐시 생성 | 캐시 쓰기 비용 (약 25% 추가) |
| 출력 토큰 | 가장 단가 높음 — 불필요한 긴 답변 줄이면 절약 |

## 절약 팁 (리포트 후 안내)

- 🟢 70% 미만: 양호. 계속 진행.
- 🟡 70~100%: 주의. `/compact` 로 컨텍스트 압축 고려.
- 🔴 초과: `/clear` 로 세션 초기화 또는 작업 마무리 권장.
