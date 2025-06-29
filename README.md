# Trainify_AI-Powered-Smart-Mirror-For-Real-Time-Posture-Monitoring-and-Exercise-Guidance
Trainify is a real-time smart fitness application designed to assist users in performing physical exercises with correct posture and form. It uses computer vision and pose detection algorithms to provide visual feedback and rep counting, ensuring a more accurate and injury-free workout experience.
Sure! Here's a **concise but well-explained `README.md` file** for your **Trainify** project, written in proper Markdown format and suitable for GitHub:

---

## 🚀 Features

- ✅ **Real-time posture detection** via webcam  
- ✅ **Green/Red line feedback** based on correct/incorrect angles  
- ✅ **Automatic repetition counter**  
- ✅ Supports exercises like **bicep curls**, **lateral raises**, etc.  
- ✅ Built using **Python**, **OpenCV**, and **MediaPipe**

---

## 🛠️ Technologies Used

- Python 3  
- OpenCV  
- MediaPipe  
- VS Code  
- (Optional) Tkinter or Streamlit for GUI  
- Arduino (for extended applications)

---

## 📸 How It Works

- The app uses your webcam to detect body landmarks.
- During an exercise:
  - **Green lines** appear if the posture is correct.
  - **Red lines** show when angles fall outside the acceptable range.
- The system automatically counts each **correct rep**.
- You get real-time feedback, helping reduce the risk of injury.

---

## 🗂️ Project Structure

```

TRAINIFY/
├── assets/ # Images or icons used in the app
├── data/ # Placeholder for any logs or session data
├── models/ # Posture detection models for each exercise
│ ├── bicep_curl.py
│ ├── hand_side.py
│ ├── lateral_raise.py
├── app.py # Main application entry point
├── history.txt # Session logs or summary (optional)
└── requirements.txt # Python package dependencies

````

## 🚀 Key Features

- 🧍‍♂️ **Real-time body posture monitoring**
- ✅ **Green/Red line feedback** to indicate form correctness
- 🔢 **Automatic repetition counting** with angle-based logic
- 🧠 Modular code with separate models for each exercise:
  - Bicep Curl
  - Lateral Raise
  - Hand Side Raise
---

## 🛠️ Tech Stack

- Python 3  
- OpenCV  
- MediaPipe  
- (Optional) Tkinter or Streamlit for GUI  
- Visual Studio Code

---
## 📦 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/trainify.git
   cd trainify
````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python trainify_app.py
   ```


## 🧠 Future Improvements

- Add support for more exercise types (e.g., squats, shoulder press)  
- Integrate voice feedback for form guidance  
- Log user workout history  
- Mobile version or web deployment

---

## 🙋‍♀️ Author

**Shumiam Sajid** – Biomedical Engineer | Developer of Trainify
For queries or collaboration: [shumiamsajid09@gmail.com]

