from create_db import create, Result, session
from random import choice, choices, randint
from string import ascii_lowercase
from time import sleep, time
import os
import pygame

pygame.init()
menu_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')
screen.fill((0, 0, 0))
score = 0


def load_image(obj, name, x=0, y=0, width=width, height=height):
    path = os.path.dirname(__file__)
    name = os.path.join(path, 'data', name)
    image = pygame.image.load(name)
    image = image.convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    setattr(obj, 'image', image)
    obj.rect = obj.image.get_rect()
    obj.rect.x = x
    obj.rect.y = y


class Menu(pygame.sprite.Sprite):
    def __init__(self, group, width, height):
        super().__init__(group)
        self.width = width
        self.height = height
        self.menu = [
            'Input your name: ', '|',
            'Start', 'Records', 'About'
        ]
        self.item = 2
        self.current_screen = 'menu'
        self.screenplay = {
            '0': ['hall.png', 'shadow.png', ['Понедельник. 8:30am'], ['...']],
            '1.': ['room.png', 'book.png', ['Ух, надо поторопится...'], ['Положить'], 3],
            '1.1.': ['locker.png', 'watches.png', ['Фух... успел'], ['Проверить шкафчик', 'Пойти в класс'], 3],
            '1.1.1.': ['open_locker.png', 'open_locker.png', ['Что это?'], ['Взять письмо'], 3],
            '1.1.1.1.': ['open_locker.png', 'letter.png', ['...'], ['...'], 2],
            '1.1.2.': ['classroom.png', 'classroom.png', ['Скоро домой.'], ['...'], 2],
            '1.1.1.1.1.': ['classroom.png', 'classroom.png', ['Теперь не могу сосредоточиться'], ['...'], 2],
            '1.1.1.1.1.1.': ['clock.png', 'letter.png', ['Время назначенной встречи..'],
                             ['Пойти на крышу', 'Проигнорировать и пойти домой'], 2],
            '1.1.2.1.': ['clock.png', 'letter.png', ['*звонок*'], ['Пойти на крышу, подышать', 'Пойти домой'], 3],
            '1.1.2.1.1.': ['meeting.png', 'meeting.png',
                           ['О! Ты пришел, я так рада! Значит ты согласен встречаться!? Я так рада, что это взаимно!!'],
                           ['Эмм.. что..я не... это не..'], 3],
            '1.1.2.1.2.': ['meeting.png', 'meeting.png', ['Почему ты не прочитал... Я тебя так долго ждала!!!'],
                           ['Чего?'], 1],
            '1.1.1.1.1.1.1.': ['meeting.png', 'meeting.png', ['Почему ты прочел и проигнорировал...? я тебя так долго '
                                                              'ждала!!'],
                               ['Эмм.. да, на счет этого, я пока ничего подобного не планировал....'], 2],
            '1.1.1.1.1.1.2.': ['meeting.png', 'meeting.png', [
                'О! Ты пришел, я так рада! Значит ты согласен встречаться!? Я так рада, что это взаимно!!'],
                               ['Стой, ты не правильно поняла, я сожалею, но я не думал е о чем таком.'], 3],
            '1.1.2.1.1.1.': ['meeting2.png', 'meeting2.png',
                             [
                                 'Всмысле, ты меня обманул???? Почему мне всегда так не везет. Ненавижу!! Я тебя '
                                 'ненавижу!!'],
                             ['Ох....'], 1],
            '1.1.2.1.2.1.': ['meeting2.png', 'meeting2.png', ['Почему ты не прочитал... Я тебя так долго ждала!!!'],
                             ['Ох....'], 1],
            '1.1.1.1.1.1.1.1.': ['meeting2.png', 'meeting2.png',
                                 ['Почему ты прочел и проигнорировал...? я тебя так долго ждала!!'],
                                 ['Ох....'], 1],
            '1.1.1.1.1.1.2.1.': ['meeting2.png', 'meeting2.png', [
                'Всмысле, ты меня обманул???? Почему мне всегда так не везет. Ненавижу!! Я тебя ненавижу!!'],
                                 ['Ох....'], 1],
            '1.1.2.1.1.1.1.': runner,
            '1.1.2.1.2.1.1.': runner,
            '1.1.1.1.1.1.1.1.1.': runner,
            '1.1.1.1.1.1.2.1.1.': runner,
        }
        load_image(self, 'hall.png')

    def draw_menu(self, screen, brightness=0, delta_x=0):
        if self.item < 2:
            self.item = 2
        elif self.item > len(self.menu) - 1:
            self.item = len(self.menu) - 1
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        delta_y = 0
        for i, row in enumerate(self.menu):
            if i != 0:
                delta_x *= 0
            if self.item == i:
                text = font.render(row, True, (180 - brightness, 0, 0))
            else:
                text = font.render(row, True, (0, 180 - brightness, 0))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = self.width // 2 - text_w // 2 + delta_x
            text_y = self.height // 4 - text_h // 2 + delta_y
            screen.blit(text, (text_x, text_y))
            delta_y += 60
        pygame.display.flip()

    def add_result(self):
        new_result = Result(
            player=self.menu[1][:-1],
            points=score
        )
        session.add(new_result)
        session.commit()

    def draw_results(self, screen, all_results):
        all_results.insert(0, ('PLAYER POINTS'))
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        delta_y = 10
        for result in all_results[:10]:
            result = str(result).split()
            print(result)
            user = font.render(str(result[0]), True, (0, 180, 0))
            points = font.render(str(result[1]), True, (0, 180, 0))
            screen.blit(user, (10, delta_y))
            screen.blit(points, (790 - points.get_width(), delta_y))
            delta_y += 60

    def start(self, bg, image, story, answers, vector=0):
        x = 2
        y = 2
        self.current_screen = 'first'
        screen.fill((0, 0, 0))
        load_image(self, bg)
        menu_sprites.draw(screen)
        if bg != image:
            load_image(self, image, x=x, y=y)
            menu_sprites.draw(screen)
            for i in range(1):
                load_image(self, bg)
                menu_sprites.draw(screen)
                if vector == 0:
                    y -= 2
                    x = 0
                elif vector == 1:
                    y += 2
                    x = 0
                elif vector == 2:
                    x += 2
                    y = 0
                elif vector == 3:
                    x -= 2
                    print("nya")
                    y = 0
                load_image(self, image, x=x, y=y)
                menu_sprites.draw(screen)
                pygame.display.flip()
        font = pygame.font.Font(None, 50)
        rows = [font.render(row, True, (200, 0, 0)) for row in story]
        y = 50
        for row in rows:
            screen.blit(row, (50, y))
            y += 60
        s = pygame.Surface((800, 100), pygame.SRCALPHA)
        screen.blit(s, (0, 500))
        answers = [font.render(answer, True, (200, 0, 0)) for answer in answers]
        y = 450
        for answer in answers:
            screen.blit(answer, (0, y))
            y += 50

    def show_results(self):
        all_results = Result.query.order_by(Result.points.desc()).all()
        self.draw_results(screen, all_results)

    def show_about(self):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render('authors snd etc', True, pygame.Color('white'))
        screen.blit(text, (200, 50))

    def update(self, delta_x=0, delta_y=0):
        self.rect.x += delta_x
        self.rect.y += delta_y


