import requests
import collections
import random
import time
from concurrent.futures import ThreadPoolExecutor

class VeritabaniYonetici:
    def __init__(self):
        # Veritabanına bağlanın
        pass
    def get_all_proxies(self):
        # Tüm proxy'leri veritabanından alın
        pass

class ProxyManager:
    def __init__(self, api_urls):
        self.db_manager = VeritabaniYonetici()
        self.proxies = collections.deque()
        self.api_urls = api_urls
    def get_proxy(self):
        if not self.proxies:
            self.refresh_proxies()
        return self.proxies.popleft()
    def refresh_proxies(self):
        for api_url in self.api_urls:
            response = requests.get(api_url)
            proxy_list = response.text.split('\n')
            for proxy in proxy_list:
                if proxy:
                    self.proxies.append(proxy)
    def is_working(self):
        for _ in range(100):
            proxy = self.get_proxy()
            proxies = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
            try:
                response = requests.get(
                    "https://www.google.com",
                    proxies=proxies,
                    timeout=5
                )
                return True
            except requests.exceptions.RequestException:
                pass
        return False

if __name__ == "__main__":
    api_urls = [
        "https://www.proxynova.com/api/v1/proxy.php?format=json&country=TR",
        "https://hidemy.name/proxy-list/?country=TR",
        "https://free-proxy-list.net/api/v1/?limit=10&country=TR",
        "https://sslproxies.org/api/v1/?country=TR&protocol=http&sort=reliability&page=1",
        "https://proxylistpro.com/v2/?type=http&country=TR&limit=10&sort=reliability",
        "https://proxy-list.org/type=http&anon=elite&sort=reliability",
        "https://proxy-scraper.com/?protocol=http",
        "https://proxyscrape.com/",
        "https://proxydb.net/v2/",
        "https://www.my-proxy.net/api/get_proxy.php?protocol=https",
        "https://spys.one/en/free-proxy-list/TR/",
        "https://free-proxy.cz/en/proxylist/country/TR/https/",
        "https://proxylist.org.ua/en/HTTPS",
        "https://premproxy.com/proxy-list/elite-proxy",
        "https://fastproxies.co/elite-proxy",
        "https://freeproxylists.net/HTTPS-Proxy-List",
        "https://list.proxylistplus.com/HTTPS-Proxy-List",
        "https://fineproxy.org/proxy-list/HTTPS",
    ]

    proxy_manager = ProxyManager(api_urls)

    while True:
        if proxy_manager.is_working():
            print("proxy-ok")
            break
        else:
            time.sleep(1)
