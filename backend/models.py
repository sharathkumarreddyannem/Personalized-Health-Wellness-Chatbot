from sqlmodel import SQLModel, Field
from typing import Optional

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    age: Optional[int]
    gender: Optional[str]
    health_conditions: Optional[str]
    dietary_preferences: Optional[str]
    fitness_goals: Optional[str]
    sleep_habits: Optional[str]

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int]
    role: str
    text: str
