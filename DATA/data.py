from ctypes import wintypes
import curses
import logging
import os
import random as r
import sys
import time
import json
import ctypes
import DATA.audio.data_audio as da
import DATA.level_data as ld
import DATA.tregers as t
import DATA.item_data as itemd
from EVENT.debug import debug

# Получаем абсолютный путь к текущему скрипту
current_directory = os.path.dirname(os.path.abspath(__file__))
openInventory_path = os.path.join(current_directory, 'EVENT', 'openInventory.py')
appdata_dir = os.getenv('LOCALAPPDATA')
save_dir = os.path.join(appdata_dir, 'TextRPG', 'gameSAVE')
os.makedirs(save_dir, exist_ok=True)

class Config:
    delayOutput = 0.1
    language = "EN" 
    anim = False
    

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
        self.seting = False

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
    def __init__(self, config, player, win):
        self.config = config
        self.player = player
        self.win = win
        self.table_x = 1
        self.table_y = 1
        self.alignmentTable = None

    def calculate_position(self, width, height, x=None, y=None):
        if self.alignmentTable == 'c':
            self.table_x = (curses.COLS - width) // 2
            self.table_y = (curses.LINES - height) // 2
        elif self.alignmentTable == 'r':
            self.table_x = curses.COLS - width - 1
            self.table_y = (curses.LINES - height) // 2
        elif self.alignmentTable == 'l':
            self.table_x = 1
            self.table_y = 1

        if x is not None:
            self.table_x = x
        if y is not None:
            self.table_y = y

    def create_table(self, *args, style="info", use_clear=True, separator_positions=None, alignment=None, alignmentTable="c", table_width=22, x=None, y=None):
        self.alignmentTable = alignmentTable

        self.calculate_position(table_width + 7, len(args) + 2, x, y)

        def separator_up_info():
            self.win.addstr(self.table_y, self.table_x, "Xx" + "_" * (table_width + 2) + "xX")
            self.table_y += 1

        def separator_centr_info():
            self.win.addstr(self.table_y, self.table_x, "||" + "-" * (table_width + 2) + "||")
            self.table_y += 1

        def separator_down_info():
            self.win.addstr(self.table_y, self.table_x, "Xx" + "¯" * (table_width + 2) + "xX")
            self.table_y += 1

        def separator_up_error():
            self.win.addstr(self.table_y, self.table_x, ">>>" + "═" * (table_width + 2) + "<<<")
            self.table_y += 1

        def separator_centr_error():
            self.win.addstr(self.table_y, self.table_x, "!!!" + "-" * (table_width + 2) + "!!!")
            self.table_y += 1

        def separator_down_error():
            self.win.addstr(self.table_y, self.table_x, ">>>" + "═" * (table_width + 2) + "<<<")
            self.table_y += 1

        if use_clear:
            self.win.clear()

        if style == "info":
            separator_up_info()
        elif style == "error":
            separator_up_error()

        da.play_sound_print()
        self.win.refresh()
        time.sleep(self.config.delayOutput)

        if style == "info":
            for index, row in enumerate(args):
                self.win.refresh()
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
                        self.win.addstr(self.table_y, self.table_x, "|| {:<{width}} ||".format(formatted_line, width=table_width))
                        self.table_y += 1
                        da.play_sound_print()
                else:
                    if alignment is not None and index in alignment:
                        if alignment[index] == "center":
                            self.win.addstr(self.table_y, self.table_x, "|| {:^{width}} ||".format(row, width=table_width))
                        elif alignment[index] == "right":
                            self.win.addstr(self.table_y, self.table_x, "|| {:>{width}} ||".format(row, width=table_width))
                    else:
                        self.win.addstr(self.table_y, self.table_x, "|| {:<{width}} ||".format(row, width=table_width))
                    self.table_y += 1
                    da.play_sound_print()

                if separator_positions is not None and index in separator_positions:
                    separator_centr_info()

        elif style == "error":
            for index, row in enumerate(args):
                self.win.refresh()
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
                        self.win.addstr(self.table_y, self.table_x, "!!! {:<{width}} !!!".format(formatted_line, width=table_width))
                        self.table_y += 1
                        da.play_sound_print()
                else:
                    if alignment is not None and index in alignment:
                        if alignment[index] == "center":
                            self.win.addstr(self.table_y, self.table_x, "!!! {:^{width}} !!!".format(row, width=table_width))
                        elif alignment[index] == "right":
                            self.win.addstr(self.table_y, self.table_x, "!!! {:>{width}} !!!".format(row, width=table_width))
                    else:
                        self.win.addstr(self.table_y, self.table_x, "!!! {:<{width}} !!!".format(row, width=table_width))
                    self.table_y += 1
                    da.play_sound_print()

                if separator_positions is not None and index in separator_positions:
                    separator_centr_error()

        self.win.refresh()
        time.sleep(self.config.delayOutput)
        if style == "info":
            separator_down_info()
        elif style == "error":
            separator_down_error()

        da.play_sound_print()
        self.win.refresh()

    def play_animation(self, frames, delay=0.3, alignmentTable="c", x=None, y=None):
        self.alignmentTable = alignmentTable
        self.calculate_position(len(frames[0]), len(frames), x, y)

        self.win.clear()
        for frame in frames:
            self.win.addstr(self.table_y, self.table_x, frame)
            da.play_sound_print2()
            time.sleep(delay)
            self.win.refresh()
            self.table_y+=1

    def display_map(self, map_array, player, alignmentTable="c", x=None, y=None):
        self.alignmentTable = alignmentTable

        self.win.clear()
        self.win.refresh()

        self.calculate_position(len(map_array[0]), len(map_array), x, y)

        for row_index, row in enumerate(map_array):
            for char_index, char in enumerate(row):
                table_x = self.table_x + char_index  # вычисляем x координату для каждого символа
                table_y = self.table_y + row_index  # вычисляем y координату для каждого символа

                if player.x == char_index and player.y == row_index:
                    self.win.addch(table_y, table_x, '@')
                elif not self.player.playerMap and (abs(player.x - char_index) > 3 or abs(player.y - row_index) > 3):
                    self.win.addch(table_y, table_x, ' ')
                else:
                    self.win.addch(table_y, table_x, char)
            self.win.refresh()
            da.play_sound_print()
            time.sleep(0.08)
        
        self.win.refresh()

    def loading_animation(self, imports):
        animation_symbols = ['|', '/', '-', '\\']
        max_length = max(len(module) for module in imports)
        height, width = self.win.getmaxyx()
        y = 0
        for module in imports:
            module_text = f"| {module}{' '*(max_length - len(module))} "
            if len(module_text) + max_length + 6 > width - 1:
                module_text = module_text[:width - max_length - 7]
            self.win.addstr(y, 0, module_text)
            for i in range(r.randint(2, 6)):
                if max_length + 4 < width - 1:
                    self.win.addstr(y, max_length + 4, animation_symbols[i % len(animation_symbols)])
                self.win.refresh()
                time.sleep(0.1)
                if max_length + 4 < width - 1:
                    self.win.addstr(y, max_length + 4, ' ')
            if max_length + 4 < width - 1:
                self.win.addstr(y, max_length + 4, "DONE |")
            self.win.refresh()
            time.sleep(r.uniform(0.02, 0.09))
            y += 1
        self.win.refresh()

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short),
                ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.ULONG),
                ("nFont", wintypes.DWORD),
                ("dwFontSize", COORD),
                ("FontFamily", wintypes.UINT),
                ("FontWeight", wintypes.UINT),
                ("FaceName", wintypes.WCHAR * 32)]

