from string import ascii_lowercase
import pygame
from time import sleep


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.second = '|'
        self.item = 2

    def draw_menu(self, screen):
        if self.item < 2:
            self.item = 2
        elif self.item > 3:
            self.item = 3
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        menu = ['Insert your name: ', self.second, 'Start', 'About']
        delta = 0
        for i, row in enumerate(menu):
            if self.item == i:
                text = font.render(row, True, (180, 0, 0))
            else:
                text = font.render(row, True, (0, 180, 0))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = self.width // 2 - text_w // 2
            text_y = self.height // 4 - text_h // 2 + delta
            screen.blit(text, (text_x, text_y))
            delta += 60
            # pygame.draw.rect(screen, (0, 250, 0), pygame.Rect(30, 30, 200, 200), 1)


if __name__ == '__main__':
    pygame.init()
    game = Menu(600, 600)
    screen = pygame.display.set_mode((game.width, game.height))
    pygame.display.set_caption('Menu')
    running = True
    clock = pygame.time.Clock()
    game.draw_menu(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.item += 1
                    game.draw_menu(screen)
                if event.key == pygame.K_UP:
                    game.item += -1
                    game.draw_menu(screen)
                for letter in ascii_lowercase:
                    if event.key == getattr(pygame, f'K_{letter}'):
                        game.second = game.second[:-1] + f'{letter}|'
                        game.draw_menu(screen)
                        t = 0
                        break
            # game.draw_menu(screen)
            # sleep(.5)
            # if '|' in game.second:
            #     game.second = game.second.replace('|', ' ')
            # else:
            #     game.second = game.second.replace(' ', '|')
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()
