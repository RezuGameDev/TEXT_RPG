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

class Monster:
    def __init__(self):
        random_monster = random.choice(list(md.forest.keys()))
        self.name = md.forest[random_monster]["name"]
        self.hp = md.forest[random_monster]["Hp"]
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

class BaseEvent:
    def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d):
        self.player = player
        self.config = config
        self.equipment = equipment
        self.game_flags = game_flags
        self.world_values = world_values
        self.ability = ability
        self.resistances = resistances
        self.consolas = consolas
        self.save_manager = save_manager
        self.d = d

class Event(BaseEvent):
    def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d):
        super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d)

    class MonsterAtak(BaseEvent):
        def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d):
            super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d)

        def monster_encounter(self):
            self.game_flags.battle = True
            self.monster = Monster()

            self.consolas.create_table("info", True, None, {0: "center"}, 40, f"On your way you met a {self.monster.name}")
            input("> ")
            self.d.da.stop_background_music()
            self.d.da.play_battle_music()

            while self.game_flags.battle:
                self.consolas.create_table(
                    "info",
                    True,
                    [0],
                    {0: "center"},
                    25,
                    f"{self.monster.name}",
                    f"HP : {self.monster.hp}",
                    f"DAMAGE : {self.monster.damage}"
                )
                self.consolas.create_table(
                    "info",
                    False,
                    [0, 2],
                    {0: "center"},
                    25,
                    f"{self.player.name}",
                    f"HP : {self.player.Hp}",
                    f"DAMAGE : {self.player.Dm}",
                    f"1, attack {self.monster.name}",
                    "2, run"
                )
                action = input("> ")

                if action == "1":
                    self.attack_monster(self.monster)
                elif action == "2":
                    self.run_from_monster(self.monster)

                if self.monster.hp <= 0:
                    self.victory(self.monster)
                    break

                self.monster_attack(self.monster)

            self.d.da.stop_battle_music()
            self.d.da.play_background_music()

        def attack_monster(self, monster):
            damage_multiplier = 2 if self.player.heroClass == "THIEF" else 1

            if self.player.heroClass == "SWORDSMAN":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.p_resist)
            elif self.player.heroClass == "THIEF":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.p_resist)
            elif self.player.heroClass == "MAGICIAN":
                monster.hp -= math.ceil((self.player.Dm * damage_multiplier) * monster.m_resist)
            elif self.player.heroClass == "NULL":
                monster.hp -= 5 + self.player.Dm * damage_multiplier

            monster.hp = max(0, monster.hp)
            self.consolas.create_table("info", True, None, {0: "center"}, 45, f"You hit the {monster.name}, it has {monster.hp} HP")
            input("> ")

        def run_from_monster(self, monster):
            if random.random() > monster.aggression or self.player.speed > monster.speed:
                self.consolas.create_table("info", True, [0], {0: "center"}, 25, "You run away", "Gold : 0", "XP : 0")
                self.game_flags.battle = False
                input("")
            else:
                self.consolas.create_table("info", True, None, {0: "center"}, 25, "You couldn't escape")
                input("> ")

        def victory(self, monster):
            if self.ability.EarningCoinsAndXP:
                monster.xp *= 2
                monster.coin *= 2
            self.player.Xp += monster.xp
            self.player.gold += monster.coin
            self.consolas.create_table("info", True, [0], {0: "center"}, 25, "VICTORY", f"Gold : {monster.coin}", f"XP : {self.player.Xp}/{self.player.XpToLv}")
            if self.player.Xp >= self.player.XpToLv:
                self.level_up()
            input("> ")
            self.game_flags.battle = False

        def level_up(self):
            while self.player.Xp >= self.player.XpToLv:
                self.player.Lv += 1
                self.player.Xp -= self.player.XpToLv
                self.player.XpToLv = math.ceil(self.player.XpToLv * 1.5)
                self.player.maxHp = math.ceil(self.player.maxHp * 1.5)
                self.player.Hp = self.player.maxHp
                self.player.improvementStar += 1
                self.player.Dm += 5
                self.consolas.create_table(
                    "info",
                    False,
                    [0],
                    {0: "center"},
                    25,
                    "NEW LEVEL",
                    f"HP : {self.player.maxHp}",
                    f"XP : {self.player.Xp}/{self.player.XpToLv}",
                    f"Damage : {self.player.Dm}",
                    f"Improvement star : {self.player.improvementStar}"
                )

        def monster_attack(self, monster):
            if monster.p_damage:
                self.player.Hp -= math.ceil(((monster.damage * (1 - self.resistances.PhysicalResistInt)) * (1 - self.resistances.MagicPhysicalResistInt)) * (1 - (self.resistances.helmetResistInt + self.resistances.chestplateResistInt + self.resistances.shieldResistInt)))
            elif monster.m_damage:
                self.player.Hp -= math.ceil(((monster.damage * (1 - self.resistances.MagicResistInt)) * (1 - self.resistances.MagicPhysicalResistInt)) * (1 - (self.resistances.helmetResistInt + self.resistances.chestplateResistInt + self.resistances.shieldResistInt)))
            if self.player.Hp <= 0:
                self.game_flags.game_over = True

    class Shop(BaseEvent):
        def __init__(self, player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d):
            super().__init__(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d)

        def visit_shop(self, shop_type, phrases, items):
            random_items = random.sample(items, 3)
            item_names = [item['name'] for item in random_items]
            gold_prices = [random.randint(item["minGold"], item["maxGold"]) for item in random_items]

            self.consolas.create_table("info", True, [0], {0: "center"}, 35, shop_type, phrases)
            self.game_flags.shop = True
            input("> ")

            while self.game_flags.shop:
                self.consolas.create_table(
                    "info",
                    True,
                    [0, 3],
                    {0: "center"},
                    35,
                    shop_type,
                    *[f"{i + 1}, {item_names[i]} | {gold_prices[i]} gold" for i in range(3)],
                    f"GOLD : {self.player.gold}",
                    "[0] exit"
                )
                action = input("> ")

                if action == "0":
                    exit_phrases = dp.blacksmith_purchase_exit if shop_type == "blacksmith" else dp.alchemist_purchase_exit
                    self.consolas.create_table(
                        "info",
                        True,
                        [0],
                        {0: "center"},
                        35,
                        shop_type,
                        random.choice(exit_phrases)
                    )
                    input("> ")
                    return False
                elif action.isdigit() and 0 < int(action) <= len(random_items):
                    self.buy_item(shop_type, item_names, gold_prices, int(action) - 1, random_items)
                else:
                    self.consolas.create_table(
                        "info",
                        True,
                        [0],
                        {0: "center"},
                        35,
                        shop_type,
                        "Invalid option. Please try again."
                    )
                    input("> ")

            return True

        def buy_item(self, shop_type, item_names, gold_prices, item_index, random_items):
            if item_names[item_index] == "--------":
                no_product_phrases = dp.blacksmith_phrases_no_product if shop_type == "blacksmith" else dp.alchemist_phrases_no_product
                self.consolas.create_table("info", True, [0], {0: "center"}, 35, shop_type, random.choice(no_product_phrases))
                input("> ")
            else:
                if self.player.gold >= gold_prices[item_index]:
                    self.player.gold -= gold_prices[item_index]
                    self.player.item.append(random_items[item_index]['ID'])
                    thank_phrases = dp.blacksmith_purchase_phrases if shop_type == "blacksmith" else dp.alchemist_purchase_phrases
                    self.consolas.create_table("info", True, [0, 3], {0: "center"}, 35, shop_type, random.choice(thank_phrases))
                    input("> ")
                    item_names[item_index] = "--------"
                else:
                    no_gold_phrases = dp.blacksmith_purchase_no_gold if shop_type == "blacksmith" else dp.alchemist_purchase_no_gold
                    self.consolas.create_table("info", True, [0], {0: "center"}, 35, shop_type, random.choice(no_gold_phrases))
                    input("> ")

        def shop(self):
            self.shop_type = random.choice(self.world_values.shop_types)
            self.near_store = True

            while self.near_store:
                self.consolas.create_table("info", True, [0], {0: "center"}, 40, f"This is a {self.shop_type} shop", "0, move on", "1, go inside")
                action = input("> ")

                if action == "0":
                    self.near_store = False
                    break
                elif action == "1":
                    self.d.da.stop_background_music()
                    self.d.da.play_shop_music()

                    if self.shop_type == "blacksmith":
                        self.phrases = random.choice(dp.blacksmith_phrases)
                        self.items = itemd.blacksmith_items
                    elif self.shop_type == "alchemist":
                        self.phrases = random.choice(dp.alchemist_phrases)
                        self.items = itemd.alchemical_items

                    self.near_store = self.visit_shop(self.shop_type, self.phrases, self.items)
                    self.d.da.stop_shop_music()
                    self.d.da.play_background_music()
                    break


    def randomEvent(self, monstr_max):
        event = random.choices([1, 2], weights=self.world_values.chances, k=1)[0]

        if event == 1 and monstr_max > 0:
            monstar = self.MonsterAtak(
                self.player,
                self.config,
                self.equipment,
                self.game_flags,
                self.world_values,
                self.ability,
                self.resistances,
                self.consolas,
                self.save_manager,
                self.d
            )
            monstar.monster_encounter()

            self.world_values.chances[0] = max(0, self.world_values.chances[0] - 5)  # Уменьшаем шансы для события 1 на 10
            self.world_values.chances[1] = min(100, self.world_values.chances[1] + 10)  # Увеличиваем шансы для события 2 на 10
            monstr_max = monstr_max - 1
        else:
            shop = self.Shop(
                self.player,
                self.config,
                self.equipment,
                self.game_flags,
                self.world_values,
                self.ability,
                self.resistances,
                self.consolas,
                self.save_manager,
                self.d
            )
            shop.shop()
            # Изменяем шансы для следующего события
            self.world_values.chances[0] = min(100, self.world_values.chances[0] + 10)  # Увеличиваем шансы для события 1 на 10
            self.world_values.chances[1] = max(0, self.world_values.chances[1] - 10)  # Уменьшаем шансы для события 2 на 10
        return monstr_max

    def start_game(self, layer, player):
        map_layers = {
            1: (self.d.ld.layerMapGUI_1, self.d.ld.layer1),
            2: (self.d.ld.layerMapGUI_2, self.d.ld.layer2),
            3: (self.d.ld.layerMapGUI_3, self.d.ld.layer3),
            4: (self.d.ld.layerMapGUI_4, self.d.ld.layer4),
            5: (self.d.ld.layerMapGUI_5, self.d.ld.layer5),
            6: (self.d.ld.layerMapGUI_6, self.d.ld.layer6),
            7: (self.d.ld.layerMapGUI_7, self.d.ld.layer7),
            8: (self.d.ld.layerMapGUI_8, self.d.ld.layer8),
            9: (self.d.ld.layerMapGUI_9, self.d.ld.layer9)
        }

        map, layer_info = map_layers.get(layer, (self.d.ld.layerMapGUI_cheatcr, self.d.ld.layer1))

        while self.game_flags.trips:
            if self.game_flags.game_over:
                self.game_flags.trips = False
                break

            self.consolas.display_map(map, player)

            self.consolas.create_table("info", False, [0], None, 22, "Where do you want to go? (W|A|S|D|)", "Q-quit", "I-inventory", "M-monstronomicon")
            move = input("> ").lower()

            if move == 'q':
                self.player.Px = player.x
                self.player.Py = player.y
                self.save_manager.save_file()
                self.game_flags.trips = False
                break

            elif move in {'w', 's', 'a', 'd'}:
                dx, dy = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)}[move]
                new_x, new_y = player.x + dx, player.y + dy

                if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map):
                    if map[new_y][new_x] != '*':
                        player.x, player.y = new_x, new_y
                        layer_info.monsterMax = self.randomEvent(layer_info.monsterMax)
                    else:
                        self.consolas.create_table("erorre", True, None, None, 22, "You cannot go there")
                else:
                    self.consolas.create_table("erorre", True, None, None, 22, "Beyond the bounds of the gaming world")

            elif move == 'i':
                self.openInventory()

            elif move == 'm':
                if self.player.playerMonstronomicon:
                    pass
                else:
                    # Доделать
                    self.consolas.create_table("info", True, None, None, 22, "")


    def openInventory(self):
        self.consolas.clear()
        self.game_flags.inventory = True
        item_ids = self.player.item

        while self.game_flags.inventory:

            matching_classes_names = []
            matching_classes = {}

            item_index = 1

            # Перебираем все ID предметов
            for item_id in item_ids:
                for class_item in itemd.all_item:
                    if item_id == class_item["ID"]:
                        matching_classes[item_index] = class_item

                        matching_classes_names.append(f"{class_item['name']} | {item_index}")

                        item_index += 1
                        break

            self.consolas.create_table("info", True, [0], {0 : "center"}, 45, "inventory", *matching_classes_names )
            self.consolas.create_table(
                "info",
                False, 
                [0],
                None,
                45,
                f"name : {self.player.name}",
                f"class : {self.player.heroClass}",
                f"HP : {self.player.Hp} / {self.player.maxHp}",
                f"gold : {self.player.gold}",
                f"XP : {self.player.Xp} / {self.player.XpToLv}",
                f"Lv : {self.player.Lv}",
                f"Mana : {self.player.mana} / {self.player.maxMana}",
                f"IS : {self.player.improvementStar}",
                f"layer : {self.player.layer} / 9",
            )
            self.consolas.create_table(
                "info",
                False, 
                None,
                None,
                45,
                f"helmet : {self.player.helmet}",
                f"chestplate : {self.player.chestplate}",
                f"right hand : {self.player.weapon}",
                f"left hand : {self.player.weapon2}",
            )
            self.consolas.create_table("info", False, None, None, 15, "0, - exit")

            choice = input("> ")
            
            if choice.isdigit() and int(choice) in matching_classes:
                chosen_item = matching_classes[int(choice)]
                
                while (True):
                    self.consolas.create_table("info", True, None, {0 : "center"}, 35, "[1] INFO | [2] USE | [3] BACK" )
                    choice = input("> ")
                    if choice == "1":
                        self.consolas.create_table("info", True, None, {0 : "center"}, 22, chosen_item["info"] )
                        input()

                    if choice == "2":

                        if chosen_item["type"] == 1:
                            itemd.use_potions(chosen_item["ID"])
                        
                        elif chosen_item["type"] == 2:
                            self.resistances.helmetResistInt = chosen_item["Physical_Resist"]
                            self.player.helmet = chosen_item["name"]
                            self.equipment.helmetID =chosen_item["ID"]
                            self.player.item.remove(chosen_item["ID"])

                        elif chosen_item["type"] == 3:
                            self.resistances.chestplateResistInt = chosen_item["Physical_Resist"]
                            self.player.chestplate = chosen_item["name"]
                            self.equipment.chestplateID =chosen_item["ID"]
                            self.player.item.remove(chosen_item["ID"])

                        elif chosen_item["type"] == 4:
                            if self.player.heroClass == "SWORDSMAN":
                                self.player.Dm += chosen_item["damage"]
                                self.player.weapon = chosen_item["name"]
                                self.equipment.weaponID =chosen_item["ID"]
                                self.player.item.remove(chosen_item["ID"])
                            else:
                                self.consolas.create_table("info", True, None, {0 : "center"}, 35, "this weapon is not suitable for you" )

                        elif chosen_item["type"] == 5:
                            if  self.player.heroClass == "THIEF":
                                while True:
                                    self.consolas.create_table("info", True, None, {0 : "center", 1 : "center"}, 35, "Which hand should I take the dagger in?", "[1] left | [2] right")
                                    choice = input("> ")
                                    if choice == "1":
                                        self.player.Dm += chosen_item["damage"]
                                        self.player.weapon = chosen_item["name"]
                                        self.equipment.weaponID =chosen_item["ID"]
                                        self.player.item.remove(chosen_item["ID"])
                                    elif choice == "2":
                                        self.player.Dm += chosen_item["damage"]
                                        self.player.weapon2 = chosen_item["name"]
                                        self.equipment.weapon2ID =chosen_item["ID"]
                                        self.player.item.remove(chosen_item["ID"])
                            else:
                                self.consolas.create_table("info", True, None, {0 : "center"}, 35, "this weapon is not suitable for you" )

                        elif chosen_item["type"] == 6:
                            if self.player.heroClass == "MAGICIAN":
                                self.player.Dm += chosen_item["damage"]
                                self.player.weapon = chosen_item["name"]
                                self.equipment.weaponID = chosen_item["ID"]
                                self.playerd.maxMana += chosen_item["mana"]
                                self.playerd.item.remove(chosen_item["ID"])
                            else:
                                self.consolas.create_table("info", True, None, {0 : "center"}, 35, "this weapon is not suitable for you" )
                        
                        elif chosen_item["type"] == 7:
                            if self.player.heroClass == "SWORDSMAN":
                                self.resistances.shieldResistInt = chosen_item["Physical_Resist"]
                                self.player.weapon2 = chosen_item["name"]
                                self.equipment.weapon2ID =chosen_item["ID"]
                                self.player.item.remove(chosen_item["ID"])
                            else:
                                self.consolas.create_table("info", True, None, {0 : "center"}, 35, "this weapon is not suitable for you" )


                        input("> ")
                        break
                    
                    if choice == "3":
                        break
            elif choice == "0":
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

    a = Event(player, config, equipment, game_flags, world_values, ability, resistances, consolas, save_manager, d)
    a.start_game()
