from tkinter import messagebox
from modAPI.base_mod import BaseMod

class TestMod(BaseMod):
    def __init__(self, core):
        super().__init__(core)
        self.mod_name = "Test Mod"
        self.mod_description = "A test mod for demonstration purposes"
        self.author = "Fantomm"
        self.version = "1.0"
        self.mod_update_interval = 0.1

    def run(self):
        pass

    def update_mods(self):
        if self.Tregers.autorsMeny:
            messagebox.showinfo("Debug", "OK | OK | OK | OK")
