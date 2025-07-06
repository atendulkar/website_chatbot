from chatbot.hybrid_search import hybrid_semantic_search

GREETINGS = ["hi", "hello", "hey", "good morning", "good afternoon"]
FAREWELLS = ["bye", "goodbye", "see you", "take care"]
THANKS = ["thank you", "thanks", "appreciate it"]

def classify_intent(user_input):
    lower = user_input.lower()
    if any(greet in lower for greet in GREETINGS):
        return "greeting"
    elif any(farewell in lower for farewell in FAREWELLS):
        return "farewell"
    elif any(thank in lower for thank in THANKS):
        return "thanks"
    return "search"

def get_bot_response(user_input):
    intent = classify_intent(user_input)

    if intent == "greeting":
        return "Hello! How can I assist you with NAIC information today?"
    elif intent == "farewell":
        return "Goodbye! Let me know if you need anything else."
    elif intent == "thanks":
        return "You're welcome! Happy to help."
    else:
        return hybrid_semantic_search(user_input)
