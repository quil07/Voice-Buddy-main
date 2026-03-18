import datetime
import os
import subprocess
import webbrowser
from difflib import get_close_matches

from core.intent_engine import IntentEngine
from core.math_engine import safe_eval
from core.speaker import Speaker
from core.voice_listener import VoiceListener
from core.app_indexer import AppIndexer


# ===================== SYSTEM APPS =====================
SYSTEM_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "control panel": "control.exe"
}

# ===================== WEBSITES =====================
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com"
}


class Assistant:
    def __init__(self, ui):
        self.ui = ui
        self.intent_engine = IntentEngine()
        self.speaker = Speaker()
        self.voice = VoiceListener(self.on_voice_result)
        self.app_indexer = AppIndexer()

    # ===================== MAIN HANDLER =====================
    def handle(self, text: str):
        intent = self.intent_engine.detect(text)

        if intent == "greet":
            reply = (
                "Hello! I’m VoiceBuddy. "
                "I can help with time, date, calculations, apps, and searches."
            )

        elif intent == "time":
            reply = datetime.datetime.now().strftime(
                "The time is %I:%M %p."
            )

        elif intent == "date":
            reply = datetime.datetime.now().strftime(
                "Today is %A, %B %d, %Y."
            )

        elif intent == "math":
            try:
                expr = (
                    text.lower()
                    .replace("calculate", "")
                    .replace("what is", "")
                    .strip()
                )
                reply = f"The result is {safe_eval(expr)}."
            except:
                reply = "I couldn't calculate that."

        elif intent == "search":
            reply = self.search_google(text)

        elif intent == "open":
            reply = self.open_target(text)

        else:
            # 🔍 Final fallback → Google search
            reply = self.search_google(text)

        # UI update (thread-safe)
        self.ui.after(0, lambda: self.ui.log(reply))

        # 🔊 Speak ONLY greeting
        if intent == "greet":
            self.speaker.say(reply)

    # ===================== GOOGLE SEARCH =====================
    def search_google(self, text: str):
        query = (
            text.lower()
            .replace("search", "")
            .replace("find", "")
            .replace("look up", "")
            .strip()
        )

        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching Google for {query}."

    # ===================== OPEN APP / WEBSITE =====================
    def open_target(self, text: str):
        query = (
            text.lower()
            .replace("open", "")
            .replace("launch", "")
            .replace("start", "")
            .strip()
        )

        if not query:
            return "Please tell me what to open."

        # 🌐 1️⃣ Full URL
        if query.startswith("http://") or query.startswith("https://"):
            webbrowser.open(query)
            return f"Opening {query}."

        # 🌐 2️⃣ Website exact match
        if query in WEBSITES:
            webbrowser.open(WEBSITES[query])
            return f"Opening {query}."

        # 🌐 3️⃣ Website fuzzy match
        site_match = get_close_matches(query, WEBSITES.keys(), n=1, cutoff=0.6)
        if site_match:
            site = site_match[0]
            webbrowser.open(WEBSITES[site])
            return f"Opening {site}."

        # 🌐 4️⃣ Domain-like input
        if "." in query:
            webbrowser.open("https://" + query)
            return f"Opening {query}."

        # 🖥️ 5️⃣ System apps
        for name, cmd in SYSTEM_APPS.items():
            if name == query or name in query:
                try:
                    subprocess.Popen(cmd)
                    return f"Opening {name}."
                except:
                    return f"I couldn't open {name}."

        # 🖥️ 6️⃣ Installed apps (Start Menu, fuzzy)
        shortcut = self.app_indexer.find(query)
        if shortcut:
            try:
                os.startfile(shortcut)
                return f"Opening {shortcut.stem}."
            except:
                return f"I found {shortcut.stem}, but couldn't open it."

        # 🔍 7️⃣ Final fallback → Google search
        return self.search_google(query)

    # ===================== VOICE INPUT =====================
    def listen(self):
        self.ui.after(0, lambda: self.ui.set_status("🎙 Listening..."))
        self.voice.start()

    def on_voice_result(self, text):
        self.ui.after(0, lambda: self.ui.set_status("Ready"))

        if not text:
            self.ui.after(0, lambda: self.ui.log(
                "Sorry, I didn't catch that. Please try again.", "assistant"
            ))
            return

        # Log exactly what was recognized
        self.ui.after(0, lambda: self.ui.log(text, "user"))
        self.handle(text)
