import customtkinter as ctk
from tkinter import messagebox
from backend.auth import UserManager

# Tema ayarları her dosyada tekrar edilebilir veya main.py'de bir kere yapılabilir.
# Garanti olsun diye buraya da ekliyoruz.
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

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