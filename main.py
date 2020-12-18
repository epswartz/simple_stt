from PIL import ImageTk, Image
from pydub import AudioSegment
from tkinter import filedialog, INSERT, DISABLED, NORMAL, WORD
from datetime import datetime
import io
import os
import speech_recognition as sr
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk

TEXT_WIDTH = 100


# Set up SR
rzr = sr.Recognizer()

def transcribe_audio_file(filename):

    text_area.insert(INSERT, f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {filename}\n")
    text_area.insert(INSERT, "-"*TEXT_WIDTH + "\n")
    # SR only takes wav, so convert it in memory.
    file_type = os.path.splitext(filename)[1][1:]
    pd_segment = AudioSegment.from_file(filename, file_type)
    wav_filelike = io.BytesIO()
    pd_segment.export(wav_filelike, "wav")
    wav_filelike.seek(0) # we just wrote so have to go back to the start of it

    # Read it into SR, and recognize the speech.
    input_audio_file = sr.AudioFile(wav_filelike)
    with input_audio_file as source:
        audio = rzr.record(source)

    return rzr.recognize_google(audio)

def transcribe_btn_clicked():
    text_area.config(state=NORMAL)
    root.filename = filedialog.askopenfilename(initialdir = root.filedialog_initialdir, title = "Select Audio File")
    if root.filename == '': # They exited without picking a file
        return
    root.filedialog_initialdir = os.path.dirname(root.filename) # For next time
    text = "An Error Occurred."
    try:
        text = transcribe_audio_file(root.filename)
    except:
        pass
    text_area.insert(INSERT, text + "\n" + "-"*TEXT_WIDTH+"\n"*3)

# Build UI
root = tk.Tk()
root.filedialog_initialdir = "~/Desktop"
root.title("Speech to Text")
root.minsize(600,700)

#transcribe_btn_img = ImageTk.PhotoImage(Image.open("./static/transcribe_btn.png"))
#transcribe_btn = tk.Button(root, command=transcribe_btn_clicked, text="Transcribe Audio", image=transcribe_btn_img)
transcribe_btn = ttk.Button(root, command=transcribe_btn_clicked, text="Transcribe Audio")
transcribe_btn.pack(anchor='center')

text_area = ScrolledText(root, width=TEXT_WIDTH, wrap=WORD, height=40)
text_area.pack(anchor='center')
text_area.config(state=DISABLED)
root.mainloop()
