# Ustudy maktab boti

Telegram uchun o'quv boti (Python + [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)).

## Imkoniyatlar

- `/start` — salomlashish va asosiy tugmalar (reply keyboard)
- `📅 Dars jadvali` / `/jadval` / `/jadval juma` — haqiqiy dars jadvali (7.09.2026 – 27.12.2026)
- `📝 Ro'yxatdan o'tish` / `/royxat` — ism → yosh → telefon raqam (contact tugmasi), `royxat.json` ga saqlanadi
- `/royxatlar` — ro'yxatdan o'tganlar ro'yxati (faqat admin)
- `🧠 Test` / `/test` — 3 savollik inline test, oxirida natija
- `/sinov` — inline tugmani ikki marta bosish tajribasi
- rasm, stiker va lokatsiyaga javob

## Ishga tushirish

```bash
git clone <repo-url>
cd <repo-papka>
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp config.example.py config.py   # Windows: copy config.example.py config.py
# config.py ichiga TOKEN va ADMIN_ID ni yozing

python bot.py
```

> Token `config.py` da turadi va `.gitignore` orqali GitHub'ga yuklanmaydi.

## Skrinshotlar

> Skrinshotlarni `screenshots/` papkasiga shu nomlar bilan qo'ying.

### /start
![/start](screenshots/start.png)

### Tugmalar
![Tugmalar](screenshots/buttons.png)

### Ro'yxatdan o'tish dialogi
![Dialog](screenshots/dialog.png)

### Inline test
![Inline test](screenshots/test.png)