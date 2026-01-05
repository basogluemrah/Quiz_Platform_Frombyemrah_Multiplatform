# 🎓 Quiz Platformu

Modern, şık ve kullanımı kolay çoklu ders quiz platformu.

![Quiz Platformu](https://img.shields.io/badge/Platform-Quiz-6366f1?style=for-the-badge)
![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?style=for-the-badge&logo=vite)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 🌐 Demo

**[quiz-platform-frombyemrah-multiplat.vercel.app](https://quiz-platform-frombyemrah-multiplat.vercel.app)**

---

## ✨ Özellikler

- 📚 **Çoklu Ders Desteği** - Farklı dersler ekleyebilme
- 🎲 **Karışık Quiz Modu** - Tüm ünitelerden rastgele sorular
- 🎧 **Medya Desteği** - Ses ve video dosyaları
- 🎛️ **Admin Paneli** - Şifre korumalı içerik yönetimi
- 📱 **Responsive Tasarım** - Mobil uyumlu
- 🌙 **Dark Theme** - Göz yormayan modern tasarım

---

## 🚀 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/basogluemrah/Quiz_Platform_Frombyemrah_Multiplatform.git

# Klasöre gir
cd Quiz_Platform_Frombyemrah_Multiplatform

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```

Site `http://localhost:3000` adresinde açılacak.

---

## 📁 Proje Yapısı

```
├── index.html          # Ana sayfa
├── admin.html          # Admin paneli
├── src/
│   ├── main.js         # Quiz mantığı
│   ├── admin.js        # Admin panel mantığı
│   ├── style.css       # Stiller
│   ├── admin.css       # Admin stiller
│   └── data/
│       ├── courses.json
│       └── isg/        # İSG dersi
│           ├── units.json
│           ├── audio.json
│           └── unit1-11.json
└── public/
    └── audio/          # Medya dosyaları
```

---

## 🎛️ Admin Paneli

**URL:** `/admin.html`  
**Şifre:** `quiz2024`

Admin panelden:
- Yeni ders oluşturma
- Ünite ekleme
- Soru ekleme
- Medya yönetimi

---

## 📝 Yeni Ders Ekleme

1. Admin panele git
2. "Dersler" sekmesini seç
3. Formu doldur
4. JSON dosyalarını indir
5. `src/data/` klasörüne koy

---

## 🛠️ Teknolojiler

- **Vite** - Hızlı geliştirme ortamı
- **Vanilla JS** - Framework bağımsız
- **CSS3** - Modern stiller, animasyonlar
- **Vercel** - Hosting

---

## 👤 Geliştirici

**Emrah Başoğlu**

---

## 📄 Lisans

MIT License
