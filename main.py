from source.CreateImage import IMAGE
from source.TsetmcApi import Tsetmc
from pyrogram import Client,filters
from decouple import config
from source import jalali
import sqlite3
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton)

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute(
""" CREATE TABLE IF NOT EXISTS PERSON
    (                           
        ID      INTEGER     PRIMARY KEY
    );
"""
)


app = Client(
    config('session_name'),
    api_id = int(config('api_id')),
    api_hash = config('api_hash'),
    bot_token = config('bot_token')
)

with app:
    app.send_message(int(config('admin_id')), "Started ...!")

main_keyboard = ReplyKeyboardMarkup(
                [
                    ["👨‍🏫 راهنما"],
                    ["☎️ ارتباط با من"],
                ],
                resize_keyboard = True,
                one_time_keyboard = True
            )

@app.on_message(filters.command("start",["/"]))
async def me(client, message):
    try:
        c.execute("INSERT INTO PERSON (ID) values(?)",(message.from_user.id,))
    except Exception as e:
        print(e)
    finally:
        conn.commit()
    await message.reply("سلام،\nخوش اومدی!\nبرای استفاده از ربات یا از دکمه های زیر استفاده کن یا به طور کامل اسم نماد مورد نظرتو بفرست." , reply_markup=main_keyboard)

@app.on_message(filters.regex("👨‍🏫 راهنما"))
async def me(client, message):
    await message.reply("""✅ معرفی ربات بورسینیو

📈 برای دیدن تابلوی نماد مورد نظرت، اسمشو داخل ربات وارد کن.

@BoursinioBot""", reply_markup=main_keyboard)

@app.on_message(filters.regex("☎️ ارتباط با من"))
async def me(client, message):
    await message.reply("""در خدمتم.

🧨 جهت ارتباط به صورت مستقیم 👈🏻 @iramia9O 
⚖️ کاربر گرامی، چنانچه شما از ربات بمب سورس استفاده نمایید به منزله قبول قوانین است""" , reply_markup=main_keyboard)


@app.on_message(filters.text)
async def just_text(client, message):
    await client.send_message(message.from_user.id, "درحال دریافت اطلاعات از سایت ...")
    try:
        code = Tsetmc().search(message.text)["instrumentSearch"][0]['insCode']
        IMAGE(str(code)).create()
        await message.reply_photo(
            f"images/{code}.png",
        reply_markup=InlineKeyboardMarkup(
            [
                [ 
                    InlineKeyboardButton(  # Generates a callback query when pressed
                        "پیام های ناظر",
                        callback_data=f"{code}"
                    )
                ]
            ]
        )
        )
    except:
        await client.send_message(message.from_user.id, "مشکلی رخ داد دوباره امتحان کنید.")

@app.on_callback_query()
async def answer(client, callback_query):
    code = callback_query.data
    jmonths = ["فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند"]

    counter = 0
    for data in Tsetmc().supervisor_messages(str(code))["msg"]:
        time_to_str = "{},{},{}".format(str(data['dEven'])[0:4], str(data['dEven'])[4:6],str(data['dEven'])[6:8]) 
        time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
        month_persian = jmonths[time_to_tuple[1]-1]

        output = "{} {} {}, ساعت {}:{}".format(
            time_to_tuple[2],
            month_persian,
            time_to_tuple[0],
            str(data['hEven'])[0:2],
            str(data['hEven'])[2:4]
        )
        counter += 1
        await client.send_message(callback_query.from_user.id, "⌚️"+output+"\n\n⌨️"+data['tseTitle']+"\n\n"+data['tseDesc'])
        if counter == 5:
            break

app.run()

