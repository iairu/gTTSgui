from gtts import gTTS
import gui
import time
from tkinter import filedialog, messagebox
import re
import threading

def update_status(message, color="#2c3e50"):
    """Update the status bar with a message"""
    gui.top.status_bar.configure(text=message, bg=color)
    gui.root.update()

def get_language_code():
    """Extract language code from the combobox selection"""
    selection = gui.top.TCombobox1.get()
    # Extract the language code (e.g., "en - English" -> "en")
    if " - " in selection:
        return selection.split(" - ")[0]
    return selection if selection else "en"

def TTS(event=None):
    """Convert text to speech and save as MP3"""
    # Obtain text from GUI
    text = gui.top.Text1.get("1.0", "end-1c")
    if text.replace("\n", "").replace(" ", "") == "":
        update_status("⚠️ Error: Text is empty. Please enter some text.", "#e74c3c")
        messagebox.showwarning("Empty Text", "Please enter some text to convert to speech.")
        return

    # Obtain lang from GUI
    lang = get_language_code()

    # Update status
    update_status("🔄 Synthesizing speech...", "#3498db")

    def synthesize():
        try:
            # Obtain TTS audio from Google
            print("Synthesizing voices...")
            out = gTTS(text, lang=lang)
            while out == "":
                time.sleep(0.5)

            # Ask the user where to save the file
            print("Saving the output...")
            update_status("💾 Choose save location...", "#3498db")

            filename = filedialog.asksaveasfilename(
                title="Save audio file",
                defaultextension=".mp3",
                filetypes=[("MP3 Audio File", "*.mp3"), ("All Files", "*.*")]
            )

            if filename == "":
                print("No filename specified, cancelled.")
                update_status("Ready | Tip: Use Ctrl+S to save", "#2c3e50")
                return

            if not filename.endswith(".mp3"):
                filename += ".mp3"

            # Save the file
            print("Saving to " + filename)
            update_status("💾 Saving file...", "#3498db")
            out.save(filename)
            print("Done!")
            update_status("✅ Successfully saved to " + filename, "#27ae60")
            messagebox.showinfo("Success", f"Audio file saved successfully!\n{filename}")

            # Reset status after 5 seconds
            gui.root.after(5000, lambda: update_status("Ready | Tip: Use Ctrl+S to save", "#2c3e50"))

        except Exception as e:
            print(f"Error: {e}")
            update_status(f"❌ Error: {str(e)}", "#e74c3c")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # Run synthesis in a thread to keep UI responsive
    thread = threading.Thread(target=synthesize)
    thread.daemon = True
    thread.start()

def StatsCounter(event):
    """Update word count and estimated duration"""
    # Figure out the word count
    text = gui.top.Text1.get("1.0", "end-1c")
    words = re.split(r" |\t|\n|\.", text)
    while "" in words:
        words.remove("")
    count = len(words)

    # Add word count to future label text
    label = f"📊 Word count: {count}"

    # Figure out the rough estimate for recording length in minutes
    lang = get_language_code()
    if lang in ["sk", "en"]:
        if lang == "en":
            speed = count / 120
        elif lang == "sk":
            speed = count / 110
        label += f" (≈ {speed:.2f} min)"

    # Update the GUI label
    gui.top.Label1.configure(text=label)
    return

def on_focus_in(event):
    """Handle focus in event for text area"""
    gui.top.Text1.configure(highlightcolor="#2196F3", highlightbackground="#2196F3")

def on_focus_out(event):
    """Handle focus out event for text area"""
    gui.top.Text1.configure(highlightbackground="#e0e0e0")

# Controller
gui.init()

# Configure button command
gui.top.Button1.configure(command=TTS)

# Bind keyboard events
gui.top.Text1.bind("<KeyRelease>", StatsCounter)
gui.top.Text1.bind("<FocusIn>", on_focus_in)
gui.top.Text1.bind("<FocusOut>", on_focus_out)

# Add keyboard shortcuts
gui.root.bind("<Control-s>", TTS)  # Ctrl+S to save
gui.root.bind("<Control-S>", TTS)  # Ctrl+Shift+S also works

# Set focus to text area on startup
gui.top.Text1.focus_set()

# Start the application
gui.start()