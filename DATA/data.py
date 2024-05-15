import os
# Whats up man its me lol
# Очистка экрана
def clear():
    os.system("cls")

clear()

import random
import sys
import time
import DATA.audio.data_audio as da
import json
import pyautogui
import ctypes
import DATA.level_data as ld

# Получаем абсолютный путь к текущему скрипту
current_directory = os.path.dirname(os.path.abspath(__file__))

openInventory_path = os.path.join(current_directory, 'EVENT', 'openInventory.py')
appdata_dir = os.getenv('LOCALAPPDATA')
save_dir = os.path.join(appdata_dir, 'TextRPG', 'gameSAVE')
os.makedirs(save_dir, exist_ok=True)

shop_types = ["firearms", "alchemy"]
#                                                                                                                 run   meny  play   autor  skipE  errorL  CH   batl   GO     SH   data  Trip   Inv
run, meny, play, autors, skip_enter, errore_load, creating_hero, batle, game_over, shop, data, trips, inventory, = True, True, False, False, False, False, True, True, False, False, {}, False, False
#            L 
Language = "EN" 

#                                              DP     ManaR  ECAXP
DoublePunch, ManaRecovery, EarningCoinsAndXP = False, False, False
#                                                                      MRI  PRI   poiRI  TRI
MagicResistInt, PhysicalResistInt, PoisonResistInt, ToxinResistInt = -0.8, -0.8, -0.8,  -0.8 
#                                                      HR CR SR
helmetResistInt, chestplateResistInt, shieldResistInt = 0, 0, 0
#
helmetID, chestplateID, shieldID, weaponID, weapon2ID = None, None, None, None, None
#                       MPRI
MagicPhysicalResistInt = 0
#                                                                                                 name    class   Dm  HP  mHP G  XP XTL L  IS P  L   !map
name, heroClass, Dm, Hp, maxHp, gold, Xp, XpToLv, Lv, improvementStar, points, layer, playerMap = "NULL", "NULL", 20, 70, 70, 0, 0, 50, 0, 0, 0, 1, True
#                                                              PM    x  y   E  M   mM  S
playerMonstronomicon, Px, Py, Effects, mana, maxMana, speed = False, 0, 0, [], 50, 50, 1
#                                            item    H  CH  WE1 WE2
item, helmet, chestplate, weapon, weapon2 = [1, 1], "", "", "", ""


room_map = []

hdl = ctypes.windll.kernel32.GetStdHandle(-11)