class ConsoleSettings:
    def __init__(self) -> None:
        self.LF_FACESIZE = 32
        self.STD_OUTPUT_HANDLE = -11

    def set_console_buffer_size(self, cols, rows):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        hConsole = kernel32.GetStdHandle(-11)
        if hConsole == wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())
        
        bufferSize = wintypes._COORD(cols, rows)
        success = kernel32.SetConsoleScreenBufferSize(hConsole, bufferSize)
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())
        
    def set_console_font(self, font_name='Consolas', font_size=24):
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        hConsole = kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        if hConsole == wintypes.HANDLE(-1).value:
            raise ctypes.WinError(ctypes.get_last_error())

        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = 0
        font.dwFontSize.X = 0
        font.dwFontSize.Y = font_size
        font.FontFamily = 54
        font.FontWeight = 400
        font.FaceName = font_name

        success = kernel32.SetCurrentConsoleFontEx(hConsole, ctypes.c_long(False), ctypes.byref(font))
        if not success:
            raise ctypes.WinError(ctypes.get_last_error())

    def create_fullscreen_window(self, stdscr):
        height, width = stdscr.getmaxyx()
        win = curses.newwin(height, width, 0, 0)
        return win

    def set_borderless_fullscreen(self):
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

        hwnd = kernel32.GetConsoleWindow()
        if hwnd == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        
        style = user32.GetWindowLongW(hwnd, -16)
        style &= ~0x00CF0000
        user32.SetWindowLongW(hwnd, -16, style)
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, 0x0020)
        user32.ShowWindow(hwnd, 3)

