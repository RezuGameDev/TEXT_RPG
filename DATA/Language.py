import i18n

# Создаем словарь с переводами
translations = {
    'en': {
        'exit_menu': "[0] Exit to menu",
        'graphics': "Graphics: Fantomm",
        'music': "Music: Fantomm",
        'code': "Code: Fantomm",
        'plot': "Plot: Факсянь ---ihateniggers",
        'new_game': "[1] New game",
        'load_game': "[2] Load game",
        'authors': "[3] Authors",
        'exit_game': "[0] Exit game",
        'enter_name': "Enter your name",
        'name_too_long': "Name is too long, maximum length is 7 characters",
        'class': "class",
        'magician': "Magician",
        'magician_button': "[1] Magician | [q] info",
        'magician_resistance': "Magic resistance",
        'magician_mana': "Mana regeneration ++",
        'magician_hp': "HP: 160",
        'magician_damage': "Damage: 15",
        'thief': "Thief",
        'thief_button': "[2] Thief | [w] info",
        'thief_poison_resistance': "Poison resistance",
        'thief_toxin_resistance': "Toxin resistance",
        'thief_rewards': "More chances of receiving coins and experience",
        'thief_hp': "HP: 140",
        'thief_damage': "Damage: 10 + DP",
        'swordsman': "Swordsman",
        'swordsman_button': "[3] Swordsman | [e] info",
        'swordsman_physical_resistance': "Physical attack resistance",
        'swordsman_hp': "HP: 190",
        'swordsman_damage': "Damage: 30",
        'welcome': "Welcome, ",
        'start_game': "[1] to start",
        'player_name': "name :",
        'player_gold': "gold",
    },
    'ru': {
        'exit_menu': "[0] Выйти в меню",
        'graphics': "Графика: Fantomm",
        'music': "Музыка: Fantomm",
        'code': "Код: Fantomm",
        'plot': "Сюжет: Факсянь",
        'new_game': "[1] Новая игра",
        'load_game': "[2] Загрузить игру",
        'authors': "[3] Авторы",
        'exit_game': "[0] Выход из игры",
        'enter_name': "Введите ваше имя",
        'name_too_long': "Имя слишком длинное, максимальная длина 7 символов",
        'class': "Класс",
        'magician': "Маг",
        'magician_button': "[1] Маг | [q] инфо",
        'magician_resistance': "Сопротивление магии",
        'magician_mana': "Восстановление маны ++",
        'magician_hp': "HP: 160",
        'magician_damage': "Урон: 15",
        'thief': "Вор",
        'thief_button': "[2] Вор | [w] инфо",
        'thief_poison_resistance': "Сопротивление яду",
        'thief_toxin_resistance': "Сопротивление токсинам",
        'thief_rewards': "Больше шансов на получение монет и опыта",
        'thief_hp': "HP: 140",
        'thief_damage': "Урон: 10 + DP",
        'swordsman': "Мечник",
        'swordsman_button': "[3] Мечник | [e] инфо",
        'swordsman_physical_resistance': "Сопротивление физическим атакам",
        'swordsman_hp': "HP: 190",
        'swordsman_damage': "Урон: 30",
        'welcome': "Добро пожаловать, ",
        'start_game': "[1] для старта",
        'player_name': "имя :",
        'player_gold': "золото",
    }
}

# Добавляем переводы в библиотеку Language
for lang, translations_dict in translations.items():
    for key, value in translations_dict.items():
        i18n.add_translation(key, value, locale=lang)

if __name__ == "__main__":
    i18n.set('locale', 'en')
    print(i18n.t('welcome'))
    input()
