"""Deprecated compatibility entry point.

Candidate construction is staged by sequence_trials/run_repair_round.py using
portable hash-pinned template inputs. Active promotion is deliberately
one-time and decision-specific; the only accepted candidate is B3, guarded by
promote_sequence_merge.py. This file intentionally has no write path.
"""
raise SystemExit(
    "No active merge generation is available here. Use the staged trial runner "
    "for review; promote only a documented decision through the guarded "
    "one-time promotion script."
)
