import logging
import math
import sys
import os
import random

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..'))

import DATA.monster_data as md
import DATA.data_persons as dp
import DATA.item_data as itemd
import EVENT.debug as db
import DATA.data as d

class Monster:
    def __init__(self, player):
        self.player = player

        random_monster = random.choice(list(md.forest.keys()))
        while md.forest[random_monster]["Lv"] >= self.player.Lv + 3:
            random_monster = random.choice(list(md.forest.keys()))
        self.name = md.forest[random_monster]["name"]
        self.hp = md.forest[random_monster]["Hp"]
        self.max_hp = md.forest[random_monster]["MaxHp"]
        self.damage = md.forest[random_monster]["Damage"]
        self.p_resist = md.forest[random_monster]["PhysicalResist"]
        self.m_resist = md.forest[random_monster]["MagicResist"]
        self.p_damage = md.forest[random_monster]["PhysicalDamage"]
        self.m_damage = md.forest[random_monster]["MagicDamage"]
        self.poi_resist = md.forest[random_monster]["PoisonResist"]
        self.aggression = md.forest[random_monster]["agresia"]
        self.xp = md.forest[random_monster]["Xp"]
        self.coin = md.forest[random_monster]["Coin"]
        self.speed = md.forest[random_monster]["speed"]
        self.lv = md.forest[random_monster]["Lv"]
        self.item = md.forest[random_monster]["item"]
        self.luck = md.forest[random_monster]["luck"]
        self.frame0 = md.forest[random_monster]["IDLE_1"]
        self.frame1 = md.forest[random_monster]["IDLE_2"]
        self.dead_frame0 = md.forest[random_monster]["DEAD"]

class BaseEvent:
    def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells):
        self.player = player
        self.config = config
        self.equipment = equipment
        self.game_flags = game_flags
        self.world_values = world_values
        self.ability = ability
        self.resistances = resistances
        self.consolas = consolas
        self.save_manager = save_manager
        self.win = win
        self.table_menu = table_menu
        self.item_meneger = item_meneger
        self.spells = spells

