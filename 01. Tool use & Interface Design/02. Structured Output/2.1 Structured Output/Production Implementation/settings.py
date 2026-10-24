"""LLM call settings, read once at startup so a bad value stops the service at boot."""
import os
from dataclasses import dataclass

EFFORT_LEVELS = ("low", "medium", "high")


@dataclass(frozen=True)
class Settings:
    model: str = "claude-sonnet-5-5"
    # Thinking counts toward max_tokens even when it isn't shown, so this has to cover the
    # model's reasoning (thinking tokens) plus the JSON answer.
    max_tokens: int = 8_000
    # Set explicitly because the default effort differs from model to model.
    effort: str = "medium"

    def __post_init__(self) -> None:
        #Our system doesn't allow XHigh or Max cause they cost too much hence we use this validation
        if self.effort not in EFFORT_LEVELS: 
            raise ValueError(f"effort must be one of {EFFORT_LEVELS}, got {self.effort!r}")
        # Anthropic's rule: Above 21,333 the SDK requires streaming. 
        # Means, if we want the full response at once we need to have max_tokens <=21,333
        if not 1_024 <= self.max_tokens <= 21_333:
            raise ValueError(f"max_tokens must be between 1,024 and 21,333, got {self.max_tokens}")

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            model=os.getenv("TRIAGE_MODEL", cls.model),
            max_tokens=int(os.getenv("TRIAGE_MAX_TOKENS", cls.max_tokens)),
            effort=os.getenv("TRIAGE_EFFORT", cls.effort),
        )