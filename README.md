# 🛡️ ShieldX - Dolandırıcılık ve Tehdit Engelleme Platformu

**ShieldX**, sahte aramaları (özellikle WhatsApp `+145`, `+234` vb. sanal numaralar), görüntülü şantaj tuzaklarını, cevapsız çağrıları (Wangiri) ve bahis/oltama SMS'lerini tespit eden açık kaynaklı bir güvenlik sistemidir.

🌐 **Canlı Web Sitesi:** [https://shieldx-h7nw.onrender.com](https://shieldx-h7nw.onrender.com)

---

## 🚀 Özellikler

- **Canlı Web Taraması (Web Scraping):** Şüpheli numaraları anında internetteki şikayet sitelerinde ve forumlarda aratır.
- **Alan Kodu & Sanal Numara Tespiti:** Şantaj ve bot aramalarında kullanılan yurt dışı / sanal hatları otomatik tespit eder.
- **Risk Skoru Analizi:** Gelen veriye göre %0 ile %100 arasında canlı kritiklik seviyesi ve tavsiyeler üretir.
- **Kullanıcı Dostu Arayüz:** Modern, karanlık tema (Dark Mode) destekli web paneli.

---

## 💻 Kendi Bilgisayarınızda veya Sunucunuzda Kurun (Self-Hosted)

Projeyi kendi ortamınızda çalıştırabilirsiniz:

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/kullanici-adi/ShieldX.git](https://github.com/kullanici-adi/ShieldX.git)
cd ShieldX
```

### 2. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Çalıştırın

```bash
python app.py
```

### 4. Tarayıcınızda Açın

```
http://127.0.0.1:5000
```

---

### 🛠️ Kullanılan Teknolojiler

- **Backend**: Python 3, Flask, Requests, BeautifulSoup4

- **Frontend**: HTML5, CSS3, JavaScript (Fetch API)

- **Deployment**: Render, Gunicorn