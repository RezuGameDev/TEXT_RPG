# base_mod.py
class BaseMod:
    def __init__(self, core):
        self.core = core
        self.mod_name = "Base Mod"
        self.mod_description = "Base description"
        self.author = "Author"
        self.version = "1.0"
        self.mod_update_interval=0.5

    def run(self):
        raise NotImplementedError("Each mod must implement the run method")
    
    def update(self):
        pass
