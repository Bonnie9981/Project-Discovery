"""Run a command, keep the full log on disk, print only a short summary.

    python -m discovery.quiet -- python -m pytest -q
    python -m discovery.quiet --tail 30 --log logs/lake.log -- lake build

Long outputs (pytest, lake build, batch runs) are what fill a conversation.
The full log is kept under logs/ (not in git) so anyone can still read every
line; the conversation only sees the exit code, error-looking lines and the tail.
The exit code is passed through, so CI and scripts behave the same.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERR = re.compile(r"error|fail|traceback|exception|sorry|warning: declaration uses", re.I)


def summarize(lines: list[str], tail: int, max_err: int) -> list[str]:
    errs = [ln for ln in lines[:-tail] if ERR.search(ln)] if tail else [ln for ln in lines if ERR.search(ln)]
    out = []
    if errs:
        shown = errs[:max_err]
        out.append(f"--- {len(errs)} error-like lines before the tail (showing {len(shown)}) ---")
        out += shown
    if tail:
        out.append(f"--- last {min(tail, len(lines))} of {len(lines)} lines ---")
        out += lines[-tail:]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m discovery.quiet")
    ap.add_argument("--tail", type=int, default=15)
    ap.add_argument("--max-err", type=int, default=20)
    ap.add_argument("--log", default=None, help="default: logs/<command>.log")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        ap.error("no command given")
    log = Path(a.log) if a.log else ROOT / "logs" / (re.sub(r"[^\w.-]+", "_", " ".join(cmd))[:60] + ".log")
    log.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                       encoding="utf-8", errors="replace")
    log.write_text(p.stdout, encoding="utf-8")
    lines = p.stdout.splitlines()
    print(f"exit={p.returncode}  lines={len(lines)}  full log: {log}")
    for ln in summarize(lines, a.tail, a.max_err):
        print(ln)
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
