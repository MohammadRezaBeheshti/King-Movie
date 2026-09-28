# 🎬 کینگ‌مووی | King-Movie

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Open Source](https://img.shields.io/badge/Open%20Source-❤️-red?style=for-the-badge)

<p align="center">
  <b>پلتفرم متن‌باز مدیریت کاتالوگ فیلم و سریال، پخش آنلاین ویدیو و دانلود با معماری مدرن و ماژولار مبتنی بر جنگو</b>
</p>

[گزارش باگ و مشکل](https://github.com/MohammadRezaBeheshti/King-Movie/issues) • [درخواست فیچر جدید](https://github.com/MohammadRezaBeheshti/King-Movie/issues) • [راهنمای مشارکت](#-راهنمای-مشارکت-و-همکاری-در-پروژه-contributing)

</div>

---

## 📖 درباره پروژه (About The Project)

**King-Movie** یک پروژه وب کامل و متن‌باز برای سرویس‌های استریم و کاتالوگ فیلم و سریال است. این سیستم با هدف ارائه یک تجربه کاربری سریع، زیبا و بهینه‌سازی‌شده برای دیتابیس‌های حجیم طراحی شده است.

در این پروژه، تفکیک وظایف (Separation of Concerns)، معماری ماژولار اپلیکیشن‌ها، امنیت بالا و رعایت استانداردهای کوئری‌نویسی ORM برای جلوگیری از مشکل N+1 در اولویت قرار گرفته است.

---

## ✨ ویژگی‌های کلیدی (Features)

- 🎥 **مدیریت کاتالوگ جامع:** پشتیبانی همزمان از فیلم سینمایی، سریال چندفصلی، انیمه و انیمیشن.
- 📺 **پخش آنلاین هوشمند (Streaming):** پلیر داخلی HTML5 با قابلیت جست‌وجو و پرش زمانی بدون نیاز به دانلود کل فایل (پشتیبانی از HTTP Byte-Range).
- 📥 **پشتیبانی از چند کیفیت و دوبله:** تعریف منابع چندگانه برای هر اثر (۱۰۸۰p, ۷۲۰p, ۴۸۰p, ۴K) به تفکیک نسخه زیرنویس چسبیده و دوبله فارسی.
- 🔍 **موتور جستجو و فیلترینگ ترکیبی:** فیلتر آنی بر اساس ژانر، کشور سازنده، بازه سال ساخت، عوامل و امتیاز IMDb به کمک اشیاء `Q` در جنگو ORM.
- 👥 **سیستم تعاملی کاربران:**
  - ثبت نقد و دیدگاه با سیستم تایید ادمین (`Reviews`)
  - ثبت امتیاز ۱ تا ۱۰ با اعتبارسنجی سطح دیتابیس (`Ratings`)
  - ایجاد فهرست علاقه‌مندی‌ها (`Favorites`) و لیست تماشا (`Watchlist`)
- ⚡ **پایپ‌لاین اتوماتیک واردسازی داده (ETL):** دستور اختصاصی خط فرمان برای تزریق دسته‌ای صدها فیلم و سریال از روی دیتاست JSON به همراه روابط کامل بازیگران و ژانرها به‌صورت Transactional.
- 🎨 **طراحی ریسپانسیو و تمیز:** استایل‌دهی با Tailwind CSS 4 و اسلایدرهای اختصاصی Embla Carousel.

---

## 🛠️ تکنولوژی‌ها و ابزارها (Tech Stack)

- **بک‌اند:** Python 3.13 / Django 6.x
- **پایگاه‌داده:** SQLite (پیش‌فرض توسعه) / سازگار با PostgreSQL و MySQL
- **فرانت‌اند:** Tailwind CSS 4, Vite, Vanilla JavaScript, Embla Carousel
- **مدیریت دارایی‌ها:** WhiteNoise و Pillow

---

## 📂 ساختار ماژولار پروژه (Project Architecture)

```text
King-Movie/
│
├── accounts/         # مدیریت احراز هویت، ورود، ثبت‌نام و مدل Profile
├── media_library/    # هسته اصلی رسانه‌ها (Media, Season, Episode, MediaSource, Cast)
├── interactions/     # سیستم‌های تعاملی (Favorites, Watchlist, Ratings, Reviews)
├── dashboard/        # پنل کاربری و داشبورد مدیریت فعالیت‌های شخصی
├── common/           # سرویس‌ها و ابزارهای مشترک و کمکی (DRY)
├── config/           # تنظیمات سراسری پروژه، تنظیمات روتینگ و WSGI/ASGI
├── templates/        # قالب‌های HTML سه‌لایه (Layouts, Pages, Components)
├── static/           # فایل‌های استاتیک کامپایل‌شده (CSS, JS, Fonts)
├── frontend/         # ابزارها و کدهای بیلد فرانت‌اند با Vite و Tailwind
├── data/             # فایل دیتاست نمونه برای Seeding
└── docs/             # مستندات گام‌به‌گام فنی و معماری سیستم
```

---

## 🚀 راهنمای نصب و راه‌اندازی لوکال (Quick Start)

### ۱. پیش‌نیازها

- **پایتون:** نسخه 3.11 به بالا (ترجیحاً 3.13)
- **نودجی‌اس:** نسخه 18 به بالا (برای بیلد استایل‌ها)
- **گیت (Git)**

### ۲. کلون کردن ریپازیتوری

```bash
git clone https://github.com/MohammadRezaBeheshti/King-Movie.git
cd King-Movie
```

### ۳. راه‌اندازی محیط مجازی و وابستگی‌های پایتون

```bash
# ساخت محیط مجازی
python -m venv venv

# فعال‌سازی محیط در ویندوز (PowerShell)
.\venv\Scripts\activate

# فعال‌سازی در لینوکس / مک
# source venv/bin/activate

# نصب پکیج‌ها
pip install -r requirements.txt
```

### ۴. نصب و بیلد فرانت‌اند

```bash
npm install
npm run build
```

### ۵. اعمال مایگریشن‌ها و آماده‌سازی پایگاه‌داده

```bash
python manage.py makemigrations
python manage.py migrate
```

### ۶. تزریق اطلاعات اولیه (دیتاست فیلم‌ها)

برای پر شدن سایت با نمونه فیلم‌ها، سریال‌ها، بازیگران و ژانرها، دستور اتوماسیون اختصاصی پروژه را اجرا کنید:

```bash
python manage.py import_media_dataset
```

### ۷. ساخت مدیر سیستم (Superuser)

```bash
python manage.py createsuperuser
```

### ۸. اجرای سرور توسعه

```bash
python manage.py runserver
```

اکنون پروژه در آدرس `http://127.0.0.1:8000/` و پنل مدیریت در `http://127.0.0.1:8000/admin/` در دسترس است!

---

## 🤝 راهنمای مشارکت و همکاری در پروژه (Contributing)

این پروژه کاملاً **متن‌باز (Open Source)** است و ما صمیمانه از هرگونه مشارکت، از رفع ساده‌ترین باگ‌ها و اصلاح غلط‌های املایی تا افزودن ماژول‌های بزرگ جدید استقبال می‌کنیم!

### چگونه شروع به همکاری کنید؟

1. **ریپازیتوری را Fork کنید:**
   دکمه **Fork** در بالای صفحه گیت‌هاب را بزنید تا یک نسخه از پروژه روی اکانت شما قرار گیرد.

2. **پروژه را کلون کنید و یک Branch مجزا بسازید:**

   ```bash
   git checkout -b feature/نام-قابلیت-جدید
   # یا
   git checkout -b fix/نام-باگ
   ```

3. **تغییرات خود را اعمال کنید:**
   - کدهای خود را طبق استاندارد **PEP 8** برای پایتون تمیز و خوانا بنویسید.
   - مطمئن شوید که کامنت‌های غیرضروری و فایل‌های اضافی (مثل کش‌ها یا پوشه `venv`) کامیت نمی‌شوند.

4. **تغییرات را Commit کنید:**
   از پیام‌های کامیت واضح و معنادار استفاده کنید:

   ```bash
   git commit -m "feat: add subtitle parser for online stream player"
   ```

5. **تغییرات را Push کنید:**

   ```bash
   git push origin feature/نام-قابلیت-جدید
   ```

6. **درخواست ادغام (Pull Request) ثبت کنید:**
   به صفحه اصلی ریپازیتوری در گیت‌هاب رفته و یک **Pull Request** جدید با توضیح شفاف درباره کاری که انجام داده‌اید باز کنید.

---

### 💡 زمینه‌های پیشنهادی برای مشارکت (Roadmap & Ideas)

اگر دوست دارید در پروژه مشارکت کنید اما ایده خاصی ندارید، این موارد در اولویت توسعه قرار دارند:

- [ ] **اتصال به پروتکل‌های مدرن استریمینگ:** پیاده‌سازی پروتکل HLS (`.m3u8`) یا DASH برای تطبیق خودکار کیفیت با سرعت اینترنت کاربر.
- [ ] **سیستم پیشنهادگر هوشمند (Recommendation System):** پیشنهاد فیلم‌های مشابه بر اساس ژانر و سابقه تماشای کاربر با استفاده از الگوریتم‌های یادگیری ماشین یا Gemini API.
- [ ] **همگام‌سازی زیرنویس در پلیر:** قابلیت بارگذاری فایل زیرنویس (`.vtt` یا `.srt`) روی پلیر آنلاین.
- [ ] **داکرایز کردن پروژه (Docker & Docker Compose):** ایجاد `Dockerfile` و کانفیگ محیط استقرار با PostgreSQL و Nginx.
- [ ] **سیستم نوتیفیکیشن و ایمیل:** ارسال ایمیل خوش‌آمدگویی یا اطلاع‌رسانی انتشار فصل و قسمت جدید سریال‌های موجود در لیست تماشای کاربر.
- [ ] **تست‌نویسی جامع (Unit & Integration Tests):** تکمیل تست‌های خودکار در `tests.py` اپلیکیشن‌ها.

---

## 🐛 گزارش مشکلات و بازخورد (Issues & Support)

اگر با مشکلی مواجه شدید یا پیشنهادی برای بهتر شدن پروژه دارید:

1. ابتدا بخش [Issues](https://github.com/MohammadRezaBeheshti/King-Movie/issues) را بررسی کنید تا مطمئن شوید موضوع تکراری نیست.
2. یک Issue جدید با عنوان مشخص و شرح دقیق مشکل (همراه با متن خطا و اسکرین‌شات) باز کنید.

---

## 📜 لایسنس (License)

این پروژه تحت لایسنس آزاد **MIT** منتشر شده است. استفاده، ویرایش و توسعه این سورس‌کد برای مقاصد آموزشی و تجاری با ذکر منبع کاملاً آزاد است.

---

<div align="center">
  با عشق و افتخار برای جامعه برنامه‌نویسان متن‌باز ❤️<br>
  <b>King-Movie</b>
</div>
