import os
import importlib.util
from modAPI.base_mod import BaseMod
import time as t


class ModLoader:
    def __init__(self, core, win, config, mods_directory='mods'):
        self.mods_directory = mods_directory
        self.core = core
        self.core.mods = []  # Инициализируем список модов в Core
        self.win = win
        self.config = config
        self.mods = []

        self.y = 0

    def load_mods(self):
        for mod_name in os.listdir(self.mods_directory):
            mod_path = os.path.join(self.mods_directory, mod_name)
            if os.path.isdir(mod_path):
                init_file = os.path.join(mod_path, '__init__.py')
                if os.path.isfile(init_file):
                    spec = importlib.util.spec_from_file_location(mod_name, init_file)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    for attribute_name in dir(mod):
                        attribute = getattr(mod, attribute_name)
                        if isinstance(attribute, type) and issubclass(attribute, BaseMod) and attribute is not BaseMod:
                            mod_instance = attribute(self.core)  # Передаём core в конструктор мода
                            self.mods.append(mod_instance)
                            self.core.mods.append(mod_instance)  # Добавляем мод в core

    def run_mods(self):
        for mod in self.mods:
            mod.run()

    def print_mods_info(self):
        self.win.clear()
        self.win.addstr(self.y, 0,"Loaded Mods Information:")
        self.y=+1
        t.sleep(self.config.delayOutput)
        self.win.refresh()
        for mod in self.mods:
            self.win.addstr(self.y, 0,f" => {mod.mod_name}:")
            self.y = self.y + 1
            t.sleep(self.config.delayOutput)
            self.win.refresh()

            self.win.addstr(self.y, 0,f"  -> {mod.mod_description}")
            self.y = self.y + 1
            t.sleep(self.config.delayOutput)
            self.win.refresh()

            self.win.addstr(self.y, 0,f"  -> {mod.author}")
            self.y = self.y + 1
            t.sleep(self.config.delayOutput)
            self.win.refresh()

            self.win.addstr(self.y, 0,f"  -> {mod.version}")
            self.y = self.y + 1
            t.sleep(self.config.delayOutput)
            self.win.refresh()
