import os
import random
import sys
import time
import json
import pyautogui
import ctypes
import DATA.audio.data_audio as da
import DATA.level_data as ld
import DATA.tregers as t

# Получаем абсолютный путь к текущему скрипту
current_directory = os.path.dirname(os.path.abspath(__file__))
openInventory_path = os.path.join(current_directory, 'EVENT', 'openInventory.py')
appdata_dir = os.getenv('LOCALAPPDATA')
save_dir = os.path.join(appdata_dir, 'TextRPG', 'gameSAVE')
os.makedirs(save_dir, exist_ok=True)

hdl = ctypes.windll.kernel32.GetStdHandle(-11)

class Config:
    seting, delayOutput = False, 0.1
    language = "EN" 
    anim = False #!!!!!

class WorldValues:
    def __init__(self):
        self.chances = [70, 30]
        self.shop_types = ["blacksmith", "alchemist"]

class GameFlags:
    def __init__(self):
        self.run = True
        self.meny = True
        self.play = False
        self.autors = False
        self.skip_enter = False
        self.errore_load = False
        self.creating_hero = True
        self.batle = True
        self.game_over = False
        self.shop = False
        self.data = {}
        self.trips = False
        self.inventory = False
        self.room_map = []
        self.battle = False

class Resistances:
    def __init__(self):
        self.MagicResistInt = -0.8
        self.PhysicalResistInt = -0.8
        self.PoisonResistInt = -0.8
        self.ToxinResistInt = -0.8
        self.helmetResistInt = 0
        self.chestplateResistInt = 0
        self.shieldResistInt = 0
        self.MagicPhysicalResistInt = 0

class Equipment:
    def __init__(self):
        self.helmetID = None
        self.chestplateID = None
        self.shieldID = None
        self.weaponID = None
        self.weapon2ID = None

class Player:
    def __init__(self):
        self.name = "NULL"
        self.heroClass = "NULL"
        self.Dm = 20
        self.Hp = 70
        self.maxHp = 70
        self.gold = 0
        self.Xp = 0
        self.XpToLv = 50
        self.Lv = 0
        self.improvementStar = 0
        self.points = 0
        self.layer = 1
        self.playerMap = True
        self.playerMonstronomicon = False
        self.Px = 0
        self.Py = 0
        self.Effects = []
        self.mana = 50
        self.maxMana = 50
        self.speed = 1
        self.item = [1, 1]
        self.helmet = ""
        self.chestplate = ""
        self.weapon = ""
        self.weapon2 = ""

class Ability:
    def __init__(self):
        self.DoublePunch = False
        self.ManaRecovery = False
        self.EarningCoinsAndXP = False

