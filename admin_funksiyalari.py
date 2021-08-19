

import json

baza_fayl_nomi = "ob_havo_bot_baza.json"


def users_list(file=baza_fayl_nomi):
    with open(file, "r") as f:
        data = json.load(f)
    data = data["users"]
    n = 0
    matn = ''
    for a in data.keys():
        n += 1
        user = data[a]
        # <username> bor yoki yo'qligini tekshiradi
        if user["user_name"]:
            matn += f"{n}. {user['full_name']} — @{user['user_name']} — {a}\n"
        else:
            matn += f"{n}. {user['full_name']} — Mavjud emas — {a}\n"
    return matn

def users_number(file=baza_fayl_nomi):
    with open(file, "r") as f:
        data = json.load(f)
    data = data["users"]
    return len(data)