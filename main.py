import vosk
import pyaudio
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import threading  # Arayüzün donmaması için gerekli

# -------------------------------
# AYARLAR VE GLOBAL DEĞİŞKENLER
# -------------------------------
from src.risk_words import risk_words

is_listening = False  # Dinleme durumunu kontrol eden bayrak
sms_sent_flag = False # Aynı oturumda tekrar tekrar SMS atmaması için kontrol

# -------------------------------
# MANTIK FONKSİYONLARI
# -------------------------------
def calculate_risk(text):
    score = 0
    detected = []
    for word, weight in risk_words.items():
        if word.lower() in text.lower():
            score += weight
            detected.append(word)
    return score, detected

def risk_level(score):
    if score < 25: return "GÜVENLİ", "#90EE90"  # Açık Yeşil
    elif score < 50: return "ŞÜPHELİ (SARI)", "#ffd700"
    elif score < 75: return "MUHTEMEL (TURUNCU)", "orange"
    else: return "YÜKSEK RİSK (KIRMIZI)", "red"

def send_sms_simulation():
    """SMS Gönderme Simülasyonu (Gerçek API buraya entegre edilecek)"""
    print("--- SİSTEM UYARISI ---")
    print("SMS GÖNDERİLİYOR: 'Yakınınız şu an riskli bir görüşme yapıyor!'")
    # Gerçek uygulamada burada Twilio veya benzeri bir API kullanılır.

# -------------------------------
# KELİME HAVUZU YÖNETİMİ
# -------------------------------
def update_word_list():
    word_list_box.delete(0, tk.END)
    for word, weight in risk_words.items():
        word_list_box.insert(tk.END, f"{word} ({weight} Puan)")

def add_word():
    new_word = simpledialog.askstring("Yeni Kelime", "Eklemek istediğiniz kelime:")
    if new_word:
        new_weight = simpledialog.askinteger("Puan", f"'{new_word}' için risk puanı (1-20):", minvalue=1, maxvalue=20)
        if new_weight:
            risk_words[new_word.lower()] = new_weight
            update_word_list()

def remove_word():
    try:
        selected = word_list_box.get(word_list_box.curselection())
        word_to_remove = selected.split(" (")[0]
        del risk_words[word_to_remove]
        update_word_list()
    except:
        messagebox.showwarning("Uyarı", "Lütfen silmek için listeden bir kelime seçin.")

# -------------------------------
# SES DİNLEME (THREAD İÇİNDE ÇALIŞACAK)
# -------------------------------
def listen_thread():
    global is_listening, sms_sent_flag
    
    if not os.path.exists("./src/model-tr"):
        messagebox.showerror("Hata", "'model-tr' klasörü bulunamadı! Lütfen model dosyasını indirin.")
        # Butonu eski haline getir
        start_button.config(text="🎧 Dinlemeyi Başlat", bg="#2c7a2c", state="normal")
        stop_button.config(state="disabled")
        return

    try:
        model = vosk.Model("./src/model-tr")
        recognizer = vosk.KaldiRecognizer(model, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        text_accumulated = ""
        
        # SÜREKLİ DÖNGÜ (Durdur butonuna basılana kadar)
        while is_listening:
            data = stream.read(4000, exception_on_overflow=False)
            
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                new_text = result.get("text", "")
                
                if new_text:
                    text_accumulated += " " + new_text
                    
                    # GUI Güncelleme (Thread içinden güvenli erişim için)
                    text_box.delete(1.0, tk.END)
                    text_box.insert(tk.END, text_accumulated)
                    text_box.see(tk.END) # Otomatik aşağı kaydır

                    # Risk Analizi
                    score, detected = calculate_risk(text_accumulated)
                    level_text, color = risk_level(score)
                    
                    # Risk Etiketi Güncelleme
                    risk_label.config(text=f"{level_text}\nSkor: {score}", bg=color)
                    
                    # Kırmızı Kod ve SMS Mantığı
                    if color == "red":
                        if not sms_sent_flag: # Daha önce SMS atılmadıysa at
                            send_sms_simulation()
                            status_label.config(text="⚠️ SMS GÖNDERİLDİ!", fg="red")
                            sms_sent_flag = True # Flag'i kaldır ki tekrar tekrar atmasın
                    
                    # NOT: Dinlemeyi "break" ile kırmıyoruz, devam ediyor.

        # Döngü bittiğinde temizlik
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    except Exception as e:
        print(f"Hata: {e}")
    
    # İşlem bitince butonları resetle
    status_label.config(text="🛑 Durduruldu", fg="black")
    start_button.config(text="🎧 Dinlemeyi Başlat", bg="#2c7a2c", state="normal")
    stop_button.config(state="disabled")

# -------------------------------
# BUTON FONKSİYONLARI
# -------------------------------
def start_process():
    global is_listening, sms_sent_flag
    is_listening = True
    sms_sent_flag = False # Yeni oturumda SMS hakkını sıfırla
    
    status_label.config(text="🎤 Dinleniyor... (Kesintisiz)", fg="green")
    start_button.config(state="disabled")
    stop_button.config(state="normal", bg="#a83232")
    
    # İşlemi ayrı bir çekirdekte (thread) başlat
    t = threading.Thread(target=listen_thread)
    t.daemon = True # Ana program kapanınca thread de kapansın
    t.start()

def stop_process():
    global is_listening
    is_listening = False # While döngüsünü kırar
    status_label.config(text="⏳ Durduruluyor...", fg="orange")

# -------------------------------
# ARAYÜZ (GUI)
# -------------------------------
root = tk.Tk()
root.title("Anti-Fraud Ses Analiz Sistemi")
root.geometry("750x550")

# Sol Panel
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(left_frame, text="📞 Ses Analiz Paneli", font=("Arial", 14, "bold")).pack()
status_label = tk.Label(left_frame, text="Hazır", font=("Arial", 10))
status_label.pack()

# Buton Çerçevesi
btn_frame = tk.Frame(left_frame)
btn_frame.pack(pady=10, fill=tk.X)

start_button = tk.Button(btn_frame, text="🎧 Dinlemeyi Başlat", bg="#2c7a2c", fg="white", font=("Arial", 11, "bold"), command=start_process)
start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

stop_button = tk.Button(btn_frame, text="🛑 Durdur", bg="#a83232", fg="white", font=("Arial", 11, "bold"), command=stop_process, state="disabled")
stop_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)

text_box = tk.Text(left_frame, height=15, width=40, font=("Arial", 11))
text_box.pack(pady=5, fill=tk.BOTH, expand=True)

risk_label = tk.Label(left_frame, text="RİSK DURUMU: GÜVENLİ", font=("Arial", 12, "bold"), bg="#90EE90", height=3)
risk_label.pack(fill=tk.X, pady=10)

# Sağ Panel
right_frame = tk.Frame(root, padx=10, pady=10, bg="#e0e0e0")
right_frame.pack(side=tk.RIGHT, fill=tk.Y)

tk.Label(right_frame, text="🎯 Kelime Havuzu", font=("Arial", 11, "bold"), bg="#e0e0e0").pack()
word_list_box = tk.Listbox(right_frame, width=30, height=20)
word_list_box.pack(pady=5)

btn_add = tk.Button(right_frame, text="➕ Kelime Ekle", command=add_word, bg="white")
btn_add.pack(fill=tk.X, pady=2)

btn_remove = tk.Button(right_frame, text="➖ Seçileni Sil", command=remove_word, bg="white")
btn_remove.pack(fill=tk.X, pady=2)

update_word_list()

# Pencere kapatılınca thread'i güvenli kapatmak için
def on_closing():
    global is_listening
    is_listening = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()