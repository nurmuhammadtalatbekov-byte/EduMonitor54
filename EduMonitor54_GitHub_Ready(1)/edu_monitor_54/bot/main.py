import asyncio
import os
import aiosqlite
from datetime import date
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
DB = 'school.db'

if not TOKEN or TOKEN.startswith('PASTE_'):
    raise RuntimeError('BOT_TOKEN ni .env faylida kiriting')

bot = Bot(TOKEN)
dp = Dispatcher()

MAIN = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='📚 Sinfni tanlash'), KeyboardButton(text='📊 Reyting')],
    [KeyboardButton(text='📈 Dinamika'), KeyboardButton(text='⚠️ E’tibor kerak')],
    [KeyboardButton(text='ℹ️ Yordam')]
], resize_keyboard=True)

async def db_init():
    async with aiosqlite.connect(DB) as db:
        await db.executescript(open('db/schema.sql', encoding='utf-8').read())
        await db.commit()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        '🏫 *EduMonitor 54*\n\n'
        '54-maktab o‘quvchilarining kunlik tayyorgarligi va o‘zlashtirishini monitoring qilish tizimi.\n\n'
        'Quyidagi menyudan foydalaning.',
        reply_markup=MAIN, parse_mode='Markdown')

@dp.message(F.text == 'ℹ️ Yordam')
async def help_(message: Message):
    await message.answer(
        '🧭 *Ishlash tartibi*\n\n'
        '1. Sinfni tanlang\n'
        '2. Fanni tanlang\n'
        '3. O‘quvchini tanlang\n'
        '4. 5 ta ko‘rsatkich bo‘yicha 0–100 ball kiriting\n'
        '5. Bot natijani saqlaydi va reyting/dinamikani yangilaydi.\n\n'
        '💡 Keyingi versiyada direktor uchun web-dashboard va avtomatik hisobotlar qo‘shiladi.',
        parse_mode='Markdown')

@dp.message(F.text == '📚 Sinfni tanlash')
async def classes(message: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute('SELECT DISTINCT class_name FROM students WHERE active=1 ORDER BY CAST(class_name AS INTEGER), class_name')
        rows = await cur.fetchall()
    classes = [r[0] for r in rows]
    if not classes:
        await message.answer('Hozircha o‘quvchilar bazasi bo‘sh. CSV import qiling.')
        return
    await message.answer('🎓 Sinfni tanlang:\n\n' + '\n'.join(f'• {c}' for c in classes))

@dp.message(F.text == '📊 Reyting')
async def rating(message: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute('''
        SELECT s.full_name, ROUND(AVG((sc.readiness+sc.understanding+sc.independent_work+sc.activity+sc.assessment)/5.0),1) avg_score
        FROM scores sc JOIN students s ON s.school_id=sc.school_id
        GROUP BY sc.school_id ORDER BY avg_score DESC LIMIT 10''')
        rows = await cur.fetchall()
    if not rows:
        await message.answer('📊 Reytingni hisoblash uchun hali baholash kiritilmagan.')
        return
    text = '🏆 *TOP-10 o‘quvchi*\n\n'
    for i,(name,score) in enumerate(rows,1):
        medal = ['🥇','🥈','🥉'][i-1] if i<=3 else f'{i}.'
        text += f'{medal} {name.title()} — *{score}%*\n'
    await message.answer(text, parse_mode='Markdown')

@dp.message(F.text == '📈 Dinamika')
async def dynamics(message: Message):
    await message.answer('📈 Dinamika moduli tayyor: kunlik/haftalik/oylik o‘zgarishlar keyingi qadamda grafik ko‘rinishida chiqariladi.')

@dp.message(F.text == '⚠️ E’tibor kerak')
async def attention(message: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute('''
        SELECT s.full_name, ROUND(AVG((sc.readiness+sc.understanding+sc.independent_work+sc.activity+sc.assessment)/5.0),1) avg_score
        FROM scores sc JOIN students s ON s.school_id=sc.school_id
        GROUP BY sc.school_id HAVING avg_score < 60 ORDER BY avg_score ASC LIMIT 10''')
        rows = await cur.fetchall()
    if not rows:
        await message.answer('🟢 Hozircha 60% dan past natijali o‘quvchi aniqlanmadi.')
        return
    text='⚠️ *E’tibor talab qiluvchi o‘quvchilar*\n\n'
    text += '\n'.join(f'🔴 {n.title()} — {s}%' for n,s in rows)
    await message.answer(text, parse_mode='Markdown')

async def main():
    await db_init()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
