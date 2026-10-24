from dataclasses import dataclass
from typing import Literal

from anthropic.types import Message


@dataclass(frozen=True)
class TruncationDetail:
    """Why a max_tokens stop happened. Holds counts only, never ticket text."""

    phase: Literal["thinking", "answer", "unknown"]  # what was being generated when the limit hit
    max_tokens: int
    output_tokens: int              # thinking + answer, as billed
    thinking_tokens: int
    answer_tokens: int | None
    answer_chars: int               # length of the partial JSON, not its content

    @property
    def thinking_share(self) -> float | None:
        if self.thinking_tokens is None or self.output_tokens == 0:
            return None
        return self.thinking_tokens / self.output_tokens


def truncation_detail(response: Message, max_tokens: int) -> TruncationDetail:
    last = response.content[-1] if response.content else None
    if last is not None and last.type in ("thinking", "redacted_thinking"):
        phase = "thinking"   # the limit hit before any JSON was written
    elif last is not None and last.type == "text":
        phase = "answer"     # the JSON was cut partway through
    else:
        phase = "unknown"

    thinking = response.usage.output_tokens_details.thinking_tokens
    output = response.usage.output_tokens
    return TruncationDetail(
        phase=phase,
        max_tokens=max_tokens,
        output_tokens=output,
        thinking_tokens=thinking,
        answer_tokens=output - thinking if thinking is not None else None,
        answer_chars=sum(len(b.text) for b in response.content if b.type == "text"),
    )