logo = [
    "                                                                                                                                                                                  ",
    "      ____________________                                                                                                                                                        ",
    "     /                   /|      ▄▄▄█████▓ █     █░ ██▓ ██▓     ██▓  ▄████  ██░ ██ ▄▄▄█████▓    ▄████▄   ██░ ██  ██▀███   ▒█████   ███▄    █  ██▓ ▄████▄   ██▓    ▓█████   ██████ ",
    "    / /  ¯¯¯¯¯¯¯¯¯¯¯  / //|      ▓  ██▒ ▓▒▓█░ █ ░█░▓██▒▓██▒    ▓██▒ ██▒ ▀█▒▓██░ ██▒▓  ██▒ ▓▒   ▒██▀ ▀█  ▓██░ ██▒▓██ ▒ ██▒▒██▒  ██▒ ██ ▀█   █ ▓██▒▒██▀ ▀█  ▓██▒    ▓█   ▀ ▒██    ▒ ",
    "   /_/_/_____T_____/_/_// |      ▒ ▓██░ ▒░▒█░ █ ░█ ▒██▒▒██░    ▒██▒▒██░▄▄▄░▒██▀▀██░▒ ▓██░ ▒░   ▒▓█    ▄ ▒██▀▀██░▓██ ░▄█ ▒▒██░  ██▒▓██  ▀█ ██▒▒██▒▒▓█    ▄ ▒██░    ▒███   ░ ▓██▄   ",
    "  / / /      C    / / //  /      ░ ▓██▓ ░ ░█░ █ ░█ ░██░▒██░    ░██░░▓█  ██▓░▓█ ░██ ░ ▓██▓ ░    ▒▓▓▄ ▄██▒░▓█ ░██ ▒██▀▀█▄  ▒██   ██░▓██▒  ▐▌██▒░██░▒▓▓▄ ▄██▒▒██░    ▒▓█  ▄   ▒   ██▒",
    " / /  ___________  / //  /         ▒██▒ ░ ░░██▒██▓ ░██░░██████▒░██░░▒▓███▀▒░▓█▒░██▓  ▒██▒ ░    ▒ ▓███▀ ░░▓█▒░██▓░██▓ ▒██▒░ ████▓▒░▒██░   ▓██░░██░▒ ▓███▀ ░░██████▒░▒████▒▒██████▒▒",
    "/___________________//  /          ▒ ░░   ░ ▓░▒ ▒  ░▓  ░ ▒░▓  ░░▓   ░▒   ▒  ▒ ░░▒░▒  ▒ ░░      ░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ ░▓  ░ ░▒ ▒  ░░ ▒░▓  ░░░ ▒░ ░▒ ▒▓▒ ▒ ░",
    "|═══════════════════|  /             ░      ▒ ░ ░   ▒ ░░ ░ ▒  ░ ▒ ░  ░   ░  ▒ ░▒░ ░    ░         ░  ▒    ▒ ░▒░ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░░   ░ ▒░ ▒ ░  ░  ▒   ░ ░ ▒  ░ ░ ░  ░░ ░▒  ░ ░",
    "|═══════════════════| /            ░        ░   ░   ▒ ░  ░ ░    ▒ ░░ ░   ░  ░  ░░ ░  ░         ░         ░  ░░ ░  ░░   ░ ░ ░ ░ ▒     ░   ░ ░  ▒ ░░          ░ ░      ░   ░  ░  ░  ",
    "|═══════════════════|/                        ░     ░      ░  ░ ░        ░  ░  ░  ░            ░ ░       ░  ░  ░   ░         ░ ░           ░  ░  ░ ░          ░  ░   ░  ░      ░  ",
    "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯                                                                          ░                                                 ░                                ",
]

text_rpg_logo = [
    "████████╗███████╗██╗░░██╗████████╗  ██████╗░██████╗░░██████╗░",
    "╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝  ██╔══██╗██╔══██╗██╔════╝░",
    "░░░██║░░░█████╗░░░╚███╔╝░░░░██║░░░  ██████╔╝██████╔╝██║░░██╗░",
    "░░░██║░░░██╔══╝░░░██╔██╗░░░░██║░░░  ██╔══██╗██╔═══╝░██║░░╚██╗",
    "░░░██║░░░███████╗██╔╝╚██╗░░░██║░░░  ██║░░██║██║░░░░░╚██████╔╝",
    "░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░░░░░╚═════╝░",
]

# Функции сохранения и загрузки данных
def saveFile():
    global errore_load, name, heroClass, Hp, maxHp, gold, Dm, Xp, XpToLv, Lv, DoublePunch, \
           MagicResistInt, PhysicalResistInt, PoisonResistInt, \
           ToxinResistInt, ManaRecovery, EarningCoinsAndXP, improvementStar, points, item, \
           helmet, chestplate, weapon, weapon2, layer, Px, Py

    data = {
        "name": name,
        "heroClass": heroClass,
        "Hp": Hp,
        "maxHp": maxHp,
        "gold": gold,
        "Dm": Dm,
        "Xp": Xp,
        "XpToLv": XpToLv,
        "Lv": Lv,
        "DoublePunch": DoublePunch,
        "MagicResistInt": MagicResistInt,
        "PhysicalResistInt": PhysicalResistInt,
        "PoisonResistInt": PoisonResistInt,
        "ToxinResistInt": ToxinResistInt,
        "ManaRecovery": ManaRecovery,
        "EarningCoinsAndXP": EarningCoinsAndXP,
        "improvementStar": improvementStar,
        "points": points,
        "item": item,
        "helmet": helmet, 
        "chestplate": chestplate, 
        "weapon": weapon, 
        "weapon2": weapon2,
        "layer" : layer,
        "Px" : Px,
        "Py" : Py,
    }

    with open(os.path.join(save_dir, "save.json"), "w") as f:
        json.dump(data, f, indent=4)

