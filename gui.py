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

# Theme manager for dark/light mode
class ThemeManager:
    def __init__(self):
        self.is_dark = False
        self.themes = {
            'light': {
                'bg': '#f5f5f5',
                'fg': '#212121',
                'card_bg': '#ffffff',
                'border': '#e0e0e0',
                'primary': '#2196F3',
                'accent': '#00BCD4',
                'success': '#4CAF50',
                'error': '#e74c3c',
                'warning': '#f39c12',
                'info': '#3498db',
                'secondary_fg': '#757575',
                'status_bg': '#2c3e50',
                'status_fg': 'white',
                'button_hover': '#1976D2'
            },
            'dark': {
                'bg': '#1e1e1e',
                'fg': '#e0e0e0',
                'card_bg': '#2d2d2d',
                'border': '#404040',
                'primary': '#64B5F6',
                'accent': '#4DD0E1',
                'success': '#81C784',
                'error': '#ef5350',
                'warning': '#FFB74D',
                'info': '#64B5F6',
                'secondary_fg': '#b0b0b0',
                'status_bg': '#1a1a1a',
                'status_fg': '#e0e0e0',
                'button_hover': '#42A5F5'
            }
        }

    def get_theme(self):
        return self.themes['dark' if self.is_dark else 'light']

    def toggle(self):
        self.is_dark = not self.is_dark
        return self.get_theme()

