import time
import threading
from tkinter import messagebox

class Core:
    def __init__(self, Config, WorldValues, GameFlags, Resistances, Equipment, Player, Ability, SaveManager, Logo, Consolas, TableMenu, Tregers, Spells):
        self.Config = Config
        self.WorldValues = WorldValues
        self.GameFlags = GameFlags
        self.Resistances = Resistances
        self.Equipment = Equipment
        self.Player = Player
        self.Ability = Ability
        self.SaveManager = SaveManager
        self.Logo = Logo
        self.Consolas = Consolas
        self.TableMenu = TableMenu
        self.Tregers = Tregers
        self.Spells = Spells

        self.mod_update_interval = 0.5  # Интервал обновления модов в секундах
        self.mods = []
        self.mod_update_thread = threading.Thread(target=self.update_mods)
        self.mod_update_thread.daemon = True

    def run(self):
        pass

    def update_mods(self):
        while True:
            for mod in self.mods:
                mod.update()
            time.sleep(self.mod_update_interval)
    
    def start_mod_updates(self):
        self.mod_update_thread.start()

