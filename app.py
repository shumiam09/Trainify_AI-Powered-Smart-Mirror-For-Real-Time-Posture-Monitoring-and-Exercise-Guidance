import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

# Global variables for BMI and last exercise
last_exercise = "None"
bmi_result = ""

# Main window
root = tk.Tk()
root.title("Trainify")
root.geometry("500x500")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# ---------------- PAGE 1: Welcome ----------------
page1 = tk.Frame(root)
page1.grid(row=0, column=0, sticky='nsew')

tk.Label(page1, text="Trainify", font=("Arial", 28, "bold")).pack(pady=20)
tk.Label(page1, text="Where fitness is digitalized", font=("Arial", 14)).pack(pady=10)

# Logo loading with path check
try:
    if os.path.exists("logo.png"):
        logo_img = Image.open("logo.png").resize((200, 200))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(page1, image=logo).pack(pady=10)
    else:
        raise FileNotFoundError
except:
    tk.Label(page1, text="[Logo missing]", font=("Arial", 12)).pack()

tk.Button(page1, text="Next", command=lambda: show_frame(page2)).pack(pady=20)

# ---------------- PAGE 2: BMI Calculator ----------------
page2 = tk.Frame(root)
page2.grid(row=0, column=0, sticky='nsew')

tk.Label(page2, text="BMI Calculator", font=("Arial", 20)).pack(pady=20)

tk.Label(page2, text="Weight (kg)").pack()
weight_entry = tk.Entry(page2)
weight_entry.pack()

tk.Label(page2, text="Height (feet)").pack()
height_entry = tk.Entry(page2)
height_entry.pack()

bmi_display = tk.Label(page2, text="")
bmi_display.pack(pady=10)

recommendation_label = tk.Label(page2, text="")
recommendation_label.pack()

def calculate_bmi():
    global last_exercise, bmi_result
    try:
        weight = float(weight_entry.get())
        height_ft = float(height_entry.get())
        height_m = height_ft * 0.3048
        bmi = round(weight / (height_m ** 2), 2)
        bmi_result = bmi
        bmi_display.config(text=f"BMI: {bmi}")

        if bmi < 18.5:
            recommendation = "Do: Side Kicks"
            last_exercise = "side_kicks"
        elif bmi <= 24.9:
            recommendation = "Do: Bicep Curls"
            last_exercise = "bicep_curl"
        else:
            recommendation = "Do: Leg Curl"
            last_exercise = "leg_curl"

        recommendation_label.config(text=recommendation)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

tk.Button(page2, text="Calculate BMI", command=calculate_bmi).pack(pady=5)
tk.Button(page2, text="Next", command=lambda: show_frame(page3)).pack(pady=10)

# ---------------- PAGE 3: Model Selection ----------------
page3 = tk.Frame(root)
page3.grid(row=0, column=0, sticky='nsew')

tk.Label(page3, text="Model Selection", font=("Arial", 20)).pack(pady=20)

def open_model(model_name):
    try:
        subprocess.Popen(["python", f"models/{model_name}.py"])
    except Exception as e:
        messagebox.showerror("Execution Error", f"Could not open model: {e}")

tk.Button(page3, text="Bicep Curl", command=lambda: open_model("bicep_curl")).pack(pady=5)
tk.Button(page3, text="Side Kicks", command=lambda: open_model("side_kicks")).pack(pady=5)
tk.Button(page3, text="Leg Curl", command=lambda: open_model("leg_curl")).pack(pady=5)

tk.Button(page3, text="Next", command=lambda: show_frame(page4)).pack(pady=20)

# ---------------- PAGE 4: History ----------------
page4 = tk.Frame(root)
page4.grid(row=0, column=0, sticky='nsew')

tk.Label(page4, text="History", font=("Arial", 20)).pack(pady=20)
history_label = tk.Label(page4, text="Last Exercise: None", font=("Arial", 14))
history_label.pack(pady=10)

def update_history():
    formatted = last_exercise.replace('_', ' ').title()
    history_label.config(text=f"Last Exercise: {formatted}")

tk.Button(page4, text="Next", command=lambda: [update_history(), show_frame(page5)]).pack(pady=20)

# ---------------- PAGE 5: Calorie Counter ----------------
page5 = tk.Frame(root)
page5.grid(row=0, column=0, sticky='nsew')

tk.Label(page5, text="Calorie Counter", font=("Arial", 20)).pack(pady=20)

exercise_type = tk.StringVar(value="bicep_curl")
tk.OptionMenu(page5, exercise_type, "bicep_curl", "side_kicks", "leg_curl").pack()

tk.Label(page5, text="Reps:").pack()
reps_entry = tk.Entry(page5)
reps_entry.pack()

tk.Label(page5, text="Your Weight (kg):").pack()
user_weight_entry = tk.Entry(page5)
user_weight_entry.pack()

calories_label = tk.Label(page5, text="", font=("Arial", 12))
calories_label.pack(pady=10)

def calculate_calories():
    try:
        reps = int(reps_entry.get())
        weight = float(user_weight_entry.get())
        MET_values = {"bicep_curl": 3, "side_kicks": 4, "leg_curl": 3.5}
        MET = MET_values.get(exercise_type.get(), 3)
        calories_burned = round((MET * weight * 3.5 / 200) * (reps / 10), 2)
        calories_label.config(text=f"Calories Burned: {calories_burned} kcal")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

tk.Button(page5, text="Calculate", command=calculate_calories).pack(pady=5)
tk.Button(page5, text="Next", command=lambda: show_frame(page6)).pack(pady=10)

# ---------------- PAGE 6: Thank You ----------------
page6 = tk.Frame(root)
page6.grid(row=0, column=0, sticky='nsew')

tk.Label(page6, text="Thank You!", font=("Arial", 24)).pack(pady=60)
tk.Label(page6, text="Stay fit with Trainify 💪", font=("Arial", 14)).pack()

# Show first page
show_frame(page1)
root.mainloop()
