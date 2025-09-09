from transformers import pipeline
import spacy

_intent_classifier = None
_nlu_labels = [
    "greeting","goodbye","ask_symptom","ask_nutrition","ask_exercise",
    "set_profile","smalltalk","ask_sleep","ask_mood","fallback"
]

try:
    _intent_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    _intent_classifier = None

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

def predict_intent(text: str) -> dict:
    if _intent_classifier:
        res = _intent_classifier(text, _nlu_labels)
        top_label = res["labels"][0]
        score = float(res["scores"][0])
        return {"intent": top_label, "score": score}
    return {"intent": "fallback", "score": 0.0}

def extract_entities(text: str) -> dict:
    entities = {}
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            entities.setdefault(ent.label_, []).append(ent.text)
    keywords = {
        "diet": ["vegetarian","vegan","keto","paleo","gluten"],
        "exercise": ["run","jog","yoga","gym","weight","cardio","swim"],
        "symptoms": ["fever","cough","headache","pain","nausea"]
    }
    for k, vals in keywords.items():
        for v in vals:
            if v in text.lower():
                entities.setdefault(k, []).append(v)
    return entities
