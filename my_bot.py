from pyrogram import Client, filters
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
import requests
import sqlite3

BOT_TOKEN = "توکن_جدید_ربات"

API_ID = 33624693
API_HASH = "758e111d4262da0325760aec64149521"

ADMIN_ID = 6849800497

FORCE_CHANNEL = "samirhock"

SUPPORT = "@samirhock_420"

app = Client(
    "AiBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")
db.commit()


def joined(user_id):
    try:
        member = app.get_chat_member(
            FORCE_CHANNEL,
            user_id
        )
        return member.status in [
            "member",
            "administrator",
            "owner"
        ]
    except:
        return False


main_keyboard = ReplyKeyboardMarkup(
    [
        ["🤖 چت با هوش مصنوعی"],
        ["📢 کانال", "🛠 پشتیبانی"],
        ["👤 پروفایل"]
    ],
    resize_keyboard=True
)


join_keyboard = ReplyKeyboardMarkup(
    [
        ["📢 عضویت در کانال"],
        ["✅ عضو شدم"]
    ],
    resize_keyboard=True
)


@app.on_message(filters.private & filters.command("start"))
def start(client, message):

    user_id = message.from_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?)",
        (user_id,)
    )
    db.commit()

    if not joined(user_id):

        message.reply_text(
            f"""
✨ سلام {message.from_user.first_name}

برای استفاده از ربات،
ابتدا باید عضو کانال ما شوی 🌹

📢 @{FORCE_CHANNEL}

بعد روی «✅ عضو شدم» بزن.
""",
            reply_markup=join_keyboard
        )
        return

    message.reply_text(
        f"""
✨ سلام {message.from_user.first_name}

به ربات هوش مصنوعی خوش آمدی 🤖

🧠 سوال بپرس
⚡ سریع جواب بگیر
🚀 آنلاین 24 ساعته

از دکمه‌های زیر استفاده کن 👇
""",
        reply_markup=main_keyboard
    )


@app.on_message(filters.private & filters.text)
def all_messages(client, message):

    text = message.text
    user_id = message.from_user.id

    if text == "📢 عضویت در کانال":
        message.reply(
            "لینک کانال 👇\nhttps://t.me/samirhock"
        )
        return

    if text == "✅ عضو شدم":

        if joined(user_id):

            message.reply(
                "✅ عضویت تایید شد",
                reply_markup=main_keyboard
            )

        else:

            message.reply(
                "❌ هنوز عضو کانال نشدی"
            )

        return

    if not joined(user_id):

        message.reply(
            "❌ اول عضو کانال شو",
            reply_markup=join_keyboard
        )
        return

    if text == "🛠 پشتیبانی":

        message.reply(
            f"آیدی پشتیبانی:\n{SUPPORT}"
        )
        return

    if text == "📢 کانال":

        message.reply(
            "کانال ما 👇\nhttps://t.me/samirhock"
        )
        return

    if text == "👤 پروفایل":

        message.reply(
            f"""
👤 اطلاعات شما

🆔 آیدی: {user_id}
📛 نام: {message.from_user.first_name}
"""
        )
        return

    if text == "🤖 چت با هوش مصنوعی":

        message.reply(
            "🧠 سوالت رو بفرست..."
        )
        return

    try:

        response = requests.get(
            f"https://api.safone.dev/ai/chat?message={text}"
        )

        answer = response.json()["response"]

        message.reply(answer)

    except:

        message.reply(
            "❌ خطا در اتصال به هوش مصنوعی"
        )


@app.on_message(filters.command("panel") & filters.user(ADMIN_ID))
def panel(client, message):

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    users = cursor.fetchone()[0]

    message.reply(
        f"""
⚙ پنل مدیریت

👥 کاربران:
{users}
"""
    )


print("Bot Started...")
app.run()