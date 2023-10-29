import re
import requests
import logging
from functools import lru_cache
from proxy_manager import ProxyManager
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Client:
    def __init__(self, api_urls):
        self.proxy_manager = ProxyManager(api_urls)
        self.URL = "https://www.turkiye.gov.tr/imei-sorgulama"
        self.session = requests.Session()
        self.token = None
        self.ua = UserAgent()
        self.session.headers['User-Agent'] = self.ua.random 
        self.selected_proxies = []

        # Loglama için ayarlar
        logging.basicConfig(level=logging.INFO)

    @lru_cache(maxsize=1000)
    def query(self, imei):
        if not re.match(r'^\d{15}$', imei):
            return f"IMEI: {imei} - Geçersiz IMEI formatı"
        
        try:
            if not self.token or "token" not in self.session.cookies:
                response = self.session.get(self.URL)
                self.token = re.search(r'name="token" value="([^"]+)"', response.text).group(1)
            data = {"txtImei": imei, "token": self.token}
            self.session.headers['User-Agent'] = self.ua.random 
            
            if self.selected_proxies:
                proxy = self.selected_proxies.pop()
            else:
                proxy = self.proxy_manager.get_proxy()
            
            response_content = self.session.post(self.URL + "?submit", data=data, proxies={"http": proxy, "https": proxy}).text

            soup = BeautifulSoup(response_content, 'html.parser')
            results = soup.find_all('dd')

            if len(results) >= 4:
                imei_value = results[0].text.strip()
                durum_value = results[1].text.strip()
                sorgu_tarihi_value = results[2].text.strip()
                
                # Marka/Model bilgisini çıkarmak için "Marka: " metnini kaldıralım
                marka_model_dd = soup.find("dt", text="Marka/Model")
                if marka_model_dd:
                    marka_model_text = marka_model_dd.find_next("dd").text.strip()
                    # "Marka: " metnini kaldır
                    marka_model_parts = marka_model_text.split("Model Bilgileri:")
                    if len(marka_model_parts) == 2:
                        marka_model_value = marka_model_parts[1].strip()
                    else:
                        marka_model_value = marka_model_text.strip()
                else:
                    marka_model_value = ""

                original_result = (
                    f"IMEI: {imei_value}\n"
                    f"Durum: {durum_value}\n"
                    f"Marka/Model: {marka_model_value}\n"
                    f"Proxy: {proxy}"
                )

                # Kayıtlı IMEI'leri yeşil, kayıtsızları kırmızı yapalım
                if "IMEI NUMARASI KAYITLI" in durum_value:
                    return f"\033[92m{original_result}\033[0m"
                else:
                    return f"\033[91m{original_result}\033[0m"
            else:
                return f"IMEI: {imei} - Bilgi bulunamadı - {proxy}"

        except requests.ConnectionError:
            logging.error(f"IMEI: {imei} - Bağlantı hatası")
            return f"IMEI: {imei} - Bağlantı hatası"
        except requests.Timeout:
            logging.error(f"IMEI: {imei} - Zaman aşımı hatası")
            return f"IMEI: {imei} - Zaman aşımı hatası"
        except Exception as e:
            logging.error(f"IMEI: {imei} - Hata: {e}")
            return f"IMEI: {imei} - Hata: {e}"

if __name__ == "__main__":
    client = Client()
    result = client.query("355115063353731")
    print(result)
