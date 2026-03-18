import threading
import queue
import time

try:
    import pyttsx3
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False


class Speaker:
    def __init__(self):
        self.enabled = TTS_AVAILABLE
        if not self.enabled:
            return

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 180)
        self.engine.setProperty("volume", 1.0)

        self.queue = queue.Queue()
        threading.Thread(
            target=self._speech_loop,
            daemon=True
        ).start()

    def say(self, text: str):
        if self.enabled:
            self.queue.put(text)

    def _speech_loop(self):
        while True:
            text = self.queue.get()
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
            time.sleep(0.05)
