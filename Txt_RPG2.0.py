import sys
import json
import random

class Objects:
    class Player:
        def __init__(self, name, race, c_class, class_m, lvl, exp, cap_exp, hp, mp, hp_max, mp_max, defense, str, mag_str, gold, inventory, location,  spell_book, estus, ashen, main_quest, boss_item):
            self.name = name
            self.race = race
            self.c_class = c_class
            self.class_m = class_m
            self.lvl = lvl
            self.exp = exp
            self.cap_exp = cap_exp
            self.hp = hp
            self.mp = mp
            self.hp_max = hp_max
            self.mp_max = mp_max
            self.defense = defense
            self.str = str
            self.mag_str = mag_str
            self.gold = gold
            self.inventory = inventory
            self.location = location
            self.spell_book = spell_book
            self.estus = estus
            self.ashen = ashen
            self.main_quest = main_quest
            self.boss_item = boss_item

        def data_save(self):
            return { 'name': self.name,
                    'race': self.race, 
                    'c_class': self.c_class,
                    'class_m': self.class_m,
                    'lvl': self.lvl,
                    'exp': self.exp,
                    'cap_exp': self.cap_exp,
                    'hp': self.hp,
                    'mp': self.mp,
                    'hp_max': self.hp_max,
                    'mp_max': self.mp_max,
                    'defense': self.defense,
                    'str': self.str,
                    'mag_str': self.mag_str,
                    'gold': self.gold,
                    'inventory': list(self.inventory),
                    'location': self.location,
                    'spell_book': self.spell_book,
                    'estus': self.estus,
                    'ashen': self.ashen,
                    'main_quest': self.main_quest,
                    'boss_item': self.boss_item
            }

        @classmethod
        def data_load(cls, data):
            return cls(
                name=data['name'],
                race=data['race'],
                c_class=data['c_class'],
                class_m=data['class_m'],
                lvl=data['lvl'],
                exp=data['exp'],
                cap_exp=data['cap_exp'],
                hp=data['hp'],
                mp=data['mp'],
                hp_max=data['hp_max'],
                mp_max=data['mp_max'],
                defense=data['defense'],
                str=data['str'],
                mag_str=data['mag_str'],
                gold=data['gold'],
                inventory=tuple(data.get('inventory', [])),
                location=tuple(data['location']),
                spell_book=data.get('spell_book', {}),
                estus=data['estus'],
                ashen=data['ashen'],
                main_quest=data['main_quest'],
                boss_item=data['boss_item'],
            )

        def elf(self, player):
            player.race = 'Elf'
            player.hp = 70
            player.mp = 150
            player.str = 3
            player.mag_str = 10
            player.defense = 0.6
            player.spell_book.update({"ball": 25})

        def human(self, player):
            player.race = 'Human'
            player.hp = 100
            player.mp = 100
            player.str = 10
            player.mag_str = 5
            player.defense = 1
            player.spell_book.update({"Fireball": 20})
        
        def dwarf(self, player):
            player.race = 'Dwarf'
            player.hp = 150
            player.mp = 30
            player.str = 12
            player.mag_str = 3
            player.defense = 1.5
            player.spell_book.update({"Fireball": 20})

        def warrior(self, player):
            player.c_class = 'Warrior'
            player.class_m = 3
            player.hp += 30
            player.hp_max = player.hp
            player.mp = 30
            player.mp_max = player.mp
            player.str = 12
            player.mag_str = 3
            player.defense = 1.5
            player.spell_book.update({"Fireball": 20})

        def wizard(self, player):
            player.class_m = 1
            player.c_class = 'Wizard'
            player.hp -= 10
            player.hp_max = player.hp
            player.mp += 30
            player.mp_max = player.mp
            player.str -= 2
            player.mag_str += 3
            player.spell_book.update({"Fireball": 20})

        def merchant(self, player):
            player.class_m = 2
            player.c_class = 'Merchant'
            player.hp_max = player.hp
            player.mp += 30
            player.mp_max = player.mp
            player.mag_str += 1 
            player.gold += 100
            player.spell_book.update({"Fireball": 20})

        def level_up(self):
            if self.exp >= self.cap_exp:
                self.lvl += 1
                self.exp -= self.cap_exp
                self.cap_exp = int(self.cap_exp * 1.1)
                self.hp_max += round(10*self.class_m)
                self.mp_max += round(5*(1/self.class_m))
                self.str += round(2*self.class_m)
                self.mag_str += round(4*(1/self.class_m))
                self.hp = self.hp_max
                self.mp = self.mp_max
                print(f"{self.name} leveled up to level {self.lvl}!")
        
        def get_input(self, prompt):
            choice = input(prompt).strip().lower()
            if choice in ('q', 'quit'):
                self.quit_game()
            return choice

        def quit_game(self):
            print('Quitting game. Goodbye!')
            sys.exit(0)

        def melee(self, enemy):
            dmg = round(self.str / enemy.defense)
            enemy.hp -= dmg
            print(f"You attack the {enemy.name} for {dmg} damage!")
        
        def magic(self, enemy):
            spells = list(self.spell_book.keys())
            if self.spell_book: 
                how_many_spells = len(self.spell_book)
                x = 1
                print("Spell book:")   
                for i in range(how_many_spells):
                    print(f"{x}. {spells[x-1]}")
                    x += 1

                spell_choice = self.get_input("Choose your spell: ")

                if str(spell_choice) in self.spell_book:
                    spell_mana = self.spell_book[spell_choice]

                elif spell_choice.isdigit():
                    index = int(spell_choice) - 1
                    if 0 <= index < how_many_spells:
                        spell_choice = spells[index]
                        spell_mana = self.spell_book[spell_choice]
                    else:
                        print("Invalid spell choice.")
                        return
                    
                else:
                    print("Invalid spell choice.")
                    return 
                
                if self.mp >= spell_mana:
                    self.mp -= spell_mana
                    dmg = 5 + round(self.mag_str*(spell_mana/10))
                    enemy.hp -= dmg
                    print(f"You cast {spell_choice} on the {enemy.name} for {dmg} damage!")

                else:
                    print(f"Not enough MP to cast {spell_choice}!")

            else:
                print("You don't have any spells to cast!")
            
        def item(self):
                if self.estus > 0 or self.ashen > 0:
                    print("Quick Inventory: \n")
                    print("1. Estus Flask\n" 
                        "2. Ashen Flask\n"
                        "3. Back \n")

                    item_choice = self.get_input("Choose your item: ")
                    if item_choice in ('1', 'estus', 'estusflask'):
                        if self.estus > 0:
                            self.hp += 20
                            if self.hp > self.hp_max:
                                self.hp = self.hp_max
                            self.estus -= 1
                            print(f"You used an estus flask and restored 20 HP! You have {self.estus} estus flasks left.")
                        else:
                            print("Sadly your estus flask have exhausted")

                    elif item_choice in ('2', 'ashen', 'ashenflask'):
                        if self.ashen > 0:
                            self.mp += 20
                            if self.mp > self.mp_max:
                                self.mp = self.mp_max
                            self.ashen -= 1
                            print(f"You used an ashen flask and restored 20 MP! You have {self.ashen} ashen flasks left.")
                        else:
                            print("Sadly your ashen flask have exhausted")
                    
                    elif item_choice in (3, 'back'):
                        return
                    else:
                        print("Invalid item choice.")
                else:
                    print("Your inventory is empty!")

        def escape(self, enemy, move, game_map):
            print("You attempt to run away...")
            escape_chance = random.randint(1, 100) + self.lvl - (enemy.hp/4)
            if escape_chance > 70:
                print("You successfully escaped!")
                self.move_back(move, game_map, restore_char='E')
                return True
                
            elif escape_chance > 50 and escape_chance <= 70:
                print("You barely escaped and was hurt in the process!")
                self.hp -= 10
                self.move_back(move, game_map, restore_char='E')
                return True

            else:
                print("You failed to escape and the battle continues!")
                return False


        def move(self, direction, game_map):
            x, y = self.location
            if direction == 'w':
                y -= 1
            elif direction == 'a':
                x -= 1
            elif direction == 's':
                y += 1
            elif direction == 'd':
                x += 1
            elif direction == 'menu' or 'b':
                pass
            else:
                print('Invalid direction')
                return self.location

            if x < 0 or x >= game_map.width or y < 0 or y >= game_map.height:
                print("You can't go there!")
                return self.location

            game_map.map[self.location[1]][self.location[0]] = '.'
            self.location = (x, y)
            game_map.map[y][x] = 'P'

            return self.location
        
        def move_back(self, direction, game_map, restore_char=''):
            x, y = self.location
            game_map.map[y][x] = restore_char
            if direction == 'w':
                y += 1
            elif direction == 'a':
                x += 1
            elif direction == 's':
                y -= 1
            elif direction == 'd':
                x -= 1
         
            self.location = (x, y)
            game_map.map[y][x] = 'P'

            return self.location  
                

    class Enemy:
        def __init__(self, name, hp, mp, hp_max, mp_max, defense, str, mag_str, spell_book, location, gold, exp):
            self.name = name
            self.hp = hp
            self.mp = mp
            self.hp_max = hp_max
            self.mp_max = mp_max
            self.defense = defense
            self.str = str
            self.mag_str = mag_str
            self.spell_book = spell_book
            self.location = location
            self.gold = gold
            self.exp = exp

            hp = hp_max
            mp = mp_max

        def data_save(self):
            return {
                'name': self.name,
                'hp': self.hp,
                'mp': self.mp,
                'hp_max': self.hp_max,
                'mp_max': self.mp_max,
                'defense': self.defense,
                'str': self.str,
                'mag_str': self.mag_str,
                'spell_book': self.spell_book,
                'location': self.location,
                'gold': self.gold,
                'exp': self.exp,
            }

        @classmethod
        def data_load(cls, data):
            return cls(
                name=data['name'],
                hp=data['hp'],
                mp=data['mp'],
                hp_max=data['hp_max'],
                mp_max=data['mp_max'],
                defense=data['defense'],
                str=data['str'],
                mag_str=data['mag_str'],
                spell_book=data.get('spell_book', {}),
                location=tuple(data['location']),
                gold=data['gold'],
                exp=data['exp']
                )

        def attack(self, player):
            dmg = round(self.str / player.defense)
            player.hp -= dmg
            print(f"{self.name} attacked you for {dmg} damage!")

        def heal(self, player, need_mana=False):
            if need_mana:
                self.mp += self.mp_max / 5
                need_mana = False
            elif self.hp <= self.hp_max / 2 or self.hp <= self.hp_max - 50:
                self.hp += self.hp_max / 10
            elif self.hp < self.mp_max / 2 or self.mp <= self.mp_max - 50:
                self.mp += self.mp_max / 5
            else:
                self.attack(player)
            
        def magic(self, player):
            spells = list(self.spell_book.keys())
            spell_choice = random.choice(spells)

            if self.spell_book: 
                spell_mana = self.spell_book[spell_choice]
                if self.mp >= spell_mana:
                    self.mp -= spell_mana
                    dmg = 5 + round(self.mag_str*(spell_mana/10))
                    player.hp -= dmg
                    print(f"{self.name} casted {spell_choice} on you for {dmg} damage!")

                else:
                    self.heal(player, need_mana = True)

            else:
                self.attack(player)

    class Boss:
        def __init__(self, name, hp, mp, mp_max, hp_max, defense, str, mag_str, gold, exp):
            self.name = name
            self.hp = hp
            self.mp = mp
            self.hp_max = hp_max
            self.mp_max = mp_max
            self.defense = defense
            self.str = str
            self.mag_str = mag_str
            self.gold = gold
            self.exp = exp

        def data_save(self):
            return { 'name': self.name,
                    'hp': self.hp,
                    'mp': self.mp,
                    'hp_max': self.hp_max,
                    'mp_max': self.mp_max,
                    'defense': self.defense,
                    'str': self.str,
                    'mag_str': self.mag_str,
                    'gold': self.gold,
                    'exp': self.exp,
            }
        
        @classmethod
        def data_load(cls, data):
            return cls(
                name=data['name'],
                hp=data['hp'],
                mp=data['mp'],
                hp_max=data['hp_max'],
                mp_max=data['mp_max'],
                defense=data['defense'],
                str=data['str'],
                mag_str=data['mag_str'],
                location=tuple(data['location']),
                gold=data['gold'],
                exp=data['exp'],
            )

    class Town:
        def __init__(self, name, hp, hp_max, defense, str, location, gold, exp, player, game_map):
            self.name = name
            self.hp = hp
            self.hp_max = hp_max
            self.defense = defense
            self.str = str
            self.location = location
            self.gold = gold
            self.exp = exp
            self.player = player
            self.game_map = game_map

            self.entry_direction = None
            self.town_menu_choice = {
                                    '1':self.inn,
                                    'inn':self.inn,
                                    '2':self.shop,
                                    'shop':self.shop,
                                    '3':self.town_leave,
                                    'leave':self.town_leave,
                                    '4':self.town_raid,
                                    'raid':self.town_raid,
                                    'attack':self.town_raid
                                    }

      
        def town_menu(self, entry_direction=None):
            if entry_direction is not None:
                self.entry_direction = entry_direction
            print("Welcome to the town! What would you like to do?")
            while True:
                print("1. Go to the inn")
                print("2. Go to the shop")
                print("3. Leave town")
                print("4. Raid the town")
                choice = self.player.get_input("Your choice: ")
                if choice in self.town_menu_choice:
                    if choice in ('3', 'leave'):
                        self.town_menu_choice[choice](self.entry_direction)
                    else:
                        self.town_menu_choice[choice]()
                    break
                else:
                    print("Invalid choice. Please try again.")

        def inn(self):
            inn_menu_choice = {
                            '1': self.rent_room,
                            'rent': self.rent_room,
                            'room': self.rent_room,
                            '2': self.talk_bartender,
                            'talk': self.talk_bartender,
                            'bartender': self.talk_bartender,
                            '3': self.town_menu,
                            'back': self.town_menu,
                            'exit': self.town_menu,
                            'town': self.town_menu
                            }
            
            print('''Welcome to the inn "Silver Hearth"! What would you like to do?''')
            while True:
                print("1. Rent a room for 20 coins")
                print("2. Talk with the bartender")
                print("3. Go back to town")
                choice = self.player.get_input("Your choice: ")
                if choice in inn_menu_choice:
                    inn_menu_choice[choice]()
                    break
                else:
                    print("Invalid choice. Please try again.")

        def rent_room(self):
            if self.player.gold >= 20:
                self.player.gold -= 20
                print("You rent a room for 20 coins and take a good night's sleep.")
                self.player.hp = self.player.hp_max
                self.player.mp = self.player.mp_max
                print("Your HP and MP have been fully restored!")
            else:
                print("You don't have enough coins to afford a room so you return to the main room")
            self.inn()

        def talk_bartender(self):
            print("The bartender tells you stories of distant lands and ancient treasures.")
            print("'Come back when you need rest or supplies,' he says.")
            if self.player.boss_item == True:
                print('Bye')
                self.player.main_quest = True

        def shop(self):
            pass

        def town_leave(self, entry_direction=None):
            print("You leave town.")
            if entry_direction is None:
                entry_direction = self.entry_direction
            self.player.move_back(entry_direction, self.game_map, restore_char='T')


        def town_raid(self):
            print('The town raid feature is not implemented yet.')


    class Dungeon:
        def __init__(self, name, location, gold, exp, player, game_map):
            self.name = name
            self.location = location
            self.gold = gold
            self.exp = exp
            self.player = player
            self.game_map = game_map
            
            self.entry_direction = None
            self.dungeon_menu_choice = {'1':self.dungeon_leave,
                                        'leave':self.dungeon_leave,
                                        'back': self.dungeon_leave,
                                        'deeper': self.boss_battle,
                                        '2': self.boss_battle}

        def dungeon_menu(self, entry_direction=None):
            if entry_direction is not None:
                self.entry_direction = entry_direction
            print("Dungeon")
            while True:
                print("1. Go back to the world")
                print("2. Go deeper")
                choice = self.player.get_input("Your choice: ")
                if choice in self.dungeon_menu_choice:
                    self.dungeon_menu_choice[choice](self.entry_direction)
                    break
                else:
                    print("Invalid choice. Please try again.")

        def dungeon_leave(self, entry_direction=None):
            print("You leave dungeon.")
            if entry_direction is None:
                entry_direction = self.entry_direction
            self.player.move_back(entry_direction, self.game_map, restore_char='D')

        def boss_battle(self):
            pass
        
