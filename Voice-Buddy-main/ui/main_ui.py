import customtkinter as ctk
from core.assistant import Assistant

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VoiceBuddy")
        self.geometry("900x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.label = ctk.CTkLabel(
            self,
            text="VoiceBuddy Assistant",
            font=("Segoe UI", 24, "bold")
        )
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Type your command here...",
            width=600
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.on_run())

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)

        ctk.CTkButton(
            btn_frame, text="Run", width=120, command=self.on_run
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame, text="🎙 Mic", width=120,
            command=self.on_mic, fg_color="green"
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            btn_frame, text="Clear", width=120, command=self.clear_log
        ).grid(row=0, column=2, padx=10)

        self.log_box = ctk.CTkTextbox(self, width=800, height=350)
        self.log_box.pack(pady=10)

        self.status = ctk.CTkLabel(self, text="Ready")
        self.status.pack(pady=5)

        self.assistant = Assistant(self)

        self.after(500, self.startup_greeting)

    def startup_greeting(self):
        self.log("Hello, I am VoiceBuddy.", "assistant")
        self.assistant.speaker.say("Hello, I am VoiceBuddy.")

    def on_run(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.log(text, "user")
        self.entry.delete(0, "end")
        self.assistant.handle(text)

    def on_mic(self):
        self.assistant.listen()

    def log(self, text, role="assistant"):
        prefix = "You: " if role == "user" else "Assistant: "
        self.log_box.insert("end", prefix + text + "\n")
        self.log_box.see("end")

    def clear_log(self):
        self.log_box.delete("1.0", "end")

    def set_status(self, text):
        self.status.configure(text=text)
