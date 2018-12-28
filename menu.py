import pygame
from constants import *


class Menu:
    def __init__(self, screen):
        self.open = False
        self.screen = screen
        self.menu = pygame.Surface((576, 100))
        self.menu.fill(WHITE)

        pygame.font.init()
        font = pygame.font.SysFont(font_name, 25)
        self.new = font.render('New', False, BLACK)
        self.easy = font.render('Easy', False, BLACK)
        self.medium = font.render('Medium', False, BLACK)
        self.hard = font.render('Hard', False, BLACK)

    def display(self):
        self.menu.blit(self.new, (35, 25))
        pygame.draw.rect(self.menu, GRAY,
                         (self.new.get_rect()[0] + 35, self.new.get_rect()[1] + 25,
                          self.new.get_rect()[2], self.new.get_rect()[3]), 1)
        self.screen.blit(self.menu, (0, 0))

    def show(self):
        # Draw item easy level
        pos_x = 35 + self.new.get_rect()[2] + 5
        pos_y = 25
        self.menu.blit(self.easy, (pos_x, pos_y))
        pygame.draw.rect(self.menu, GRAY, (pos_x, pos_y, self.easy.get_rect()[2], self.easy.get_rect()[3]), 1)

        # Draw item medium level
        pos_x += self.easy.get_rect()[2] + 5
        self.menu.blit(self.medium, (pos_x, pos_y))
        pygame.draw.rect(self.menu, GRAY, (pos_x, pos_y, self.medium.get_rect()[2], self.medium.get_rect()[3]), 1)

        # Draw item hard level
        pos_x += self.medium.get_rect()[2] + 5
        self.menu.blit(self.hard, (pos_x, pos_y))
        pygame.draw.rect(self.menu, GRAY, (pos_x, pos_y, self.hard.get_rect()[2], self.hard.get_rect()[3]), 1)

        self.open = True
        self.display()
        pygame.display.update()

    def hide(self):
        self.menu.fill(WHITE)
        self.open = False
        self.display()
        pygame.display.update()

    def change_level(self, pos_click):
        global difficulty
        pos = (35 + self.new.get_rect()[2] + 5, 25)
        print('Rect easy: ' + str(pos) + str((pos[0] + self.easy.get_rect()[2], pos[1] + self.easy.get_rect()[3])) +
              ', click position: ' + str(pos_click))
        if pos <= pos_click <= (pos[0] + self.easy.get_rect()[2], pos[1] + self.easy.get_rect()[3]):
            difficulty = 'easy'
            return True

        pos = (pos[0] + self.easy.get_rect()[2] + 5, pos[1])
        print('Rect medium: ' + str(pos) + str((pos[0] + self.easy.get_rect()[2], pos[1] + self.easy.get_rect()[3])) +
              ', click position: ' + str(pos_click))
        if pos <= pos_click <= (pos[0] + self.medium.get_rect()[2], pos[1] + self.medium.get_rect()[3]):
            difficulty = 'medium'
            return True

        pos = (pos[0] + self.medium.get_rect()[2] + 5, pos[1])
        print('Rect hard: ' + str(pos) + str((pos[0] + self.easy.get_rect()[2], pos[1] + self.easy.get_rect()[3])) +
              ', click position: ' + str(pos_click))
        if pos <= pos_click <= (pos[0] + self.hard.get_rect()[2], pos[1] + self.hard.get_rect()[3]):
            difficulty = 'hard'
            return True

        return False
