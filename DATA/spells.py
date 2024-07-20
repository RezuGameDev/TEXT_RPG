import random as r

class BaseSpell:
    def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
        self.player = player
        self.consolas = consolas
        self.table_menu = table_menu
        self.ability = ability
        self.equipment = equipment
        self.resistances = resistances
        self.game_flags = game_flags
        self.win = win

class Spells(BaseSpell):
    def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
        super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)
        self.all_spells = {
            0: Spells.TextRPG.TestSpell(player, consolas, table_menu, ability, equipment, resistances, game_flags, win),
            1: Spells.TextRPG.HealingTouch1Spell(player, consolas, table_menu, ability, equipment, resistances, game_flags, win),
            2: Spells.TextRPG.HealingTouch2Spell(player, consolas, table_menu, ability, equipment, resistances, game_flags, win),
            3: Spells.TextRPG.FireFlashSpell(player, consolas, table_menu, ability, equipment, resistances, game_flags, win),
        }

    def use_spell(self, spell_id, monstrHP, monstrMaxHP):
        if spell_id in self.all_spells:
            spell = self.all_spells[spell_id]
            return spell.use(monstrHP, monstrMaxHP)
        else:
            raise ValueError(f"Spell with ID {spell_id} does not exist.")

    class TextRPG(BaseSpell):
        def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
            super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)

        class TestSpell(BaseSpell):
            def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
                super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)
                self.ID = 0
                self.name = "Test Spell"
                self.force = 1
                self.damage = 22
                self.required_mana = 10
                self.spell_info = -1
                self.info = "Test Spell INFO"

            def use(self, monstrHP, monstrMaxHP):
                if self.has_enough_mana():
                    monstrHP = self.cast_spell(monstrHP, monstrMaxHP)
                    self.spell_info = 1
                else:
                    self.handle_not_enough_mana()
                
                return monstrHP, self.spell_info

            def has_enough_mana(self):
                return self.player.mana >= self.required_mana

            def cast_spell(self, monstrHP, monstrMaxHP):
                self.player.mana -= self.required_mana
                monstrHP -= self.damage

                if monstrHP < 0:
                    monstrHP = 0

                self.consolas.create_table(f"{self.player.mana} / {self.player.maxMana} mana | -{self.required_mana} mana", table_width=26)
                self.win.getch()
                self.consolas.create_table(f"monstr : {monstrHP} / {monstrMaxHP} | damage : {self.damage}", table_width=30)
                self.win.getch()

                return monstrHP

            def handle_not_enough_mana(self):
                if r.randint(1, 20) + self.player.luck > r.randint(1, 20):
                    self.consolas.create_table("you didn't have enough mana but you avoided the enemy's hit", table_width=34)
                    self.spell_info = 0
                else:
                    self.consolas.create_table("you didn't have enough mana, the Varangian took advantage of your confusion and attacked", table_width=45)
                    self.spell_info = -1
                self.win.getch()

        class HealingTouch1Spell(BaseSpell):
            def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
                super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)
                self.ID = 1
                self.name = "Healing Touch I"
                self.force = 1
                self.required_mana = 10
                self.spell_info = -1
                self.heal = 10
                self.info = "heals you for 10, requires 10 mana"

            def use(self, monstrHP, monstrMaxHP):
                if self.has_enough_mana():
                    monstrHP = self.cast_spell(monstrHP)
                    self.spell_info = 1
                else:
                    self.handle_not_enough_mana()
                
                return monstrHP, self.spell_info

            def has_enough_mana(self):
                return self.player.mana >= self.required_mana

            def cast_spell(self, monstrHP):
                self.player.mana -= self.required_mana
                self.player.Hp += self.heal

                if self.player.Hp > self.player.maxHp:
                    self.player.Hp = self.player.maxHp

                self.consolas.create_table(f"{self.player.mana} / {self.player.maxMana} mana | -{self.required_mana} mana", table_width=26)
                self.win.getch()
                self.consolas.create_table(f"{self.player.name} : {self.player.Hp} / {self.player.maxHp} | heal : {self.heal}", table_width=30)
                self.win.getch()

                return monstrHP

            def handle_not_enough_mana(self):
                if r.randint(1, 20) + self.player.luck > r.randint(1, 20):
                    self.consolas.create_table("you didn't have enough mana but you avoided the enemy's hit", table_width=34)
                    self.spell_info = 0
                else:
                    self.consolas.create_table("you didn't have enough mana, the Varangian took advantage of your confusion and attacked", table_width=45)
                    self.spell_info = -1
                self.win.getch()

        class HealingTouch2Spell(BaseSpell):
            def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
                super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)
                self.ID = 2
                self.name = "Healing Touch II"
                self.force = 1
                self.required_mana = 15
                self.spell_info = -1
                self.heal = 20
                self.info = "heals you for 20, requires 15 mana"

            def use(self, monstrHP, monstrMaxHP):
                if self.has_enough_mana():
                    monstrHP = self.cast_spell(monstrHP)
                    self.spell_info = 1
                else:
                    self.handle_not_enough_mana()
                
                return monstrHP, self.spell_info

            def has_enough_mana(self):
                return self.player.mana >= self.required_mana

            def cast_spell(self, monstrHP):
                self.player.mana -= self.required_mana
                self.player.Hp += self.heal

                if self.player.Hp > self.player.maxHp:
                    self.player.Hp = self.player.maxHp

                self.consolas.create_table(f"{self.player.mana} / {self.player.maxMana} mana | -{self.required_mana} mana", table_width=26)
                self.win.getch()
                self.consolas.create_table(f"{self.player.name} : {self.player.Hp} / {self.player.maxHp} | heal : {self.heal}", table_width=30)
                self.win.getch()

                return monstrHP

            def handle_not_enough_mana(self):
                if r.randint(1, 20) + self.player.luck > r.randint(1, 20):
                    self.consolas.create_table("you didn't have enough mana but you avoided the enemy's hit", table_width=34)
                    self.spell_info = 0
                else:
                    self.consolas.create_table("you didn't have enough mana, the Varangian took advantage of your confusion and attacked", table_width=45)
                    self.spell_info = -1
                self.win.getch()

        class FireFlashSpell(BaseSpell):
            def __init__(self, player, consolas, table_menu, ability, equipment, resistances, game_flags, win):
                super().__init__(player, consolas, table_menu, ability, equipment, resistances, game_flags, win)
                self.ID = 3
                self.name = "Fire Flash"
                self.force = 1
                self.damage = 27
                self.required_mana = 20
                self.spell_info = -1
                self.info = "deals 27 damage to the enemy, requires 20 mana"

            def use(self, monstrHP, monstrMaxHP):
                if self.has_enough_mana():
                    monstrHP = self.cast_spell(monstrHP, monstrMaxHP)
                    self.spell_info = 1
                else:
                    self.handle_not_enough_mana()
                
                return monstrHP, self.spell_info

            def has_enough_mana(self):
                return self.player.mana >= self.required_mana

            def cast_spell(self, monstrHP, monstrMaxHP):
                self.player.mana -= self.required_mana
                monstrHP -= self.damage

                if monstrHP < 0:
                    monstrHP = 0

                self.consolas.create_table(f"{self.player.mana} / {self.player.maxMana} mana | -{self.required_mana} mana", table_width=26)
                self.win.getch()
                self.consolas.create_table(f"monstr : {monstrHP} / {monstrMaxHP} | damage : {self.damage}", table_width=30)
                self.win.getch()

                return monstrHP

            def handle_not_enough_mana(self):
                if r.randint(1, 20) + self.player.luck > r.randint(1, 20):
                    self.consolas.create_table("you didn't have enough mana but you avoided the enemy's hit", table_width=34)
                    self.spell_info = 0
                else:
                    self.consolas.create_table("you didn't have enough mana, the Varangian took advantage of your confusion and attacked", table_width=45)
                    self.spell_info = -1
                self.win.getch()