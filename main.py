import customtkinter as ctk
# ÖNCEKİ: from frontend.interface import LoginWindow, SecureNotepadApp
# YENİ HALİ: İlgili dosyalardan ayrı ayrı çekiyoruz
from frontend.login_ui import LoginWindow
from frontend.main_ui import SecureNotepadApp

# Global değişkenler (Pencereleri yönetmek için)
login_app = None
main_app = None

def show_login_screen():
    """Login penceresini başlatır."""
    global login_app
    # Eğer ana uygulama açıksa kapatıldığından emin ol
    if main_app:
        try:
            main_app.destroy()
        except:
            pass

    login_app = LoginWindow(on_success_callback=show_main_app)
    login_app.mainloop()


def show_main_app(username, password):
    """Ana uygulamayı başlatır."""
    global main_app, login_app

    # Login penceresini kapat
    if login_app:
        login_app.destroy()

    # Ana uygulamayı başlat ve ona "çıkış yaparsam login'i aç" komutunu ver
    main_app = SecureNotepadApp(username, password, logout_callback=show_login_screen)
    main_app.mainloop()


if __name__ == "__main__":
    show_login_screen()