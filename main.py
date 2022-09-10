



import logging
import json
from telegram.constants import PARSEMODE_HTML
from telegram.keyboardbutton import KeyboardButton



from admin_funksiyalari import users_list, users_number
from ob_havo import (
    kun_batafsil,
    kun_qisqa,
    hafta_yasa,
)

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    CallbackContext,
    CallbackQueryHandler,
)



# import os

# PORT = int(os.environ.get('PORT', '8443'))


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)






#Kerakli parametrlar

bot_link = "@iObHavo_bot"
# kerakli_id = 1748843939
BOT_TOKEN = ""

# #XP bot token
# BOT_TOKEN = "1898387737:AAEhjGQr0LhHZeM4d4u5LYLPi_mxG9aOy6E"

asosiy_tugma1 = "⛅️ Ob-havo ma'lumoti"
asosiy_tugma2 = "📍 Joylashuvni sozlash"
bosh_menu = "🗒 Bosh menyu 📋"

baza_fayl_nomi = "ob_havo_bot_baza.json"

main_buttons = ReplyKeyboardMarkup(
    [
        [asosiy_tugma1],
        [asosiy_tugma2]
	],
    resize_keyboard=True
)

sozlash_button = ReplyKeyboardMarkup(
    [
        [KeyboardButton("Mening joylashuvim", request_location=True)],
        [bosh_menu]
    ],
    resize_keyboard=True
)






def start(update: Update, context: CallbackContext) -> None:
    
    foydalanuvchi = update.effective_user
    username = foydalanuvchi.full_name


    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    with open(baza_fayl_nomi, "r") as f:
        baza_malumoti = json.load(f)

    with open(baza_fayl_nomi, "w") as f:
        baza_malumoti["users"][str(foydalanuvchi.id)] = {
            "full_name" : foydalanuvchi.full_name,
            "user_name" : foydalanuvchi.username,
        }
        json.dump(baza_malumoti, f, indent=4)



    txt = f"<b>Assalom-u alaykum, <i> {username}</i> </b>!\n"
    txt += "⛅️ Ob-havo botimizga xush kelibsiz!\n\n"
    txt += "Bu bot🤖 orqali o'z hududingiz ob-havosini bilishingiz mumkin."
    update.message.reply_html(text=txt)
    
    txt2 = "<b>Ob-havo ma'lumoti</b>ni olish uchun o'z <b><i>📍joylashuvingiz (location) </i></b>ni yuboring "
    txt2 += "yoki <b><i>pastdagi tugma</i></b>ni bosing.\n"
    txt2 += "Bunda <b>GPS</b> yoniq holatda ekanligiga ishonch hosil qiling.\n"
    txt2 += "Aks holda bu ❌xatolikka olib kelishi mumkin."
    update.message.reply_html(text=txt2, reply_markup=sozlash_button)


def admin_sozlamalari(update: Update, context: CallbackContext):
    parol = context.args[0]
    if parol == "hunter2003":
        keyboard = [
            [
                InlineKeyboardButton("Foydalanuvchilar ro'yxati", callback_data="foydalanuvchilar_royxati"),
            ],
            [
                InlineKeyboardButton("Baza(json) fayli", callback_data="baza_fayl")
            ]
        ]
        reply_keyboard = InlineKeyboardMarkup(keyboard)

        matn = "<b>Xush kelibsiz!</b>\n\n"
        matn += f"<i>Hozirda <b>bot</b>dan </i> <b>{users_number()}</b> <i>nafar odam foydalanmoqda</i>"
        update.message.reply_html(text=matn, reply_markup=reply_keyboard)
 



def changing_location(update: Update, context: CallbackContext):
    # Foydalanuvchi joylashuv ma'lumotlarini o'zgartiradi
    # va bazaga saqlaydi
    foydalanuvchi = update.effective_user


    #Locationdan kerakli koordinatalar ajratiladi
    data = update.message.location
    latitude = data['latitude']
    longitude = data['longitude']

     #Kiritilgan shahar aniqlanadi
    shahar = kun_qisqa(latitude, longitude)[0]


    # Foydalanuvchilar haqidagi ma'lumotni bazaga saqlab boradi
    with open(baza_fayl_nomi, "r") as f:
        baza_malumoti = json.load(f)

    with open(baza_fayl_nomi, "w") as f:
        baza_malumoti["users"][str(foydalanuvchi.id)] = {
            "full_name" : foydalanuvchi.full_name,
            "user_name" : foydalanuvchi.username,
            "location" : {
                "latitude" : latitude,
                "longitude" : longitude,
                "shahar": shahar,
            }
        }
        json.dump(baza_malumoti, f, indent=4)


    # Kerakli odamdan location kelsa forward qiladi
    try:
        context.bot.forward_message(chat_id=1039835085, 
                            from_chat_id=update.effective_message.chat_id, 
                            message_id=update.effective_message.message_id)
    except:
        print("Jo'natishda xatolik!")
    

   
    matn = f"📍<i> Joylashuvingizni <b>{shahar}</b> hududiga o'zgartirdingiz ☑️</i>"

    update.message.reply_html(text=matn, reply_markup=main_buttons)