class GameMap:

    def __init__(self, height, width, map_data=None, town_location=None, dungeon_location=None):
        self.height = height
        self.width = width
        if isinstance(map_data, list) and map_data:
            self.map = [list(row) for row in map_data]
        else:
            self.map = [['.' for x in range(width)] for y in range(height)]
        if town_location is not None:
            self.town_location = town_location
        else:
            self.town_location = self.get_random_empty_location()
        self.dungeon_location = dungeon_location if dungeon_location is not None else self.get_random_empty_location()


    def place_enemies(self, enemies):
        for enemy in enemies: 
            enemy.location = self.get_random_empty_location()
            self.map[enemy.location[1]][enemy.location[0]] = 'E'

    def place_town(self, town):
        self.map[self.town_location[1]][self.town_location[0]] = 'T'

    def place_dungeon(self, dungeon):
        self.map[self.dungeon_location[1]][self.dungeon_location[0]] = 'D'
       
    def get_random_empty_location(self):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.map[y][x] == '.' and (x, y) != (1,1):
                return x, y
        
    def display_map(self):
        for row in self.map:
            print(' '.join(row))
            
    def data_save(self):
            return {
                'height': self.height,
                'width': self.width,
                'map_data': self.map,
                'town_location': self.town_location,
                'dungeon_location': self.dungeon_location
            }

    @classmethod
    def data_load(cls, data):
            return cls(
                height=data['height'],
                width=data['width'],
                map_data=data['map_data'],
                town_location=tuple(data['town_location']),
                dungeon_location=tuple(data ['dungeon_location'])
                )
    