class MainWindow:
    def __init__(self, top=None):
        self.root = top
        self.theme_manager = ThemeManager()
        self.current_font_size = 11

        # Build the UI
        self.setup_window()
        self.create_menu_bar()
        self.create_widgets()
        self.apply_theme()

    def setup_window(self):
        """Configure main window properties"""
        self.root.geometry("900x700+300+50")
        self.root.title("gTTS GUI - Text to Speech Converter")
        self.root.minsize(700, 500)

        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_menu_bar(self):
        """Create menu bar with File, Edit, View, Help menus"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Import Text File...", accelerator="Ctrl+O")
        self.file_menu.add_command(label="Load Sample Text", accelerator="Ctrl+L")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save as MP3...", accelerator="Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator="Ctrl+Q")

        # Edit menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A")
        self.edit_menu.add_command(label="Clear Text", accelerator="Ctrl+D")

        # View menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Dark Mode", accelerator="Ctrl+T")
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Increase Font Size", accelerator="Ctrl++")
        self.view_menu.add_command(label="Decrease Font Size", accelerator="Ctrl+-")
        self.view_menu.add_command(label="Reset Font Size", accelerator="Ctrl+0")

        # Help menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Keyboard Shortcuts", accelerator="F1")
        self.help_menu.add_command(label="About")

    def create_widgets(self):
        """Create all UI widgets"""
        theme = self.theme_manager.get_theme()

        # Header frame with better padding
        self.header_frame = tk.Frame(self.root, pady=15, padx=20)
        self.header_frame.grid(row=0, column=0, sticky="ew")

        # Title label with modern font
        title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        self.title_label = tk.Label(self.header_frame,
                              text="🎙️ Text to Speech Converter",
                              font=title_font)
        self.title_label.pack(anchor="w")

        # Subtitle with instructions
        subtitle_font = tkfont.Font(family="Segoe UI", size=9)
        self.subtitle_label = tk.Label(self.header_frame,
                                 text="Enter your text below and convert it to speech in your preferred language",
                                 font=subtitle_font)
        self.subtitle_label.pack(anchor="w", pady=(2, 0))

        # Main content frame
        self.content_frame = tk.Frame(self.root, padx=20)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Control panel frame
        self.control_frame = tk.Frame(self.content_frame, pady=5)
        self.control_frame.grid(row=0, column=0, sticky="ew")

        # Language selector with label
        lang_frame = tk.Frame(self.control_frame)
        lang_frame.pack(side="left", padx=(0, 15))

        lang_label_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.lang_label = tk.Label(lang_frame,
                             text="Language:",
                             font=lang_label_font)
        self.lang_label.pack(side="left", padx=(0, 8))

        # Configure modern combobox style
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')

        self.TCombobox1 = ttk.Combobox(lang_frame, style='Modern.TCombobox')
        self.value_list = [
            "en - English",
            "es - Spanish",
            "fr - French",
            "de - German",
            "it - Italian",
            "pt - Portuguese",
            "ru - Russian",
            "ja - Japanese",
            "ko - Korean",
            "zh-CN - Chinese (Simplified)",
            "ar - Arabic",
            "hi - Hindi",
            "nl - Dutch",
            "pl - Polish",
            "sv - Swedish",
            "da - Danish",
            "fi - Finnish",
            "no - Norwegian",
            "cs - Czech",
            "sk - Slovak",
            "tr - Turkish",
            "el - Greek",
            "he - Hebrew",
            "th - Thai",
            "vi - Vietnamese"
        ]
        self.TCombobox1.configure(values=self.value_list)
        self.TCombobox1.current(0)  # Default to English
        self.TCombobox1.configure(width=22, font=("Segoe UI", 10))
        self.TCombobox1.configure(state="readonly")  # Better accessibility
        self.TCombobox1.pack(side="left")

        # Add tooltip for language selector
        ToolTip(self.TCombobox1, "Select the language for text-to-speech conversion")

        # Stats label (word & character count)
        self.Label1 = tk.Label(self.control_frame,
                              text="📊 Words: 0 | Characters: 0",
                              font=("Segoe UI", 10),
                              anchor="w")
        self.Label1.pack(side="left", padx=(0, 15))

        # Action buttons frame
        self.button_frame = tk.Frame(self.control_frame)
        self.button_frame.pack(side="right")

        # Clear button
        button_font = tkfont.Font(family="Segoe UI", size=9, weight="bold")
        self.clear_button = tk.Button(self.button_frame,
                                text="🗑️ Clear",
                                font=button_font,
                                relief="flat",
                                padx=15,
                                pady=8,
                                cursor="hand2",
                                borderwidth=0)
        self.clear_button.pack(side="left", padx=(0, 10))
        ToolTip(self.clear_button, "Clear all text (Ctrl+D)")

        # Save button with modern styling
        save_button_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.Button1 = tk.Button(self.button_frame,
                                text="💾 Save as MP3",
                                font=save_button_font,
                                relief="flat",
                                padx=20,
                                pady=10,
                                cursor="hand2",
                                borderwidth=0)
        self.Button1.pack(side="left")
        ToolTip(self.Button1, "Save the text as an MP3 audio file (Ctrl+S)")

        # Text input frame with card-like appearance
        text_frame = tk.Frame(self.content_frame, pady=(10, 5))
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(1, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Text area header with label and controls
        text_header = tk.Frame(text_frame)
        text_header.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.text_label = tk.Label(text_header,
                             text="Enter Text:",
                             font=lang_label_font,
                             anchor="w")
        self.text_label.pack(side="left")

        # Quick action buttons
        quick_actions = tk.Frame(text_header)
        quick_actions.pack(side="right")

        small_button_font = tkfont.Font(family="Segoe UI", size=8)
        self.import_button = tk.Button(quick_actions,
                                text="📁 Import",
                                font=small_button_font,
                                relief="flat",
                                padx=10,
                                pady=4,
                                cursor="hand2")
        self.import_button.pack(side="left", padx=(0, 5))
        ToolTip(self.import_button, "Import text from file (Ctrl+O)")

        self.sample_button = tk.Button(quick_actions,
                                text="📝 Sample",
                                font=small_button_font,
                                relief="flat",
                                padx=10,
                                pady=4,
                                cursor="hand2")
        self.sample_button.pack(side="left")
        ToolTip(self.sample_button, "Load sample text (Ctrl+L)")

        # Text widget with modern styling and scrollbar
        text_container = tk.Frame(text_frame, relief="solid", borderwidth=1)
        text_container.grid(row=1, column=0, sticky="nsew")
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        # Scrollbar for text area
        scrollbar = tk.Scrollbar(text_container)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Text widget
        text_font = tkfont.Font(family="Segoe UI", size=self.current_font_size)
        self.Text1 = tk.Text(text_container,
                            font=text_font,
                            relief="flat",
                            padx=15,
                            pady=15,
                            wrap="word",
                            yscrollcommand=scrollbar.set,
                            undo=True,  # Enable undo/redo
                            maxundo=-1,
                            highlightthickness=2)
        self.Text1.grid(row=0, column=0, sticky="nsew")
        scrollbar.config(command=self.Text1.yview)

        # Progress bar (initially hidden)
        self.progress_frame = tk.Frame(self.content_frame)
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))

        self.progress_label = tk.Label(self.progress_frame,
                                      text="Processing...",
                                      font=("Segoe UI", 9))
        self.progress_label.pack(side="left", padx=(0, 10))

        self.progress = ttk.Progressbar(self.progress_frame,
                                       mode='indeterminate',
                                       length=300)
        self.progress.pack(side="left", fill="x", expand=True)

        # Hide progress by default
        self.progress_frame.grid_remove()

        # Status bar at bottom
        self.status_bar = tk.Label(self.root,
                                   text="Ready | Tip: Press F1 for keyboard shortcuts",
                                   font=("Segoe UI", 9),
                                   anchor="w",
                                   padx=20,
                                   pady=8)
        self.status_bar.grid(row=2, column=0, sticky="ew")

    def apply_theme(self):
        """Apply current theme to all widgets"""
        theme = self.theme_manager.get_theme()

        # Update root and frames
        self.root.configure(background=theme['bg'])
        self.header_frame.configure(background=theme['bg'])
        self.content_frame.configure(background=theme['bg'])
        self.control_frame.configure(background=theme['bg'])

        # Update labels
        self.title_label.configure(background=theme['bg'], foreground=theme['fg'])
        self.subtitle_label.configure(background=theme['bg'], foreground=theme['secondary_fg'])
        self.lang_label.configure(background=theme['bg'], foreground=theme['fg'])
        self.Label1.configure(background=theme['bg'], foreground=theme['secondary_fg'])
        self.text_label.configure(background=theme['bg'], foreground=theme['fg'])

        # Update text widget
        self.Text1.configure(
            background=theme['card_bg'],
            foreground=theme['fg'],
            insertbackground=theme['primary'],
            selectbackground=theme['primary'],
            selectforeground='white',
            highlightcolor=theme['primary'],
            highlightbackground=theme['border']
        )

        # Update buttons
        self.Button1.configure(
            background=theme['primary'],
            foreground='white',
            activebackground=theme['button_hover'],
            activeforeground='white'
        )

        self.clear_button.configure(
            background=theme['error'],
            foreground='white',
            activebackground='#c0392b',
            activeforeground='white'
        )

        self.import_button.configure(
            background=theme['border'],
            foreground=theme['fg'],
            activebackground=theme['secondary_fg']
        )

        self.sample_button.configure(
            background=theme['border'],
            foreground=theme['fg'],
            activebackground=theme['secondary_fg']
        )

        # Update status bar
        self.status_bar.configure(
            background=theme['status_bg'],
            foreground=theme['status_fg']
        )

        # Update progress frame
        self.progress_frame.configure(background=theme['bg'])
        self.progress_label.configure(background=theme['bg'], foreground=theme['fg'])

    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.theme_manager.toggle()
        self.apply_theme()
        mode = "Dark" if self.theme_manager.is_dark else "Light"
        return f"Switched to {mode} Mode"

    def change_font_size(self, delta):
        """Change text area font size"""
        self.current_font_size = max(8, min(24, self.current_font_size + delta))
        text_font = tkfont.Font(family="Segoe UI", size=self.current_font_size)
        self.Text1.configure(font=text_font)
        return f"Font size: {self.current_font_size}"

    def show_progress(self, message="Processing..."):
        """Show progress bar"""
        self.progress_label.configure(text=message)
        self.progress_frame.grid()
        self.progress.start(10)

    def hide_progress(self):
        """Hide progress bar"""
        self.progress.stop()
        self.progress_frame.grid_remove()