def menyuga_ot(update: Update, context: CallbackContext):
    matn = "<b>📱 Bosh menyu</b>"
    update.message.reply_html(text=matn, reply_markup=main_buttons)

def funk_a1(latitude, longitude, day=''):
    #Berilga kun haqida qisqa ma'lumot
    #Agar sana ko'rsatilmasa bugungi kunni oladi

    data = kun_qisqa(latitude, longitude, day)
    matn = f"<b>{data[0]}</b> hududida kutilayotgan ob-havo:\n<b><i>{data[1]}</i></b>\n\n"
    matn += f"<b>🌡 Harorat  ➟ </b> {data[2]}°C / {data[3]}°C\n\n"
    matn += f"<b>💨 Shamol tezligi  ➟</b>  {data[4]} km/soat\n"
    if not day:
        matn += f"<b>🌁 Bosim  ➟</b>  {data[8]} millibar\n"
    matn += f"<b>🌧 Yog'ingarchilik ehtimoli  ➟</b>  {data[5]} %\n\n"
    matn += f"<b>🌅 Quyosh chiqishi  ➟</b>  {data[6]}\n"
    matn += f"<b>🌆 Quyosh botishi  ➟</b>  {data[7]}\n\n"
    matn += f"Doimiy ob-havo ma'lumotlari:\n👉 {bot_link}"
    return matn, data[1]

def funk_a2(latitude, longitude, day):
    #Berilgan sana haqida batafsil malumot beradi

    data = kun_batafsil(latitude, longitude, day)
    # data - list ko'rinishida
    # 1-elementi - shahar, 2-elementi - soatlik malumot

    shahar = data[0]
    malumot = data[1]
    matn = f"<b>{shahar}</b> hududida <b><i>{day}</i></b> sanadagi 24 soatlik ob-havo ma'lumoti\n"
    matn += f"(<i>harorat, yog'ingarchilik ehtimoli, shamol tezligi</i> tartibida ko'rsatilgan)\n\n"
    for a in malumot:
        matn += f"🕖 <b>{a[0]}   —   {a[1]}</b>°C,  <b>{a[2]}</b>%,  <b>{a[3]}</b> km/soat\n"
    matn += f"\nDoimiy ob-havo ma'lumotlari:\n👉 {bot_link}"

    return matn


def funk_hafta(latitude, longitude):
    data = hafta_yasa(latitude, longitude)
    shahar = data[0]
    hafta_kunlari = data[1]

    matn = f"<b>🗓 Haftalik ob-havo \n{shahar}</b> <i>hududi</i>\n\n"
    keyboard = [[]]

    for a in range(7):
        keyboard[0].append(InlineKeyboardButton(f"{a+1}", 
                        callback_data=f"hafta_kunlari|{hafta_kunlari[a]}|{latitude}|{longitude}"))
        
        malumot = kun_qisqa(latitude, longitude, hafta_kunlari[a])
        matn += f"<b>{a+1}.  <i>{malumot[1]}</i></b>\n"
        matn += f"<b>🌡 Harorat:</b>   {malumot[2]}°C / {malumot[3]}°C\n"
        matn += f"<b>🌧 Yog'ingarchilik ehtimoli:</b>   {malumot[5]} %\n\n"
    matn += f"\nDoimiy ob-havo ma'lumotlari:\n👉 {bot_link}"
    reply_keyboard = InlineKeyboardMarkup(keyboard)
    

    return matn, reply_keyboard


