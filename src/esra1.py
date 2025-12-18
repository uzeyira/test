import vosk
import pyaudio
import json
import tkinter as tk
from tkinter import messagebox

# -------------------------------
# RİSKLİ KELİMELER VE AĞIRLIKLARI
# -------------------------------
risk_words = {
    "polis": 10,
    "savcı": 10,
    "emniyet": 8,
    "mahkeme": 8,
    "hemen": 6,
    "acil": 6,
    "bekleme": 5,
    "hesap": 7,
    "iban": 9,
    "şifre": 10,
    "transfer": 8,
    "soruşturma": 12,
    "terör": 15,
    "kimseye söyleme": 15
}

# -------------------------------
# RİSK HESAPLAMA
# -------------------------------
def calculate_risk(text):
    score = 0
    for word, weight in risk_words.items():
        if word in text:
            score += weight
    return score

def risk_level(score):
    if score < 20:
        return "GÜVENLİ", "green"
    elif score < 40:
        return "ŞÜPHELİ (SARI KOD)", "yellow"
    elif score < 60:
        return "MUHTEMEL (TURUNCU KOD)", "orange"
    else:
        return "YÜKSEK RİSK (KIRMIZI KOD)", "red"

# -------------------------------
# SMS SİMÜLASYONU
# -------------------------------
def send_sms():
    messagebox.showwarning(
        "SMS Gönderildi",
        "⚠ Aile bireyine UYARI SMS'i gönderildi!\n(Simülasyon)"
    )

# -------------------------------
# SES → METİN ve ANALİZ
# -------------------------------
def start_listening():
    status_label.config(text="🎤 Dinleniyor...")
    root.update()

    model = vosk.Model("model-tr")
    recognizer = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8000)
    stream.start_stream()

    text = ""

    for _ in range(20):  # 20 döngü = kısa demo
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text += " " + result.get("text", "")
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, text)

            score = calculate_risk(text)
            level, color = risk_level(score)

            risk_label.config(text=level, bg=color)

            if color == "red":
                send_sms()
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    status_label.config(text="🛑 Dinleme Bitti")

# -------------------------------
# ARAYÜZ (YAŞLI DOSTU)
# -------------------------------
root = tk.Tk()
root.title("Telefon Dolandırıcılığı Erken Uyarı Sistemi")
root.geometry("520x420")

title = tk.Label(root, text="📞 Dolandırıcılık Uyarı Sistemi",
                 font=("Arial", 18, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="Hazır", font=("Arial", 14))
status_label.pack(pady=5)

start_button = tk.Button(root,
                          text="🎧 Dinlemeyi Başlat",
                          font=("Arial", 16),
                          command=start_listening)
start_button.pack(pady=10)

text_box = tk.Text(root, height=6, font=("Arial", 12))
text_box.pack(pady=10)

risk_label = tk.Label(root,
                      text="Risk Durumu",
                      font=("Arial", 16),
                      width=30)
risk_label.pack(pady=15)

root.mainloop()