def loadFile():
    global errore_load, name, heroClass, Hp, maxHp, gold, Dm, Xp, XpToLv, Lv, DoublePunch, \
           MagicResistInt, PhysicalResistInt, PoisonResistInt, \
           ToxinResistInt, ManaRecovery, EarningCoinsAndXP, improvementStar, points, item, \
           helmet, chestplate, weapon, weapon2, layer, Px, Py

    try:
        with open(os.path.join(save_dir, "save.json"), "r") as f:
            data = json.load(f)

        # Проверка наличия всех необходимых ключей в загруженных данных
        required_keys = ["name", "heroClass", "Hp", "maxHp", "gold", "Dm", "Xp", "XpToLv", "Lv", "DoublePunch", "MagicResistInt",
                         "PhysicalResistInt", "PoisonResistInt", "ToxinResistInt", "ManaRecovery",
                         "EarningCoinsAndXP", "improvementStar", "points", "item", "helmet", "chestplate",
                         "weapon", "weapon2", "layer", "Px", "Py"]
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Key '{key}' not found in the loaded data")

        # Присваивание данных из загруженного JSON
        name = data["name"]
        heroClass = data["heroClass"]
        Hp = data["Hp"]
        maxHp = data["maxHp"]
        gold = data["gold"]
        Dm = data["Dm"]
        Xp = data["Xp"]
        XpToLv = data["XpToLv"]
        Lv = data["Lv"]
        DoublePunch = data["DoublePunch"]
        MagicResistInt = data["MagicResistInt"]
        PhysicalResistInt = data["PhysicalResistInt"]
        PoisonResistInt = data["PoisonResistInt"]
        ToxinResistInt = data["ToxinResistInt"]
        ManaRecovery = data["ManaRecovery"]
        EarningCoinsAndXP = data["EarningCoinsAndXP"]
        improvementStar = data["improvementStar"]
        points = data["points"]
        item = data["item"]
        helmet = data["helmet"]
        chestplate = data["chestplate"]
        weapon = data["weapon"]
        weapon2 = data["weapon2"]
        layer = data["layer"]
        Px = data["Px"]
        Py = data["Py"]

    except FileNotFoundError:
        create_table("error", True, None, {0: "center"}, 45, "ERROR: File not found. Creating a new one.")
        input("> ")
        errore_load = True
    except json.JSONDecodeError as e:
        create_table("error", True, None, {0: "center"}, 45, "ERROR: Corrupted JSON file.")
        input("> ")
        errore_load = True
    except KeyError as e:
        create_table("error", True, None, {0: "center"}, 45, f"ERROR: Missing key {str(e)}.")
        input("> ")
        errore_load = True

