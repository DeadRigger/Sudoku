from sudoku import *
from menu import Menu

# Event
POS_DOWN = (0, 0)


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
                    if m.open:
                        if (35, 25) <= event.pos <= (75, 55):
                            m.hide()
                        else:
                            if m.change_level(event.pos):
                                restart()
                            else:
                                m.hide()
                    else:
                        if (35, 25) <= event.pos <= (75, 55):
                            m.show()

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


def restart():
    global s
    global m
    s = Sudoku()
    m = Menu(game_display)

    game_display.fill(WHITE)

    m.display()
    display_footer()
    s.show(game_display)


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
