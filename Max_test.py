from random import randint
from random import choice

SIZE_GAME_POLE = 10

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp
        self._x = x
        self._y = y
        self._is_move = True
        self._cells = [1] * self._length

    def __setattr__(self, key, value):
        if key == '_length' and not 1 <= value <= 4:
            raise ValueError
        elif key == '_tp' and not 1 <= value <= 2:
            raise ValueError
        # elif key in ('_x', '_y') and not (0 <= value <= SIZE_GAME_POLE):
        #     raise ValueError
        super().__setattr__(key, value)

    def set_start_coords(self, x, y):
        """установка начальных координат (запись значений в локальные атрибуты _x, _y)"""
        self._x = x
        self._y = y


    def get_start_coords(self):
        """получение начальных координат корабля в виде кортежа x, y"""
        return self._x, self._y

    def move(self, go):
        """перемещение корабля в направлении его ориентации на go клеток
        (go = 1 - движение в одну сторону на клетку;
        go = -1 - движение в другую сторону на одну клетку);
        движение возможно только если флаг _is_move = True"""
        if not self._is_move:
            return False
        self.set_start_coords(self._x + go if self._tp == 1 else self._x, self._y + go if self._tp == 2 else self._y)
        if not (0 <= self._x <= 9) or not (0 <= self._y <= 9):
            return False
        return True



    def check_diap(self, aX1, aX2, bX1, bX2):
        """Возвращает True, если есть пересечение"""
        return (aX1 in range(bX1-1, bX2 + 2)) or \
            (aX2 in range(bX1-1, bX2 + 2)) or \
            (bX1 in range(aX1-1, aX2 + 2)) or \
            (bX2 in range(aX1-1, aX2 + 2))

    def is_collide(self, ship):
        """проверка на столкновение с другим кораблем ship (столкновением считается,
        если другой корабль или пересекается с текущим или просто соприкасается,
        в том числе и по диагонали);
        метод возвращает True, если столкновение есть и False - в противном случае"""
        if ship._x is None:
            return False
        x2 = self._x + (self._length - 1) * int(self._tp == 1)
        y2 = self._y + (self._length - 1) * int(self._tp == 2)
        ship_x2 = ship._x + (ship._length - 1) * int(ship._tp == 1)
        ship_y2 = ship._y + (ship._length - 1) * int(ship._tp == 2)

        return self.check_diap(self._x, x2, ship._x, ship_x2) and \
            self.check_diap(self._y, y2, ship._y, ship_y2)



    def is_out_pole(self, size):
        """проверка на выход корабля за пределы игрового поля
        (size - размер игрового поля, обычно, size = 10);
        возвращается булево значение True, если корабль вышел из игрового поля
        и False - в противном случае"""
        return self._x + (self._length - 1) * int(self._tp == 1) > size - 1 or \
            self._y + (self._length - 1) * int(self._tp == 2) > size - 1

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value


class GamePole:
    def __init__(self, size):
        self._size = size
        self._ships = []

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def ship_is_collide(self, ship):
        for ship2 in self._ships:
            if (ship != ship2) and ship.is_collide(ship2):
                return True
        return False

        # return any(lambda s1, s2: s1.is_collide(s2) for s1 in self._ships for s2 in self._ships)

    def init(self):
        """начальная инициализация игрового поля; здесь создается список из кораблей
        (объектов класса Ship):
        однопалубных - 4;
        двухпалубных - 3;
        трехпалубных - 2;
        четырехпалубный - 1
        (ориентация этих кораблей должна быть случайной)"""
        # self._pole = [[0] * self._size for i in range(self._size)]
        self._ships = [Ship(4, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))
                       ]
        for ship in self._ships:
            while True:
                ship.set_start_coords(randint(0, SIZE_GAME_POLE - 1), randint(0, SIZE_GAME_POLE - 1))
                # print(self.ship_is_collide(ship), ship.is_out_pole(SIZE_GAME_POLE), ship.get_start_coords(), ship._tp, ship._length)
                if not self.ship_is_collide(ship) and not ship.is_out_pole(SIZE_GAME_POLE):
                    # self.show()
                    break


    def get_ships(self):
        """возвращает коллекцию _ships"""
        return self._ships

    def move_ships(self):
        """перемещает каждый корабль из коллекции _ships на одну клетку
        (случайным образом вперед или назад) в направлении ориентации корабля;
        если перемещение в выбранную сторону невозможно
        (другой корабль или пределы игрового поля),
        то попытаться переместиться в противоположную сторону,
        иначе (если перемещения невозможны), оставаться на месте"""
        for ship in self._ships:
            x = ship._x
            y = ship._y

            m = choice([-1, 1])
            res = ship.move(m)
            if not res or self.ship_is_collide(ship) or ship.is_out_pole(SIZE_GAME_POLE):
                ship.set_start_coords(x, y)
                res = ship.move(-m)
                if not res or self.ship_is_collide(ship) or ship.is_out_pole(SIZE_GAME_POLE):
                    ship.set_start_coords(x, y)



    def show(self):
        """отображение игрового поля в консоли
        (корабли должны отображаться значениями из коллекции _cells каждого корабля,
        вода - значением 0)"""
        for row in self.get_pole():
            for x in row:
                print(x, end=' ')
            print()

    def get_pole(self):
        """получение текущего игрового поля в виде двумерного (вложенного) кортежа
        размерами size x size элементов"""
        pole = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            x, y = ship._x, ship._y
            if x is not None:
                for l in range(ship._length):
                    pole[y][x] = ship._cells[l]
                    x += int(ship._tp == 1)
                    y += int(ship._tp == 2)
        for i in range(len(pole)):
            pole[i] = tuple(pole[i])
        return tuple(pole)




pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()
