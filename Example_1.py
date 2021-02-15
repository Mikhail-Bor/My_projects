# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

HUMAN_FOOD = 'еда для людей'
CAT_FOOD = 'кошачий корм'


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.dirt = 0
        self.fridge = {HUMAN_FOOD: 50, CAT_FOOD: 30}
        self.earned_money = 0
        self.food_eaten = 0
        self.fur_coat = 0

    def __str__(self):
        return 'В доме: денег осталось {}, в холодильнике осталось {}, грязи {}' \
            .format(self.money, self.fridge, self.dirt)

    def act(self):
        self.dirt += 5

    def overall_result(self):
        print('Итоги жизни за год: заработано денег {}, сьедено еды {}, куплено шуб {}'.format(self.earned_money,
                                                                                               self.food_eaten,
                                                                                               self.fur_coat))


class LivingBeing:

    def __init__(self, name, house, food, max_meal, saturation_factor):
        self.name = name
        self.fullness = 30
        self.home = house
        self.suitable_food = food
        self.max_food = max_meal
        self.saturation_factor = saturation_factor

    def is_alive(self):
        if self.fullness <= 0:
            cprint('{} умер(ла) от голода!'.format(self.name), color='red')
            return False
        return True

    def eat(self):
        if self.home.fridge[self.suitable_food] > 0:
            serving_size = min(self.max_food, self.home.fridge[self.suitable_food])
            print('{} поел(а)'.format(self.name))
            self.fullness += serving_size * self.saturation_factor
            self.home.fridge[self.suitable_food] -= serving_size
            self.home.food_eaten += serving_size
        else:
            cprint('{} Нет еды!'.format(self.name), color='yellow')
            self.fullness -= 10


class Human(LivingBeing):

    def __init__(self, name, house, max_meal):
        super().__init__(name=name, house=house, food=HUMAN_FOOD, max_meal=max_meal, saturation_factor=1)
        self.happiness = 100

    def is_alive(self):
        if not super().is_alive():
            return False

        if self.happiness <= 10:
            cprint('{} умер(ла) от депрессии!'.format(self.name), color='red')
            return False

        return True

    def petting_cat(self):
        print('{} погладил(а) кота'.format(self.name))
        self.happiness += 5

    def __str__(self):
        return '{}, сытость {}, счастье {}'.format(self.name, self.fullness, self.happiness)


class Husband(Human):
    def __init__(self, name, house):
        super().__init__(name=name, house=house, max_meal=30)

    def act(self):
        if self.home.dirt >= 90:
            self.happiness -= 10

        dice = randint(1, 6)
        if self.fullness <= 30:
            self.eat()
        elif self.home.money <= 100:
            self.work()
        elif self.happiness <= 30 and self.home.money >= 450:
            self.gaming()
        elif dice == 1:
            self.petting_cat()
        elif dice == 2:
            self.gaming()
        else:
            self.work()

    def work(self):
        print('{} сходил на работу'.format(self.name))
        self.home.money += 150
        self.home.earned_money += 150
        self.fullness -= 10

    def gaming(self):
        print('{} играет в WoT'.format(self.name))
        self.happiness += 20
        self.fullness -= 10


class Wife(Human):
    def __init__(self, name, house):
        super().__init__(name=name, house=house, max_meal=30)

    def act(self):
        if self.home.dirt >= 90:
            self.happiness -= 10

        dice = randint(1, 6)
        if self.fullness <= 30:
            self.eat()
        elif self.home.fridge[self.suitable_food] <= 100:
            self.shopping()
        elif self.home.fridge[CAT_FOOD] <= 100:
            self.shopping_food_cat()
        elif self.happiness <= 30:
            self.buy_fur_coat()
        elif self.home.dirt >= 80:
            self.clean_house()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.petting_cat()
        elif dice == 3:
            self.buy_fur_coat()
        else:
            self.clean_house()

    def shopping(self):
        purchase_size = min(100, self.home.money)
        print('{} сходила в магазин'.format(self.name))
        self.fullness -= 10
        self.home.fridge[self.suitable_food] += purchase_size
        self.home.money -= purchase_size

    def shopping_food_cat(self):
        purchase_size = min(100, self.home.money)
        print('{} сходила в зоомагазин'.format(self.name))
        self.fullness -= 10
        self.home.fridge[CAT_FOOD] += purchase_size
        self.home.money -= purchase_size

    def buy_fur_coat(self):
        if self.home.money >= 450:
            print('{} купила шубу'.format(self.name))
            self.fullness -= 10
            self.home.money -= 350
            self.home.fur_coat += 1
            self.happiness += 60

    def clean_house(self):
        if self.home.dirt >= 0:
            print('{} убралась дома'.format(self.name))
            self.fullness -= 10
            self.home.dirt -= min(100, self.home.dirt)


class Cat(LivingBeing):

    def __init__(self, name, house):
        super().__init__(name=name, house=house, food=CAT_FOOD, max_meal=10, saturation_factor=2)

    def act(self):
        dice = randint(1, 3)

        if self.fullness <= 30:
            self.eat()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.sleep()
        else:
            self.soil()

    def sleep(self):
        print('{} спит'.format(self.name))
        self.fullness -= 10

    def soil(self):
        print('{} дерет обои'.format(self.name))
        self.fullness -= 10
        self.home.dirt += 5

    def __str__(self):
        return '{}, сытость {}'.format(self.name, self.fullness)


class Child(Human):

    def __init__(self, name, house):
        super().__init__(name=name, house=house, max_meal=10)

    def act(self):
        dice = randint(1, 2)
        if self.fullness <= 30:
            self.eat()
        elif dice % 2:
            self.eat()
        else:
            self.sleep()

    def sleep(self):
        print('{} спит'.format(self.name))
        self.fullness -= 10


home = House()
serge = Husband(name='Сережа', house=home)
masha = Wife(name='Маша', house=home)
barsik = Cat(name='Барсик', house=home)
sasha = Child(name='Саша', house=home)
attendees = (serge, masha, sasha, barsik)

f_success = True
for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    for i in attendees:
        i.act()
        f_success &= i.is_alive()
        cprint(i, color='cyan')
    home.act()
    cprint(home, color='cyan')

    if not f_success:
        break

home.overall_result()
