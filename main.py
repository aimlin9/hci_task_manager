import customtkinter as ctk
import tkinter as tk

# ── App configuration ──────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Task Manager")
app.geometry("620x720")
app.resizable(False, False)

# ── State ──────────────────────────────────────────────────────────
tasks = []
is_dark = False
completed = set()

# ── Color themes ───────────────────────────────────────────────────
LIGHT = {
    "bg": "#f5f5f5",
    "listbox_bg": "#ffffff",
    "listbox_fg": "#1a1a1a",
    "listbox_select_bg": "#3b8ed0",
    "listbox_select_fg": "#ffffff",
    "highlight": "#cccccc",
    "strike_fg": "#aaaaaa",
}

DARK = {
    "bg": "#2b2b2b",
    "listbox_bg": "#3c3c3c",
    "listbox_fg": "#f0f0f0",
    "listbox_select_bg": "#1f6aa5",
    "listbox_select_fg": "#ffffff",
    "highlight": "#555555",
    "strike_fg": "#777777",
}

# ── Helper functions ───────────────────────────────────────────────
def get_theme():
    return DARK if is_dark else LIGHT

def refresh_list():
    task_listbox.delete(0, "end")
    theme = get_theme()

    if not tasks:
        task_listbox.insert("end", "   No tasks yet!  Add one above 🎉")
        task_listbox.config(fg="#aaaaaa")
    else:
        task_listbox.config(fg=theme["listbox_fg"])
        for i, task in enumerate(tasks):
            prefix = "   ✔   " if i in completed else f"   {i + 1}.   "
            task_listbox.insert("end", f"{prefix}{task}")

        # Gray out completed items
        for i in completed:
            task_listbox.itemconfig(i, fg=theme["strike_fg"])

    # Update counter
    count = len(tasks)
    done = len(completed)
    if count == 0:
        counter_label.configure(text="No tasks yet", text_color="gray")
    elif done > 0:
        counter_label.configure(
            text=f"{count} tasks  •  {done} completed",
            text_color="#3b8ed0"
        )
    else:
        counter_label.configure(
            text=f"{count} task{'s' if count > 1 else ''}",
            text_color="#3b8ed0"
        )

def apply_listbox_theme():
    theme = get_theme()
    task_listbox.config(
        bg=theme["listbox_bg"],
        fg=theme["listbox_fg"],
        selectbackground=theme["listbox_select_bg"],
        selectforeground=theme["listbox_select_fg"],
        highlightbackground=theme["highlight"],
        highlightcolor=theme["highlight"],
    )

def show_status(message, color="green"):
    status_label.configure(text=message, text_color=color)
    app.after(3000, lambda: status_label.configure(text=""))

def add_task():
    task = entry.get().strip()
    if not task:
        show_status("⚠️   Please enter a task before adding.", color="orange")
        return
    tasks.append(task)
    entry.delete(0, "end")
    refresh_list()
    show_status(f"✅   Task added: '{task}'")

def delete_task():
    global completed
    selected = task_listbox.curselection()
    if not selected:
        show_status("⚠️   Please select a task to delete.", color="orange")
        return
    if not tasks:
        show_status("⚠️   No tasks to delete.", color="orange")
        return
    index = selected[0]
    if index >= len(tasks):
        show_status("⚠️   Please select a valid task.", color="orange")
        return
    removed = tasks.pop(index)
    completed.discard(index)
    completed = {i if i < index else i - 1 for i in completed}
    refresh_list()
    show_status(f"🗑️   Task deleted: '{removed}'", color="red")

def toggle_complete():
    global completed
    selected = task_listbox.curselection()
    if not selected:
        show_status("⚠️   Please select a task to mark complete.", color="orange")
        return
    if not tasks:
        return
    index = selected[0]
    if index >= len(tasks):
        show_status("⚠️   Please select a valid task.", color="orange")
        return
    if index in completed:
        completed.remove(index)
        show_status(f"↩️   Marked incomplete: '{tasks[index]}'", color="gray")
    else:
        completed.add(index)
        show_status(f"✔️   Marked complete: '{tasks[index]}'", color="green")
    refresh_list()

def toggle_dark_mode():
    global is_dark
    is_dark = not is_dark
    mode = "dark" if is_dark else "light"
    ctk.set_appearance_mode(mode)
    toggle_btn.configure(text="☀️  Light Mode" if is_dark else "🌙  Dark Mode")
    apply_listbox_theme()
    refresh_list()

# ── UI Layout ──────────────────────────────────────────────────────

# Title
title_label = ctk.CTkLabel(app, text="📝  Task Manager",
                            font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(pady=(30, 5))

subtitle_label = ctk.CTkLabel(app, text="Stay organised. Stay productive.",
                               font=ctk.CTkFont(size=13), text_color="gray")
subtitle_label.pack(pady=(0, 20))

# Input frame
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(padx=30, fill="x")

entry = ctk.CTkEntry(input_frame, placeholder_text="Enter a new task...",
                     height=42, font=ctk.CTkFont(size=14))
entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
entry.bind("<Return>", lambda e: add_task())

add_btn = ctk.CTkButton(input_frame, text="Add Task", width=110,
                         height=42, command=add_task,
                         font=ctk.CTkFont(size=14, weight="bold"))
add_btn.pack(side="left")

# Status label
status_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=12))
status_label.pack(pady=(8, 0))

# Counter + list label row
list_header = ctk.CTkFrame(app, fg_color="transparent")
list_header.pack(padx=30, pady=(15, 5), fill="x")

list_label = ctk.CTkLabel(list_header, text="Your Tasks",
                           font=ctk.CTkFont(size=15, weight="bold"))
list_label.pack(side="left")

counter_label = ctk.CTkLabel(list_header, text="No tasks yet",
                              font=ctk.CTkFont(size=12), text_color="gray")
counter_label.pack(side="right")

# Task listbox — larger font + more line height = wider spacing, no empty rows
task_listbox = tk.Listbox(app, font=("Helvetica", 14), height=11,
                           selectmode="single", relief="flat",
                           bd=0, highlightthickness=1,
                           activestyle="none",
                           selectborderwidth=0)
task_listbox.pack(padx=30, pady=(0, 5), fill="x")

# Apply initial theme and show empty state
apply_listbox_theme()
refresh_list()

# Bottom buttons
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(padx=30, pady=(10, 5), fill="x")

delete_btn = ctk.CTkButton(btn_frame, text="🗑️  Delete Selected",
                            width=180, height=40, fg_color="#e05252",
                            hover_color="#c0392b", command=delete_task,
                            font=ctk.CTkFont(size=13, weight="bold"))
delete_btn.pack(side="left")

complete_btn = ctk.CTkButton(btn_frame, text="✔️  Mark Complete",
                              width=170, height=40, fg_color="#2ecc71",
                              hover_color="#27ae60", command=toggle_complete,
                              font=ctk.CTkFont(size=13, weight="bold"))
complete_btn.pack(side="left", padx=(10, 0))

toggle_btn = ctk.CTkButton(btn_frame, text="🌙  Dark Mode",
                            width=150, height=40, fg_color="#555",
                            hover_color="#333", command=toggle_dark_mode,
                            font=ctk.CTkFont(size=13, weight="bold"))
toggle_btn.pack(side="right")

# Footer hint
hint_label = ctk.CTkLabel(app, text="💡 Tip: Press Enter to add  •  Click a task to select it",
                           font=ctk.CTkFont(size=11), text_color="gray")
hint_label.pack(pady=(5, 15))

# ── Run ────────────────────────────────────────────────────────────
app.mainloop()