from pydantic import BaseModel, Field


class UserInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    user_id: str = Field(min_length=1, max_length=80)
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0, lt=500)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=1, max_length=2000)
