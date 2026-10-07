# auth.py — a FAKE login system.
# Real apps would check a password or login token here. We just read the
# user ID from a request header, defaulting to "u_1". This lets you
# pretend to be different users and test the ownership check.

from dataclasses import dataclass
from typing import Annotated

from fastapi import Header


@dataclass
class User:
    id: str


async def current_user(x_user_id: Annotated[str, Header()] = "u_1") -> User:
    # FastAPI reads a header called "X-User-Id" from the request
    return User(id=x_user_id)
