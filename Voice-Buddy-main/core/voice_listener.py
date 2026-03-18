import threading

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except:
    SR_AVAILABLE = False


class VoiceListener:
    def __init__(self, callback):
        self.callback = callback
        self.listening = False

    def start(self):
        if not SR_AVAILABLE or self.listening:
            return

        self.listening = True
        threading.Thread(
            target=self._listen,
            daemon=True
        ).start()

    def _listen(self):
        r = sr.Recognizer()
        r.energy_threshold = 200
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1.0

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=8, phrase_time_limit=8)

            text = r.recognize_google(audio, language="en-US")
            print("[VOICE DEBUG] Heard:", text)
            self.callback(text.strip())

        except sr.UnknownValueError:
            print("[VOICE DEBUG] Could not understand audio")
            self.callback(None)

        except sr.RequestError as e:
            print("[VOICE DEBUG] Request error:", e)
            self.callback(None)

        except Exception as e:
            print("[VOICE DEBUG] Error:", e)
            self.callback(None)

        finally:
            self.listening = False
