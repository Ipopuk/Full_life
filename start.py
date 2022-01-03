from create_db import create, Result, session
from random import choice, randint
from string import ascii_lowercase
from time import sleep
import os
import pygame


pygame.init()
menu_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Menu')
screen.fill((0, 0, 0))


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
            'Start', 'Start 2', 'Records', 'About'
            ]
        self.item = 2
        self.current_screen = 'menu'

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
            points=randint(10, 99)
        )
        session.add(new_result)
        session.commit()

    def draw_results(self, screen, all_results):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        delta_y = 0
        for result in all_results:
            text = font.render(str(result), True, (0, 180, 0))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = self.width // 2 - text_w // 2
            text_y = self.height // 4 - text_h // 2 + delta_y
            screen.blit(text, (text_x, text_y))
            delta_y += 60

    def start(self): #, current_screen):
        self.current_screen = 'first'
        font = pygame.font.Font(None, 50)
        rows = ['Давным-давно', 'в далекой-далекой галактике...']
        rows = [font.render(row, True, (0, 0, 0)) for row in rows]
        y = 50
        for row in rows:
            screen.blit(row, (50, y))
            y += 60
        s = pygame.Surface((800, 100), pygame.SRCALPHA)
        screen.blit(s, (0, 500))
        answers = [f'{i} ответ' for i in range(1, 5)]
        answers = [font.render(answer, True, (0, 0, 0)) for answer in answers]
        x = 0
        y = 500
        answer = 0
        for row in range(2):
            for col in range(2):
                screen.blit(answers[answer], (x, y))
                x += 400
                answer += 1
            x = 0
            y += 50
        print('готово!')

    def show_results(self):
        all_results = Result.query.all()
        self.draw_results(screen, all_results)


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

    def update(self):
        if self.status == 'forward':
            self.boys.append(self.boys.pop(0))
            load_image(self, self.boys[0], self.x, self.y, self.width, self.height)
        else:
            if self.status == 'up':
                if self.y > 460:
                    self.y -= 8
                else:
                    self.status = 'down'
            elif self.status == 'down':
                if self.y < 500:
                    self.y += 10
                else:
                    self.status = 'forward'
            load_image(self, 'boy1.png', self.x, self.y, self.width, self.height)


class Coin(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        load_image(self, 'coin.png', x, y, 30, 30)

    def update(self):
        self.rect.x -= 5


if __name__ == '__main__':
    if 'database.db' not in os.listdir(os.path.dirname(__file__)):
        create()
    clock = pygame.time.Clock()
    game = Menu(menu_sprites, width, height)
    game.draw_menu(screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.current_screen != 'menu':
                    x, y = event.pos
                    if 0 <= x < 400 and 500 <= y < 550:
                        print('1 вариант ответа')
                    elif 400 <= x <= 800 and 500 <= y < 550:
                        print('2 вариант ответа')
                    elif 0 <= x < 400 and 550 <= y <= 600:
                        print('3 вариант ответа')
                    elif 400 <= x <= 800 and 550 <= y <= 600:
                        print('4 вариант ответа')

            if event.type == pygame.KEYDOWN:
                for letter in ascii_lowercase:
                    if event.key == getattr(pygame, f'K_{letter}'):
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
                            screen.fill((0, 0, 0))
                            load_image(game, '1.png')
                            menu_sprites.draw(screen)
                            game.start()
                    elif game.menu[game.item] == 'Records':
                        game.show_results()
                    elif game.menu[game.item] == 'Start 2':
                        for i in range(10, 181, 10):
                            game.draw_menu(screen, i)
                            sleep(0.04)
                        i = 0
                        bg1 = Background(all_sprites, 'bg1.png', 0, 0)
                        bg2 = Background(all_sprites, 'bg2.png', 800, 0)
                        boy = Boy(all_sprites)
                        font = pygame.font.Font(None, 40)
                        scores = 0
                        probability = [1, 1, 0]
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        boy.status = 'up'
                            if bg1.rect.x == -800:
                                bg1.rect.x = 800
                            elif bg2.rect.x == -800:
                                bg2.rect.x = 800
                            i += 5
                            if i % 50 == 0:
                                if choice(probability) == 1:
                                    Coin(all_sprites, 850, choice([540, 470]))
                            all_sprites.update()
                            all_sprites.draw(screen)
                            text = font.render(f'Scores: {scores}', True, pygame.Color('yellow'))
                            screen.blit(text, (790 - text.get_width(), 20))
                            pygame.display.flip()
                            screen.fill((0, 0, 0))

                if event.key == pygame.K_ESCAPE:
                    for i in range(170, -1, -10):
                        game.draw_menu(screen, i)
                        sleep(0.1)
                if event.key == pygame.K_BACKSPACE:
                    if len(game.menu[1]) > 1:
                        game.menu[1] = game.menu[1][:-2] + '|'
                        game.draw_menu(screen)
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
