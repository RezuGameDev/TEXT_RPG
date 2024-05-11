import DATA.data as d
from EVENT.event import randomEvent

def start_game(leyer, player):
    if leyer == 1:
        map = d.ld.layerMapGUI_1
        Leyer = d.ld.layer1

    elif leyer == 2:
        map = d.ld.layerMapGUI_2
        Leyer = d.ld.layer2

    elif leyer == 3:
        map = d.ld.layerMapGUI_3
        Leyer = d.ld.layer3

    elif leyer == 4:
        map = d.ld.layerMapGUI_4
        Leyer = d.ld.layer4

    elif leyer == 5:
        map = d.ld.layerMapGUI_5
        Leyer = d.ld.layer5

    elif leyer == 6:
        map = d.ld.layerMapGUI_6
        Leyer = d.ld.layer6

    elif leyer == 7:
        map = d.ld.layerMapGUI_7
        Leyer = d.ld.layer7

    elif leyer == 8:
        map = d.ld.layerMapGUI_8
        Leyer = d.ld.layer8

    elif leyer == 9:
        map = d.ld.layerMapGUI_9
        Leyer = d.ld.layer9

    else:
        map = d.ld.layerMapGUI_cheatcr
        Leyer = d.ld.layer1

    while d.trips:
        if d.game_over:
            d.trips = False
            break

        d.display_map(map, player)

        d.create_table("info", False, [0], None, 22, "where do you want to go? (W|A|S|D|)", "Q-qute", "I-inventory", "M-monstronomicon")
        move = input("> ")

        if move.lower() == 'w' and map[player.y - 1][player.x] != '*':
            if player.y < 0:
                d.create_table("erorre", True, None, None, 22, "beyond the bounds of the gaming world")
                player.y = Leyer.YSpawn
                player.x = Leyer.XSpawn
            else:
                player.y -= 1
                Leyer.monsterMax = randomEvent(Leyer.monsterMax)

        elif move.lower() == 's' and map[player.y + 1][player.x] != '*':
            if player.y > 22:
                d.create_table("erorre", True, None, None, 22, "beyond the bounds of the gaming world")
                player.y = Leyer.YSpawn
                player.x = Leyer.XSpawn
            else:
                player.y += 1
                Leyer.monsterMax = randomEvent(Leyer.monsterMax)

        elif move.lower() == 'a' and map[player.y][player.x - 1] != '*':
            if player.x < 0:
                d.create_table("erorre", True, None, None, 22, "beyond the bounds of the gaming world")
                player.y = Leyer.YSpawn
                player.x = Leyer.XSpawn
            else:
                player.x -= 1
                Leyer.monsterMax = randomEvent(Leyer.monsterMax)

        elif move.lower() == 'd' and map[player.y][player.x + 1] != '*':
            if player.x > 48:
                d.create_table("erorre", True, None, None, 22, "beyond the bounds of the gaming world")
                player.y = Leyer.YSpawn
                player.x = Leyer.XSpawn
            else:
                player.x += 1
                Leyer.monsterMax = randomEvent(Leyer.monsterMax)

        elif move.lower() == 'q':
            d.Px = player.x
            d.Py = player.y
            d.saveFile()
            d.trips = False

        elif move.lower() == 'm':
            if d.playerMonstronomicon == True:
                pass
            else:
                #доделать
                d.create_table("info", True, None, None, 22, "")


d.trips = True
if d.layer == 1:
    d.loadFile
    if d.Px == 0 and d.Py == 0:
        d.Px = d.ld.layer1.XSpawn
        d.Py = d.ld.layer1.YSpa
    player = d.Player(d.Px, d.Py)
    start_game(1, player)
                     
if d.layer == 2:
    d.loadFile
    if d.Px == 0 and d.Py == 0:
        d.Px = d.ld.layer2.XSpawn
        d.Py = d.ld.layer2.YSpa
    player = d.Player(d.Px, d.Py)
    start_game(2, player)
                     
elif d.layer == 3:
    d.loadFile
    if d.Px == 0 and d.Py == 0:
        d.Px = d.ld.layer3.XSpawn
        d.Py = d.ld.layer3.YSpa
    player = d.Player(d.Px, d.Py)
    start_game(3, player)