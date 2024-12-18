import random

class Hero:
    def __init__(self, name, health=100, attack_power=20, dodge_chance=0.2):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.dodge_chance = dodge_chance

    def attack(self, other):
        if random.random() > other.dodge_chance:
            damage = random.randint(self.attack_power // 2, self.attack_power)
            other.health -= damage
            print(f'{self.name} атакует {other.name} и наносит {damage} урона.')
        else:
            print(f'{other.name} увернулся от атаки!')

    def is_alive(self):
        return self.health > 0


class Boss(Hero):
    def __init__(self, name, health=300, attack_power=40, dodge_chance=0.1):
        super().__init__(name, health, attack_power, dodge_chance)


class Game:
    def __init__(self, player_name):
        self.player = Hero(player_name, health=120, attack_power=25, dodge_chance=0.3)
        self.enemies = [
            Hero("Гоблин", health=80, attack_power=15),
            Hero("Орк", health=100, attack_power=20),
            Hero("Тролль", health=120, attack_power=25),
            Hero("Тёмный эльф", health=90, attack_power=18, dodge_chance=0.4),
            Hero("Некромант", health=110, attack_power=22)
        ]
        self.boss = Boss("Дракон")
        self.current_enemy = None

    def start(self):
        print("Игра начинается!\n")
        while self.enemies:
            self.current_enemy = self.enemies.pop(0)
            print(f"Ваш противник: {self.current_enemy.name}\n")
            self.fight(self.current_enemy)

            if not self.player.is_alive():
                print(f"{self.player.name} погиб! Игра окончена.")
                return

        print("Вы победили всех врагов! Появляется босс...\n")
        self.fight(self.boss)

        if self.player.is_alive():
            print(f"{self.player.name} победил босса и выиграл игру!")
        else:
            print(f"Босс победил {self.player.name}. Попробуйте снова!")

    def fight(self, enemy):
        while self.player.is_alive() and enemy.is_alive():
            self.player_turn(enemy)
            if enemy.is_alive():
                self.enemy_turn(enemy)

    def player_turn(self, enemy):
        print(f"\nХод {self.player.name}!")
        self.player.attack(enemy)
        if enemy.is_alive():
            print(f"У {enemy.name} осталось {enemy.health} здоровья.\n")
        else:
            print(f"{enemy.name} побеждён!\n")

    def enemy_turn(self, enemy):
        print(f"Ход {enemy.name}!")
        enemy.attack(self.player)
        if self.player.is_alive():
            print(f"У {self.player.name} осталось {self.player.health} здоровья.\n")
        else:
            print(f"{self.player.name} погиб!\n")


# Запуск игры
game = Game("Игрок")
game.start()
