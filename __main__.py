from gtts import gTTS
import gui
import time
from tkinter import filedialog
import re

def TTS():
    # Obtain text from GUI
    text = gui.top.Text1.get("1.0","end-1c")
    if (text.replace("\n", "").replace(" ", "") == ""):
        print("Text is empty, nothing to translate")
        return
    # Obtain lang from GUI
    lang = gui.top.TCombobox1.get()
    if (lang == ""):
        print("Warn: Empty language, setting to 'en'") 
        lang = "en"
    # Obtain TTS audio from Google
    print("Synthesizing voices...")
    out = gTTS(text, lang=lang)
    while(out == ""): time.sleep(0.5)
    # Ask the user where to save the file
    print("Saving the output...")
    filename = filedialog.asksaveasfilename(title="Saving audio...",filetypes=[("MPEG Layer 3 Audio file",".mp3")])
    if (filename == ""):
        print("No filename specified, cancelled.")
        return
    if not (filename.endswith(".mp3")):
        filename += ".mp3"
    # Save the file
    print("Saving to " + filename)
    out.save(filename)
    print("Done!")
    return

def StatsCounter(event):
    # Figure out the word count
    text = gui.top.Text1.get("1.0","end-1c")
    words = re.split(" |\t|\n|\.",text)
    while("" in words): words.remove("")
    count = len(words)
    # Add word count to future label text
    label = "Word count: " + str(count)
    # Figure out the rough estimate for recording length in minutes
    lang = gui.top.TCombobox1.get()
    if (lang in ["sk", "en"]):
        if (lang == "en"): speed = count/120
        elif (lang == "sk"): speed = count/110
        label += " (~ " + str("%.2f" % speed) + " minutes in " + lang + " lang)"
    # Update the GUI label
    gui.top.Label1.configure(text=label)
    return

# Controller
gui.init()
gui.top.Button1.configure(command=TTS)
gui.top.Text1.bind("<KeyRelease>", StatsCounter)
gui.start()