class TableMenu:
    def __init__(self, config, win):
        self.config = config
        self.is_first_display = True  # флаг для первого отображения
        self.menu_x = 1
        self.menu_y = 1
        self.info_x = 35
        self.info_y = 1
        self.alignment = None
        self.win = win

    def calculate_position(self, width, height, x, y):
        if self.alignment == 'c':
            self.menu_x = (curses.COLS - width) // 2
            self.menu_y = (curses.LINES - height) // 2
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y
        elif self.alignment == 'r':
            self.menu_x = curses.COLS - width - 1
            self.menu_y = (curses.LINES - height) // 2
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y
        elif self.alignment == 'l':
            self.menu_x = 1
            self.menu_y = 1
            self.info_x = self.menu_x + 35
            self.info_y = self.menu_y

        if x is not None:
            self.menu_x = x
            self.info_x = self.menu_x + 35
        if y is not None:

            self.menu_y = y
            self.info_y = self.menu_y

    def create_table(self, win, title, options, selected_index, table_width=22):
        def separator_up_info():
            win.addstr("Xx" + "_" * (table_width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()

        def separator_centr_info():
            win.addstr("||" + "-" * (table_width + 2) + "||\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()

        def separator_down_info():
            win.addstr("Xx" + "¯" * (table_width + 2) + "xX\n")

        separator_up_info()
        da.play_sound_print()
        win.addstr("|| {:^{width}} ||\n".format(title, width=table_width))
        separator_centr_info()
        da.play_sound_print()

        for index, option in enumerate(options):
            if index == selected_index:
                option_str = "> {:<{width}}".format(option, width=table_width - 2)
                win.addstr("|| ", curses.color_pair(1))
                win.addstr(option_str, curses.color_pair(2))
                win.addstr(" ||\n", curses.color_pair(1))
            else:
                option_str = "  {:<{width}}".format(option, width=table_width - 2)
                win.addstr("|| ", curses.color_pair(1))
                win.addstr(option_str, curses.color_pair(1))
                win.addstr(" ||\n", curses.color_pair(1))

            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()

        separator_down_info()
        da.play_sound_print()

    def menu(self, title, options, additional_info=["","","","","",""], alignment="c", x=None, y=None, color='cyan', tips=True, clear=True):
        self.alignment = alignment
        curses.curs_set(0)

        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }
        col = {v: k for k, v in icol.items()}
        bc = curses.COLOR_BLACK

        curses.start_color()
        curses.init_pair(1, 7, bc)  # normal
        curses.init_pair(2, col[color], bc)  # highlighted
        
        if clear:
            self.win.clear()
            self.win.refresh()

        self.calculate_position(30, len(options) + 5, x, y)

        menu_win = curses.newwin(len(options) + 5, 30, self.menu_y, self.menu_x)
        if tips:
            info_win = curses.newwin(len(options) + 5, 50, self.info_y, self.info_x)

        c = 0
        option = 0
        while c != 10:  # Loop until 'Enter' key (ASCII 10) is pressed
            menu_win.erase()
            if tips:
                info_win.erase()
                info_win.box()
                self.display_info(info_win, additional_info, option)

            # Draw the menu options
            self.create_table(menu_win, title, options, option)

            # Refresh the window to show changes
            menu_win.refresh()
            if tips:
                info_win.refresh()

            # Get user input
            c = self.win.getch()
            logging.info(f"INFO: Key pressed: {c}", exc_info=False)

            if c == curses.KEY_UP:
                option = (option - 1) % len(options)
            elif c == curses.KEY_DOWN:
                option = (option + 1) % len(options)

            self.is_first_display = False

        self.is_first_display = True
        return str(option)

    def display_info(self, info_win, additional_info, option):
        info_lines = additional_info[option].split('\n')
        for i, line in enumerate(info_lines, start=1):
            info_win.addstr(i, 1, line)


    def create_table_text_box(self, win, width):
        def separator_up_info():
            win.addstr(self.menu_y, self.menu_x, "Xx" + "_" * (width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()

        def separator_down_info():
            win.addstr(self.menu_y + 2, self.menu_x , "Xx" + "¯" * (width + 2) + "xX\n")
            if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()
        
        separator_up_info()
        win.addstr(self.menu_y + 1, self.menu_x, "||" + " " * (width + 2) + "||")
        if self.is_first_display:
                time.sleep(self.config.delayOutput)
                da.play_sound_print()
                win.refresh()
        separator_down_info()

        return [self.menu_x + 3, self.menu_y + 1]



    def text_box(self, table_alignment = "c", clear=True, x=None, y=None, width=22, max_sumbol=22):
        self.alignment = table_alignment

        if clear:
            self.win.clear()
            self.win.refresh()

        self.calculate_position(width+7, 3, x=x, y=y)

        c_pozition = self.create_table_text_box(self.win, width)
        self.win.move(c_pozition[1], c_pozition[0])

        curses.curs_set(1)
        text = ""
        c = 0
        while True:  # Бесконечный цикл
            c = self.win.getch()
            
            logging.info(f"INFO: Key pressed: {c}", exc_info=False)

            if c == 8:
                if len(text) > 0:
                    text = text[:-1]
                    self.win.move(c_pozition[1], c_pozition[0] + len(text))
                    self.win.addstr(' ')
                    da.play_sound_print()
            elif c == 10:
                self.win.clear()
                self.win.refresh()
                da.play_sound_print()
                break
            elif c < 256 and len(text) < max_sumbol and c != 8:
                text += chr(c)
                da.play_sound_print()
            
            self.win.move(c_pozition[1], c_pozition[0])
            self.win.addstr(text)
            self.win.refresh()

            self.is_first_display = False
        curses.curs_set(0)
        self.is_first_display = True
        return text

class PlayerDog:
    def __init__(self, x, y):
        self.x = x
        self.y = y