# Функция создания таблицы
def create_table(style="info", use_clear=True, separator_positions=None, alignment=None, table_width=22, *args):

    def separator_up_info():
        print("Xx" + "_" * (table_width + 2) + "xX")

    def separator_centr_info():
        print("||" + "-" * (table_width + 2) + "||")

    def separator_down_info():
        print("Xx" + "¯" * (table_width + 2) + "xX")

    def separator_up_error():
        print(">>>" + "═" * (table_width + 2) + "<<<")

    def separator_centr_error():
        print("!!!" + "-" * (table_width + 2) + "!!!")

    def separator_down_error():
        print(">>>" + "═" * (table_width + 2) + "<<<")

    if use_clear:
        clear()

    if style == "info":
        separator_up_info()
    elif style == "error":
        separator_up_error()
    da.play_sound_print()
    time.sleep(0.1)

    if style == "info":
        for index, row in enumerate(args):
            time.sleep(0.1)

            if len(row) > table_width:
                words = row.split()  # Разбиваем строку на слова
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= table_width:
                        current_line += word + " "
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)
                for line in lines:
                    formatted_line = " ".join(line.strip().split())
                    print("|| {:<{width}} ||".format(formatted_line, width=table_width))
                    da.play_sound_print()  # проигрываем звук после вывода каждой строки
            else:
                if alignment is not None and index in alignment:
                    if alignment[index] == "center":
                        print("|| {:^{width}} ||".format(row, width=table_width))
                    elif alignment[index] == "right":
                        print("|| {:>{width}} ||".format(row, width=table_width))
                else:
                    print("|| {:<{width}} ||".format(row, width=table_width))
                    da.play_sound_print()  # проигрываем звук после вывода каждой строки

            if separator_positions is not None and index in separator_positions:
                separator_centr_info()

    elif style == "error":
        for index, row in enumerate(args):
            time.sleep(0.1)

            if len(row) > table_width:
                words = row.split()
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 <= table_width:
                        current_line += word + " "
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)
                for line in lines:
                    formatted_line = " ".join(line.strip().split())
                    print("!!! {:<{width}} !!!".format(formatted_line, width=table_width))
                    da.play_sound_print()
            else:
                if alignment is not None and index in alignment:
                    if alignment[index] == "center":
                        print("!!! {:^{width}} !!!".format(row, width=table_width))
                    elif alignment[index] == "right":
                        print("!!! {:>{width}} !!!".format(row, width=table_width))
                else:
                    print("!!! {:<{width}} !!!".format(row, width=table_width))
                    da.play_sound_print()

            if separator_positions is not None and index in separator_positions:
                separator_centr_error()


    time.sleep(0.1)
    if style == "info":
        separator_down_info()
    elif style == "error":
        separator_down_error()
    da.play_sound_print()


def play_animation(frames, delay=0.3):
    clear()
    for frame in frames:
        print(frame)
        da.play_sound_print2()
        time.sleep(delay)

def open_console_fullscreen():
    pyautogui.press('f11')

def set_font_size(size):
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 0
    font.dwFontSize.X = 0
    font.dwFontSize.Y = size
    font.FontFamily = 0
    font.FontWeight = 400
    font.FaceName = "Consolas"

    ctypes.windll.kernel32.SetCurrentConsoleFontEx(hdl, ctypes.c_ulong(False), ctypes.pointer(font))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def display_map(map_array, player):
    clear()
    for y, row in enumerate(map_array):
        for x, char in enumerate(row):
            if player.x == x and player.y == y:
                print('@', end='')
            elif not playerMap and (abs(player.x - x) > 3 or abs(player.y - y) > 3):  # Если карта закрыта и клетка находится далеко от игрока
                print(' ', end='')  # Показываем пустую клетку
            else:
                print(char, end='')
        print()
        da.play_sound_print()
        time.sleep(0.08)  # добавим небольшую задержку для лучшей анимации

def loading_animation(imports):
    animation_symbols = ['|', '-', '-', '-']  # Символы для анимации
    max_length = max(len(module) for module in imports)
    for module in imports:
        sys.stdout.write(f"\r| {module}{' '*(max_length - len(module))} ")
        sys.stdout.flush()
        for _ in range(5):  # Проходим по всем символам анимации
            sys.stdout.write(animation_symbols[_ % len(animation_symbols)] + ' ')
            sys.stdout.flush()
            time.sleep(0.005)  # Задержка между символами анимации
            sys.stdout.write('\b')  # Удаляем предыдущий символ анимации
            sys.stdout.flush()
        sys.stdout.write('\b\b\b\b\b\b')  # Удаляем анимацию
        sys.stdout.write(" DONE\n")
        sys.stdout.flush()
        time.sleep(random.uniform(0.05, 0.2))  # Случайная задержка от 0.1 до 0.4 секунд