class Game:
    def __init__(self, player, game_map, enemies, dungeon, town):
        self.player = player
        self.game_map = game_map
        self.enemies = enemies
        self.dungeon = dungeon
        self.town = town

    def get_input(self, prompt):
        choice = input(prompt).strip().lower()
        if choice in ('q', 'quit'):
            self.player.quit_game()
        elif choice in ('b', 'menu'):
            new_game = self.menu()
            if isinstance(new_game, Game):
                return new_game
            return self.get_input(prompt)
        return choice

    def game_save(self, filename='savegame1.json'):
        data = {
            'player': self.player.data_save(),
            'enemies': [enemy.data_save() for enemy in self.enemies],
            'game_map': self.game_map.data_save(),
            'player_flags': {
                'main_quest': self.player.main_quest,
                'boss_item': self.player.boss_item,
            }
        }
        with open(filename, 'w') as save_file:
            json.dump(data, save_file, indent=2)
        print(f'Game saved to {filename}!')

    @classmethod
    def load_game(cls, filename='savegame1.json'):
        try:
            with open(filename, 'r') as save_file:
                data = json.load(save_file)
        except FileNotFoundError:
            print('Save file not found.')
            return None
        player = Objects.Player.data_load(data['player'])
        enemies = [Objects.Enemy.data_load(enemy_data) for enemy_data in data['enemies']]
        game_map = GameMap.data_load(data['game_map'])
        town = Objects.Town(name='', hp=1000, hp_max=1000, defense=5, str=50, location=game_map.town_location,
                            gold=random.randint(300, 1000), exp=random.randint(500, 1500),
                            player=player, game_map=game_map)
        dungeon = Objects.Dungeon(name='', location=game_map.dungeon_location,
                                  gold=random.randint(300, 1000), exp=random.randint(500, 1500),
                                  player=player, game_map=game_map)
        loaded_game = cls(player, game_map, enemies, dungeon, town)
        loaded_game.loaded = True
        return loaded_game
    
    def menu(self):
        while True:
            print('Hello to the game')
            print('1. Start new game')
            print('2. Load the game')
            print('3. Save the game')
            print('4. Quit')
            choice = self.player.get_input('Your choice:  ')
            if choice in ['1', 'start']:
                self.start()
                return self
            elif choice in ['2', 'load', 'l']:
                loaded_game = self.load_game()
                if loaded_game is not None:
                    return loaded_game
            elif choice in ['3', 'save']:
                self.game_save()
                continue
            elif choice in ['4']:
                self.player.quit_game()
            else:
                print("Invalid choice")
                continue

    def start(self):
        while not self.player.race:
            print('You were born years ago, in land far away. Your parents were.....\n'
                '\n'
                '1.Elves\n'
                '2.Humans\n'
                '3.Dwarfs')
            self.player.lvl = 1
            self.player.exp = 0
            self.player.cap_exp = 100
            self.player.estus = 1
            self.player.ashen = 1
            self.player.race = self.player.get_input('Your choice:  ')
            if self.player.race in ['1', 'elf', 'elves']:
                self.player.elf(self.player)
            elif self.player.race in ['2', 'human', 'humans']:
                self.player.human(self.player)
            elif self.player.race in ['3', 'dwarf', 'dwarfs']:
                self.player.dwarf(self.player)
            else:
                self.player.race = ""
                print('Invalid choice.')

        while not self.player.name:
            self.player.name = input("And your parents named you... ")

        while not self.player.c_class:
            print('You started to learn about the world almost as soon as you could walk and talk.'
                  ' You spent most of your life as.....\n'
                  '1.Merchant\n'
                  '2.Warrior\n'
                  '3.Wizard')
            self.player.c_class = self.player.get_input('Your choice:  ')
            if self.player.c_class in ['1', 'merchant']:
                self.player.merchant(self.player)
            elif self.player.c_class in ['2', 'warrior']:
                self.player.warrior(self.player)
            elif self.player.c_class in ['3', 'wizard']:
                self.player.wizard(self.player)
            else:
                self.player.c_class = ""
                print('Invalid choice.')

        return self

    def battle(self, enemy, player, direction, need_mana=False):
        print(f"You encounter a {enemy.name}!\n"
              'Battle starts!\n')
        while self.player.hp > 0 and enemy.hp > 0:        
            print(f"{self.player.name} HP: {self.player.hp}/{self.player.hp_max} | MP: {self.player.mp}/{self.player.mp_max}") 
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.hp_max}\n")
            print("Actions:\n" \
            "1. Attack\n"
            "2. Magic\n"
            "3. Item\n"
            "4. Run\n")
            action = self.player.get_input("Choose your action: ")
            if action in ('1', 'attack'):
                self.player.melee(enemy)
            elif action in ('2', 'magic'):
                self.player.magic(enemy)
            elif action in ('3', 'item'):
                self.player.item()
            elif action in ('4', 'run'):
                if self.player.escape(enemy, direction, self.game_map):
                    break
            else:
                print("Invalid action. Please choose again.")
                continue

            if enemy.hp > 0: 
                enemy_actions = (
                    lambda: enemy.attack(player),
                    lambda: enemy.magic(player),
                    lambda: enemy.heal(player, need_mana)
                )
                enemy_action = random.choice(enemy_actions)
                enemy_action()

        if self.player.hp <= 0:
            print("You have been defeated! Game Over.")
            self.player.quit_game()
        elif enemy.hp <= 0:
            print(f'You have defeated the {enemy.name}!')
            self.player.exp += enemy.exp
            self.player.gold += enemy.gold
            print(f'You gained {enemy.exp} experience points and {enemy.gold} gold.')
            self.player.level_up()
            self.enemies.remove(enemy)

        
    def run(self):
        x, y = self.game_map.dungeon_location
        self.game_map.map[y][x] = 'D'

        x, y = self.game_map.town_location
        self.game_map.map[y][x] = 'T'

        x, y = self.player.location
        self.game_map.map[y][x] = 'P'

        if not getattr(self, 'loaded', False):
            self.game_map.place_enemies(self.enemies)

        while self.player.main_quest == False:
            self.game_map.display_map()
            direction = self.get_input("Move W/A/S/D: ")
            if isinstance(direction, Game):
                return direction
            new_location = self.player.move(direction, self.game_map)

            if new_location == self.game_map.town_location:
                self.town.town_menu(direction)

            elif new_location == self.game_map.dungeon_location:
                self.dungeon.dungeon_menu(direction)

            else: 
                for enemy in self.enemies:
                    if enemy.location == new_location:
                        self.battle(enemy, player, direction)
                        break

            if self.player.hp <= 0:
                print('"You have been defeated! Game Over."')
                self.player.quit_game()



