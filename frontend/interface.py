import customtkinter as ctk
from tkinter import messagebox
from backend.auth import UserManager
from backend.crypto import SecurityManager

# --- MODERN AYARLAR ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


# --- NETFLIX TARZI GİRİŞ EKRANI (DEĞİŞMEDİ) ---
class LoginWindow(ctk.CTk):
    def __init__(self, on_success_callback):
        super().__init__()
        self.on_success = on_success_callback
        self.user_manager = UserManager()

        self.title("Giriş Yap - SecureNotes")
        self.geometry("400x500")
        self.resizable(False, False)

        self.container = ctk.CTkFrame(self, corner_radius=15)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.show_profile_selection()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_profile_selection(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="KİM GİRİŞ YAPIYOR?", font=("Roboto Medium", 18)).pack(pady=(30, 20))

        users = self.user_manager.get_all_usernames()
        scroll_frame = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not users:
            ctk.CTkLabel(scroll_frame, text="Henüz kayıtlı kullanıcı yok.", text_color="gray").pack(pady=20)

        for user in users:
            btn = ctk.CTkButton(scroll_frame, text=user,
                                command=lambda u=user: self.show_password_input(u),
                                height=50, corner_radius=10,
                                fg_color="#2B2B2B", hover_color="#3A3A3A",
                                font=("Roboto", 16))
            btn.pack(fill="x", pady=5, padx=5)

        ctk.CTkButton(self.container, text="+ YENİ PROFİL OLUŞTUR", command=self.show_register_input,
                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                      height=40).pack(side="bottom", pady=20, padx=20, fill="x")

    def show_password_input(self, username):
        self.clear_container()
        ctk.CTkButton(self.container, text="< Geri", command=self.show_profile_selection,
                      width=60, fg_color="transparent", text_color="gray").pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(self.container, text=f"Merhaba, {username}", font=("Roboto", 22, "bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.container, text="Devam etmek için şifreni gir", font=("Roboto", 12), text_color="gray").pack(
            pady=(0, 20))

        self.entry_pass = ctk.CTkEntry(self.container, width=220, placeholder_text="Parola", show="*", height=40)
        self.entry_pass.pack(pady=10)
        self.entry_pass.bind("<Return>", lambda event: self.perform_login(username))

        ctk.CTkButton(self.container, text="GİRİŞ YAP",
                      command=lambda: self.perform_login(username),
                      width=220, height=40, corner_radius=20, fg_color="#2CC985", hover_color="#229A65").pack(pady=20)

    def show_register_input(self):
        self.clear_container()
        ctk.CTkButton(self.container, text="< Geri", command=self.show_profile_selection,
                      width=60, fg_color="transparent", text_color="gray").pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(self.container, text="YENİ PROFİL", font=("Roboto Medium", 20)).pack(pady=20)
        self.reg_user = ctk.CTkEntry(self.container, width=220, placeholder_text="Kullanıcı Adı")
        self.reg_user.pack(pady=10)
        self.reg_pass = ctk.CTkEntry(self.container, width=220, placeholder_text="Parola Oluştur", show="*")
        self.reg_pass.pack(pady=10)

        ctk.CTkButton(self.container, text="KAYDET VE GİRİŞ YAP", command=self.perform_register,
                      width=220, height=40, corner_radius=20).pack(pady=20)

    def perform_login(self, username):
        pwd = self.entry_pass.get()
        success, msg = self.user_manager.login_user(username, pwd)
        if success:
            self.on_success(username, pwd)
        else:
            messagebox.showerror("Hata", msg)
            self.entry_pass.delete(0, "end")

    def perform_register(self):
        user = self.reg_user.get()
        pwd = self.reg_pass.get()
        if not user or not pwd:
            messagebox.showwarning("Eksik", "Lütfen tüm alanları doldurun.")
            return
        success, msg = self.user_manager.register_user(user, pwd)
        if success:
            messagebox.showinfo("Başarılı", "Profil oluşturuldu!")
            self.show_profile_selection()
        else:
            messagebox.showerror("Hata", msg)


# --- ANA UYGULAMA (GÜNCELLENDİ: ARAMA ÇUBUĞU) ---
class SecureNotepadApp(ctk.CTk):
    def __init__(self, username, password, logout_callback):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback

        self.title(f"SecureNotes | {username}")
        self.geometry("1000x650")

        self.filename = f"notlar_{username}.bin"
        self.manager = SecurityManager(password)
        self.notes = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.load_data()
        self.setup_ui()

    def load_data(self):
        try:
            self.notes = self.manager.load_and_decrypt(self.filename)
        except ValueError:
            self.notes = {}

    def setup_ui(self):
        # --- SOL PANEL (SIDEBAR) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        # Grid ayarı: Arama çubuğu ve liste esnemeli
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        # Logo
        ctk.CTkLabel(self.sidebar_frame, text="SECURE NOTES", font=("Roboto", 20, "bold")).grid(row=0, column=0,
                                                                                                padx=20, pady=(20, 10))

        # Yeni Not Butonu
        self.btn_new = ctk.CTkButton(self.sidebar_frame, text="+ YENİ NOT", command=self.new_note,
                                     height=40, corner_radius=10, fg_color="#2CC985", hover_color="#229A65",
                                     font=("Roboto", 14, "bold"), text_color="white")
        self.btn_new.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # --- YENİ: ARAMA ÇUBUĞU ---
        self.entry_search = ctk.CTkEntry(self.sidebar_frame, placeholder_text="🔍 Ara...", height=35)
        self.entry_search.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="ew")
        # Tuş bırakıldığında (KeyRelease) filtreleme fonksiyonunu çağır
        self.entry_search.bind("<KeyRelease>", self.filter_notes)

        # Not Listesi
        self.scrollable_list = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Notlarım")
        self.scrollable_list.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        # Alt Butonlar
        bottom_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        bottom_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        self.btn_save_exit = ctk.CTkButton(bottom_frame, text="🔒 ŞİFRELE & ÇIK", command=self.save_and_exit,
                                           fg_color="#34495E", hover_color="#2C3E50")
        self.btn_save_exit.pack(fill="x", pady=5)

        self.btn_delete_account = ctk.CTkButton(bottom_frame, text="⚠️ HESABI SİL",
                                                command=self.delete_account_permanently, fg_color="#C0392B",
                                                hover_color="#922B21")
        self.btn_delete_account.pack(fill="x", pady=5)

        # --- SAĞ PANEL (EDİTÖR) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.entry_title = ctk.CTkEntry(self.main_frame, placeholder_text="Başlıksız Not...",
                                        font=("Roboto", 24, "bold"), height=50,
                                        border_width=0, fg_color="transparent")
        self.entry_title.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.text_content = ctk.CTkTextbox(self.main_frame, font=("Roboto", 16), undo=True)
        self.text_content.grid(row=1, column=0, sticky="nsew")

        self.action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, sticky="ew", pady=10)

        ctk.CTkButton(self.action_frame, text="Kaydet (RAM)", command=self.save_to_ram, width=100).pack(side="right",
                                                                                                        padx=5)
        ctk.CTkButton(self.action_frame, text="Notu Sil", command=self.delete_note, fg_color="#E67E22",
                      hover_color="#D35400", width=80).pack(side="right", padx=5)

        # Başlangıçta tüm listeyi göster
        self.update_sidebar_list()

    # --- YENİ: FİLTRELEME FONKSİYONU ---
    def filter_notes(self, event=None):
        """Arama kutusuna yazılan metne göre listeyi filtreler."""
        search_query = self.entry_search.get().lower()  # Küçük harfe çevir

        # Eğer kutu boşsa hepsini göster
        if not search_query:
            self.update_sidebar_list()
            return

        # Eşleşenleri bul (List Comprehension - Pythonic Way)
        filtered_notes = [title for title in self.notes if search_query in title.lower()]

        # Listeyi sadece filtreli olanlarla güncelle
        self.update_sidebar_list(filtered_notes)

    # Güncellendi: Artık opsiyonel olarak bir liste alabiliyor
    def update_sidebar_list(self, notes_to_show=None):
        # Eğer özel bir liste gelmediyse (filtre yoksa), hepsini göster
        if notes_to_show is None:
            notes_to_show = list(self.notes.keys())

        # Önce temizle
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        # Listeyi doldur
        for title in notes_to_show:
            btn = ctk.CTkButton(self.scrollable_list, text=title, anchor="w",
                                command=lambda t=title: self.load_note_content(t),
                                fg_color="transparent", border_width=1, border_color="#3E454F",
                                text_color=("gray10", "#DCE4EE"), hover_color=("gray70", "#2B2B2B"))
            btn.pack(fill="x", pady=2)

    def new_note(self):
        self.entry_title.delete(0, "end")
        self.text_content.delete("0.0", "end")
        self.entry_title.focus()
        # Yeni not oluştururken arama filtresini temizlemek kullanıcı dostu olur
        self.entry_search.delete(0, "end")
        self.update_sidebar_list()

    def load_note_content(self, title):
        content = self.notes.get(title, "")
        self.new_note()  # Ekranı temizle (Search bar'ı temizlemesin diye new_note içindeki temizlemeye dikkat)
        self.entry_title.insert(0, title)
        self.text_content.insert("0.0", content)

    def save_to_ram(self):
        title = self.entry_title.get()
        content = self.text_content.get("0.0", "end").strip()
        if not title:
            messagebox.showwarning("Eksik", "Lütfen bir başlık girin.")
            return
        self.notes[title] = content
        # Kaydedince arama filtresini temizle ve listeyi yenile
        self.entry_search.delete(0, "end")
        self.update_sidebar_list()

    def delete_note(self):
        title = self.entry_title.get()
        if title in self.notes:
            if messagebox.askyesno("Onay", f"'{title}' notunu silmek istediğine emin misin?"):
                del self.notes[title]
                self.new_note()
        else:
            messagebox.showwarning("Hata", "Silinecek kayıtlı bir not seçilmedi.")

    def save_and_exit(self):
        try:
            self.manager.encrypt_and_save(self.notes, self.filename)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Kritik Hata", str(e))

    def delete_account_permanently(self):
        confirm = messagebox.askyesno("DİKKAT",
                                      "Bu işlem GERİ ALINAMAZ!\n\nHesabınız ve tüm şifreli notlarınız kalıcı olarak silinecek.\nDevam etmek istiyor musunuz?")
        if confirm:
            user_mgr = UserManager()
            success, msg = user_mgr.delete_user(self.username)
            if success:
                messagebox.showinfo("Hoşçakal", msg)
                self.destroy()
                self.logout_callback()
            else:
                messagebox.showerror("Hata", msg)