from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import init_db, engine
from models import UserProfile, ChatMessage
from schemas import ProfileIn, MessageIn, BotResponse
from nlu import predict_intent, extract_entities
from recommendations import meal_plan, exercise_routine
import uvicorn

app = FastAPI(title="Personalized Health & Wellness Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/profile", response_model=dict)
def create_or_update_profile(profile: ProfileIn):
    with Session(engine) as session:
        stmt = select(UserProfile).where(UserProfile.name == profile.name) if profile.name else None
        user = session.exec(stmt).first() if stmt else None
        if user:
            for k, v in profile.dict().items():
                setattr(user, k, v)
            session.add(user)
            session.commit()
            session.refresh(user)
        else:
            user = UserProfile(**profile.dict())
            session.add(user)
            session.commit()
            session.refresh(user)
        return {"user_id": user.id}

@app.post("/message", response_model=BotResponse)
def process_message(msg: MessageIn):
    with Session(engine) as session:
        chat = ChatMessage(user_id=msg.user_id, role="user", text=msg.text)
        session.add(chat)
        session.commit()
    intent = predict_intent(msg.text)
    entities = extract_entities(msg.text)
    reply = ""
    suggestions = {}
    if intent["intent"] == "greeting":
        reply = "Hi! I'm your wellness assistant — how can I help today?"
    elif intent["intent"] == "ask_nutrition":
        profile = None
        if msg.user_id:
            with Session(engine) as session:
                profile = session.get(UserProfile, msg.user_id)
        profile_dict = profile.dict() if profile else {}
        suggestions["meal_plan"] = meal_plan(profile_dict)
        reply = "I created a simple meal plan suggestion based on your profile."
    elif intent["intent"] == "ask_exercise":
        profile = None
        if msg.user_id:
            with Session(engine) as session:
                profile = session.get(UserProfile, msg.user_id)
        profile_dict = profile.dict() if profile else {}
        suggestions["exercise"] = exercise_routine(profile_dict)
        reply = "Here's a suggested exercise routine."
    elif intent["intent"] == "ask_symptom":
        reply = "I can provide general information about symptoms but not medical diagnosis. Please consult a doctor."
    else:
        reply = "I can help with nutrition, exercise, sleep, and mood tips. What would you like to do?"
    with Session(engine) as session:
        chat = ChatMessage(user_id=msg.user_id, role="bot", text=reply)
        session.add(chat)
        session.commit()
    return BotResponse(reply=reply, suggestions=suggestions)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
