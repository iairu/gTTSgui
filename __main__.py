from gtts import gTTS
import gui
import time
from tkinter import filedialog, messagebox
import re
import threading
import os

# Sample texts for different languages
SAMPLE_TEXTS = {
    "en": "Welcome to the Text to Speech Converter! This application allows you to convert any written text into natural-sounding speech in multiple languages. Simply type or paste your text, select your desired language, and click save to generate an MP3 audio file.",
    "es": "¡Bienvenido al Convertidor de Texto a Voz! Esta aplicación te permite convertir cualquier texto escrito en un habla natural en múltiples idiomas.",
    "fr": "Bienvenue dans le convertisseur de texte en parole ! Cette application vous permet de convertir n'importe quel texte écrit en parole naturelle dans plusieurs langues.",
    "de": "Willkommen beim Text-zu-Sprache-Konverter! Diese Anwendung ermöglicht es Ihnen, jeden geschriebenen Text in natürlich klingende Sprache in mehreren Sprachen umzuwandeln.",
    "ja": "テキスト読み上げコンバータへようこそ！このアプリケーションを使用すると、書かれたテキストを複数の言語で自然な音声に変換できます。",
    "ko": "텍스트 음성 변환기에 오신 것을 환영합니다! 이 애플리케이션을 사용하면 작성된 텍스트를 여러 언어로 자연스러운 음성으로 변환할 수 있습니다.",
}

def update_status(message, color=None):
    """Update the status bar with a message"""
    theme = gui.top.theme_manager.get_theme()
    if color is None:
        color = theme['status_bg']
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
        theme = gui.top.theme_manager.get_theme()
        update_status("⚠️ Error: Text is empty. Please enter some text.", theme['error'])
        messagebox.showwarning("Empty Text", "Please enter some text to convert to speech.")
        return

    # Obtain lang from GUI
    lang = get_language_code()

    # Show progress bar
    gui.top.show_progress("Synthesizing speech...")
    theme = gui.top.theme_manager.get_theme()
    update_status("🔄 Synthesizing speech...", theme['info'])

    def synthesize():
        try:
            # Obtain TTS audio from Google
            print("Synthesizing voices...")
            out = gTTS(text, lang=lang)
            while out == "":
                time.sleep(0.5)

            # Ask the user where to save the file
            print("Saving the output...")
            gui.top.hide_progress()
            update_status("💾 Choose save location...", theme['info'])

            filename = filedialog.asksaveasfilename(
                title="Save audio file",
                defaultextension=".mp3",
                initialfile="speech.mp3",
                filetypes=[("MP3 Audio File", "*.mp3"), ("All Files", "*.*")]
            )

            if filename == "":
                print("No filename specified, cancelled.")
                update_status("Ready | Tip: Press F1 for keyboard shortcuts")
                return

            if not filename.endswith(".mp3"):
                filename += ".mp3"

            # Save the file
            print("Saving to " + filename)
            gui.top.show_progress("Saving file...")
            update_status("💾 Saving file...", theme['info'])
            out.save(filename)
            gui.top.hide_progress()
            print("Done!")
            update_status("✅ Successfully saved: " + os.path.basename(filename), theme['success'])
            messagebox.showinfo("Success", f"Audio file saved successfully!\n\n{filename}")

            # Reset status after 5 seconds
            gui.root.after(5000, lambda: update_status("Ready | Tip: Press F1 for keyboard shortcuts"))

        except Exception as e:
            gui.top.hide_progress()
            print(f"Error: {e}")
            update_status(f"❌ Error: {str(e)}", theme['error'])
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # Run synthesis in a thread to keep UI responsive
    thread = threading.Thread(target=synthesize)
    thread.daemon = True
    thread.start()

def StatsCounter(event):
    """Update word and character count"""
    text = gui.top.Text1.get("1.0", "end-1c")

    # Word count
    words = re.split(r" |\t|\n|\.", text)
    while "" in words:
        words.remove("")
    word_count = len(words)

    # Character count
    char_count = len(text.replace("\n", "").replace(" ", ""))

    # Build label text
    label = f"📊 Words: {word_count} | Characters: {char_count}"

    # Figure out the rough estimate for recording length in minutes
    lang = get_language_code()
    if lang in ["sk", "en"] and word_count > 0:
        if lang == "en":
            speed = word_count / 120
        elif lang == "sk":
            speed = word_count / 110
        label += f" | ≈ {speed:.1f} min"

    # Update the GUI label
    gui.top.Label1.configure(text=label)
    return

def clear_text(event=None):
    """Clear all text from the text area"""
    if gui.top.Text1.get("1.0", "end-1c").strip():
        if messagebox.askyesno("Clear Text", "Are you sure you want to clear all text?"):
            gui.top.Text1.delete("1.0", "end")
            update_status("Text cleared")
            return "break"  # Prevent default behavior

