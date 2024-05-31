# mod_loader.py
import os
import importlib.util
from modAPI.base_mod import BaseMod

class ModLoader:
    def __init__(self, core, mods_directory='mods'):
        self.mods_directory = mods_directory
        self.core = core
        self.core.mods = []  # Инициализируем список модов в Core
        self.mods = []

    def load_mods(self):
        for mod_name in os.listdir(self.mods_directory):
            mod_path = os.path.join(self.mods_directory, mod_name)
            if os.path.isdir(mod_path):
                init_file = os.path.join(mod_path, '__init__.py')
                if os.path.isfile(init_file):
                    print(f"Loading mod ({mod_name})...")
                    spec = importlib.util.spec_from_file_location(mod_name, init_file)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    for attribute_name in dir(mod):
                        attribute = getattr(mod, attribute_name)
                        if isinstance(attribute, type) and issubclass(attribute, BaseMod) and attribute is not BaseMod:
                            mod_instance = attribute(self.core)  # Передаём core в конструктор мода
                            self.mods.append(mod_instance)
                            self.core.mods.append(mod_instance)  # Добавляем мод в core
                            print(f"Mod ({mod_instance.mod_name}) loaded")
                            print(f"Mod ({mod_instance.mod_name}) added to the list of mods")

    def run_mods(self):
        for mod in self.mods:
            mod.run()

    def print_mods_info(self):
        print("\nLoaded Mods Information:")
        for mod in self.mods:
            print(f"{mod.mod_name}:")
            print(f" - {mod.mod_description}")
            print(f" - {mod.author}")
            print(f" - {mod.version}")
