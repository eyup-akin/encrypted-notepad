import customtkinter as ctk
from tkinter import messagebox
from backend.auth import UserManager
from backend.crypto import SecurityManager

# --- MODERN AYARLAR ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class LoginWindow(ctk.CTk):
    def __init__(self, on_success_callback):
        super().__init__()
        self.on_success = on_success_callback
        self.user_manager = UserManager()

        self.title("Giriş Yap - SecureNotes")
        self.geometry("400x450")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self, width=320, height=360, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.frame, text="HOŞ GELDİNİZ", font=("Roboto Medium", 20)).place(relx=0.5, rely=0.15,
                                                                                        anchor="center")

        self.entry_user = ctk.CTkEntry(self.frame, width=220, placeholder_text="Kullanıcı Adı")
        self.entry_user.place(relx=0.5, rely=0.35, anchor="center")

        self.entry_pass = ctk.CTkEntry(self.frame, width=220, placeholder_text="Parola", show="*")
        self.entry_pass.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(self.frame, text="GİRİŞ YAP", command=self.login, width=220, height=40, corner_radius=20).place(
            relx=0.5, rely=0.7, anchor="center")
        ctk.CTkButton(self.frame, text="HESAP OLUŞTUR", command=self.register, width=220, height=30,
                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE")).place(relx=0.5,
                                                                                                      rely=0.85,
                                                                                                      anchor="center")

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        success, msg = self.user_manager.login_user(user, pwd)
        if success:
            self.on_success(user, pwd)
        else:
            messagebox.showerror("Hata", msg)

    def register(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        if not user or not pwd:
            messagebox.showwarning("Uyarı", "Alanlar boş olamaz!")
            return
        success, msg = self.user_manager.register_user(user, pwd)
        if success:
            messagebox.showinfo("Başarılı", msg)
        else:
            messagebox.showerror("Hata", msg)


class SecureNotepadApp(ctk.CTk):
    # DİKKAT: logout_callback parametresi eklendi
    def __init__(self, username, password, logout_callback):
        super().__init__()
        self.username = username
        self.logout_callback = logout_callback  # Main'e geri dönmek için anahtar

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
        self.sidebar_frame.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="SECURE NOTES", font=("Roboto", 20, "bold")).grid(row=0, column=0,
                                                                                                padx=20, pady=20)

        self.btn_new = ctk.CTkButton(self.sidebar_frame, text="+ YENİ NOT", command=self.new_note,
                                     height=40, corner_radius=10, fg_color="#2CC985", hover_color="#229A65",
                                     font=("Roboto", 14, "bold"), text_color="white")
        self.btn_new.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.scrollable_list = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Notlarım")
        self.scrollable_list.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # --- ALT BUTONLAR (SIDEBAR) ---
        # Butonlar için ayrı bir frame yapalım ki düzenli dursun
        bottom_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        bottom_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # 1. Kaydet ve Çık Butonu
        self.btn_save_exit = ctk.CTkButton(bottom_frame, text="🔒 ŞİFRELE & ÇIK", command=self.save_and_exit,
                                           fg_color="#34495E", hover_color="#2C3E50")
        self.btn_save_exit.pack(fill="x", pady=5)

        # 2. YENİ EKLENEN: HESABI SİL BUTONU
        self.btn_delete_account = ctk.CTkButton(bottom_frame, text="⚠️ HESABI SİL",
                                                command=self.delete_account_permanently, fg_color="#C0392B",
                                                hover_color="#922B21")
        self.btn_delete_account.pack(fill="x", pady=5)

        # --- SAĞ PANEL ---
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

        self.update_sidebar_list()

    def update_sidebar_list(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        for title in self.notes:
            btn = ctk.CTkButton(self.scrollable_list, text=title, anchor="w",
                                command=lambda t=title: self.load_note_content(t),
                                fg_color="transparent", border_width=1, border_color="#3E454F",
                                text_color=("gray10", "#DCE4EE"), hover_color=("gray70", "#2B2B2B"))
            btn.pack(fill="x", pady=2)

    def new_note(self):
        self.entry_title.delete(0, "end")
        self.text_content.delete("0.0", "end")
        self.entry_title.focus()

    def load_note_content(self, title):
        content = self.notes.get(title, "")
        self.new_note()
        self.entry_title.insert(0, title)
        self.text_content.insert("0.0", content)

    def save_to_ram(self):
        title = self.entry_title.get()
        content = self.text_content.get("0.0", "end").strip()
        if not title:
            messagebox.showwarning("Eksik", "Lütfen bir başlık girin.")
            return
        self.notes[title] = content
        self.update_sidebar_list()
        # Kayıt bildirimi yerine butonu yanıp söndürebilirsin ama şimdilik pop-up yeterli
        # messagebox.showinfo("Başarılı", "Not geçici belleğe alındı.")

    def delete_note(self):
        title = self.entry_title.get()
        if title in self.notes:
            if messagebox.askyesno("Onay", f"'{title}' notunu silmek istediğine emin misin?"):
                del self.notes[title]
                self.new_note()
                self.update_sidebar_list()
        else:
            messagebox.showwarning("Hata", "Silinecek kayıtlı bir not seçilmedi.")

    def save_and_exit(self):
        try:
            self.manager.encrypt_and_save(self.notes, self.filename)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Kritik Hata", str(e))

    # --- HESAP SİLME FONKSİYONU ---
    def delete_account_permanently(self):
        confirm = messagebox.askyesno("DİKKAT",
                                      "Bu işlem GERİ ALINAMAZ!\n\nHesabınız ve tüm şifreli notlarınız kalıcı olarak silinecek.\nDevam etmek istiyor musunuz?")
        if confirm:
            user_mgr = UserManager()
            success, msg = user_mgr.delete_user(self.username)

            if success:
                messagebox.showinfo("Hoşçakal", msg)
                self.destroy()  # Uygulamayı kapat
                self.logout_callback()  # Login ekranını geri çağır
            else:
                messagebox.showerror("Hata", msg)