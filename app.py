from flask import Flask, render_template, request, jsonify
import re
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

class ShieldXWebEngine:
    def __init__(self):
        self.risky_country_codes = {
            "+145": "Kuzey Amerika Sanal Hat (Şantaj / Bot)",
            "+184": "Sanal Numara Servisi",
            "+180": "Sanal Oltalama Numarası",
            "+234": "Nijerya Sanal Dolandırıcılık",
            "+254": "Kenya Ödül Tuzağı",
            "+92": "Pakistan Şüpheli Çağrı",
            "+62": "Endonezya İş İlanı Tuzağı",
            "+212": "Fas Çaldır-Kapat (Wangiri)",
            "0850": "850'li İnternet Hattı (Sahte Çağrı Merkezi / İnternet Taahhüt Tuzağı Riski)",
            "+90850": "850'li İnternet Hattı (Sahte Çağrı Merkezi / Taahhüt Tuzağı Riski)",
            "0212": "İstanbul Avrupa Yakası Hat (Sahte Hukuk / İcra Şantajı Taraması)",
            "0216": "İstanbul Anadolu Yakası Hat (Sahte Müşteri Hizmetleri Taraması)"
        }

    # --- İNTERNETTE ANLIK DOLANDIRICI ARAMA FONKSİYONU ---
    def search_web_for_scam(self, number):
        if not number or len(number) < 5:
            return None
        
        try:
            # Google/İnternet üzerinde numarayı arat
            clean_num = number.replace("+", "").replace(" ", "")
            search_url = f"https://html.duckduckgo.com/html/?q={clean_num}+dolandirici+sikayet"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            
            response = requests.get(search_url, headers=headers, timeout=4)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('a', class_='result__snippet')
                
                found_snippets = []
                for res in results[:3]: # İlk 3 internet sonucunu al
                    text = res.get_text()
                    if any(w in text.lower() for w in ["dolandırıcı", "açmayın", "şantaj", "şikayet", "sanal"]):
                        found_snippets.append(text)
                
                if found_snippets:
                    return found_snippets
        except Exception:
            pass
        return None

    def analyze(self, number, call_type, message):
        score = 0
        reasons = []
        advice = []

        # Yerli Numara Blokları Taraması (0850, 0212 vb.)
        for l_code, l_desc in self.risky_local_codes.items():
            if clean_number.startswith(l_code):
                score += 20
                reasons.append(f"📞 Yerli Numara Bloğu Tespiti: {l_code} ({l_desc})")
                break

        clean_number = number.strip().replace(" ", "").replace("-", "")
        message_lower = message.lower().strip()

        # 1. Alan Kodu Analizi
        if clean_number:
            for code, desc in self.risky_country_codes.items():
                if clean_number.startswith(code):
                    score += 55
                    reasons.append(f"🚨 YÜKSEK TEHDİT NUMARASI: {code} ({desc})")
                    break

            # İNTERNETTE CANLI ARAMA YAP
            web_results = self.search_web_for_scam(clean_number)
            if web_results:
                score += 35
                reasons.append("🌐 İNTERNET BULGUSU: Bu numara hakkında web üzerinde dolandırıcılık/şikayet kayıtları bulundu!")
                for snippet in web_results:
                    reasons.append(f"🔍 Web Alıntısı: \"{snippet[:120]}...\"")

        # 2. Arama Tipi Analizi
        if call_type == "video_call":
            score += 40
            reasons.append("📹 Görüntülü Arama Tespiti (Ekran kaydı & Şantaj Riski)")
            advice.append("❌ Kameranızı kapatın, yüzünüzü asla göstermeyin.")
        elif call_type == "missed_call":
            score += 30
            reasons.append("📞 Cevapsız Çağrı (Çaldır-Kapat / Wangiri Tuzağı)")
            advice.append("❌ Numarayı geri aramayın.")

        # 3. Mesaj Taraması
        if any(w in message_lower for w in ["yardim edebilin mi", "kardeş", "kardesim", "stok", "1000 tl", "bonus"]):
            score += 30
            reasons.append("💬 Şüpheli Mesaj / Duygu İstismarı Tespiti")

        final_score = min(score, 100)

        if final_score >= 65:
            level = "CRITICAL / TEHLİKELİ DOLANDIRICI"
            color = "#ef4444"
            advice.append("⛔ Numarayı derhal engelleyin.")
        elif final_score >= 30:
            level = "MEDIUM / ŞÜPHELİ ARAMA"
            color = "#f59e0b"
            advice.append("⚠️ Şüpheli numara/mesaj. Yanıt vermeyin.")
        else:
            level = "SAFE / TEMİZ"
            color = "#10b981"
            advice.append("✅ Belirgin bir risk faktörü bulunamadı.")

        return {
            "score": final_score,
            "level": level,
            "color": color,
            "reasons": reasons,
            "advice": advice
        }

engine = ShieldXWebEngine()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    data = request.get_json() or {}
    result = engine.analyze(
        data.get('number', ''), 
        data.get('call_type', 'none'), 
        data.get('message', '')
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)