from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inmenu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Test yaratish", callback_data="jointest"),
        ],
        [
            InlineKeyboardButton(text="✅ Test ishlash", callback_data="checktest"),
        ],
[
            InlineKeyboardButton(text="❌ Tugatish", callback_data="stoptest"),
        ],
    ],
)