player = Objects.Player(
    name="", race="", c_class="", class_m="", lvl=0, exp=0, cap_exp=0,
    hp=0, mp=0, hp_max=0, mp_max=0, defense=0, str=0, mag_str=0,
    gold=0, inventory=(), location=(1,1), spell_book={}, estus=0,
    ashen=0, main_quest=False, boss_item=True
)

enemies = [Objects.Enemy(name="Goblin", hp=20, hp_max=0, mp=20, mp_max=0, defense=1, str=1,
                        mag_str=0, spell_book={'Fireball': 20}, location=(0, 0), gold=random.randint(1, 20),
                        exp=random.randint(1, 20))
           
            ]

game_map = GameMap(5, 5)

town = Objects.Town(name='', hp=1000, hp_max=1000, defense=5, str=50, location=(0,0),
                    gold=random.randint(300, 1000), exp=random.randint(500, 1500),
                    player=player, game_map=game_map)

dungeon = Objects.Dungeon(name='', location=(0,0),
                    gold=random.randint(300, 1000),
                    exp=random.randint(500, 1500), player=player, game_map=game_map)

game = Game(player, game_map, enemies, dungeon, town)

game = game.menu()
while True:
    next_game = game.run()
    if isinstance(next_game, Game):
        game = next_game
        continue
    break

