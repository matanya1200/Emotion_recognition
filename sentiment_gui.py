import tkinter as tk
from tkinter import filedialog
import requests


# שליחת טקסט ל-API
def send_to_api(text):
    try:
        response = requests.post("http://127.0.0.1:5000/analyze", json={"text": text})
        return response.json()
    except Exception as e:
        return {"sentiment": "שגיאה", "score": 0.0, "error": str(e)}


# ניתוח רגשות של טקסט מהתיבה
def analyze_sentiment():
    text = input_box.get("1.0", tk.END).strip()
    if not text:
        result_label.config(text="יש להזין טקסט לניתוח.")
        return

    data = send_to_api(text)
    if "error" in data:
        result_label.config(text="שגיאה בחיבור לשרת: " + data["error"])
        return

    sentiment = data["sentiment"]
    score = data["score"]
    result_label.config(text=f"רגש: {sentiment} (ציון: {score:.2f})")


# העלאת קובץ וניתוח רגשות
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception as e:
        result_label.config(text="שגיאה בקריאת הקובץ: " + str(e))
        return

    results = []
    total_score = 0.0

    for idx, line in enumerate(lines, 1):
        data = send_to_api(line)
        if "error" in data:
            results.append(f"{idx}. שגיאה בשורה: {data['error']}")
            continue
        sentiment = data["sentiment"]
        score = data["score"]
        total_score += score
        results.append(f"{idx}. '{line}' → {sentiment} (ציון: {score:.2f})")

    # ממוצע כולל
    avg_score = total_score / len(lines)
    if avg_score >= 0.05:
        overall = "חיובי"
    elif avg_score <= -0.05:
        overall = "שלילי"
    else:
        overall = "ניטרלי"

    results.append(f"\nרגש כולל לקובץ: {overall} (ממוצע ציון: {avg_score:.2f})")

    result_label.config(text="\n".join(results))


# === GUI ===
root = tk.Tk()
root.title("ניתוח רגשות - VADER")

input_box = tk.Text(root, height=6, width=50)
input_box.pack(pady=10)

analyze_button = tk.Button(root, text="נתח טקסט", command=analyze_sentiment)
analyze_button.pack(pady=5)

upload_button = tk.Button(root, text="העלה קובץ לניתוח", command=upload_file)
upload_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
result_label.pack(pady=10)

root.mainloop()
