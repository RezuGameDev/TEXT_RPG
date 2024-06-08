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
    def __init__(self, config ,player, equipment, game_flags, logo, resistances, ability, consolas, save_manager, world_values, d, event):
        self.config = config
        self.player = player
        self.equipment = equipment
        self.game_flags = game_flags
        self.logo = logo
        self.resistances = resistances
        self.ability = ability
        self.consolas = consolas
        self.save_manager = save_manager
        self.world_values = world_values

        self.d = d
        self.events = event
        self.core = Core(self.config, self.world_values, self.game_flags, self.resistances, self.equipment, self.player, self.ability, self.save_manager, self.logo, self.consolas)

        self.event = self.events.Event(
                                        self.player,
                                        self.config,
                                        self.equipment,
                                        self.game_flags,
                                        self.world_values,
                                        self.ability,
                                        self.resistances,
                                        self.consolas,
                                        self.save_manager,
                                        self.d
                                    )

    def start(self):
        self.load_modules()
        self.show_main_menu()

    def load_mods(self):
        loader = ml.ModLoader(core=self.core)
        loader.load_mods()
        loader.run_mods()

        mod_update_thread = threading.Thread(target=self.core.update_mods, daemon=True)
        mod_update_thread.start()

    def load_modules(self):
        self.consolas.clear()
        self.consolas.open_console_fullscreen()
        self.consolas.set_font_size(22)

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
        input()

    def show_main_menu(self):
        if self.config.anim:
            self.consolas.play_animation(self.logo.company_logo, 0.3)
        self.d.time.sleep(1)
        self.consolas.set_font_size(23)

        while self.game_flags.run:
            self.d.t.startGame = True
            self.d.da.play_background_music()
            self.d.t.startGame = False

            while self.game_flags.meny:
                self.d.t.mainMeny = True
                self.consolas.clear()
                self.d.t.mainMeny = False

                self.show_sub_menus()

            while self.game_flags.play:
                self.consolas.play_animation(self.logo.text_rpg_logo, 0.2)
                self.save_manager.save_file()
                self.show_game_menu()

            while self.game_flags.game_over:
                self.show_game_over_screen()

    def show_sub_menus(self):
        while self.game_flags.autors:
            self.d.t.autorsMeny = True
            self.create_authors_table()
            self.d.t.autorsMeny = False

            self.game_flags.skip_enter = True
            self.game_flags.autors = False
            choice = input("> ")
            if choice == "0":
                self.game_flags.autors = False
                break

        while self.config.seting:
            self.create_settings_table()

            self.game_flags.skip_enter = True
            self.game_flags.seting = False
            choice = input("> ")
            if choice == "0":
                self.game_flags.seting = False
                break
            elif choice == "1":
                self.change_delay_output()

        self.create_main_menu_table()
        choice = input("> ")

        if choice == "1":
            self.create_hero()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            self.game_flags.autors = True
        elif choice == "4":
            self.game_flags.seting = True
        elif choice == "0":
            self.game_flags.run = False
            self.game_flags.meny = False

    def create_authors_table(self):
        self.consolas.create_table(
            "info",
            True,
            [0, 1, 2, 3, 4, 5, 6, 7],
            {1: "center", 3: "center", 5: "center", 7: "center"},
            22,
            "[0] Exit to menu",
            "Graphics", "Fantomm",
            "Music", "Fantomm",
            "Code", "Fantomm",
            "Plot", "Факсянь",
            "ihateniggers",
        )

    def create_settings_table(self):
        self.consolas.create_table(
            "info",
            True,
            [0],
            {0: "center"},
            44,
            "Setting",
            "[1] delay between output = 0.1 s.",
            "[0] Exit to menu",
        )

    def change_delay_output(self):
        self.consolas.create_table(
            "info",
            True,
            [0],
            {0: "center"},
            44,
            "Setting",
            "enter what value to change to (maximum 1 second)"
        )
        delay_output = input()

    def create_main_menu_table(self):
        self.consolas.create_table(
            "info",
            True,
            None,
            None,
            22,
            "[1] New game",
            "[2] Load game",
            "[3] Authors",
            "[4] Seting",
            "[0] Exit game",
        )


    def create_hero(self):
        self.game_flags.creating_hero = True
        self.d.t.newGame = True
        self.d.time.sleep(0.1)
        self.d.t.newGame = False

        while self.game_flags.creating_hero:
            self.consolas.create_table(
                "info",
                True,
                None,
                {0: "center"},
                22,
                "Enter your name",
            )
            self.player.name = input("> ")

            if len(self.player.name) > 7:
                self.consolas.create_table(
                    "error",
                    True,
                    None,
                    None,
                    22,
                    "Name is too long, maximum length is 7 characters",
                )
                input("> ")
            elif self.player.name == "NULL":
                self.player.name = " "
                self.game_flags.meny = False
                self.game_flags.play = True
                break
            else:
                self.choose_hero_class()

    def choose_hero_class(self):
        while self.game_flags.creating_hero:
            self.consolas.create_table(
                "info",
                True,
                [0],
                {0: "center"},
                26,
                "class",
                "[1] Magician | [q] info",
                "[2] Thief | [w] info",
                "[3] Swordsman | [e] info",
            )

            class_choice = input("> ")

            if class_choice == "q":
                self.show_magician_info()
            elif class_choice == "w":
                self.show_thief_info()
            elif class_choice == "e":
                self.show_swordsman_info()
            elif class_choice == "1":
                self.set_hero_class("MAGICIAN", 70, 160, 15, 0.89, 1, 1, 1, True, False, False, 160, 160, 2)
            elif class_choice == "2":
                self.set_hero_class("THIEF", 120, 140, 10, 1, 1, 0.89, 0.89, False, True, True, 60, 60, 3)
            elif class_choice == "3":
                self.set_hero_class("SWORDSMAN", 50, 190, 30, 1, 0.89, 1, 1, False, False, False, 20, 20, 1)

    def show_magician_info(self):
        self.consolas.create_table(
            "info",
            True,
            [0, 2],
            {0: "center"},
            22,
            "Magician",
            "Magic resistance",
            "Mana regeneration ++",
            "HP: 160",
            "Damage: 15",
        )
        input("> ")

    def show_thief_info(self):
        self.consolas.create_table(
            "info",
            True,
            [0, 3],
            {0: "center"},
            22,
            "Thief",
            "Poison resistance",
            "Toxin resistance",
            "More chances of receiving coins and experience",
            "HP: 140",
            "Damage: 10 + DP",
        )
        input("> ")

    def show_swordsman_info(self):
        self.consolas.create_table(
            "info",
            True,
            [0, 1],
            {0: "center"},
            22,
            "Swordsman",
            "Physical attack resistance",
            "HP: 190",
            "Damage: 30",
        )
        input("> ")

    def set_hero_class(self, hero_class: str, gold: int, hp: int, damage: int, magic_resist: float, physical_resist: float,
                    poison_resist: float, Toxin_resist: float , mana_recovery: bool, double_punch: bool, earning_coins_and_XP: bool,
                    max_mana: int, mana: int, speed: int):
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

    def load_game(self):
        self.d.t.loadGame = True
        self.save_manager.load_file()
        self.d.t.loadGame = False

        if not self.game_flags.errore_load:
            self.consolas.create_table(
                "info",
                True,
                None,
                {0: "center"},
                26,
                f"Welcome, {self.player.name}",
            )
            input("> ")
            self.game_flags.meny = False
            self.game_flags.play = True

    def show_game_menu(self):
        self.consolas.create_table(
            "info",
            False,
            [1],
            None,
            22,
            "[0] Exit to menu",
            "[1] to start",
            f"name : {self.player.name}",
            f"class : {self.player.heroClass}",
            f"HP : {self.player.Hp}",
            f"gold : {self.player.gold}",
            f"XP : {self.player.Xp} / {self.player.XpToLv}",
            f"Lv : {self.player.Lv}"
        )

        self.d.time.sleep(0.1)
        choice = input("> ")

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
            self.player.Px = getattr(self.d.ld, f"layer{self.player.layer}").XSpawn
            self.player.Py = getattr(self.d.ld, f"layer{self.player.layer}").YSpawn

        playerDog = self.d.PlayerDog(self.player.Px, self.player.Py)
        self.event.start_game(self.player.layer, playerDog)

    def show_game_over_screen(self):
        self.consolas.create_table(
            "info",
            True,
            [0, 1],
            {0: "center", 1: "center"},
            25,
            f"{self.player.name}",
            f"point : {self.player.points}",
            f"HP : {self.player.maxHp}",
            f"damage : {self.player.Dm}",
            f"gold : {self.player.gold}",
            f"Lv : {self.player.Lv}"
        )
        input("> ")
        self.game_flags.play = False
        self.game_flags.meny = True
        self.game_flags.game_over = False


if __name__ == "__main__":
    import DATA.data as d
    import EVENT.event as event

    logger = Logger(log_folder='LOG')

    config = d.Config()
    player = d.Player()
    equipment = d.Equipment()
    game_flags = d.GameFlags()
    logo = d.Logo()
    resistances = d.Resistances()
    ability = d.Ability()
    world_values = d.WorldValues()
    consolas = d.Consolas(config, player)
    save_manager = d.SaveManager(player, resistances, equipment, ability)

    game = Game(config ,player, equipment, game_flags, logo, resistances, ability, consolas, save_manager, world_values, d, event)
    try:
        game.start()
    except Exception as e:
        logging.error(f'ERROR: {str(e)}', exc_info=True)
