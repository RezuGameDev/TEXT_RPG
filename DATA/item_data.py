# названия предмета = {
#   ID : 1
#   названия : "названия",
#   редкость : "Common"\"Uncommon"\"Rare"\"Epic"\"Legendary",
#   тип : 1 - зелье \ 2 - шлем \ 3 - нагрудник \ 4 - меч \ 5 - кинжал \ 6 - посох \ 7 - щит, 
#       type: 1 - potion \ 2 - helmet \ 3 - breastplate \ 4 - sword \ 5 - dagger \ 6 - staff \ 7 - shield,
#   защита\урон : "защита\урон",
#   указание какая защита\урон (физичиская\мфгичиская),
#   другие показатели по надобности
#}
class ItemManager:
    class Item:
        def __init__(self, manager, ID, name, rarity, item_type, minGold, maxGold, info):
            self.manager = manager
            self.ID = ID
            self.name = name
            self.rarity = rarity
            self.item_type = item_type
            self.minGold = minGold
            self.maxGold = maxGold
            self.info = info

    class Potion(Item):
        def __init__(self, manager, ID, name, rarity, item_type, minGold, maxGold, info, hp_increase=0, mana_increase=0):
            super().__init__(manager, ID, name, rarity, item_type, minGold, maxGold, info)
            self.hp_increase = hp_increase
            self.mana_increase = mana_increase

        def use(self):
            if self.hp_increase:
                self.manager.player.Hp += self.hp_increase
                if self.manager.player.Hp > self.manager.player.maxHp:
                    self.manager.player.Hp = self.manager.player.maxHp
                self.manager.consolas.create_table(f"HP: {self.manager.player.Hp} / {self.manager.player.maxHp}", alignment={0: "center"}, table_width=22)
            if self.mana_increase:
                self.manager.player.mana += self.mana_increase
                if self.manager.player.mana > self.manager.player.maxMana:
                    self.manager.player.mana = self.manager.player.maxMana
                self.manager.consolas.create_table(f"Mana: {self.manager.player.mana} / {self.manager.player.maxMana}", alignment={0: "center"}, table_width=22)
            self.manager.player.item.remove(self.ID)

    class StrengthTonic(Item):
        def __init__(self, manager, ID, name, rarity, item_type, minGold, maxGold, info, damage_increase):
            super().__init__(manager, ID, name, rarity, item_type, minGold, maxGold, info)
            self.damage_increase = damage_increase

        def use(self):
            self.manager.player.Effects.append(self.ID)
            self.manager.player.item.remove(self.ID)

    class Equipment(Item):
        def __init__(self, manager, ID, name, rarity, item_type, minGold, maxGold, info, damage=0, mana=0, physical_resist=0):
            super().__init__(manager, ID, name, rarity, item_type, minGold, maxGold, info)
            self.damage = damage
            self.mana = mana
            self.physical_resist = physical_resist

        def equip(self):
            if self.item_type == 2:
                if self.manager.equipment.helmetID == None:
                    self.manager.resistances.helmetResistInt = self.physical_resist
                    self.manager.player.helmet = self.name
                    self.manager.equipment.helmetID = self.ID
                    self.manager.player.item.remove(self.ID)
                else:
                    self.manager.player.item.append(self.manager.equipment.helmetID)

                    self.manager.resistances.helmetResistInt = self.physical_resist
                    self.manager.player.helmet = self.name
                    self.manager.equipment.helmetID = self.ID
                    self.manager.player.item.remove(self.ID)

            elif self.item_type == 3:
                if self.manager.equipment.chestplateID == None:
                    self.manager.resistances.chestplateResistInt = self.physical_resist
                    self.manager.player.chestplate = self.name
                    self.manager.equipment.chestplateID = self.ID
                    self.manager.player.item.remove(self.ID)
                else:
                    self.manager.player.item.append(self.manager.equipment.chestplateID)

                    self.manager.resistances.chestplateResistInt = self.physical_resist
                    self.manager.player.chestplate = self.name
                    self.manager.equipment.chestplateID = self.ID
                    self.manager.player.item.remove(self.ID)

            elif self.item_type == 4:
                if self.manager.player.heroClass == "SWORDSMAN":
                    if self.manager.equipment.weaponID == None:
                        self.manager.player.Dm += self.damage
                        self.manager.player.weapon = self.name
                        self.manager.equipment.weaponID = self.ID
                        self.manager.player.item.remove(self.ID)
                    else:
                        self.manager.player.item.append(self.manager.equipment.weaponID)

                        self.manager.player.Dm += self.damage
                        self.manager.player.weapon = self.name
                        self.manager.equipment.weaponID = self.ID
                        self.manager.player.item.remove(self.ID)
                else:
                    self.manager.consolas.create_table("this weapon is not suitable for you", alignment={0: "center"}, table_width=35)

            elif self.item_type == 5:
                if self.manager.player.heroClass == "THIEF":
                    while True:
                        choice = self.manager.table_menu.menu("inventory", ["left hand", "right hand"], tips=False, y=1)
                        if choice == "0":
                            if self.manager.equipment.weaponID == None:
                                self.manager.player.Dm += self.damage
                                self.manager.player.weapon = self.name
                                self.manager.equipment.weaponID = self.ID
                                self.manager.player.item.remove(self.ID)
                            else:
                                self.manager.player.item.append(self.manager.equipment.weaponID)

                                self.manager.player.Dm += self.damage
                                self.manager.player.weapon = self.name
                                self.manager.equipment.weaponID = self.ID
                                self.manager.player.item.remove(self.ID)
                        elif choice == "1":
                            if self.manager.equipment.weapon2ID == None:
                                self.manager.player.Dm += self.damage
                                self.manager.player.weapon2 = self.name
                                self.manager.equipment.weapon2ID = self.ID
                                self.manager.player.item.remove(self.ID)
                            else:
                                self.manager.player.item.append(self.manager.equipment.weapon2)

                                self.manager.player.Dm += self.damage
                                self.manager.player.weapon2 = self.name
                                self.manager.equipment.weapon2ID = self.ID
                                self.manager.player.item.remove(self.ID)
                else:
                    self.manager.consolas.create_table("this weapon is not suitable for you", alignment={0: "center"}, table_width=35)

            elif self.item_type == 6:
                if self.manager.player.heroClass == "MAGICIAN":
                    if self.manager.equipment.weaponID == None:
                        self.manager.player.Dm += self.damage
                        self.manager.player.weapon = self.name
                        self.manager.equipment.weaponID = self.ID
                        self.manager.player.maxMana += self.mana
                        self.manager.player.item.remove(self.ID)
                    else:
                        self.manager.player.item.append(self.manager.equipment.weaponID)

                        self.manager.player.Dm += self.damage
                        self.manager.player.weapon = self.name
                        self.manager.equipment.weaponID = self.ID
                        self.manager.player.maxMana += self.mana
                        self.manager.player.item.remove(self.ID)
                else:
                    self.manager.consolas.create_table("this weapon is not suitable for you", alignment={0: "center"}, table_width=35)

            elif self.item_type == 7:
                if self.manager.player.heroClass == "SWORDSMAN":
                    if self.manager.equipment.weapon2ID == None:
                        self.manager.resistances.shieldResistInt = self.physical_resist
                        self.manager.player.weapon2 = self.name
                        self.manager.equipment.weapon2ID = self.ID
                        self.manager.player.item.remove(self.ID)
                    else:
                        self.manager.player.item.append(self.manager.equipment.weapon2ID)

                        self.manager.resistances.shieldResistInt = self.physical_resist
                        self.manager.player.weapon2 = self.name
                        self.manager.equipment.weapon2ID = self.ID
                        self.manager.player.item.remove(self.ID)
                else:
                    self.manager.consolas.create_table("this weapon is not suitable for you", alignment={0: "center"}, table_width=35)

    def __init__(self, player, equipment, resistances, consolas, table_menu):
        self.player = player
        self.equipment = equipment
        self.resistances = resistances
        self.consolas = consolas
        self.table_menu = table_menu

        # Health Potions
        self.health_potions = [
            self.Potion(self, 0, "Health Potion I", "Common", 1, 5, 14, "Hp + 20", hp_increase=20),
            self.Potion(self, 1, "Health Potion II", "Uncommon", 1, 15, 24, "Hp + 30", hp_increase=30),
            self.Potion(self, 2, "Health Potion III", "Rare", 1, 25, 34, "Hp + 40", hp_increase=40),
            self.Potion(self, 3, "Health Potion IV", "Epic", 1, 35, 44, "Hp + 50", hp_increase=50),
            self.Potion(self, 4, "Health Potion V", "Legendary", 1, 45, 54, "Hp + 70", hp_increase=70)
        ]

        # Mana Elixirs
        self.mana_elixirs = [
            self.Potion(self, 5, "Mana Elixir I", "Common", 1, 5, 14, "Mana + 20", mana_increase=20),
            self.Potion(self, 6, "Mana Elixir II", "Uncommon", 1, 15, 24, "Mana + 30", mana_increase=30),
            self.Potion(self, 7, "Mana Elixir III", "Rare", 1, 25, 34, "Mana + 40", mana_increase=40),
            self.Potion(self, 8, "Mana Elixir IV", "Epic", 1, 35, 44, "Mana + 50", mana_increase=50),
            self.Potion(self, 9, "Mana Elixir V", "Legendary", 1, 45, 54, "Mana + 70", mana_increase=70)
        ]

        # Strength Tonics
        self.strength_tonics = [
            self.StrengthTonic(self, 10, "Strength Tonic I", "Common", 1, 5, 14, "Damage + 5", damage_increase=5),
            self.StrengthTonic(self, 11, "Strength Tonic II", "Uncommon", 1, 15, 24, "Damage + 10", damage_increase=10),
            self.StrengthTonic(self, 12, "Strength Tonic III", "Rare", 1, 25, 34, "Damage + 15", damage_increase=15),
            self.StrengthTonic(self, 13, "Strength Tonic IV", "Epic", 1, 35, 44, "Damage + 20", damage_increase=20),
            self.StrengthTonic(self, 14, "Strength Tonic V", "Legendary", 1, 45, 54, "Damage + 25", damage_increase=25)
        ]

        # Equipment Items (Weapons, Armor, etc.)
        self.equipments = {
            "swords": [
                self.Equipment(self, 15, "Iron Sword", "Common", 4, 23, 34, "10 Damage \n only for the \"swordsman\" class", damage=10),
            ],

            "daggers": [
                self.Equipment(self, 16, "Iron Dagger", "Common", 5, 15, 26, "5 Damage \n only for the \"thief\" class", damage=5),
            ],

            "shields": [
                self.Equipment(self, 17, "Iron Shield", "Common", 7, 25, 36, "Physical Resist: 2% \n only for the \"swordsman\" class", physical_resist=0.02),
            ],

            "armors": [
                self.Equipment(self, 18, "Iron Armor", "Common", 3, 28, 39, "Physical Resist: 5%", physical_resist=0.05),
            ],
            
            "helmets": [
                self.Equipment(self, 19, "Iron Helm", "Common", 2, 25, 36, "Physical Resist: 3%", physical_resist=0.03),
            ],

            "staffs": [
                self.Equipment(self, 20, "Wooden Staff", "Common", 6, 26, 37, "Damage + 1 \n Mana + 15 \n only for the \"magician\" class", damage=1, mana=15),
            ],
        }

        # Collect all items from the equipment categories
        self.all_equipment = []
        for category in self.equipments.values():
            self.all_equipment.extend(category)

        # All Potions and Tonics
        self.alchemical_items = self.health_potions + self.mana_elixirs + self.strength_tonics
        self.blacksmith_items = self.all_equipment

        # All Items
        self.all_items = self.alchemical_items + self.all_equipment

        # ID to Item Mapping
        self.item_use_functions = {item.ID: item.use for item in self.alchemical_items}
        self.item_equip_functions = {item.ID: item.equip for item in self.all_equipment}

    def use_item(self, item_id):
        if item_id in self.item_use_functions:
            self.item_use_functions[item_id]()
        elif item_id in self.item_equip_functions:
            self.item_equip_functions[item_id]()
        else:
            print("This item cannot be used or equipped.")
