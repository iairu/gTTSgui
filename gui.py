import sys
import tkinter as tk
import tkinter.ttk as ttk

root = None
top = None

def init():
    # '''Starting point when module is the main routine.'''
    global root, top
    root = tk.Tk()
    top = MainWindow(root)

def start():
    root.mainloop()

class MainWindow:
    def __init__(self, top=None):
        # '''This class configures and populates the toplevel window.
        #    top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+818+171")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.TCombobox1 = ttk.Combobox(top)
        self.TCombobox1.place(relx=0.017, rely=0.022, relheight=0.042
                , relwidth=0.105)
        self.value_list = ["sk","cz","en","pl","ja","ko",]
        self.TCombobox1.configure(values=self.value_list)
        self.TCombobox1.current(0)
        self.TCombobox1.configure(width=63)
        self.TCombobox1.configure(takefocus="")
        self.TCombobox1.configure(background="white")
        self.TCombobox1.configure(foreground="darkgray")

        self.Text1 = tk.Text(top)
        self.Text1.place(relx=0.017, rely=0.067, relheight=0.902, relwidth=0.973)

        self.Text1.configure(background="white")
        self.Text1.configure(font="TkTextFont")
        self.Text1.configure(foreground="black")
        self.Text1.configure(highlightbackground="#d9d9d9")
        self.Text1.configure(highlightcolor="black")
        self.Text1.configure(insertbackground="black")
        self.Text1.configure(selectbackground="#c4c4c4")
        self.Text1.configure(selectforeground="black")
        self.Text1.configure(width=584)
        self.Text1.configure(wrap="word")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.85, rely=0.022, height=21, width=80)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Save''')
        self.Button1.configure(width=80)

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.133, rely=0.022, height=19, width=425)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(relief="groove")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Word count: 0''')