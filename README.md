# 🔒 Secure Encrypted Notepad / Güvenli Şifreli Not Defteri

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Security](https://img.shields.io/badge/security-AES--256-red?style=for-the-badge)

[English](#english) | [Türkçe](#türkçe)

---

<a name="english"></a>
## 🇺🇸 English

**Secure Encrypted Notepad** is a desktop application built with **Python** and **CustomTkinter**, designed to keep your personal notes safe. It uses industry-standard **AES-256 encryption** (via PBKDF2HMAC key derivation) to store your data securely on your local disk.

### 🚀 Features
* **Modern UI:** A clean, dark-mode interface built with CustomTkinter.
* **Strong Encryption:** Notes are encrypted using AES-256. Each save generates a unique salt.
* **User Management:** Multi-user support with secure login/registration.
* **Privacy Focused:** "Delete Account" feature permanently wipes all user data and files.
* **Local Storage:** No cloud uploads. Your data stays on your machine.

### 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/eyup-akin/encrypted-notepad.git](https://github.com/eyup-akin/encrypted-notepad.git)
    cd encrypted-notepad
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python main.py
    ```

### 🖥️ Desktop Shortcut (Linux)
To launch the app from your desktop/menu instead of the terminal:

1.  Create a file named `SecureNotes.desktop` in `~/.local/share/applications/` or on your Desktop.
2.  Paste the following content (Update paths with your username!):

    ```ini
    [Desktop Entry]
    Type=Application
    Name=Secure Notes
    Comment=Encrypted Notepad
    # Replace 'YOUR_USER' with your actual username
    Exec=/home/YOUR_USER/encrypted-notepad/.venv/bin/python /home/YOUR_USER/encrypted-notepad/main.py
    Path=/home/YOUR_USER/encrypted-notepad/
    Icon=text-editor
    Terminal=false
    Categories=Utility;Office;
    ```
3.  Make it executable (Right Click -> Properties -> Permissions -> Allow executing file as program).

---

<a name="türkçe"></a>
## 🇹🇷 Türkçe

**Güvenli Şifreli Not Defteri**, kişisel notlarınızı güvende tutmak için **Python** ve **CustomTkinter** ile geliştirilmiş bir masaüstü uygulamasıdır. Verilerinizi yerel diskinizde saklarken endüstri standardı **AES-256 şifreleme** (PBKDF2HMAC anahtar türetme ile) kullanır.

### 🚀 Özellikler
* **Modern Arayüz:** CustomTkinter ile tasarlanmış şık Karanlık Mod (Dark Mode).
* **Güçlü Şifreleme:** Notlar AES-256 ile şifrelenir. Her kayıt işleminde benzersiz bir "Salt" (Tuzlama) kullanılır.
* **Kullanıcı Yönetimi:** Güvenli kayıt ve giriş sistemi ile çoklu kullanıcı desteği.
* **Gizlilik Odaklı:** "Hesabı Sil" özelliği, kullanıcıya ait tüm şifreli dosyaları kalıcı olarak yok eder.
* **Yerel Depolama:** Bulut yok. Verileriniz sadece sizin bilgisayarınızda.

### 🛠️ Kurulum

1.  **Projeyi klonlayın:**
    ```bash
    git clone [https://github.com/eyup-akin/encrypted-notepad.git](https://github.com/eyup-akin/encrypted-notepad.git)
    cd encrypted-notepad
    ```

2.  **Sanal ortam oluşturun (Önerilen):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı başlatın:**
    ```bash
    python main.py
    ```

### 🖥️ Masaüstü Kısayolu Oluşturma (Linux)
Uygulamayı terminal yerine masaüstünden tek tıkla açmak için:

1.  Masaüstünde `SecureNotes.desktop` adında boş bir dosya oluşturun.
2.  Dosyayı açın ve aşağıdaki kodları yapıştırın (**Dosya yollarındaki `kullanici_adi` kısmını kendinize göre düzenleyin!**):

    ```ini
    [Desktop Entry]
    Type=Application
    Name=Secure Notes
    Comment=Şifreli Not Defteri
    # Python yolu ve Main dosya yolu arasında boşluk olmalı
    Exec=/home/kullanici_adi/encrypted-notepad/.venv/bin/python /home/kullanici_adi/encrypted-notepad/main.py
    Path=/home/kullanici_adi/encrypted-notepad/
    Icon=text-editor
    Terminal=false
    Categories=Utility;Office;
    ```
3.  Dosyayı kaydedin.
4.  Sağ tıklayın -> **Özellikler** -> **İzinler** -> **Dosyayı bir program gibi çalıştırmaya izin ver** seçeneğini işaretleyin.

### ⚠️ Güvenlik Uyarısı
* Bu uygulama verileri yerel diskinizde `.bin` formatında şifreli saklar.
* Şifrenizi unutursanız notları kurtarmanın **hiçbir yolu yoktur.** (Backdoor bulunmaz).
