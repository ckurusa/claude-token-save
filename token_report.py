"""
token_report.py — Claude Code 세션 토큰 사용량 리포트
사용법: python token_report.py [세션_파일.jsonl] [--threshold 달러액]
"""
import json, os, sys, glob, re
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# 모델별 단가 ($ per 1M tokens)
PRICING = {
    "claude-opus-4-8":     {"input": 15.0,  "output": 75.0,  "cache_read": 1.5,  "cache_write": 18.75},
    "claude-opus-4-7":     {"input": 15.0,  "output": 75.0,  "cache_read": 1.5,  "cache_write": 18.75},
    "claude-sonnet-4-6":   {"input": 3.0,   "output": 15.0,  "cache_read": 0.3,  "cache_write": 3.75},
    "claude-haiku-4-5":    {"input": 0.8,   "output": 4.0,   "cache_read": 0.08, "cache_write": 1.0},
}
DEFAULT_PRICE = {"input": 3.0, "output": 15.0, "cache_read": 0.3, "cache_write": 3.75}


def find_latest_jsonl(cwd: str) -> str | None:
    """cwd 경로에서 해당 프로젝트의 가장 최근 세션 파일을 찾는다."""
    slug = re.sub(r"[^a-zA-Z0-9]", "-", cwd)
    base = Path.home() / ".claude" / "projects" / slug
    if not base.exists():
        return None
    files = sorted(base.glob("*.jsonl"), key=os.path.getmtime, reverse=True)
    return str(files[0]) if files else None


def parse_session(path: str) -> dict:
    totals = {}  # model -> {input, output, cache_read, cache_write, turns}

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if obj.get("type") != "assistant":
                continue

            msg = obj.get("message", {})
            model = msg.get("model", "unknown")
            usage = msg.get("usage", {})
            if not usage:
                continue

            if model not in totals:
                totals[model] = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "turns": 0}

            t = totals[model]
            t["input"]      += usage.get("input_tokens", 0)
            t["output"]     += usage.get("output_tokens", 0)
            t["cache_read"] += usage.get("cache_read_input_tokens", 0)
            t["cache_write"]+= usage.get("cache_creation_input_tokens", 0)
            t["turns"]      += 1

    return totals


def calc_cost(model: str, t: dict) -> float:
    p = PRICING.get(model, DEFAULT_PRICE)
    return (
        t["input"]       * p["input"]       / 1_000_000 +
        t["output"]      * p["output"]      / 1_000_000 +
        t["cache_read"]  * p["cache_read"]  / 1_000_000 +
        t["cache_write"] * p["cache_write"] / 1_000_000
    )


def fmt(n: int) -> str:
    return f"{n:,}"


def report(path: str, threshold: float = 1.0):
    totals = parse_session(path)
    if not totals:
        print("분석 가능한 데이터가 없습니다.")
        return

    print(f"\n{'─'*52}")
    print(f"  📊  토큰 리포트  |  {Path(path).name[:24]}")
    print(f"{'─'*52}")

    grand_total_cost = 0.0
    grand = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0, "turns": 0}

    for model, t in totals.items():
        cost = calc_cost(model, t)
        grand_total_cost += cost
        for k in grand:
            grand[k] += t[k]

        print(f"\n  모델: {model}")
        print(f"  {'턴 수':<16} {t['turns']:>6} 회")
        print(f"  {'입력':<16} {fmt(t['input']):>10} 토큰")
        print(f"  {'출력':<16} {fmt(t['output']):>10} 토큰")
        print(f"  {'캐시 읽기(↓90%)':<16} {fmt(t['cache_read']):>10} 토큰")
        print(f"  {'캐시 생성':<16} {fmt(t['cache_write']):>10} 토큰")
        print(f"  {'추정 비용':<16} ${cost:.4f}")

    if len(totals) > 1:
        print(f"\n  {'─'*46}")
        print(f"  {'합계 턴 수':<16} {grand['turns']:>6} 회")
        print(f"  {'총 입력':<16} {fmt(grand['input']):>10} 토큰")
        print(f"  {'총 출력':<16} {fmt(grand['output']):>10} 토큰")

    print(f"\n  총 추정 비용: ${grand_total_cost:.4f}")

    # 경고
    ratio = grand_total_cost / threshold * 100
    bar_len = min(int(ratio / 5), 20)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    status = "🔴 초과!" if grand_total_cost > threshold else ("🟡 주의" if ratio > 70 else "🟢 양호")
    print(f"  임계치 ${threshold:.2f} 대비: [{bar}] {ratio:.0f}%  {status}")
    print(f"{'─'*52}\n")


if __name__ == "__main__":
    args = sys.argv[1:]
    threshold = 1.0

    # --threshold 파싱
    if "--threshold" in args:
        idx = args.index("--threshold")
        threshold = float(args[idx + 1])
        args = [a for i, a in enumerate(args) if i not in (idx, idx + 1)]

    # 파일 경로 지정 or 자동 탐색
    if args:
        jsonl_path = args[0]
    else:
        jsonl_path = find_latest_jsonl(os.getcwd())
        if not jsonl_path:
            print("❌ 세션 파일을 찾을 수 없습니다. 경로를 직접 지정해 주세요.")
            print("   사용법: python token_report.py <파일.jsonl>")
            sys.exit(1)

    report(jsonl_path, threshold)