def location_weather(update: Update, context: CallbackContext):
    
    #Foydalanuvchi ID si
    user_id = str(update.effective_user.id)

    # Bazadan joylashuv malumotlarini oladi
    # Agar yo'q bo'lsa bu haqda xabar beradi 
    with open(baza_fayl_nomi, "r") as f:
        baza_malumoti = json.load(f)

    if user_id in baza_malumoti["users"]:
        baza_mal = baza_malumoti["users"][user_id]
        if "location" in baza_mal:
            latitude  = baza_mal["location"]['latitude']
            longitude = baza_mal["location"]['longitude']

            malumot = funk_a1(latitude, longitude)
            # malumot - kunlik qisqa ob-havo va berilgan kun
            matn = malumot[0]
            # matn - kunlik qisqa ob-havo
            # malumot[1] - kerakli sana
            keyboard = [
                [
                    InlineKeyboardButton("Batafsil ma'lumot", 
                    callback_data=f"batafsil|{malumot[1]}|{latitude}|{longitude}"),
                ],
                [
                    InlineKeyboardButton("🗓 Haftalik ob-havoni ko'rish", 
                    callback_data=f"haftalik|_|{latitude}|{longitude}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            #Foydalanuvchiga ob-havo ma'lumoti yuboradi
            update.message.reply_html(matn, reply_markup=reply_markup)
        else:
            #Foydalanuvchiga Joylashuv ma'lumotlari yo'qligini aytadi
            matn = "<b>Siz joylashuv ma'lumotlaringizni kiritmadingiz\n"
            matn += f"Buning uchun <i>\"{asosiy_tugma2}\"</i> tugmasidan foydalaning 👇</b>"
            update.message.reply_html(text=matn)
    else:       
        #Foydalanuvchiga Joylashuv ma'lumotlari yo'qligini aytadi       
        matn = "<b>Siz joylashuv ma'lumotlaringizni kiritmadingiz\n"
        matn += f"Buning uchun <i>\"{asosiy_tugma2}\"</i> tugmasidan foydalaning 👇</b>"
        update.message.reply_html(text=matn)
        


    
    

def funk_b1(update: Update, context: CallbackContext):

    ana = context.bot.send_message(chat_id=update.effective_message.chat_id,
            text="Iltimos biroz kuting ...")
    # Foydalanuvchiga kutish haqida xabar jo'natadi va o'chib ketadi


    query = update.callback_query
    query.answer()
    # data - query qaytargan malumot
    data = query.data
    

    # Admin uchun maxsus bo'lim
    if "foydalanuvchilar_royxati" in data:
        context.bot.send_message(
            chat_id=update.effective_user.id, text=users_list())
    
    elif "baza_fayl" in data:
        file = open(baza_fayl_nomi, "r")
        context.bot.send_document(
            chat_id=update.effective_user.id, document=file)

    else:
        #Oddiy foydalanuvchilar uchun:

        latitude = data.split("|")[2]
        longitude = data.split("|")[3]


        if "batafsil" in data:
            kerakli_kun = data.split("|")[1]
            matn = funk_a2(latitude, longitude, kerakli_kun)
            context.bot.send_message(chat_id=update.effective_message.chat_id,
                    text=matn, parse_mode=PARSEMODE_HTML)
            # batafsil malumot tashlovchi funksiya

        if "haftalik" in data:
            # hafta kunlari bo'yicha ma'lumot
            malumot = funk_hafta(latitude, longitude)

            matn = malumot[0]
            # matn - hafta kunlaridagi ob-havo
            keyboard = malumot[1]
            # reply_keyboard - hafta kunlari tugmalari

            context.bot.send_message(chat_id=update.effective_message.chat_id,
                    text=matn, parse_mode=PARSEMODE_HTML, reply_markup=keyboard)
        if "hafta_kunlari" in data:
            # Berilgan hafta kuni bo'yicha ma'lumot
            kun = data.split("|")[1]
            matn = funk_a1(latitude, longitude, kun)[0]
            keyboard = [
                [InlineKeyboardButton("Batafsil ma'lumot", 
                            callback_data=f"batafsil|{kun}|{latitude}|{longitude}")],
                [InlineKeyboardButton("🔙 Ortga", 
                            callback_data=f"ortga|_|{latitude}|{longitude}")],
            ]
            reply_keyboard = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=reply_keyboard)
        if "ortga" in data:
            malumot = funk_hafta(latitude, longitude)

            matn = malumot[0]
            # matn - hafta kunlaridagi ob-havo
            keyboard = malumot[1]
            # reply_keyboard - hafta kunlari tugmalari
            query.edit_message_text(text=matn, parse_mode=PARSEMODE_HTML, reply_markup=keyboard)

        # Foydalanuvchiga yuborilgan kutish haqidagi xabar o'chiriladi
        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                    message_id=ana.message_id)
        
    
    try:
        context.bot.delete_message(chat_id=update.effective_message.chat_id,
                    message_id=ana.message_id)
    except:
        print("Kutish haqidagi xabar o'chirilmadi")


def funk_b2(update: Update, context: CallbackContext):
    txt2 = "<b>📍 Joylashuv<i>(location)</i>ni o'zgartitrish</b>\n\n"
    txt2 += "Buning joylashuvingizni jo'nating yoki pastdagi tugmani bosing."
    txt2 += "Bunda <b>GPS</b> yoniq holatda ekanligiga ishonch hosil qiling.\n"
    txt2 += "Aks holda bu xatolikka olib kelishi mumkin."
    update.message.reply_html(text=txt2, reply_markup=sozlash_button)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("admin", admin_sozlamalari))

    dispatcher.add_handler(MessageHandler(Filters.location, changing_location))
    dispatcher.add_handler(CallbackQueryHandler(funk_b1))
    dispatcher.add_handler(MessageHandler(Filters.regex(bosh_menu), menyuga_ot))
    dispatcher.add_handler(MessageHandler(Filters.regex(asosiy_tugma1), location_weather))
    dispatcher.add_handler(MessageHandler(Filters.regex(asosiy_tugma2), funk_b2))

    # Start the Bot
    updater.start_polling()

    # updater.start_webhook(listen="0.0.0.0",
    #                   port=PORT,
    #                   url_path=BOT_TOKEN,
    #                   webhook_url="https://iobhavo-bot.herokuapp.com/" + BOT_TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()