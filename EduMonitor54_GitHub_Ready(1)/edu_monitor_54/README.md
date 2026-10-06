# EduMonitor 54 — Telegram bot + monitoring dashboard

Namangan viloyati, To‘raqo‘rg‘on tumani, 54-maktab uchun o‘quvchilarning fanlar kesimida kunlik tayyorgarligi, o‘zlashtirishi, reytingi va dinamikasini kuzatish tizimi.

## Muhim maxfiylik qoidasi
O‘quvchi bazasiga faqat tizim uchun zarur maydonlar kiritiladi: `school_id`, F.I.Sh., sinf. PINFL, hujjat seriyasi va hujjat raqami demo/import jarayonida ataylab ishlatilmaydi.

## MVP funksiyalar
- O‘qituvchi Telegram orqali kiradi.
- Sinf va fan tanlanadi.
- O‘quvchi uchun kunlik 0–100 ballik baholash.
- Tayyorlik, mavzuni tushunish, mustaqil ish, faollik va nazorat ko‘rsatkichlari.
- O‘quvchi reytingi va o‘sish/pasayish dinamikasi.
- Sinf va fan kesimida o‘rtacha natijalar.
- E’tibor talab qiluvchi o‘quvchilarni avtomatik ajratish.
- CSV/Excel ma’lumotlarini import qilish uchun tayyor format.
- Keyingi bosqichda direktor uchun web-dashboard.

## Ishga tushirish
1. Python 3.11+ o‘rnating.
2. `python -m venv .venv`
3. Windows: `.venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. `.env.example` nusxasini `.env` qilib, Telegram Bot Token kiriting.
6. `python bot/main.py`

## O‘quvchilarni import qilish
`data/students_template.csv` formatidan foydalaning. Excel fayl bo‘lsa, uni CSV UTF-8 qilib saqlash yoki keyingi bosqichda Excel importer qo‘shish mumkin.

## Rejalashtirilgan 2-bosqich
- PostgreSQL/Supabase
- Web admin panel
- O‘qituvchi yuklamasi va fan biriktirish
- PDF/Excel hisobotlar
- Telegram orqali haftalik avtomatik hisobot
- 7/14/30 kunlik trend tahlili
- 5E va kompetensiyaviy topshiriqlar monitoringi
