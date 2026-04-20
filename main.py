import tkinter as tk
import sqlite3

# -------------------- Database Setup --------------------
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    done INTEGER DEFAULT 0
)
""")
conn.commit()

# -------------------- Window --------------------
root = tk.Tk()
root.title("To-Do List")
root.geometry("450x600")
root.configure(bg="#0f172a")

# -------------------- Functions --------------------
def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    for row in rows:
        display = row[1] + (" ✔" if row[2] else "")
        listbox.insert(tk.END, display)

        if row[2]:
            listbox.itemconfig(tk.END, fg="#6b7280")

    update_status()

def update_status():
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]
    status_label.config(text=f"{count} Tasks")

def add_task(event=None):
    task = entry.get().strip()
    if task:
        cursor.execute("INSERT INTO tasks (task, done) VALUES (?, ?)", (task, 0))
        conn.commit()
        entry.delete(0, tk.END)
        load_tasks()

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        cursor.execute("SELECT id FROM tasks")
        task_id = cursor.fetchall()[index][0]

        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()

def mark_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        cursor.execute("SELECT id, done FROM tasks")
        row = cursor.fetchall()[index]

        if row[1] == 0:
            cursor.execute("UPDATE tasks SET done=1 WHERE id=?", (row[0],))
            conn.commit()
            load_tasks()

def clear_all():
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    load_tasks()

# -------------------- Hover Effects --------------------
def on_enter(e):
    e.widget['bg'] = "#334155"

def on_leave(e, color):
    e.widget['bg'] = color

# -------------------- Header --------------------
title = tk.Label(root, text="To-Do List",
                 font=("Segoe UI", 22, "bold"),
                 bg="#0f172a", fg="#e2e8f0")
title.pack(pady=15)

# -------------------- Input --------------------
input_frame = tk.Frame(root, bg="#0f172a")
input_frame.pack(pady=10)

entry = tk.Entry(input_frame, width=28,
                 font=("Segoe UI", 12),
                 bg="#1e293b", fg="white",
                 insertbackground="white", bd=0)
entry.grid(row=0, column=0, padx=8, ipady=6)
entry.bind("<Return>", add_task)

add_btn = tk.Button(input_frame, text="+",
                    font=("Segoe UI", 14, "bold"),
                    bg="#22c55e", fg="white",
                    width=4, bd=0,
                    command=add_task)
add_btn.grid(row=0, column=1)

add_btn.bind("<Enter>", on_enter)
add_btn.bind("<Leave>", lambda e: on_leave(e, "#22c55e"))

# -------------------- List --------------------
list_frame = tk.Frame(root, bg="#0f172a")
list_frame.pack(pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    list_frame,
    width=38,
    height=16,
    font=("Segoe UI", 12),
    bg="#1e293b",
    fg="#e2e8f0",
    selectbackground="#38bdf8",
    activestyle="none",
    bd=0,
    yscrollcommand=scrollbar.set
)
listbox.pack()
scrollbar.config(command=listbox.yview)

# -------------------- Buttons --------------------
btn_frame = tk.Frame(root, bg="#0f172a")
btn_frame.pack(pady=15)

def styled_button(text, color, command):
    btn = tk.Button(btn_frame, text=text,
                    bg=color, fg="white",
                    font=("Segoe UI", 10, "bold"),
                    width=12, bd=0,
                    command=command)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", lambda e: on_leave(e, color))
    return btn

done_btn = styled_button("✔ Done", "#22c55e", mark_done)
delete_btn = styled_button("Delete", "#ef4444", delete_task)
clear_btn = styled_button("Clear All", "#f59e0b", clear_all)

done_btn.grid(row=0, column=0, padx=6)
delete_btn.grid(row=0, column=1, padx=6)
clear_btn.grid(row=0, column=2, padx=6)

# -------------------- Status --------------------
status_label = tk.Label(root,
                        text="0 Tasks",
                        font=("Segoe UI", 10),
                        bg="#0f172a",
                        fg="#94a3b8")
status_label.pack()

# -------------------- Init --------------------
load_tasks()

# -------------------- Run --------------------
root.mainloop()