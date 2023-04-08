import sys
from random import randint  # из набора инструментов для создания рандомных чисел берем инструмент для рандомного int

import pygame as pg         # берем инструмент pygame и называем его pg для удобства


# https://pygame.readthedocs.io/en/latest/


class GameLogic:        # класс, отвечающий за игровую логику
    def __init__(self, app, max_score=0):   # если мы не передаем параметр max_scare, то он устанавливается на 0
        self.app = app
        self.field_width = self.app.screen.get_width() // 20        # устанавливаем ширину карты
        self.field_height = self.app.screen.get_height() // 20      # устанавливаем высоту карты
        """
        В строке №25 мы устанавливаем змейку по центру экрана, причем змейка строится следующим образом:
        Любая клетка имеет свои координаты, а змейка - это список клеток. Представим координаты клетки в следующем виде:
        [X, Y], то есть мы можем описать координаты клетки сделав список из двух элементов, где первый элемент - это
        координата X, а второй - это координата Y. Тогда, например, змейку, у которой длина равна 3, будем описывать
        следующим образом: [[X1, Y1], [X2, Y2], [X3, Y3]]. Здесь [X1, Y1] - это первая клетка (голова) змеи,
        [X2, Y2] - это вторая клетка змеи, [X3, Y3] - третья клетка (хвост) змеи.
        Так как в начале игры змея имеет длину 1, то чтобы ее описать, нужно сделать список вот такого вида: [[X1, Y1]],
        именно это мы и делаем в следующей строке.
        """
        self.snake = [[self.app.screen.get_width() // 40, self.app.screen.get_height() // 40]]
        """
        В строке №35 мы создадим пустой список для цветов, который заполним при помощи метода make_colors в строке №36.
        Этот список необходим, так как мы хотим сделать змею с градиентной расцветкой. Каждый элемент в этом списке
        отвечает за цвет одной из клеток змеи. Каждый элемент задает свой оттенок при помощи rgb. Например, рассмотрим
        вариант, когда змея имеет длину 3: в таком случае список цветов будет выглядеть следующим образом:
        [(r1, g1, b1), (r2, g2, b2), (r3, g3, b3)]. Здесь (r1, g1, b1) - это кортеж (tuple), который указывает цвет
        первой клетки змеи (головы) в формате rgb, (r2, g2, b2) - указывает цвет второй клетки, (r3, g3, b3) - указывает
        цвет третей клетки змеи (хвоста).
        """
        self.colors = []
        self.make_colors()      # вызываем метод для создания цветов змеи
        self.snake_direction = (1, 0)   # указываем направление змеи
        self.last_direction = (1, 0)    # указываем предыдущее направление змеи
        self.food = None        # указываем, что еды пока нет (в следующей строке мы ее заспавним)
        self.spawn_food()       # вызываем метод для спавна еды
        self.game_over = False  # указываем, что игра не проиграна (так как она только началась)
        self.timer = 0          # устанавливаем время на 0 (так как игра только началась)
        self.score = 0          # устанавливаем очки на 0 (так как игра только началась)
        self.max_score = max_score  # устанавливаем рекорд (если рекорд еще не был установлен, то =0, смотри строку №11)

    def make_colors(self):      # метод для создания цветов игры
        color1 = (26, 95, 122)  # цвет головы змеи
        color2 = (0, 43, 91)    # цвет хвоста змеи
        n = len(self.snake)     # узнаем длину змеи
        self.colors = []        # опустошаем список цветов змеи
        for i in range(n):      # идем от головы до хвоста и каждой клетке задаем свой цвет
            # some gradient magic
            self.colors.append(tuple(map(lambda x: x[0] * i / n + x[1] * (n - i) / n, zip(color1, color2))))

    def spawn_food(self):       # метод для спавна еды
        self.food = [randint(0, self.field_width-1), randint(0, self.field_height-1)]   # создаем еду в рандомном месте
        if self.food in self.snake:     # если еда случайно заспавнилась в змее
            self.food = None            # то указываем что еды нет

    def restart(self):          # метод для перезапуска игры
        self.snake = [[self.app.screen.get_width() // 40, self.app.screen.get_height() // 40]]  # смотри строку №16
        self.snake_direction = (1, 0)   # указываем направление змеи
        self.last_direction = (1, 0)    # указываем предыдущее направление змеи
        self.game_over = False          # указываем, что игра не проиграна (так как она только началась)
        self.timer = 0                  # устанавливаем время на 0 (так как игра только началась)
        self.score = 0                  # устанавливаем очки на 0 (так как игра только началась)
        self.food = None                # указываем, что еды пока нет (в двух следующих строках мы ее заспавним)
        while self.food is None:        # пока еды нет
            self.spawn_food()           # пытаемся ее заспавнить
        print(f'Max score is {self.max_score}!')    # выводим рекорд в консоль

    def update(self):       # метод обновления информации в игре (обновляет каждый шаг)
        if self.game_over:  # если игра проиграна
            return          # выходим из метода (так как в таком случае обновления не требуется)

        self.timer += self.app.dt   # обновляем время игры

        while self.food is None:    # пока еды нет
            self.spawn_food()       # пытаемся ее заспавнить

        delay = 0.1                 # указываем задержку в 0,1 секунду
        if self.timer < delay:      # если время задержки еще не прошло
            return                  # выходим из метода
        self.timer -= delay         # обнуляем время игры (чтобы потом так же сравнивать его с задержкой)

        self.last_direction = self.snake_direction  # записываем направление змеи в прошлое направление

        new_head = [    # рассчитываем клетку, где будет находиться голова змеи на следующем шагу
            (self.snake[-1][0] + self.snake_direction[0]) % self.field_width,
            (self.snake[-1][1] + self.snake_direction[1]) % self.field_height,
        ]

        if new_head in self.snake:  # если на следующем шагу голова змеи будет находиться в змее
            self.game_over = True   # то делаем игру проигранной
            if self.score > self.max_score:     # если количество очков больше рекорда
                self.max_score = self.score     # записываем в рекорд текущее количество очков
            return                              # выходим из метода

        self.snake.append(new_head)
        if new_head == self.food:
            self.spawn_food()
            self.score += 1
            self.make_colors()
        else:
            self.snake.pop(0)

    def draw(self):                 # метод прорисовки игры
        if self.game_over:          # если игра проиграна
            self.draw_snake()       # вызываем метод прорисовки змеи (смотри строку № 130)
            self.draw_food()        # вызываем метод прорисовки еды (смотри строку № 126)
            self.draw_score()       # вызываем метод прорисовки очков (смотри строку № 122)
            self.draw_game_over()   # вызываем метод прорисовки заставки "Игра окончена" (смотри строку № 118)
        else:                       # иначе
            self.draw_snake()       # вызываем метод прорисовки змеи (смотри строку № 130)
            self.draw_food()        # вызываем метод прорисовки еды (смотри строку № 126)
            self.draw_score()       # вызываем метод прорисовки очков (смотри строку № 122)

    def draw_game_over(self):   # метод прорисовки заставки "Игра окончена"
        img = self.app.score_font.render(f'You lose scoring {self.score}. Max record is {self.max_score}', True, (0, 43, 91))
        self.app.screen.blit(img, (200, 200))

    def draw_score(self):   # метод прорисовки очков
        img = self.app.score_font.render(f'Score: {self.score}', True, (0, 43, 91))
        self.app.screen.blit(img, (20, 20))

    def draw_food(self):    # метод прорисовки еды
        if self.food:
            pg.draw.rect(self.app.screen, (21, 152, 149), [self.food[0]*20, self.food[1]*20, 20, 20])

    def draw_snake(self):   # метод прорисовки змеи
        for index, square in enumerate(self.snake):
            pg.draw.rect(self.app.screen, self.colors[index], [square[0]*20, square[1]*20, 20, 20])

    def move_up(self):  # метод для движения вверх
        if self.last_direction != (0, 1):
            self.snake_direction = (0, -1)

    def move_left(self):    # метод для движения влево
        if self.last_direction != (1, 0):
            self.snake_direction = (-1, 0)

    def move_down(self):    # метод для движения вниз
        if self.last_direction != (0, -1):
            self.snake_direction = (0, 1)

    def move_right(self):   # метод для движения вправо
        if self.last_direction != (-1, 0):
            self.snake_direction = (1, 0)


class App:      # класс, отвечающий за логику работы всего приложения
    def __init__(self):
        pg.init()   # инициализируем (запускаем pygame)
        self.screen = pg.display.set_mode((1600, 900))  # создаем окно и указываем его размеры
        pg.display.set_caption('Snake')     # устанавливаем название окна
        print(type(self.screen))            # выводим тип окна (?) в консоль
        self.clock = pg.time.Clock()        # получаем таймер, который будет идти и показывать миллисекунды (1с=1000мс)
        self.score_font = pg.font.SysFont("exo2extrabold", 24)  # устанавливаем шрифт, которым будем выводить очки
        self.dt = 0.0                   # устанавливаем время, которое прошло с прошлого обновления на 0 (обнов еще нет)
        self.logic = GameLogic(self)    # создаем экземпляр класса, отвечающего за игровую логику

    def update(self):                           # метод обновления всего окна
        self.logic.update()                     # вызывает метод обновления информации в игре (смотри строку №72)
        pg.display.flip()                       # обновляем изображение на экране
        self.dt = self.clock.tick() * 0.001     # получаем время, которое прошло с пошлого обновления, но делим на 1000

    def draw(self):                         # метод прорисовки окна
        self.screen.fill((87, 197, 182))    # заливаем фон бирюзовым цветом
        self.logic.draw()                   # вызов метода прорисовки игры (смотри строку №107)

    def check_events(self):     # метод проверки событий (проверяет, нажата ли какая-нибудь клавиша)
        for e in pg.event.get():    # проходимся по всем событиям, которые произошли с окном
            """
            В строке №178 мы проверяем вот что: если была нажата кнопка "Закрыть" (e.type == pg.QUIT) или если какая-то
            клавиша была нажата (e.type == pg.KEYDOWN) и это была клавиша ESCAPE (e.key == pg.K_ESCAPE), тогда
            выполняется то, что указано в строках №179 и №180. 
            """
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()       # прекращаем работу с pygame
                sys.exit()      # закрываем окно
            if self.logic.game_over:        # если игра проиграна (смотри строку №41)
                if e.type == pg.KEYDOWN:    # если какая-то клавиша нажата
                    # TODO: save records
                    self.logic.restart()    # вызываем метод для перезапуска игры (смотри строку №60)
            elif e.type == pg.KEYDOWN:                          # если какая-то клавиша нажата
                if e.key == pg.K_UP or e.key == ord('w'):       # если это была нажата стрелочка вверх или w
                    self.logic.move_up()                        # вызываем метод для движения вверх (смотри строку №134)
                if e.key == pg.K_DOWN or e.key == ord('s'):     # если это была нажата стрелочка вниз или s
                    self.logic.move_down()                      # вызываем метод для движения вниз (смотри строку №142)
                if e.key == pg.K_LEFT or e.key == ord('a'):     # если это была нажата стрелочка влево или a
                    self.logic.move_left()                      # вызываем метод для движения влево (смотри строку №138)
                if e.key == pg.K_RIGHT or e.key == ord('d'):    # если это была нажата стрелочка вправо или d
                    self.logic.move_right()                     # вызываем метод для движения вправо (см. строку №146)

    def run(self):                  # метод, обеспечивающий работу программы
        while True:                 # бесконечный цикл
            self.check_events()     # вызываем метод проверки событий (смотри строку №171)
            self.update()           # вызывает метод обновления всего окна (смотри строку №162)
            self.draw()             # вызываем метод прорисовки окна (смотри строку №167)


if __name__ == '__main__':  # основная программа
    snake = App()           # создаем экземпляр класса, отвечающего за логику работы всего приложения (см. строку №151)
    snake.run()             # вызываем метод, обеспечивающий работу программы (смотри строку №195)
