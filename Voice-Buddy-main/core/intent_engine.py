class IntentEngine:
    def __init__(self):
        self.intents = {
            "greet": ["hello", "hi", "hey"],
            "time": ["time", "current time", "clock"],
            "date": ["date", "today", "day"],
            "math": ["calculate", "solve", "what is"],
            "open": ["open", "launch", "start"],
            "search": ["search", "find", "look up"]
        }

    def detect(self, text: str):
        text = text.lower().strip()

        # allow app name without "open"
        for keyword in ["notepad", "calculator", "calc", "paint", "cmd"]:
            if text == keyword:
                return "open"

        scores = {}
        for intent, keywords in self.intents.items():
            scores[intent] = sum(
                1 for k in keywords if text == k or k in text
            )

        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else None
