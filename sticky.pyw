import tkinter as tk
from tkinter import Menu, messagebox

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Note")
        self.root.geometry("300x200")
        self.root.attributes('-alpha', 0.8)  # Set initial transparency to 80%
        self.root.configure(bg='#2e2e2e')
        self.root.overrideredirect(True)  # Remove the title bar
        self.root.wm_attributes("-topmost", 1)  # Keep the widget always on top
        self.root.resizable(True, True)  # Make the widget resizable

        self.offset_x = 0
        self.offset_y = 0
        self.moving = False

        self.text_area = tk.Text(self.root, bg='#2e2e2e', fg='white', insertbackground='white', font=("Arial", 14), wrap=tk.WORD, bd=0, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind('<KeyRelease>', self.save_note)

        self.text_area.bind("<Button-1>", self.start_move)
        self.text_area.bind("<ButtonRelease-1>", self.stop_move)
        self.text_area.bind("<B1-Motion>", self.do_move)
        self.text_area.bind("<Control-b>", self.make_bold)
        self.text_area.bind("<Control-i>", self.make_italic)
        self.text_area.bind("<Control-u>", self.make_underline)
        self.text_area.bind("<Button-3>", self.show_context_menu)

        self.root.bind("<FocusIn>", self.make_opaque)
        self.root.bind("<FocusOut>", self.make_transparent)

        self.note_content = ""
        self.load_note()

        self.create_context_menu()

    def save_note(self, event=None):
        self.note_content = self.text_area.get(1.0, tk.END)

    def load_note(self):
        self.text_area.insert(tk.END, self.note_content)

    def make_opaque(self, event):
        self.root.attributes('-alpha', 1.0)  # Make fully opaque

    def make_transparent(self, event):
        self.root.attributes('-alpha', 0.8)  # Make transparent again

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        self.moving = True

    def stop_move(self, event):
        self.moving = False

    def do_move(self, event):
        if self.moving:
            x = self.root.winfo_pointerx() - self.offset_x
            y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry(f"+{x}+{y}")

    def create_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Minimize Sticky", command=self.minimize_sticky)
        self.context_menu.add_command(label="Close Sticky", command=self.close_sticky)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def minimize_sticky(self):
        self.root.geometry("200x30")
        self.text_area.pack_forget()
        self.root.bind("<Button-3>", self.unminimize_sticky)
        self.root.bind("<Button-1>", self.start_move)

    def unminimize_sticky(self, event):
        self.root.geometry("300x200")
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.root.bind("<Button-3>", self.show_context_menu)
        self.text_area.bind("<Button-1>", self.start_move)
        self.text_area.bind("<ButtonRelease-1>", self.stop_move)
        self.text_area.bind("<B1-Motion>", self.do_move)

    def close_sticky(self):
        self.root.destroy()

    def make_bold(self, event=None):
        self.apply_tag('bold', 'bold')

    def make_italic(self, event=None):
        self.apply_tag('italic', 'italic')

    def make_underline(self, event=None):
        self.apply_tag('underline', 'underline')

    def apply_tag(self, tag_name, font_style):
        try:
            current_tags = self.text_area.tag_names(tk.SEL_FIRST)
            if tag_name in current_tags:
                self.text_area.tag_remove(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.text_area.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
                self.text_area.tag_config(tag_name, font=(None, None, font_style))
        except tk.TclError:
            messagebox.showerror("Error", "No text selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()