class Background(pygame.sprite.Sprite):
    def __init__(self, group, name, x, y):
        super().__init__(group)
        load_image(self, name, x, y, 800, 600)

    def update(self):
        self.rect.x -= 5


class Boy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.boys = ['boy1.png', 'boy2.png', 'boy3.png', 'boy2.png']
        self.x = 300
        self.y = 500
        self.width = 45
        self.height = 95
        load_image(self, self.boys[0], self.x, self.y, self.width, self.height)
        self.boys.append(self.boys.pop(0))
        self.status = 'forward'
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.status == 'forward':
            self.boys.append(self.boys.pop(0))
            load_image(self, self.boys[0], self.x, self.y, self.width, self.height)
        else:
            if self.status == 'up':
                if self.y > 400:
                    self.y -= 8
                else:
                    self.status = 'down'
            elif self.status == 'down':
                if self.y < 500:
                    self.y += 10
                else:
                    self.status = 'forward'
            load_image(self, 'boy1.png', self.x, self.y, self.width, self.height)


class Girl(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.boys = ['girl.png', 'girl.png', 'girl.png', 'girl.png']
        self.x = 200
        self.y = 500
        self.width = 45
        self.height = 95
        load_image(self, self.boys[0], self.x, self.y, self.width, self.height)
        self.boys.append(self.boys.pop(0))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.boys.append(self.boys.pop(0))
        load_image(self, self.boys[0], self.x, self.y, self.width, self.height)
        global boy, game_over
        if pygame.sprite.collide_mask(self, boy):
            game_over = True


class Coin(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        load_image(self, 'coin.png', x, y, 30, 30)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 5
        global boy
        if pygame.sprite.collide_mask(self, boy):
            self.kill()
            global score
            score += 1


class Cow(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        load_image(self, 'cow.png', x, y, 70, 50)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= 5
        global boy, girl
        if pygame.sprite.collide_mask(self, boy):
            self.kill()
            girl.x += 20


class Scheme(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        load_image(self, 'map.png', x, y, 800, 50)


class Point(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        load_image(self, 'point.png', x, y, 20, 20)

    def update(self):
        if self.rect.x != 761:
            self.rect.x += 1
        else:
            global game_over
            game_over = True


def runner():
    global boy, girl, score
    i = 0
    bg1 = Background(all_sprites, 'bg1.png', 0, 0)
    bg2 = Background(all_sprites, 'bg2.png', 800, 0)
    boy = Boy(all_sprites)
    girl = Girl(all_sprites)
    font = pygame.font.Font(None, 40)
    Scheme(all_sprites, 0, 25)
    point = Point(all_sprites, 60, 48)
    global game_over
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    boy.status = 'up'
        if bg1.rect.x == -800:
            bg1.rect.x = 800
        elif bg2.rect.x == -800:
            bg2.rect.x = 800
        i += 5
        if i % 50 == 0:
            if choices([0, 1], [0.8, 0.2]) == [1]:
                Coin(all_sprites, 850, choice([540, 470]))
            elif choices([0, 1], [0.3, 0.7]) == [1]:
                Cow(all_sprites, 850, 530)
        all_sprites.update()
        all_sprites.draw(screen)
        text = font.render(f'Scores: {score}', True, pygame.Color('yellow'))
        screen.blit(text, (790 - text.get_width(), 10))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    font = pygame.font.Font(None, 60)
    text = font.render(f'GAME OVER', True, pygame.Color('red'))
    screen.blit(text, (400 - text.get_width() // 2, 200 - text.get_height()))
    font = pygame.font.Font(None, 50)
    text = font.render(f'Your result: {score}', True, pygame.Color('green'))
    screen.blit(text, (400 - text.get_width() // 2, 300 - text.get_height()))
    text = font.render(f'Press Esc to continue', True, pygame.Color('green'))
    screen.blit(text, (400 - text.get_width() // 2, 400 - text.get_height()))
    pygame.display.flip()
    boy.kill()
    point.kill()


if __name__ == '__main__':
    if 'database.db' not in os.listdir(os.path.dirname(__file__)):
        create()
    clock = pygame.time.Clock()
    game = Menu(menu_sprites, width, height)
    game.draw_menu(screen)
    running = True
    story_path = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.current_screen != 'menu':
                    x, y = event.pos
                    print(x, y)
                    if 0 <= x <= 800:
                        if 450 <= y < 500:
                            story_path += '1.'
                        elif 500 <= y < 550:
                            story_path += '2.'
                        elif 550 <= y <= 600:
                            story_path += '3.'
                    if story_path in game.screenplay:
                        if type(game.screenplay[story_path]) == list:
                            bg, image, story, answers, vector = game.screenplay[story_path]
                            game.start(bg, image, story, answers, vector)
                        else:
                            game.screenplay[story_path]()
                            game.add_result()
                            score = 0
                            game.current_screen = 'menu'
                    else:
                        story_path = story_path[:-2]

            if game.current_screen == 'menu' and event.type == pygame.KEYDOWN:
                for letter in ascii_lowercase:
                    if event.key == getattr(pygame, f'K_{letter}'):
                        if len(game.menu[1]) < 16:
                            game.menu[1] = game.menu[1][:-1] + f'{letter}|'
                            game.draw_menu(screen)
                            break
                if event.key == pygame.K_DOWN:
                    game.item += 1
                    game.draw_menu(screen)
                if event.key == pygame.K_UP:
                    game.item += -1
                    game.draw_menu(screen)
                if event.key == pygame.K_RETURN:
                    if game.menu[game.item] == 'Start':
                        if len(game.menu[1]) < 2:
                            x = [3, 0, -3, 0, 3, 0]
                            for i in range(6):
                                game.draw_menu(screen, delta_x=x[i])
                                sleep(0.04)
                        else:
                            for i in range(10, 181, 10):
                                game.draw_menu(screen, i)
                                sleep(0.04)
                            bg, image, story, answers = game.screenplay['0']
                            game.start(bg, image, story, answers)
                    elif game.menu[game.item] == 'Records':
                        game.show_results()
                    elif game.menu[game.item] == 'About':
                        for i in range(10, 181, 10):
                            game.draw_menu(screen, i)
                            sleep(0.04)
                        game.show_about()

                if event.key == pygame.K_ESCAPE:
                    for i in range(170, -1, -10):
                        game.draw_menu(screen, i)
                        sleep(0.1)
                if event.key == pygame.K_BACKSPACE:
                    if len(game.menu[1]) > 1:
                        game.menu[1] = game.menu[1][:-2] + '|'
                        game.draw_menu(screen)
        clock.tick(120)
        pygame.display.flip()
    pygame.quit()
