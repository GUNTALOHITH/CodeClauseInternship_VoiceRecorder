import sounddevice as sd
import numpy as np
import wave
import tkinter as tk
from tkinter import ttk

class VoiceRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder")

        self.recording = False
        self.filename = "recorded_audio.wav"

        self.create_widgets()

    def create_widgets(self):
        self.start_button = ttk.Button(self.master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.save_button = ttk.Button(self.master, text="Save Recording", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack(pady=10)

    def start_recording(self):
        self.recording = True
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL
        self.save_button["state"] = tk.DISABLED

        self.sample_rate = 44100
        self.duration = 10  # Adjust the duration as needed

        self.recording_data = []

        def callback(indata, frames, time, status):
            if status:
                print(f"Error in recording: {status}")
            self.recording_data.append(indata.copy())

        with sd.InputStream(callback=callback, channels=1, samplerate=self.sample_rate):
            self.master.after(int(self.duration * 1000), self.stop_recording)
            self.master.mainloop()

    def stop_recording(self):
        self.recording = False
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED
        self.save_button["state"] = tk.NORMAL

    def save_recording(self):
        with wave.open(self.filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(np.concatenate(self.recording_data))

        print(f"Recording saved as {self.filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
