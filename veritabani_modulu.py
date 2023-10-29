# veritabani_modulu.py

import sqlite3

class VeritabaniYonetici:
    def __init__(self, veritabani_dosyasi='veritabani.db'):
        self.baglanti = sqlite3.connect(veritabani_dosyasi)
        self.cursor = self.baglanti.cursor()
        self.tablolari_olustur()

    def tablolari_olustur(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS imei_bilgileri (
            id INTEGER PRIMARY KEY,
            imei TEXT NOT NULL,
            marka TEXT,
            model TEXT,
            durum TEXT,
            kullaniliyor_mu BOOLEAN
        )
        """)
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS proxy_listesi (
            id INTEGER PRIMARY KEY,
            proxy_adresi TEXT NOT NULL,
            kullanım_durumu TEXT,
            karaliste BOOLEAN,
            test_bekleyen_mi BOOLEAN
        )
        """)
        self.baglanti.commit()

    # IMEI fonksiyonları
    def imei_ekle(self, imei, marka, model, durum, kullaniliyor_mu):
        self.cursor.execute("INSERT INTO imei_bilgileri (imei, marka, model, durum, kullaniliyor_mu) VALUES (?, ?, ?, ?, ?)", (imei, marka, model, durum, kullaniliyor_mu))
        self.baglanti.commit()

    def imei_guncelle(self, imei_id, **kwargs):
        sorgu_parcalari = [f"{k} = ?" for k in kwargs]
        sorgu_metni = "UPDATE imei_bilgileri SET " + ", ".join(sorgu_parcalari) + " WHERE id = ?"
        degerler = list(kwargs.values()) + [imei_id]
        self.cursor.execute(sorgu_metni, degerler)
        self.baglanti.commit()

    # Proxy fonksiyonları
    def proxy_ekle(self, proxy_adresi, kullanım_durumu, karaliste, test_bekleyen_mi):
        self.cursor.execute("INSERT INTO proxy_listesi (proxy_adresi, kullanım_durumu, karaliste, test_bekleyen_mi) VALUES (?, ?, ?, ?)", (proxy_adresi, kullanım_durumu, karaliste, test_bekleyen_mi))
        self.baglanti.commit()

    def proxy_guncelle(self, proxy_id, **kwargs):
        sorgu_parcalari = [f"{k} = ?" for k in kwargs]
        sorgu_metni = "UPDATE proxy_listesi SET " + ", ".join(sorgu_parcalari) + " WHERE id = ?"
        degerler = list(kwargs.values()) + [proxy_id]
        self.cursor.execute(sorgu_metni, degerler)
        self.baglanti.commit()

    def imei_kullanim_durumu(self, imei):
        self.cursor.execute("SELECT kullaniliyor_mu FROM imei_bilgileri WHERE imei = ?", (imei,))
        sonuc = self.cursor.fetchone()
        if sonuc:
            return sonuc[0]
        return None

    # Proxy fonksiyonları için kullanım durumu
    def proxy_kullanim_durumu(self, proxy_adresi):
        self.cursor.execute("SELECT kullanım_durumu FROM proxy_listesi WHERE proxy_adresi = ?", (proxy_adresi,))
        sonuc = self.cursor.fetchone()
        if sonuc:
            return sonuc[0]
        return None

    # Genel fonksiyonlar
    def kapat(self):
        self.baglanti.close()

# Kullanım örneği:
# db = VeritabaniYonetici()
# db.imei_ekle("123456789012345", "Apple", "iPhone 12", "Aktif", True)
# db.proxy_ekle("192.168.1.1:8080", "Kullanımda", False, True)
# db.kapat()
