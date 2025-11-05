import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font as tkfont

root = None
top = None

def init():
    # '''Starting point when module is the main routine.'''
    global root, top
    root = tk.Tk()
    top = MainWindow(root)

def start():
    root.mainloop()

# Tooltip class for accessibility
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text,
                        background="#2c3e50", foreground="white",
                        relief="solid", borderwidth=1,
                        font=("Segoe UI", 9), padx=8, pady=4)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class MainWindow:
    def __init__(self, top=None):
        # Modern color scheme for better accessibility
        _bgcolor = '#f5f5f5'  # Light gray background
        _fgcolor = '#212121'  # Dark gray text for high contrast
        _primary = '#2196F3'  # Modern blue
        _accent = '#00BCD4'   # Teal accent
        _success = '#4CAF50'  # Green for success
        _card_bg = '#ffffff'  # White for cards
        _border = '#e0e0e0'   # Light border

        # Configure ttk styles
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        # Configure modern combobox style
        self.style.configure('Modern.TCombobox',
                           fieldbackground='white',
                           background=_primary,
                           foreground=_fgcolor,
                           borderwidth=1,
                           relief='flat')

        # Window configuration
        top.geometry("800x600+400+100")
        top.title("gTTS GUI - Text to Speech Converter")
        top.configure(background=_bgcolor)
        top.minsize(600, 450)

        # Configure grid weights for responsiveness
        top.grid_rowconfigure(2, weight=1)
        top.grid_columnconfigure(0, weight=1)

        # Header frame with better padding
        header_frame = tk.Frame(top, bg=_bgcolor, pady=15, padx=20)
        header_frame.grid(row=0, column=0, sticky="ew")

        # Title label with modern font
        title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        title_label = tk.Label(header_frame,
                              text="Text to Speech Converter",
                              font=title_font,
                              bg=_bgcolor,
                              fg=_fgcolor)
        title_label.pack(anchor="w")

        # Subtitle with instructions
        subtitle_font = tkfont.Font(family="Segoe UI", size=9)
        subtitle_label = tk.Label(header_frame,
                                 text="Enter your text below and convert it to speech in your preferred language",
                                 font=subtitle_font,
                                 bg=_bgcolor,
                                 fg="#757575")
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Control panel frame
        control_frame = tk.Frame(top, bg=_bgcolor, padx=20, pady=5)
        control_frame.grid(row=1, column=0, sticky="ew")

        # Language selector with label
        lang_frame = tk.Frame(control_frame, bg=_bgcolor)
        lang_frame.pack(side="left", padx=(0, 15))

        lang_label_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        lang_label = tk.Label(lang_frame,
                             text="Language:",
                             font=lang_label_font,
                             bg=_bgcolor,
                             fg=_fgcolor)
        lang_label.pack(side="left", padx=(0, 8))

        self.TCombobox1 = ttk.Combobox(lang_frame, style='Modern.TCombobox')
        self.value_list = [
            "sk - Slovak",
            "cz - Czech",
            "en - English",
            "pl - Polish",
            "ja - Japanese",
            "ko - Korean"
        ]
        self.TCombobox1.configure(values=self.value_list)
        self.TCombobox1.current(2)  # Default to English
        self.TCombobox1.configure(width=18, font=("Segoe UI", 10))
        self.TCombobox1.configure(state="readonly")  # Better accessibility
        self.TCombobox1.pack(side="left")

        # Add tooltip for language selector
        ToolTip(self.TCombobox1, "Select the language for text-to-speech conversion")

        # Word count label with modern styling
        self.Label1 = tk.Label(control_frame,
                              text="Word count: 0",
                              font=("Segoe UI", 10),
                              bg=_bgcolor,
                              fg="#757575",
                              anchor="w")
        self.Label1.pack(side="left", padx=(0, 15))

        # Save button with modern styling
        button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.Button1 = tk.Button(control_frame,
                                text="💾 Save as MP3",
                                font=button_font,
                                bg=_primary,
                                fg="white",
                                activebackground="#1976D2",
                                activeforeground="white",
                                relief="flat",
                                padx=20,
                                pady=10,
                                cursor="hand2",
                                borderwidth=0,
                                highlightthickness=0)
        self.Button1.pack(side="right")

        # Add button hover effects
        def on_enter(e):
            self.Button1.configure(bg="#1976D2")
        def on_leave(e):
            self.Button1.configure(bg=_primary)
        self.Button1.bind("<Enter>", on_enter)
        self.Button1.bind("<Leave>", on_leave)

        # Add tooltip for save button
        ToolTip(self.Button1, "Save the text as an MP3 audio file (Ctrl+S)")

        # Text input frame with card-like appearance
        text_frame = tk.Frame(top, bg=_bgcolor, padx=20, pady=(5, 10))
        text_frame.grid(row=2, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Text area label
        text_label = tk.Label(text_frame,
                             text="Enter Text:",
                             font=lang_label_font,
                             bg=_bgcolor,
                             fg=_fgcolor,
                             anchor="w")
        text_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Text widget with modern styling and scrollbar
        text_container = tk.Frame(text_frame, bg=_card_bg, relief="solid", borderwidth=1)
        text_container.grid(row=1, column=0, sticky="nsew")
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        # Scrollbar for text area
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Text widget
        text_font = tkfont.Font(family="Segoe UI", size=11)
        self.Text1 = tk.Text(text_container,
                            font=text_font,
                            bg=_card_bg,
                            fg=_fgcolor,
                            insertbackground=_primary,
                            selectbackground=_primary,
                            selectforeground="white",
                            relief="flat",
                            padx=15,
                            pady=15,
                            wrap="word",
                            yscrollcommand=scrollbar.set,
                            highlightthickness=2,
                            highlightcolor=_primary,
                            highlightbackground=_border)
        self.Text1.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.Text1.yview)

        # Status bar at bottom
        self.status_bar = tk.Label(top,
                                   text="Ready | Tip: Use Ctrl+S to save",
                                   font=("Segoe UI", 9),
                                   bg="#2c3e50",
                                   fg="white",
                                   anchor="w",
                                   padx=20,
                                   pady=8)
        self.status_bar.grid(row=3, column=0, sticky="ew")