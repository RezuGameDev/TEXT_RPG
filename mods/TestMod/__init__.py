from modAPI.base_mod import BaseMod

class TestMod(BaseMod):
    def __init__(self, core):
        super().__init__(core)
        self.mod_name = "Test Mod"
        self.mod_description = "A test mod for demonstration purposes"
        self.author = "Mod Author"
        self.version = "1.0"
        
