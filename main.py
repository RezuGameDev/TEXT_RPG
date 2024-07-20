import os
import logging
from datetime import datetime
from typing import List
import EVENT.debug as db
from modAPI.core import Core
import modAPI.mod_loader as ml
import threading

class Logger:
    def __init__(self, log_folder: str):
        self.log_folder = log_folder
        self.setup_logger()

    def setup_logger(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"LOG__{current_time}__.log"
        log_path = os.path.join(self.log_folder, log_filename)
        logging.basicConfig(filename=log_path, level=logging.DEBUG)

class Game:
    def __init__(self, config ,player, equipment, game_flags, logo, resistances, ability, save_manager, world_values, stdscr, console_settings, tregers):
        self.config = config
        self.player = player
        self.equipment = equipment
        self.game_flags = game_flags
        self.logo = logo
        self.resistances = resistances
        self.ability = ability
        self.save_manager = save_manager
        self.world_values = world_values
        self.console_settings = console_settings
        self.stdscr = stdscr
        self.tregers = tregers

        self.item_manager = None
        self.table_menu = None
        self.core = None
        self.win = None
        self.consolas = None
        self.event = None
        self.tui = None
        self.spells = None

    def start(self):
        self.console_settings.set_borderless_fullscreen()
        d.curses.resize_term(0, 0)
        d.curses.curs_set(0)

        self.win = self.console_settings.create_fullscreen_window(self.stdscr)
        self.win.keypad(True)
        self.win.clear()
        self.win.refresh()

        self.load_modules()
        self.show_main_menu()

    def load_mods(self):
        loader = ml.ModLoader(core=self.core, win=self.win, config=self.config)
        loader.load_mods()
        loader.print_mods_info()
        loader.run_mods()
        self.win.getch()

        mod_update_thread = threading.Thread(target=self.core.update_mods, daemon=True)
        mod_update_thread.start()

    def load_modules(self):
        self.table_menu = d.TableMenu(self.config, self.win)
        self.consolas = d.Consolas(self.config, player, self.win)
        self.item_manager = d.itemd.ItemManager(self.player, self.equipment, self.resistances, self.consolas, self.table_menu)
        self.spells = d.spells.Spells(self.player, self.consolas, self.table_menu, self.ability, self.equipment, self.resistances, self.game_flags, self.win)
        self.core = Core(self.config, self.world_values, self.game_flags, self.resistances, self.equipment, self.player, self.ability, self.save_manager, self.logo, self.consolas, self.table_menu, self.tregers, self.spells)
        self.event = event.Event(self.player, self.config, self.equipment, self.game_flags, self.world_values, self.ability, self.resistances, self.consolas, self.save_manager, self.win, self.table_menu, self.item_manager, self.spells)
        self.tui = self.event.TUI(self.game_flags, self.consolas, self.win, self.save_manager, self.table_menu, self.player, self.item_manager, self.world_values, self.config, self.equipment, self.ability, self.resistances, self.spells)


        imports_list = [
            "DATA.data", "EVENT.event", "sys", "time", "DATA.audio.data_audio",
            "json", "pyautogui", "ctypes", "DATA.level_data", "math", "os",
            "DATA.monster_data", "DATA.data_persons", "DATA.item_data", "load scne",
            "random", "sqlite3", "datetime", "threading", "requests",
            "beautifulsoup4", "selenium", "csv", "uuid", "hashlib",
            "socket", "pygame", "pandas", "openpyxl", "matplotlib",
            "pillow", "asyncio", "asyncpg", "xml", "re",
            "multiprocessing", "logging", "urllib", "datetime",
            "glob", "shutil", "zipfile", "argparse", "configparser"
        ]

        if self.config.anim:
            self.consolas.loading_animation(imports_list)
        self.load_mods()

    def show_main_menu(self):
        if self.config.anim:
            self.consolas.play_animation(self.logo.company_logo, 0.3, y=5)

        while self.game_flags.run:
            self.tregers.startGame = True
            d.da.play_background_music()
            self.tregers.startGame = False

            while self.game_flags.meny:
                self.tregers.mainMeny = True
                self.win.clear()
                self.tregers.mainMeny = False

                self.show_sub_menus()

            while self.game_flags.play:
                self.consolas.play_animation(self.logo.text_rpg_logo, 0.2, y=5)
                self.save_manager.save_file()
                self.show_game_menu()

            while self.game_flags.game_over:
                self.show_game_over_screen()

    def show_sub_menus(self):
        while self.game_flags.autors:
            self.tregers.autorsMeny = True
            self.create_authors_table()
            self.tregers.autorsMeny = False

            self.game_flags.skip_enter = True
            self.game_flags.autors = False

        while self.game_flags.seting:
            self.create_settings_table()

            self.game_flags.skip_enter = True
            self.game_flags.seting = False

        self.win.refresh()
        choice = self.table_menu.menu("Menu Title", ["New game", "Load game", "Authors", "Seting", "Exit game"], tips=False)

        if choice == "0":
            self.create_hero()
        elif choice == "1":
            self.load_game()
        elif choice == "2":
            self.game_flags.autors = True
        elif choice == "3":
            self.game_flags.seting = True
        elif choice == "4":
            self.game_flags.run = False
            self.game_flags.meny = False
            d.curses.endwin()

    def create_authors_table(self):
        self.consolas.create_table(
            "Graphics", "Fantomm",
            "Music", "Fantomm",
            "Code", "Fantomm",
            "Plot", "Факсянь",
            "ihateniggers",
            "didn't participate", "He'sCodi",
            separator_positions=[0, 1, 2, 3, 4, 5, 6, 8, 9],
            alignment={0: "center", 2: "center", 4: "center", 6: "center", 9:"center"},
        )

        self.table_menu.menu("authors", ["Exit to menu"], color='cyan', y=9, tips=False, clear=False)


    def create_settings_table(self):
        self.consolas.create_table(
            "Setting",
            "[1] delay between output = 0.1 s.",
            "[0] Exit to menu",
            separator_positions=[0],
            alignment={0: "center"},
            table_width=44,
        )

    def change_delay_output(self):
        self.consolas.create_table(
            "Setting",
            "enter what value to change to (maximum 1 second)",
            separator_positions=[0],
            alignment={0: "center"},
            table_width=44,
        )
        delay_output = input()

    def create_hero(self):
        self.game_flags.creating_hero = True
        self.tregers.newGame = True
        d.time.sleep(0.1)
        self.tregers.newGame = False

        while self.game_flags.creating_hero:
            self.consolas.create_table(
                "Enter your name",
                alignment={0: "center"},
                y=17,
            )
            self.player.name = self.table_menu.text_box(clear=False, max_sumbol=7)

            if len(self.player.name) > 7:
                self.consolas.create_table(
                    "Name is too long, maximum length is 7 characters",
                    style="error",
                )
                self.win.getch()
            elif self.player.name == "NULL":
                self.player.name = " "
                self.set_hero_class("NULL", 0, 70, 10, -0.8, -0.8, -0.8, -0.8, False, False, True, 50, 50, 1, 0)
                self.player.item = [1, 1, 1]
                self.game_flags.meny = False
                self.game_flags.play = True
                break
            elif self.player.name == "":
                self.consolas.create_table(
                    "name cannot be empty",
                    style="error",
                )
                self.win.getch()
            else:
                self.choose_hero_class()

    def choose_hero_class(self):
        while self.game_flags.creating_hero:

            class_info = ["Magician: \n Magic resistance \n Mana regeneration ++\n HP: 160\n Damage: 15",
                          "Thief: \n Poison resistance\n Toxin resistance\n More chances of receiving coins and experience\n HP: 140\n Damage: 10 + DP",
                          "Swordsman: \n Physical attack resistance\n HP: 190\n Damage: 30"
                          ]
            
            class_choice = self.table_menu.menu(title="classes" ,options=["MAGICIAN","THIEF","SWORDSMAN"] ,additional_info=class_info)

            if class_choice == "0":
                self.set_hero_class("MAGICIAN", 70, 100, 5, 0.95, 1, 1, 1, True, False, False, 160, 160, 2, 1)
            elif class_choice == "1":
                self.set_hero_class("THIEF", 120, 100, 10, 1, 1, 0.95, 0.95, False, True, True, 60, 60, 3, 1.5)
            elif class_choice == "2":
                self.set_hero_class("SWORDSMAN", 50, 100, 22, 1, 0.95, 1, 1, False, False, False, 20, 20, 1, 0.5)

    def set_hero_class(self, hero_class: str, gold: int, hp: int, damage: int, magic_resist: float, physical_resist: float,
                    poison_resist: float, Toxin_resist: float , mana_recovery: bool, double_punch: bool, earning_coins_and_XP: bool,
                    max_mana: int, mana: int, speed: int, luck: int,):
        self.game_flags.meny = False
        self.game_flags.creating_hero = False
        self.game_flags.play = True

        self.player.heroClass = hero_class
        self.player.gold = gold
        self.player.Hp = hp
        self.player.maxHp = hp
        self.player.Dm = damage
        self.resistances.MagicResistInt = magic_resist
        self.resistances.PhysicalResistInt = physical_resist
        self.resistances.PoisonResistInt = poison_resist
        self.resistances.ToxinResistInt = Toxin_resist
        self.ability.ManaRecovery = mana_recovery
        self.ability.DoublePunch = double_punch
        self.ability.EarningCoinsAndXP = earning_coins_and_XP
        self.player.maxMana = max_mana
        self.player.mana = mana
        self.player.speed = speed
        self.player.luck = luck

        self.player.item = [1, 1]

        if self.player.heroClass == "MAGICIAN":
            self.player.spells = [2, 3]
        elif self.player.heroClass == "THIEF":
            self.player.spells = [1]
        elif self.player.heroClass == "SWORDSMAN":
            pass
        elif self.player.heroClass == "NULL":
            self.player.spells = [0]

    def load_game(self):
        self.tregers.loadGame = True
        self.save_manager.load_file()
        self.tregers.loadGame = False

        if not self.game_flags.errore_load:
            self.consolas.create_table(
                f"Welcome, {self.player.name}",
                alignment={0: "center"},
                table_width=26,
            )
            self.win.getch()
            self.game_flags.meny = False
            self.game_flags.play = True

    def show_game_menu(self):
        self.consolas.create_table(
            f"name : {self.player.name}",
            f"class : {self.player.heroClass}",
            f"HP : {self.player.Hp}",
            f"gold : {self.player.gold}",
            f"XP : {self.player.Xp} / {self.player.XpToLv}",
            f"Lv : {self.player.Lv}",
            use_clear=False,
            separator_positions=[1],
            y=15
        )

        choice = self.table_menu.menu("Game Menu", ["exit", "start"], clear=False, tips=False, y=25)

        if choice == "0":
            self.game_flags.meny = True
            self.game_flags.play = False
            self.save_manager.save_file()
        elif choice == "1":
            self.start_game()

    def start_game(self):
        self.game_flags.trips = True
        self.save_manager.load_file()
        if self.player.Px == 0 and self.player.Py == 0:
            self.player.Px = getattr(d.ld, f"layer{self.player.layer}").XSpawn
            self.player.Py = getattr(d.ld, f"layer{self.player.layer}").YSpawn

        playerDog = d.PlayerDog(self.player.Px, self.player.Py)
        self.tui.start_game(self.player.layer, playerDog)

    def show_game_over_screen(self):
        self.consolas.create_table(
            f"{self.player.name}",
            f"point : {self.player.points}",
            f"HP : {self.player.maxHp}",
            f"damage : {self.player.Dm}",
            f"gold : {self.player.gold}",
            f"Lv : {self.player.Lv}",
            separator_positions=[0, 1],
            alignment={0: "center", 1: "center"},
            table_width=25,
        )
        self.win.getch()
        d.os.remove(d.save_path)
        self.game_flags.play = False
        self.game_flags.meny = True
        self.game_flags.game_over = False


if __name__ == "__main__":
    import DATA.data as d
    import EVENT.event as event
    from curses import wrapper

    logger = Logger(log_folder='LOG')

    config = d.Config()
    player = d.Player()
    equipment = d.Equipment()
    game_flags = d.GameFlags()
    logo = d.Logo()
    resistances = d.Resistances()
    ability = d.Ability()
    world_values = d.WorldValues()
    console_settings = d.ConsoleSettings()
    tregers = d.Tregers()
    save_manager = d.SaveManager(player, resistances, equipment, ability)


    console_settings.set_console_buffer_size(400, 59)
    console_settings.set_console_font(font_size=console_settings.get_font_size())

    def main(stdscr):
        game = Game(config ,player, equipment, game_flags, logo, resistances, ability, save_manager, world_values, stdscr, console_settings, tregers)
        game.start()
            
    try:
        wrapper(main)
    except Exception as e:
        logging.error(f'ERROR: {str(e)}', exc_info=True)
