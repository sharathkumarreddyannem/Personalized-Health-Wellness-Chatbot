from pydantic import BaseModel
from typing import Optional

class ProfileIn(BaseModel):
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    health_conditions: Optional[str]
    dietary_preferences: Optional[str]
    fitness_goals: Optional[str]
    sleep_habits: Optional[str]

class MessageIn(BaseModel):
    user_id: Optional[int]
    text: str

class BotResponse(BaseModel):
    reply: str
    suggestions: Optional[dict] = None
