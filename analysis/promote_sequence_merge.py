"""Completed one-time promotion notice; intentionally performs no writes.

The reviewed B3 merge has already been promoted and the original continuation
archived. Active native XML and the active manifest are now canonical. Future
edits should be made directly in native XML and rendered for review; this
historical promotion entry point cannot apply or overwrite anything.
"""
raise SystemExit(
    "B3 promotion is complete. This historical entry point is no-write; edit "
    "the active native XML directly and render it for review."
)
