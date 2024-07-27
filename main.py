import customtkinter as ctk
import speech_recognition as sr
import threading

class SpeechToTextApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Speech to Text App")
        self.geometry("600x400")

        self.text_box = ctk.CTkTextbox(self, width=500, height=300, wrap='word')
        self.text_box.pack(padx=20, pady=20)

        self.record_button = ctk.CTkButton(self, text="Start Recording", command=self.start_recording)
        self.record_button.pack(pady=10)
        
        self.recognizer = sr.Recognizer()

    def start_recording(self):
        self.record_button.configure(state=ctk.DISABLED)
        threading.Thread(target=self.record_speech).start()

    def record_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.update_text_box("Listening...")
            audio = self.recognizer.listen(source)

            try:
                self.update_text_box("Recognizing speech...")
                text = self.recognizer.recognize_google(audio)
                self.update_text_box(f"Recognized text: {text}")
            except sr.UnknownValueError:
                self.update_text_box("Could not understand the audio.")
            except sr.RequestError as e:
                self.update_text_box(f"Could not request results; {e}")

        self.record_button.configure(state=ctk.NORMAL)

    def update_text_box(self, text):
        self.text_box.insert('end', text + '\n')
        self.text_box.see('end')

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
    
    app = SpeechToTextApp()
    app.mainloop()
