from typing import TypedDict


class CodeReview(TypedDict):
    user_code: str
    answers: list[str]
    reasons: str
    response: str