class SaveManager:
    def __init__(self, player, resistances, equipment, ability):
        self.player = player
        self.resistances = resistances
        self.equipment = equipment
        self.ability = ability

    def save_file(self):
        data = {
            "name": self.player.name,
            "heroClass": self.player.heroClass,
            "Hp": self.player.Hp,
            "maxHp": self.player.maxHp,
            "gold": self.player.gold,
            "Dm": self.player.Dm,
            "Xp": self.player.Xp,
            "XpToLv": self.player.XpToLv,
            "Lv": self.player.Lv,
            "DoublePunch": self.ability.DoublePunch,
            "MagicResistInt": self.resistances.MagicResistInt,
            "PhysicalResistInt": self.resistances.PhysicalResistInt,
            "PoisonResistInt": self.resistances.PoisonResistInt,
            "ToxinResistInt": self.resistances.ToxinResistInt,
            "ManaRecovery": self.ability.ManaRecovery,
            "EarningCoinsAndXP": self.ability.EarningCoinsAndXP,
            "improvementStar": self.player.improvementStar,
            "points": self.player.points,
            "item": self.player.item,
            "helmet": self.player.helmet,
            "chestplate": self.player.chestplate,
            "weapon": self.player.weapon,
            "weapon2": self.player.weapon2,
            "layer": self.player.layer,
            "Px": self.player.Px,
            "Py": self.player.Py,
            "MagicPhysicalResistInt": self.resistances.MagicPhysicalResistInt,
            "helmetResistInt": self.resistances.helmetResistInt,
            "chestplateResistInt": self.resistances.chestplateResistInt,
            "shieldResistInt": self.resistances.shieldResistInt,
            "helmetID": self.equipment.helmetID,
            "chestplateID": self.equipment.chestplateID,
            "shieldID": self.equipment.shieldID,
            "weaponID": self.equipment.weaponID,
            "weapon2ID": self.equipment.weapon2ID,
            "playerMonstronomicon": self.player.playerMonstronomicon,
            "Effects": self.player.Effects,
            "mana": self.player.mana,
            "maxMana": self.player.maxMana,
            "speed": self.player.speed,
        }

        with open(os.path.join(save_dir, "save.json"), "w") as f:
            json.dump(data, f, indent=4)

    def load_file(self):
        try:
            with open(os.path.join(save_dir, "save.json"), "r") as f:
                data = json.load(f)

            required_keys = ["name", "heroClass", "Hp", "maxHp", "gold", "Dm", "Xp", "XpToLv", "Lv", "DoublePunch", 
                             "MagicResistInt", "PhysicalResistInt", "PoisonResistInt", "ToxinResistInt", "ManaRecovery",
                             "EarningCoinsAndXP", "improvementStar", "points", "item", "helmet", "chestplate",
                             "weapon", "weapon2", "layer", "Px", "Py", "MagicPhysicalResistInt", "helmetResistInt",
                             "chestplateResistInt", "shieldResistInt", "helmetID", "chestplateID", "shieldID", "weaponID", 
                             "weapon2ID", "playerMonstronomicon", "Effects", "mana", "maxMana", "speed"]
            for key in required_keys:
                if key not in data:
                    raise KeyError(f"Key '{key}' not found in the loaded data")

            self.player.name = data["name"]
            self.player.heroClass = data["heroClass"]
            self.player.Hp = data["Hp"]
            self.player.maxHp = data["maxHp"]
            self.player.gold = data["gold"]
            self.player.Dm = data["Dm"]
            self.player.Xp = data["Xp"]
            self.player.XpToLv = data["XpToLv"]
            self.player.Lv = data["Lv"]
            self.player.DoublePunch = data["DoublePunch"]
            self.resistances.MagicResistInt = data["MagicResistInt"]
            self.resistances.PhysicalResistInt = data["PhysicalResistInt"]
            self.resistances.PoisonResistInt = data["PoisonResistInt"]
            self.resistances.ToxinResistInt = data["ToxinResistInt"]
            self.player.ManaRecovery = data["ManaRecovery"]
            self.player.EarningCoinsAndXP = data["EarningCoinsAndXP"]
            self.player.improvementStar = data["improvementStar"]
            self.player.points = data["points"]
            self.player.item = data["item"]
            self.player.helmet = data["helmet"]
            self.player.chestplate = data["chestplate"]
            self.player.weapon = data["weapon"]
            self.player.weapon2 = data["weapon2"]
            self.player.layer = data["layer"]
            self.player.Px = data["Px"]
            self.player.Py = data["Py"]
            self.resistances.MagicPhysicalResistInt = data["MagicPhysicalResistInt"]
            self.resistances.helmetResistInt = data["helmetResistInt"]
            self.resistances.chestplateResistInt = data["chestplateResistInt"]
            self.resistances.shieldResistInt = data["shieldResistInt"]
            self.equipment.helmetID = data["helmetID"]
            self.equipment.chestplateID = data["chestplateID"]
            self.equipment.shieldID = data["shieldID"]
            self.equipment.weaponID = data["weaponID"]
            self.equipment.weapon2ID = data["weapon2ID"]
            self.player.playerMonstronomicon = data["playerMonstronomicon"]
            self.player.Effects = data["Effects"]
            self.player.mana = data["mana"]
            self.player.maxMana = data["maxMana"]
            self.player.speed = data["speed"]
            
        except Exception as e:
            print(f"Error loading game: {e}")

class Logo:
    def __init__(self):
        self.company_logo = [
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

        self.text_rpg_logo = [
            "████████╗███████╗██╗░░██╗████████╗  ██████╗░██████╗░░██████╗░",
            "╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝  ██╔══██╗██╔══██╗██╔════╝░",
            "░░░██║░░░█████╗░░░╚███╔╝░░░░██║░░░  ██████╔╝██████╔╝██║░░██╗░",
            "░░░██║░░░██╔══╝░░░██╔██╗░░░░██║░░░  ██╔══██╗██╔═══╝░██║░░╚██╗",
            "░░░██║░░░███████╗██╔╝╚██╗░░░██║░░░  ██║░░██║██║░░░░░╚██████╔╝",
            "░░░╚═╝░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ╚═╝░░╚═╝╚═╝░░░░░░╚═════╝░",
        ]

class Consolas:
    def __init__(self, config, player):
        self.config = config
        self.player = player


    def clear(self):
        os.system("cls")

    # Функция создания таблицы
    def create_table(self, style="info", use_clear=True, separator_positions=None, alignment=None, table_width=22, *args):

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
            self.clear()

        if style == "info":
            separator_up_info()
        elif style == "error":
            separator_up_error()
        da.play_sound_print()
        time.sleep(self.config.delayOutput)

        if style == "info":
            for index, row in enumerate(args):
                time.sleep(self.config.delayOutput)

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
                time.sleep(self.config.delayOutput)

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


        time.sleep(self.config.delayOutput)
        if style == "info":
            separator_down_info()
        elif style == "error":
            separator_down_error()
        da.play_sound_print()


    def play_animation(self, frames, delay=0.3):
        self.clear()
        for frame in frames:
            print(frame)
            da.play_sound_print2()
            time.sleep(delay)

    def open_console_fullscreen(self):
        pyautogui.press('f11')

    def set_font_size(self, size):
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

    def display_map(self, map_array, player):
        self.clear()
        for y, row in enumerate(map_array):
            for x, char in enumerate(row):
                if player.x == x and player.y == y:
                    print('@', end='')
                elif not self.player.playerMap and (abs(player.x - x) > 3 or abs(player.y - y) > 3):  # Если карта закрыта и клетка находится далеко от игрока
                    print(' ', end='')  # Показываем пустую клетку
                else:
                    print(char, end='')
            print()
            da.play_sound_print()
            time.sleep(0.08)  # добавим небольшую задержку для лучшей анимации

    def loading_animation(self, imports):
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

class PlayerDog:
    def __init__(self, x, y):
        self.x = x
        self.y = y