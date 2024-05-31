# core.py
import time

class Core:
    def __init__(self, Config, WorldValues, GameFlags, Resistances, Equipment, Player, Ability, SaveManager, Logo, Consolas):
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
        self.mod_update_interval = 0.5  # Интервал обновления модов в секундах
        self.mods = []

    def run(self):
        pass

    def update_mods(self):
        while True:
            for mod in self.mods:
                mod.update()
            time.sleep(self.mod_update_interval)