def import_text(event=None):
    """Import text from a file"""
    filename = filedialog.askopenfilename(
        title="Import text file",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if filename:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            gui.top.Text1.delete("1.0", "end")
            gui.top.Text1.insert("1.0", content)
            update_status(f"✅ Imported: {os.path.basename(filename)}")
        except Exception as e:
            theme = gui.top.theme_manager.get_theme()
            messagebox.showerror("Import Error", f"Could not import file:\n{str(e)}")
            update_status(f"❌ Import failed", theme['error'])
    return "break"

def load_sample_text(event=None):
    """Load sample text in the selected language"""
    lang = get_language_code()
    sample = SAMPLE_TEXTS.get(lang, SAMPLE_TEXTS["en"])
    gui.top.Text1.delete("1.0", "end")
    gui.top.Text1.insert("1.0", sample)
    update_status(f"Sample text loaded for {lang}")
    return "break"

def toggle_theme(event=None):
    """Toggle between light and dark mode"""
    message = gui.top.toggle_theme()
    update_status(f"✨ {message}")
    return "break"

def increase_font(event=None):
    """Increase font size"""
    message = gui.top.change_font_size(2)
    update_status(message)
    return "break"

def decrease_font(event=None):
    """Decrease font size"""
    message = gui.top.change_font_size(-2)
    update_status(message)
    return "break"

def reset_font(event=None):
    """Reset font size to default"""
    gui.top.current_font_size = 11
    message = gui.top.change_font_size(0)
    update_status(message)
    return "break"

def show_shortcuts(event=None):
    """Show keyboard shortcuts help dialog"""
    shortcuts = """
KEYBOARD SHORTCUTS

File Operations:
  Ctrl+O         Import text from file
  Ctrl+L         Load sample text
  Ctrl+S         Save as MP3
  Ctrl+Q         Exit application

Editing:
  Ctrl+Z         Undo
  Ctrl+Y         Redo
  Ctrl+X         Cut
  Ctrl+C         Copy
  Ctrl+V         Paste
  Ctrl+A         Select all
  Ctrl+D         Clear text

View:
  Ctrl+T         Toggle dark/light mode
  Ctrl++         Increase font size
  Ctrl+-         Decrease font size
  Ctrl+0         Reset font size

Help:
  F1             Show this help
"""
    messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    return "break"

def show_about(event=None):
    """Show about dialog"""
    about_text = """
gTTS GUI - Text to Speech Converter
Version 2.0

A modern, accessible text-to-speech application
powered by Google Text-to-Speech (gTTS).

Features:
• 25+ languages supported
• Dark/Light mode themes
• Adjustable font sizes
• Keyboard shortcuts
• Full accessibility support

Made with ❤️ using Python and Tkinter
"""
    messagebox.showinfo("About", about_text)
    return "break"

def exit_app(event=None):
    """Exit the application"""
    text = gui.top.Text1.get("1.0", "end-1c")
    if text.strip():
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            gui.root.quit()
    else:
        gui.root.quit()
    return "break"

def undo_text(event=None):
    """Undo last text change"""
    try:
        gui.top.Text1.edit_undo()
    except:
        pass
    return "break"

def redo_text(event=None):
    """Redo last undone change"""
    try:
        gui.top.Text1.edit_redo()
    except:
        pass
    return "break"

def select_all(event=None):
    """Select all text"""
    gui.top.Text1.tag_add("sel", "1.0", "end")
    return "break"

# Controller
gui.init()

# Configure button commands
gui.top.Button1.configure(command=TTS)
gui.top.clear_button.configure(command=clear_text)
gui.top.import_button.configure(command=import_text)
gui.top.sample_button.configure(command=load_sample_text)

# Configure menu commands
# File menu
gui.top.file_menu.entryconfig("Import Text File...", command=import_text)
gui.top.file_menu.entryconfig("Load Sample Text", command=load_sample_text)
gui.top.file_menu.entryconfig("Save as MP3...", command=TTS)
gui.top.file_menu.entryconfig("Exit", command=exit_app)

# Edit menu
gui.top.edit_menu.entryconfig("Undo", command=undo_text)
gui.top.edit_menu.entryconfig("Redo", command=redo_text)
gui.top.edit_menu.entryconfig("Select All", command=select_all)
gui.top.edit_menu.entryconfig("Clear Text", command=clear_text)

# View menu
gui.top.view_menu.entryconfig("Toggle Dark Mode", command=toggle_theme)
gui.top.view_menu.entryconfig("Increase Font Size", command=increase_font)
gui.top.view_menu.entryconfig("Decrease Font Size", command=decrease_font)
gui.top.view_menu.entryconfig("Reset Font Size", command=reset_font)

# Help menu
gui.top.help_menu.entryconfig("Keyboard Shortcuts", command=show_shortcuts)
gui.top.help_menu.entryconfig("About", command=show_about)

# Bind keyboard events
gui.top.Text1.bind("<KeyRelease>", StatsCounter)

# File operations shortcuts
gui.root.bind("<Control-o>", import_text)
gui.root.bind("<Control-O>", import_text)
gui.root.bind("<Control-l>", load_sample_text)
gui.root.bind("<Control-L>", load_sample_text)
gui.root.bind("<Control-s>", TTS)
gui.root.bind("<Control-S>", TTS)
gui.root.bind("<Control-q>", exit_app)
gui.root.bind("<Control-Q>", exit_app)

# Edit shortcuts
gui.root.bind("<Control-z>", undo_text)
gui.root.bind("<Control-Z>", undo_text)
gui.root.bind("<Control-y>", redo_text)
gui.root.bind("<Control-Y>", redo_text)
gui.root.bind("<Control-a>", select_all)
gui.root.bind("<Control-A>", select_all)
gui.root.bind("<Control-d>", clear_text)
gui.root.bind("<Control-D>", clear_text)

# View shortcuts
gui.root.bind("<Control-t>", toggle_theme)
gui.root.bind("<Control-T>", toggle_theme)
gui.root.bind("<Control-plus>", increase_font)
gui.root.bind("<Control-equal>", increase_font)  # For keyboards without numpad
gui.root.bind("<Control-minus>", decrease_font)
gui.root.bind("<Control-0>", reset_font)

# Help shortcuts
gui.root.bind("<F1>", show_shortcuts)

# Set focus to text area on startup
gui.top.Text1.focus_set()

# Trigger initial stats update
StatsCounter(None)

# Start the application
gui.start()