class Event(BaseEvent):
    def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells):
        super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells)
    class TUI:
        def __init__(self, game_flags, consolas, win, save_manager, table_menu, player, item_meneger, world_values, config, equipment, ability, resistances, spells):
            self.game_flags = game_flags
            self.consolas = consolas
            self.win = win
            self.save_manager = save_manager
            self.table_menu = table_menu
            self.player = player
            self.item_meneger = item_meneger
            self.world_values = world_values
            self.config = config
            self.equipment = equipment
            self.ability = ability
            self.resistances = resistances
            self.spells = spells

        def openInventory(self):
            self.win.clear()
            self.game_flags.inventory = True
            item_ids = self.player.item

            while self.game_flags.inventory:

                matching_classes_names = ["exit"]
                matching_classes = {}

                item_index = 1

                # Перебираем все ID предметов
                for item_id in item_ids:
                    for class_item in self.item_meneger.all_items:
                        if item_id == class_item.ID:
                            matching_classes[item_index] = class_item

                            matching_classes_names.append(f"{class_item.name}")

                            item_index += 1
                            break

                self.consolas.create_table(
                    f"name : {self.player.name}",
                    f"class : {self.player.heroClass}",
                    f"HP : {self.player.Hp} / {self.player.maxHp}",
                    f"Dm : {self.player.Dm}",
                    f"gold : {self.player.gold}",
                    f"XP : {self.player.Xp} / {self.player.XpToLv}",
                    f"Lv : {self.player.Lv}",
                    f"Mana : {self.player.mana} / {self.player.maxMana}",
                    f"IS : {self.player.improvementStar}",
                    f"layer : {self.player.layer} / 9",
                    separator_positions=[0],
                    alignment={0: "center"},
                    alignmentTable="r",
                    y=1,
                )
                self.consolas.create_table(
                    f"helmet : {self.player.helmet}",
                    f"chestplate : {self.player.chestplate}",
                    f"right hand : {self.player.weapon}",
                    f"left hand : {self.player.weapon2}",
                    use_clear=False, 
                    alignmentTable="r",
                    y=15,
                )

                choice = self.table_menu.menu("inventory", matching_classes_names, tips=False, y=1, clear=False)
                            
                if choice.isdigit() and int(choice) in matching_classes:
                    chosen_item = matching_classes[int(choice)]
                    
                    while (True):
                        choice = self.table_menu.menu("inventory", ["INFO","USE","BACK"], tips=False, y=1)
                        if choice == "0":
                            self.consolas.create_table(chosen_item.info , alignment={0 : "center"}, table_width=22)
                            self.win.getch()

                        if choice == "1":
                            if chosen_item.item_type in {1, 2, 3, 4, 5, 6 ,7}:
                                self.item_meneger.use_item(chosen_item.ID)

                            self.win.getch()
                            break
                        
                        if choice == "2":
                            break
                elif choice == "0":
                    break

        def randomEvent(self, monstr_max):
            values = list(self.world_values.chances.values())
            event = random.choices([1, 2, 3], weights=values, k=1)[0]

            if event == 1 and monstr_max > 0:
                monstar = Event.MonsterAtak(
                    self.player,
                    self.config,
                    self.equipment,
                    self.game_flags,
                    self.world_values,
                    self.ability,
                    self.resistances,
                    self.consolas,
                    self.save_manager,
                    self.win,
                    self.table_menu,
                    self.item_meneger,
                    self.spells,
                )
                monstar.monster_encounter()

                self.world_values.chances["monstr"] = max(0, self.world_values.chances["monstr"] - 5)  # Уменьшаем шансы для события 1 на 10
                self.world_values.chances["shop"] = min(100, self.world_values.chances["shop"] + 5)
                self.world_values.chances["void"] = min(100, self.world_values.chances["void"] + 5)  # Увеличиваем шансы для события 2 на 10
                monstr_max = monstr_max - 1
            elif event == 2:
                shop = Event.Shop(
                    self.player,
                    self.config,
                    self.equipment,
                    self.game_flags,
                    self.world_values,
                    self.ability,
                    self.resistances,
                    self.consolas,
                    self.save_manager,
                    self.win,
                    self.table_menu,
                    self.item_meneger,
                    self.spells,
                )
                shop.shop()
                # Изменяем шансы для следующего события
                self.world_values.chances["monstr"] = min(100, self.world_values.chances["monstr"] + 10)  # Увеличиваем шансы для события 1 на 10
                self.world_values.chances["shop"] = max(0, self.world_values.chances["shop"] - 10)
                self.world_values.chances["void"] = min(100, self.world_values.chances["void"] + 5)  # Уменьшаем шансы для события 2 на 10
            elif event == 3:
                self.world_values.chances["monstr"] = min(100, self.world_values.chances["monstr"] + 5)  # Увеличиваем шансы для события 1 на 10
                self.world_values.chances["shop"] = max(0, self.world_values.chances["shop"] + 10)
                self.world_values.chances["void"] = min(100, self.world_values.chances["void"] - 10)  # Уменьшаем шансы для события 2 на 10

            if self.player.Hp <= 0:
                self.game_flags.game_over = True
                self.game_flags.battle = False
                self.game_flags.play = False

            if self.player.mana < self.player.maxMana:
                if self.ability.ManaRecovery:
                    self.player.mana += 5
                else:
                    self.player.mana += 2
                    
                if self.player.mana > self.player.maxMana:
                    self.player.mana = self.player.maxMana
            
            return monstr_max

        def start_game(self, layer, player):
            self.structure = None
            map_layers = {
                1: (d.ld.layerMapGUI_1, d.ld.layer1),
                2: (d.ld.layerMapGUI_2, d.ld.layer2),
                3: (d.ld.layerMapGUI_3, d.ld.layer3),
                4: (d.ld.layerMapGUI_4, d.ld.layer4),
                5: (d.ld.layerMapGUI_5, d.ld.layer5),
                6: (d.ld.layerMapGUI_6, d.ld.layer6),
                7: (d.ld.layerMapGUI_7, d.ld.layer7),
                8: (d.ld.layerMapGUI_8, d.ld.layer8),
                9: (d.ld.layerMapGUI_9, d.ld.layer9)
            }

            map, layer_info = map_layers.get(layer, (d.ld.layerMapGUI_cheatcr, d.ld.layerCheatcr))

            while self.game_flags.trips: 

                if self.game_flags.game_over:
                    self.game_flags.trips = False
                    self.game_flags.play = False
                    break
                
                self.consolas.display_map(map, player, y=5)

                self.consolas.create_table("(UP|LEFT|DOWN|RIGHT|)-movement", "Q-quit", "I-inventory", "M-monstronomicon", alignmentTable="l", use_clear=False, y=1, x=5, table_width=32)
                self.consolas.create_table("ƒ-staircase", "₩-village", "ʘ-descent", "₲-Boss", "@-you", alignmentTable="l", use_clear=False, y=8, x=5, table_width=32)
                if self.structure in {0, 1, 2, 3}:
                    self.consolas.create_table("E-enter the building", alignmentTable="r", use_clear=False, y=1, table_width=32)

                move = self.win.getch()

                logging.info(f"INFO: Key pressed: {move}", exc_info=False)

                if move == 113:
                    self.player.Px = player.x
                    self.player.Py = player.y
                    self.save_manager.save_file()
                    self.game_flags.trips = False
                    break
                
                elif move == 101 and self.structure in {0, 1, 2, 3}:
                    if self.structure == 0:
                        self.entrance_village(layer, player, player.x, player.y)
                    elif self.structure == 1:
                        pass
                    elif self.structure == 2:
                        pass
                    elif self.structure == 3:
                        pass

                elif move in {d.curses.KEY_UP, d.curses.KEY_DOWN, d.curses.KEY_LEFT, d.curses.KEY_RIGHT}:
                    dx, dy = {d.curses.KEY_UP: (0, -1), d.curses.KEY_DOWN: (0, 1), d.curses.KEY_LEFT: (-1, 0), d.curses.KEY_RIGHT: (1, 0)}[move]
                    new_x, new_y = player.x + dx, player.y + dy

                    if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map):
                        if map[new_y][new_x] != '*':
                            player.x, player.y = new_x, new_y
                            if new_x in layer_info.XDungen and new_y in layer_info.YDungen:
                                if new_x == layer_info.XSettlements and new_y == layer_info.YSettlements:
                                    self.structure = 0
                                elif new_x == layer_info.XBoss and new_y == layer_info.YBoss:
                                    self.structure = 1
                                elif new_x == layer_info.XExit and new_y == layer_info.YExit:
                                    self.structure = 2
                                elif new_x == layer_info.XSpawn and new_y == layer_info.YSpawn:
                                    self.structure = 3
                            else:
                                self.structure = None
                                layer_info.monsterMax = self.randomEvent(layer_info.monsterMax)
                        else:
                            self.consolas.create_table( "You cannot go there", style="erorre")
                    else:
                        self.consolas.create_table("Beyond the bounds of the gaming world", style="erorre", table_width=22)

                elif move == 105:
                    self.openInventory()

                elif move == 109:
                    if self.player.playerMonstronomicon:
                        pass
                    else:
                        # Доделать
                        self.consolas.create_table("")

        def entrance_village(self, layer, player, Sx, Sy):
            self.shop = Event.Shop(
                    self.player,
                    self.config,
                    self.equipment,
                    self.game_flags,
                    self.world_values,
                    self.ability,
                    self.resistances,
                    self.consolas,
                    self.save_manager,
                    self.win,
                    self.table_menu,
                    self.item_meneger
            )
            self.structure = None

            map_layers = {
                1: (d.ld.settlementMapGUI_1, d.ld.settlement1),
                #2: (d.ld.layerMapGUI_2, d.ld.layer2),
                #3: (d.ld.layerMapGUI_3, d.ld.layer3),
                #4: (d.ld.layerMapGUI_4, d.ld.layer4),
                #5: (d.ld.layerMapGUI_5, d.ld.layer5),
                #6: (d.ld.layerMapGUI_6, d.ld.layer6),
                #7: (d.ld.layerMapGUI_7, d.ld.layer7),
                #8: (d.ld.layerMapGUI_8, d.ld.layer8),
                #9: (d.ld.layerMapGUI_9, d.ld.layer9)
            }

            map, layer_info = map_layers.get(layer, (d.ld.layerMapGUI_cheatcr, d.ld.layerCheatcr))

            self.AlchemistItems = self.item_meneger.alchemical_items
            self.BlacksmithItems = self.item_meneger.blacksmith_items

            player.x = layer_info.XSpawn
            player.y = layer_info.YSpawn - 1

            while self.game_flags.trips: 

                if self.game_flags.game_over:
                    self.game_flags.trips = False
                    self.game_flags.play = False
                    break
                
                self.consolas.display_map(map, player, y=5)

                self.consolas.create_table("(UP|LEFT|DOWN|RIGHT|)-movement", "Q-quit", "I-inventory", "M-monstronomicon", alignmentTable="l", use_clear=False, y=1, x=5, table_width=32)
                self.consolas.create_table(
                    "ƒ-staircase",
                    "ʊ-blacksmith",
                    "å-alchemist",
                    "ĉ-rune magician",
                    "ʣ-adventurers guild",
                    "Æ-church",
                    "ɤ-empty building",
                    "ʚ-House",
                    "ɓ-field",
                    alignmentTable="l",
                    use_clear=False,
                    y=8,
                    x=5,
                    table_width=32
                )
                if self.structure in {0, 1, 2, 3, 4, 5}:
                    self.consolas.create_table("E-enter the building", alignmentTable="r", use_clear=False, y=1, table_width=32)

                move = self.win.getch()

                logging.info(f"INFO: Key pressed: {move}", exc_info=False)

                if move == 113:
                    self.player.Px = Sx
                    self.player.Py = Sy
                    self.save_manager.save_file()
                    self.game_flags.trips = False
                    break
                
                elif move == 101 and self.structure in {0, 1, 2, 3}:
                    if self.structure == 0:
                        player.x = Sx
                        player.y = Sy
                        break
                    elif self.structure == 1:
                        self.phrases = random.choice(dp.alchemist_phrases)
                        near_store = self.shop.visit_shop("alchemist", self.phrases, self.AlchemistItems)
                    elif self.structure == 2:
                        self.phrases = random.choice(dp.blacksmith_phrases)
                        near_store = self.shop.visit_shop("blacksmith", self.phrases, self.BlacksmithItems)
                    elif self.structure == 3:
                        pass
                    elif self.structure == 4:
                        pass
                    elif self.structure == 5:
                        pass

                elif move in {d.curses.KEY_UP, d.curses.KEY_DOWN, d.curses.KEY_LEFT, d.curses.KEY_RIGHT}:
                    dx, dy = {d.curses.KEY_UP: (0, -1), d.curses.KEY_DOWN: (0, 1), d.curses.KEY_LEFT: (-1, 0), d.curses.KEY_RIGHT: (1, 0)}[move]
                    new_x, new_y = player.x + dx, player.y + dy

                    if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map):
                        if map[new_y][new_x] != '*':
                            player.x, player.y = new_x, new_y
                            if new_x in layer_info.XDungen and new_y in layer_info.YDungen:
                                if new_x == layer_info.XSpawn and new_y == layer_info.YSpawn:
                                    self.structure = 0
                                elif new_x == layer_info.XAlchemist and new_y == layer_info.YAlchemist:
                                    self.structure = 1
                                elif new_x == layer_info.XBlacksmith and new_y == layer_info.YBlacksmith:
                                    self.structure = 2
                                elif new_x == layer_info.XRuneMage and new_y == layer_info.YRuneMage:
                                    self.structure = 3
                                elif new_x == layer_info.XChurch and new_y == layer_info.YChurch:
                                    self.structure = 4
                                elif new_x == layer_info.XAdventurersGuild and new_y == layer_info.YAdventurersGuild:
                                    self.structure = 5
                            else:
                                self.structure = None
                        else:
                            self.consolas.create_table( "You cannot go there", style="erorre")
                    else:
                        self.consolas.create_table("Beyond the bounds of the gaming world", style="erorre", table_width=22)

                elif move == 105:
                    self.openInventory()

                elif move == 109:
                    if self.player.playerMonstronomicon:
                        pass
                    else:
                        # Доделать
                        self.consolas.create_table("")

    class MonsterAtak(BaseEvent):
        def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells):
            super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells)
            self.tui = Event.TUI(game_flags, consolas, win, save_manager, table_menu, player, item_meneger, world_values, config, equipment, ability, resistances, spells)

        def monster_encounter(self):
            self.hit = 1
            self.game_flags.battle = True
            self.monster = Monster(self.player)

            megic_index = 1
            name_spells = ["exit"]
            classes_spells = {}

            for spells_id in self.player.spells:  # предположим, что player.spells содержит список ID заклинаний
                if spells_id in self.spells.all_spells:
                    class_spells = self.spells.all_spells[spells_id]
                    classes_spells[megic_index] = class_spells
                    name_spells.append(class_spells.name)
                    megic_index += 1

            self.consolas.create_table( f"you noticed a {self.monster.name} on your way", alignment={0: "center"}, table_width=40)
            self.win.getch()
            d.da.stop_background_music()
            d.da.play_battle_music()

            self.monstr_win = d.curses.newwin(18, 13, 10, 10)

            while self.game_flags.battle:
                self.hit = 1

                self.consolas.create_table(
                    f"{self.monster.name}",
                    f"HP : {self.monster.hp} / {self.monster.max_hp}",
                    f"DAMAGE : {self.monster.damage}",
                    f"Lv : {self.monster.lv}",
                    separator_positions=[0],
                    alignment={0: "center"},
                    table_width=25,
                    y=1,
                    x=1,
                )
                self.consolas.create_table(
                    f"name : {self.player.name}",
                    f"class : {self.player.heroClass}",
                    f"HP : {self.player.Hp} / {self.player.maxHp}",
                    f"Dm : {self.player.Dm}",
                    f"gold : {self.player.gold}",
                    f"XP : {self.player.Xp} / {self.player.XpToLv}",
                    f"Lv : {self.player.Lv}",
                    f"Mana : {self.player.mana} / {self.player.maxMana}",
                    f"IS : {self.player.improvementStar}",
                    f"layer : {self.player.layer} / 9",
                    separator_positions=[0],
                    alignment={0: "center"},
                    alignmentTable="r",
                    use_clear= False,
                    y=1,
                )
                self.consolas.play_animation(frames=self.monster.frame0, delay=0.03, y=5, x=1, clear=False, Xdo="-")
                action = self.table_menu.menu(title="battle", options=["attack", "inventory", "magic", "run"], tips=False, clear=False)

                if action == "0":
                    self.attack_monster(self.monster)
                elif action == "1":
                    self.tui.openInventory()

                elif action == "2":
                    use_magic = self.table_menu.menu(title="magic", options=name_spells, tips=False)

                    if use_magic.isdigit() and int(use_magic) in classes_spells:
                        chosen_spell = classes_spells[int(use_magic)]
                        
                        while (True):
                            choice = self.table_menu.menu("magic", ["INFO","USE","BACK"], tips=False)

                            if choice == "0":
                                self.consolas.create_table(chosen_spell.info , alignment={0 : "center"}, table_width=22)
                                self.win.getch()

                            if choice == "1":
                                self.monster.hp, self.hit = self.spells.use_spell(chosen_spell.ID, self.monster.hp, self.monster.max_hp)

                                break
                            
                            if choice == "2":
                                break
                    elif use_magic == "0":
                        pass

                elif action == "3":
                    if self.run_from_monster(self.monster):
                        break
                
                if self.player.mana < self.player.maxMana:
                    if self.ability.ManaRecovery:
                        self.player.mana += 5
                    else:
                        self.player.mana += 2
                    
                    if self.player.mana > self.player.maxMana:
                        self.player.mana = self.player.maxMana

                if self.monster.hp <= 0:
                    self.victory(self.monster)
                    break

                if self.monster.hp <= self.monster.max_hp * 0.5 and any(value in self.monster.item for value in [0, 1, 2]):
                    item = random.choice(self.monster.item)
                    if item == 0:
                        self.monster.item.remove(0)
                        self.monster.hp += 10
                        self.consolas.create_table("the monster drinks the potion, it restores 10 HP", alignment={0: "center"}, table_width=32)
                        self.win.getch()
                    elif item == 1:
                        self.monster.item.remove(1)
                        self.monster.hp += 20
                        self.consolas.create_table("the monster drinks the potion, it restores 20 HP", alignment={0: "center"}, table_width=32)
                        self.win.getch()
                    elif item == 2:
                        self.monster.item.remove(2)
                        self.monster.hp += 30
                        self.consolas.create_table("the monster drinks the potion, it restores 30 HP", alignment={0: "center"}, table_width=32)
                        self.win.getch()
                    if self.monster.hp > self.monster.max_hp:
                        self.monster.hp = self.monster.max_hp
                    self.hit = 0

                if self.monster.hp <= self.monster.max_hp * 0.2:
                    if d.r.randint(1, 20) + self.monster.speed - self.monster.aggression + self.monster.luck > d.r.randint(1, 20) + self.player.speed + self.player.luck:
                        self.consolas.create_table("The monster ran away", "Gold : 0", "XP : 0", separator_positions=[0], alignment={0: "center"}, table_width=25)
                        self.game_flags.battle = False
                        self.win.getch()
                        break
                
                if self.hit == 1 or self.hit == -1:
                    self.monster_attack(self.monster)

            d.da.stop_battle_music()
            d.da.play_background_music()

        def attack_monster(self, monster):
            self.hit = 1
            damage_multiplier = 2 if self.player.heroClass == "THIEF" and self.equipment.weaponID != None and self.equipment.weapon2ID != None else 1

            if self.player.heroClass == "SWORDSMAN":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.p_resist)

            elif self.player.heroClass == "THIEF":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.p_resist)

            elif self.player.heroClass == "MAGICIAN":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.m_resist)

            elif self.player.heroClass == "NULL":
                monster.hp -= 5 + self.player.Dm * damage_multiplier

            monster.hp = max(0, monster.hp)
            self.consolas.create_table(f"You hit the {monster.name}, it has {monster.hp} HP", alignment={0: "center"}, table_width=45)
            self.win.getch()

        def run_from_monster(self, monster):
            if random.random() > monster.aggression or self.player.speed > monster.speed:
                self.consolas.create_table("You run away", "Gold : 0", "XP : 0", separator_positions=[0], alignment={0: "center"}, table_width=25)
                self.game_flags.battle = False
                self.win.getch()
                return True
            else:
                self.consolas.create_table( "the monster caught up with you", alignment={0: "center"}, table_width=25,)
                self.win.getch()
                return False

        def victory(self, monster):
            if self.ability.EarningCoinsAndXP:
                monster.xp *= 2
                monster.coin *= 2

            self.player.Xp += monster.xp
            self.player.gold += monster.coin
            self.consolas.create_table(
                "VICTORY",
                f"Gold : {monster.coin}",
                f"XP : {self.player.Xp}/{self.player.XpToLv}",
                separator_positions=[0],
                alignment={0: "center"},
                table_width=25
            )

            while self.player.Xp >= self.player.XpToLv:
                self.level_up()
            self.win.getch()
            self.game_flags.battle = False

        def level_up(self):
            while self.player.Xp >= self.player.XpToLv:
                self.player.Lv += 1
                self.player.Xp -= self.player.XpToLv
                self.player.XpToLv = math.ceil(self.player.XpToLv * 1.8)
                self.player.maxHp = math.ceil(self.player.maxHp * 1.1)
                self.player.Hp = self.player.maxHp
                self.player.improvementStar += 1
                self.player.Dm = math.ceil(self.player.Dm * 1.1)

                self.consolas.create_table(
                    "NEW LEVEL",
                    f"HP : {self.player.maxHp}",
                    f"XP : {self.player.Xp}/{self.player.XpToLv}",
                    f"Damage : {self.player.Dm}",
                    f"Improvement star : {self.player.improvementStar}",
                    use_clear=False,
                    separator_positions=[0],
                    alignment={0: "center"},
                    table_width=25,
                )

        def monster_attack(self, monster):
            if monster.p_damage:
                self.player.Hp -= math.ceil(((monster.damage * (1 - self.resistances.PhysicalResistInt)) * (1 - self.resistances.MagicPhysicalResistInt)) * (1 - (self.resistances.helmetResistInt + self.resistances.chestplateResistInt + self.resistances.shieldResistInt)))

            elif monster.m_damage:
                self.player.Hp -= math.ceil(((monster.damage * (1 - self.resistances.MagicResistInt)) * (1 - self.resistances.MagicPhysicalResistInt)) * (1 - (self.resistances.helmetResistInt + self.resistances.chestplateResistInt + self.resistances.shieldResistInt)))

            if self.player.Hp <= 0:
                self.game_flags.game_over = True
                self.game_flags.battle = False
            
            self.consolas.create_table(f"{monster.name} hits you, you have {self.player.Hp} HP left", alignment={0: "center"}, table_width=45)
            self.win.getch()
                
                

    class Shop(BaseEvent):
        def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells):
            super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, win, table_menu, item_meneger, spells)

        def visit_shop(self, shop_type, phrases, items):
            self.options = ["exit"]
            self.additional_info = [""]
            random_items = random.sample(items, 3)
            item_names = [item.name for item in random_items]
            item_info = [item.info for item in random_items]
            gold_prices = [random.randint(item.minGold, item.maxGold) for item in random_items]

            self.options.extend([f"{item_names[i]}" for i in range(3)])
            self.additional_info.extend([f"{gold_prices[i]} gold \n {item_info[i]}" for i in range(3)])

            self.game_flags.shop = True

            while self.game_flags.shop:
                self.consolas.create_table(
                        self.player.name,
                        f"class = {self.player.heroClass}",
                        f"gold = {self.player.gold}",
                        f"dm = {self.player.Dm}",
                        f"hp = {self.player.Hp}/{self.player.maxHp}",
                        f"mana = {self.player.mana}/{self.player.maxMana}",
                        f"lv = {self.player.Lv}",
                        f"xp = {self.player.Xp}/{self.player.XpToLv}",
                        f"layer = {self.player.layer}",
                        separator_positions=[0],
                        alignment={0: "center"},
                        alignmentTable="r",
                        y=1,
                )

                self.consolas.create_table(
                    f"helmet : {self.player.helmet}",
                    f"chestplate : {self.player.chestplate}",
                    f"right hand : {self.player.weapon}",
                    f"left hand : {self.player.weapon2}",
                    use_clear=False, 
                    alignmentTable="r",
                    y=14,
                )

                action = self.table_menu.menu(
                    title=shop_type, 
                    options=self.options,
                    additional_info=self.additional_info,
                    clear=False,
                    y=20,
                    info_width=45
                )

                if action == "0":
                    exit_phrases = dp.blacksmith_purchase_exit if shop_type == "blacksmith" else dp.alchemist_purchase_exit
                    self.consolas.create_table(
                        shop_type,
                        random.choice(exit_phrases),
                        separator_positions=[0],
                        alignment={0: "center"},
                        table_width=35,
                    )
                    self.win.getch()
                    return False
                elif action.isdigit() and 0 < int(action) <= len(random_items):
                    self.buy_item(shop_type, item_names, gold_prices, int(action) - 1, random_items)

            return True

        def buy_item(self, shop_type, item_names, gold_prices, item_index, random_items):
            if self.options[item_index+1] == "--------":
                no_product_phrases = dp.blacksmith_phrases_no_product if shop_type == "blacksmith" else dp.alchemist_phrases_no_product
                self.consolas.create_table(shop_type, random.choice(no_product_phrases), separator_positions=[0], alignment={0: "center"}, table_width=35,)
                self.win.getch()
            else:
                if self.player.gold >= gold_prices[item_index]:

                    self.player.gold -= gold_prices[item_index]
                    self.player.item.append(random_items[item_index].ID)
                    thank_phrases = dp.blacksmith_purchase_phrases if shop_type == "blacksmith" else dp.alchemist_purchase_phrases
                    self.consolas.create_table(shop_type, random.choice(thank_phrases), separator_positions=[0], alignment={0: "center"}, table_width=35)
                    self.win.getch()

                    self.options[item_index+1] = "--------"
                    self.additional_info[item_index+1] = "purchased"
                else:
                    no_gold_phrases = dp.blacksmith_purchase_no_gold if shop_type == "blacksmith" else dp.alchemist_purchase_no_gold
                    self.consolas.create_table(shop_type, random.choice(no_gold_phrases), separator_positions=[0], alignment={0: "center"}, table_width=35)
                    self.win.getch()

        def shop(self):
            self.shop_type = random.choice(self.world_values.shop_types)
            self.near_store = True

            while self.near_store:
                self.consolas.create_table(f"This is a {self.shop_type} shop", alignment={0: "center"}, table_width=28)
                action = self.table_menu.menu(
                    title="shop", 
                    options=["move on", "go inside"],
                    tips=False,
                    clear=False,
                    y=25
                )

                if action == "0":
                    self.near_store = False
                    break
                elif action == "1":
                    d.da.stop_background_music()
                    d.da.play_shop_music()

                    if self.shop_type == "blacksmith":
                        self.phrases = random.choice(dp.blacksmith_phrases)
                        self.items = self.item_meneger.blacksmith_items
                    elif self.shop_type == "alchemist":
                        self.phrases = random.choice(dp.alchemist_phrases)
                        self.items = self.item_meneger.alchemical_items

                    self.near_store = self.visit_shop(self.shop_type, self.phrases, self.items)
                    d.da.stop_shop_music()
                    d.da.play_background_music()
                    break


if __name__ == "__main__":
    import DATA.data as d
    player = d.Player()
    config = d.Config()
    equipment = d.Equipment()
    game_flags = d.GameFlags()
    world_values = d.WorldValues()
    ability = d.Ability()
    resistances = d.Resistances()
    consolas = d.Consolas(config, player)
    save_manager = d.SaveManager(player, resistances, equipment, ability)

    player.gold = 999

    a = Event(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager)
    a.start_game()
