"""Resource limits for research tasks (config/limits.json).

Limits are enforced, not just written down:
- ``verify.check`` stops at ``max_iterations`` / ``max_seconds`` and returns INCONCLUSIVE.
- ``run_limited`` runs a command in a subprocess with a wall-clock timeout and, on
  POSIX, CPU-time and address-space limits. On Windows only the timeout applies,
  and the result says so (``enforced``).
- ``records.write_record`` refuses records larger than ``max_record_mb``.
- ``api_budget_usd`` is 0: no paid API may be called by code. Raising it needs CEO approval.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

CONFIG = Path(__file__).resolve().parent.parent / "config" / "limits.json"


@dataclass(frozen=True)
class Budget:
    max_seconds: float = 600
    max_iterations: int = 1_000_000
    max_memory_mb: int = 2048
    max_output_mb: int = 50
    max_record_mb: int = 5
    api_budget_usd: float = 0
    network: str = "allowlist"
    network_allowlist: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def load(cls, profile: str = "default", path: Path = CONFIG) -> "Budget":
        data = json.loads(path.read_text(encoding="utf-8"))[profile]
        data["network_allowlist"] = tuple(data.get("network_allowlist", ()))
        return cls(**data)

    @classmethod
    def default(cls) -> "Budget":
        try:
            return cls.load()
        except (OSError, KeyError, ValueError):
            return cls()

    def as_dict(self) -> dict:
        d = asdict(self)
        d["network_allowlist"] = list(self.network_allowlist)
        return d

    def take(self, it: Iterable[int], label: str) -> list[int] | str:
        """Materialise an iterable, or return a reason string if it exceeds the budget."""
        out = []
        for x in it:
            out.append(x)
            if len(out) > self.max_iterations:
                return f"{label} exceeds max_iterations={self.max_iterations}"
        return out

    def host_allowed(self, host: str) -> bool:
        if self.network == "none":
            return False
        if self.network == "any":
            return True
        return any(host == h or host.endswith("." + h) for h in self.network_allowlist)


def _posix_limits(b: Budget):
    import resource

    def apply():
        cpu = int(b.max_seconds) + 1
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        mem = b.max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        out = b.max_output_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_FSIZE, (out, out))
    return apply


def run_limited(cmd: list[str], budget: Budget | None = None, cwd: str | Path | None = None) -> dict:
    b = budget or Budget.default()
    posix = sys.platform != "win32"
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=b.max_seconds,
                           preexec_fn=_posix_limits(b) if posix else None)
        status = "ok" if p.returncode == 0 else "failed"
        rc, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        status, rc = "timeout", None
        out = e.stdout if isinstance(e.stdout, str) else ""
        err = e.stderr if isinstance(e.stderr, str) else ""
    limit = b.max_output_mb * 1024 * 1024
    return {"status": status, "returncode": rc, "stdout": out[:limit], "stderr": err[:limit],
            "enforced": ["timeout", "cpu", "memory", "file_size"] if posix else ["timeout"],
            "budget": b.as_dict()}
