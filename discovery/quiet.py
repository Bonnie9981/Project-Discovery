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
import os
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


def _utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m discovery.quiet")
    ap.add_argument("--tail", type=int, default=15)
    ap.add_argument("--max-err", type=int, default=20)
    ap.add_argument("--log", default=None, help="default: logs/<command>.log")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args(argv)
    _utf8_stdout()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    if not cmd:
        ap.error("no command given")
    log = Path(a.log) if a.log else ROOT / "logs" / (re.sub(r"[^\w.-]+", "_", " ".join(cmd))[:60] + ".log")
    log.parent.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    # Stream to the log while the child runs, so a timeout or Ctrl-C still leaves evidence.
    with log.open("w", encoding="utf-8") as fh:
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                    encoding="utf-8", errors="replace", env=env)
        except OSError as e:
            fh.write(f"could not start {cmd[0]!r}: {e}\n")
            print(f"exit=127  could not start {cmd[0]!r}: {e}  full log: {log}")
            return 127
        try:
            for line in proc.stdout:
                fh.write(line)
            rc = proc.wait()
        except KeyboardInterrupt:
            proc.kill()
            fh.write("\n[quiet] interrupted\n")
            raise
    text = log.read_text(encoding="utf-8")
    lines = text.splitlines()
    print(f"exit={rc}  lines={len(lines)}  full log: {log}")
    for ln in summarize(lines, a.tail, a.max_err):
        print(ln)
    return rc


if __name__ == "__main__":
    sys.exit(main())
