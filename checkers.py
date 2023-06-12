import pygame

pygame.init()

screen = pygame.display.set_mode((850, 850))
board = pygame.image.load("static/images/board.svg")
red_pawn = pygame.image.load("static/images/red_pawn.png")
black_pawn = pygame.image.load("static/images/black_pawn.png")

checker_positions = [
    (125, 25),
    (325, 25),
    (525, 25),
    (725, 25),
    (25, 125),
    (225, 125),
    (425, 125),
    (625, 125),
    (125, 225),
    (325, 225),
    (525, 225),
    (725, 225),
    (25, 525),
    (225, 525),
    (425, 525),
    (625, 525),
    (125, 625),
    (325, 625),
    (525, 625),
    (725, 625),
    (25, 725),
    (225, 725),
    (425, 725),
    (625, 725),
]

while True:
    screen.fill(color="#808080")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.blit(board, (25, 25))
    for i in range(len(checker_positions)):
        if i < 12:
            screen.blit(red_pawn, checker_positions[i])
        else:
            screen.blit(black_pawn, checker_positions[i])
    pygame.display.update()
