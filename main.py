import tkinter as tk
from tkinter import ttk, messagebox
import random
import sqlite3
import time

# İçe aktardığınız modüller
from imei_uretme_modulu import generate_imeis
from proxy_manager import ProxyManager
from sorgu_modulu import Client
from veritabani_modulu import VeritabaniYonetici

class App:
    def __init__(self, root, api_urls):
        self.root = root
        self.paused = False
        self.api_urls = api_urls  # API URL'sini App sınıfına ekleyin
        self.create_widgets()
        self.imei_entry = ttk.Combobox(root, width=16)
        self.imei_entry.grid(pady=5)
        self.client = Client(api_urls=self.api_urls)  # ProxyManager API URL'sini buraya ekleyin
        self.proxy_manager = ProxyManager(api_urls=self.api_urls) 
    def add_to_database(self, imei, device_model="Unknown"):
        existing_imei = self.get_all_imeis()
        if imei in existing_imei:
            self.log_display.config(state='normal')
            self.log_display.insert(tk.END, f"IMEI {imei} zaten veritabanında kayıtlı!\n")
            self.log_display.config(state='disabled')
        else:
            self.add_imei(imei, device_model)
            self.log_display.config(state='normal')
            self.log_display.insert(tk.END, f"IMEI {imei} veritabanına eklendi.\n")
            self.log_display.config(state='disabled')

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Devam Ettir", style="Green.TButton")
        else:
            self.pause_button.config(text="Durdur", style="Red.TButton")

    def sorgula(self, imei=None, show_message=True):
        global client  # Add global variables here

        if not imei:
            imei = self.imei_combobox.get()
            if len(imei) != 15 or not imei.isdigit():
                if show_message:
                    messagebox.showerror(
                        "Hata", "IMEI numarası 15 haneli bir sayı olmalıdır."
                    )
                return
            if imei in self.log_display.get(1.0, tk.END):  # Log'daki mevcut IMEI'leri kontrol etmek için
                if show_message:
                    messagebox.showwarning(
                        "Uyarı",
                        "Bu IMEI daha önce kullanılmış. Lütfen farklı bir IMEI seçin.",
                    )
                return
            start_time = time.time()
            try:
                result = client.query(imei)
                end_time = time.time()
                if end_time - start_time > 6:
                    self.log_display.insert(
                        tk.END, f"{imei} tekrar denenmek üzere sıraya alındı.\n"
                    )
                    return
                if show_message:
                    messagebox.showinfo("Sorgu Sonucu", result)
                self.log_display.insert(tk.END, result + "\n")
            except Exception as e:
                self.log_display.insert(tk.END, f"Hata: {str(e)}\n")


    def imei_uret(self):
        yeni_imei = generate_imeis(self.imei_entry.get(), 10)
        self.imei_entry.delete(0, tk.END)
        self.imei_entry.insert(0, yeni_imei)
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, f"Yeni IMEI üretildi: {yeni_imei}\n")
        self.log_display.config(state='disabled')

    def proxy_ayarlarini_goster(self):
        current_proxy = self.get_proxy()
        self.proxy_entry.delete(0, tk.END)
        if current_proxy:
            self.proxy_entry.insert(0, current_proxy)
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, f"Aktif Proxy: {current_proxy if current_proxy else 'Yok'}\n")
        self.log_display.config(state='disabled')
        
    def query_imei(self):
        imei = self.imei_entry.get().strip()
        if imei:
            result = self.client.query(imei)
            self.operations_log.insert(0, result)

    def get_proxy(self):
        # Burada proxy almak için gerekli kodu ekleyin
        return self.proxy_manager.get_proxy() 

    def create_widgets(self):
        # Ana çerçeve
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Stilleri tanımla
        style = ttk.Style()
        style.configure("Green.TButton", foreground="white", background="#4CAF50")
        style.configure("Red.TButton", foreground="white", background="#FF5722")

        # Sol Frame (frame_a)
        frame_a = ttk.Frame(main_frame)
        frame_a.grid(row=0, column=0, sticky="nsew")
        frame_a.config(width=main_frame.winfo_width(), height=main_frame.winfo_height())

        # Sağ Frame (frame_b)
        frame_b = ttk.Frame(main_frame)
        frame_b.grid(row=0, column=1, sticky="nsew")
        frame_b.config(width=main_frame.winfo_width(), height=main_frame.winfo_height())

        # Sol Frame (frame_a) Bileşenleri
        self.log_label = tk.Label(frame_a, text="Log Gösterge Paneli:")
        self.log_label.grid(pady=5)
        
        self.log_display = tk.Text(frame_a, width=35, height=3, state='disabled')
        self.log_display.grid(pady=5)

        self.imei_etiketi = tk.Label(frame_a, text="IMEI NUMARASI:")
        self.imei_etiketi.grid(pady=10)

        self.imei_combobox = ttk.Combobox(frame_a, width=16)
        self.imei_combobox.grid(pady=5)

        self.sorgula_dugmesi = ttk.Button(frame_a, text="Sorgula", width=16, command=self.sorgula)
        self.sorgula_dugmesi.grid(pady=5)

        self.imei_uret_button = ttk.Button(frame_a, text="IMEI Üret", width=16, command=self.imei_uret)
        self.imei_uret_button.grid(pady=5)

        self.proxy_ayar_button = ttk.Button(frame_a, text="Proxy Ayarları", width=16, command=self.proxy_ayarlarini_goster)
        self.proxy_ayar_button.grid(pady=5)

        self.proxy_label = tk.Label(frame_a, text="PROXY LISTESI:")
        self.proxy_label.grid(pady=5)

        self.proxy_entry = ttk.Combobox(frame_a, width=16)
        self.proxy_entry.grid(pady=5)

        # Sağ Frame (frame_b) Bileşenleri
        self.model_label = tk.Label(frame_b, text="Cihaz Modelleri:")
        self.model_label.grid(pady=5)

        self.model_combobox = ttk.Combobox(frame_b, width=35)
        self.model_combobox.grid(pady=5)

        self.imei_list_label = tk.Label(frame_b, text="IMEI Listesi:")
        self.imei_list_label.grid(pady=5)

        self.imei_listbox = tk.Listbox(frame_b, width=40, height=10)
        self.imei_listbox.grid(pady=5)

        self.progress_label = tk.Label(frame_b, text="İşlem İlerleme Durumu:")
        self.progress_label.grid(pady=5)

        self.progress_bar = ttk.Progressbar(frame_b, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(pady=5)


        self.proxy_status_label = tk.Label(frame_b, text="Çalışan Proxy Sayısı: ?/?")
        self.proxy_status_label.grid(pady=5)

        self.pause_button = tk.Button(frame_b, text="Durdur", bg="#FF5722", fg="white", width=20, command=self.toggle_pause)
        self.pause_button.grid(pady=5)

if __name__ == "__main__":
    db = VeritabaniYonetici()
    db.tablolari_olustur()

    api_urls = "https://proxy-manager-api-url.com"  # Kullanmak istediğiniz API URL'sini burada belirtin

    root = tk.Tk()
    root.title("IMEI Sorgulama")

    app = App(root, api_urls=api_urls)  # API URL'sini geçirin

    root.mainloop()
