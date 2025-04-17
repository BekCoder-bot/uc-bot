from aiogram import Router, F
from aiogram.types import Message
from ocr_check import extract_payment_info
import os

router = Router()

@router.message(F.photo)
async def handle_payment_screenshot(message: Message):
    photo = message.photo[-1]
    path = f"media/{message.from_user.id}_check.jpg"
    await photo.download_to_drive(path)

    result = extract_payment_info(path)

    if "error" in result:
        await message.answer("❌ Chekni o‘qishda xatolik yuz berdi.")
        return

    amount = result.get("amount")
    time = result.get("time")

    if amount and int(amount) >= 7000:
        await message.answer(f"✅ To‘lov tasdiqlandi!\n\n💰 Summa: {amount} so‘m\n🕒 Vaqt: {time}")
    else:
        await message.answer("❗ To‘lov topilmadi yoki yetarli emas. Iltimos, aniq chekni yuboring.")

    os.remove(path)
