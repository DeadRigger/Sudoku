from pygame.locals import *

from sudoku import *

# Constants and variable

# Event
POS_DOWN = (0, 0)

# Game
FPS = 24
display_width = 600
display_height = 800
name_app = 'Sudoku'


# Functions
def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (
                event.type == KEYDOWN and (
                event.key == K_ESCAPE or
                event.key == K_q)
        ):
            pygame.quit()
            quit()

        elif event.type == KEYDOWN:
            if s.hint_ceil is not None:
                if 0 < event.key - 48 < 10:
                    number = event.key - 48
                    s.changeNumber(game_display, s.hint_ceil, number)

        elif event.type == MOUSEBUTTONDOWN:
            global POS_DOWN
            POS_DOWN = event.pos
            posy1 = s.pos_y
            posy2 = s.pos_y + s.height
            if event.pos[1] < posy1:
                pass
            elif posy1 <= event.pos[1] <= posy2:
                pass
            elif event.pos[1] > posy2:
                pass

        elif event.type == MOUSEBUTTONUP:
            if event.pos == POS_DOWN:
                posy1 = s.pos_y
                posy2 = s.pos_y + s.height
                if event.pos[1] < posy1:
                    if (35, 25) <= event.pos <= (75, 55):
                        if m.open:
                            m.hide()
                            pygame.display.update()
                        else:
                            m.show()
                            pygame.display.update()
                elif posy1 <= event.pos[1] <= posy2:
                    s.show(game_display, POS_DOWN)
                elif event.pos[1] > posy2:
                    number = int((event.pos[0] - 12) / 64 + 1)
                    if number == int((POS_DOWN[0] - 12) / 64 + 1) and s.hint_ceil is not None:
                        s.changeNumber(game_display, s.hint_ceil, number)


def display_footer():
    digits = pygame.Surface((576, 100))
    digits.fill(WHITE)
    for i in range(9):
        text_button(digits, (i * 64 + 25, 10), str(i + 1))

    game_display.blit(digits, (12, 700))


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

    def hide(self):
        self.menu.fill(WHITE)
        self.open = False
        self.display()


# Initialization objects pygame
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(name_app)
clock = pygame.time.Clock()
s = Sudoku()
m = Menu(game_display)

game_display.fill(WHITE)

m.display()
display_footer()
s.show(game_display)

# Main loop
while True:
    # Delay
    clock.tick(FPS)

    # Event handler
    event_handler()
