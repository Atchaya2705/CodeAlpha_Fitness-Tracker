import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from datetime import datetime

# -------------------- Database Setup --------------------
conn = sqlite3.connect('fitness_tracker.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS fitness_log (
    date TEXT,
    steps INTEGER,
    workout TEXT,
    duration INTEGER,
    calories INTEGER
)''')
conn.commit()

# -------------------- Functions --------------------
def save_data():
    date = datetime.now().strftime("%Y-%m-%d")
    steps = steps_entry.get()
    workout = workout_entry.get()
    duration = duration_entry.get()
    calories = calories_entry.get()

    if not steps or not workout or not duration or not calories:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    c.execute("INSERT INTO fitness_log VALUES (?, ?, ?, ?, ?)",
              (date, int(steps), workout, int(duration), int(calories)))
    conn.commit()
    messagebox.showinfo("Success", "Fitness data saved!")
    clear_entries()
    update_summary()

def clear_entries():
    steps_entry.delete(0, tk.END)
    workout_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    calories_entry.delete(0, tk.END)

def update_summary():
    c.execute("SELECT SUM(steps), SUM(duration), SUM(calories) FROM fitness_log WHERE date = ?", 
              (datetime.now().strftime("%Y-%m-%d"),))
    result = c.fetchone()
    total_steps = result[0] or 0
    total_duration = result[1] or 0
    total_calories = result[2] or 0

    summary_label.config(text=f"Today's Summary:\nSteps: {total_steps}\nWorkout Time: {total_duration} mins\nCalories Burned: {total_calories}")
    steps_progress['value'] = min(total_steps / 100, 100)
    calories_progress['value'] = min(total_calories / 10, 100)

# -------------------- UI Setup --------------------
app = tk.Tk()
app.title("Fitness Tracker App")
app.geometry("400x500")
app.config(bg="#f0f0f0")

tk.Label(app, text="Enter Your Daily Fitness Data", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

tk.Label(app, text="Steps Walked:", bg="#f0f0f0").pack()
steps_entry = tk.Entry(app, width=30)
steps_entry.pack()

tk.Label(app, text="Workout Type:", bg="#f0f0f0").pack()
workout_entry = tk.Entry(app, width=30)
workout_entry.pack()

tk.Label(app, text="Duration (mins):", bg="#f0f0f0").pack()
duration_entry = tk.Entry(app, width=30)
duration_entry.pack()

tk.Label(app, text="Calories Burned:", bg="#f0f0f0").pack()
calories_entry = tk.Entry(app, width=30)
calories_entry.pack()

tk.Button(app, text="Save Entry", command=save_data, bg="green", fg="white").pack(pady=10)

summary_label = tk.Label(app, text="", font=("Arial", 12), bg="#f0f0f0")
summary_label.pack(pady=10)

tk.Label(app, text="Steps Progress", bg="#f0f0f0").pack()
steps_progress = ttk.Progressbar(app, orient='horizontal', length=250, mode='determinate')
steps_progress.pack(pady=5)

tk.Label(app, text="Calories Progress", bg="#f0f0f0").pack()
calories_progress = ttk.Progressbar(app, orient='horizontal', length=250, mode='determinate')
calories_progress.pack(pady=5)

update_summary()
app.mainloop()
