def meal_plan(profile: dict) -> dict:
    plan = {"breakfast": "Oats with fruits and nuts",
            "lunch": "Grilled chicken / paneer salad + brown rice",
            "dinner": "Vegetable soup + whole grain bread"}
    dp = (profile.get("dietary_preferences") or "").lower()
    if "vegan" in dp:
        plan = {"breakfast": "Smoothie with tofu and oats",
                "lunch": "Quinoa salad with chickpeas",
                "dinner": "Lentil stew + brown rice"}
    if "keto" in dp:
        plan = {"breakfast": "Eggs and avocado",
                "lunch": "Grilled fish / paneer and salad",
                "dinner": "Low-carb vegetable stir-fry"}
    return plan

def exercise_routine(profile: dict) -> dict:
    goal = (profile.get("fitness_goals") or "general").lower()
    if "weight" in goal:
        return {"cardio": "30 min brisk walk / jog 5x week", "strength": "3x/week full-body"}
    if "tone" in goal or "muscle" in goal:
        return {"strength": "4x/week split routine", "cardio": "2x/week 20 min"}
    return {"daily": "30 min mixed activity: walk + mobility + 10 min stretching"}
