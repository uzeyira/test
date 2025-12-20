risk_words = {
    # 🔴 SEVİYE 10: KESİN KIRMIZI ALARM (Fiziksel Eylem & İzolasyon & Terör)
    "poşete koy": 10,       # Fiziksel teslimat talebi %100 dolandırıcılık
    "çöp kutusu": 10,       # Parayı bırakma noktası
    "elden teslim": 10,     # Elden para alma
    "kimseye söyleme": 10,  # İzolasyon taktiği
    "telefonu kapatma": 10, # Kurbanı hatta tutma
    "terör örgütü": 10,     # Korku imparatorluğu
    "fetö": 10,
    "pkk": 10,
    "gizli operasyon": 10,  # Devlet gizli operasyon yapmaz
    "sivil ekip": 10,       # Parayı almaya gelecek kişi

    # 🔴 SEVİYE 8-9: ÇOK YÜKSEK RİSK (Otorite & Hesap Ele Geçirme)
    "savcı": 9,
    "başsavcı": 9,
    "emniyet müdürü": 9,
    "güvenli hesap": 9,     # "Parayı güvenli hesaba at" yalanı
    "şifre": 9,             # Banka şifresi istenmesi
    "sms kodu": 9,          # Onay kodu istenmesi
    "paraları hazırla": 9,
    "adınız karıştı": 8,    # Suçlama başlangıcı
    "yalnız mısın": 8,      # İzolasyon kontrolü
    "istihbarat": 8,

    # 🟠 SEVİYE 6-7: YÜKSEK RİSK (Varlık Sorgusu & Tehdit)
    "altın": 7,
    "ziynet": 7,
    "mücevher": 7,
    "kasa": 7,              # Evdeki kasayı soruyor
    "iban": 7,              # Para isteme aşaması
    "gözaltı kararı": 7,
    "yakalama kararı": 7,
    "hesap numarası": 6,
    "mobil onay": 6,

    # 🟡 SEVİYE 4-5: ORTA RİSK (Aciliyet & Yemleme)
    "acil": 5,              # Panik yaratma
    "hemen": 5,
    "dosyanız kabarık": 5,
    "bloke": 5,             # "Hesabınız bloke oldu" yalanı
    "uzlaşma dosyası": 5,
    "kazandınız": 4,        # Ödül dolandırıcılığı
    "icra takibi": 4,
    "şüpheli işlem": 4,

    # 🟢 SEVİYE 1-3: DÜŞÜK RİSK (Genel & Bağlam Gerektiren)
    "polis": 3,             # Normal sohbette de geçebilir
    "asker": 3,
    "hakim": 3,
    "sigorta borcu": 3,
    "kargo iadesi": 3,
    "günlük limit": 3,
    "para": 2,              # Çok genel
    "güncelleme": 2,
    "bilgi doğrulama": 2,
    "müşteri hizmetleri": 1,
    "kayıt altında": 1
}