import pygame
from sudoku_generator import*


bg_color = (255,255,255)


def place(window, pos,board,original):
    # Places numbers on the board
    font = pygame.font.SysFont('Helvetica', 30)
    x, y = pos[1], pos[0]

    while True:
        for event in pygame.event.get():
            # if user has pressed quit button, quit the window
            if (event.type == pygame.QUIT):
                pygame.quit()
                return

            # if user wants to enter a value
            if event.type == pygame.KEYDOWN:
                # case 1: trying to modify original value
                if original[x - 1][y - 1] != 0:  # since the blank values are zeros
                    return

                # case 2: Trying to edit previously entered digit
                # 0 is mapped to 48 in ascii nomenclature so here we are checking with 0
                if (event.key == 48):
                    # erasing previosly entered value in backend
                    board[x - 1][y - 1] = event.key - 48
                    # erasing previosly entered value on the screen
                    pygame.draw.rect(window, bg_color, (y * 50 + 5, x * 50 + 5, 50 - 10, 50 - 10))

                    # again displaying updated window
                    pygame.display.update()
                    return

                # case 3: Trying to enter a value in a blank cell
                if (0 < event.key - 48 < 10):  # valid input
                    # erasing previosly entered value on the screen
                    pygame.draw.rect(window, bg_color, (y * 50 + 5, x * 50 + 5, 50 - 10, 50 - 10))

                    val = font.render(str(event.key - 48), True, (0,0,0))
                    window.blit(val, (y * 50 + 15, x * 50 + 5))

                    board[x - 1][y - 1] = event.key - 48

                    # again displaying updated window
                    pygame.display.update()
                    return

def draw_start_screen(screen,screen_width,screen_height):
        # initialize fonts
        title_font = pygame.font.Font(None, 70)
        button_font = pygame.font.Font(None, 40)

        # BG color
        screen.fill((125, 199, 52))

        # title
        title_surface = title_font.render('Sudoku', 0, (0, 0, 0))
        title_rectangle = title_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        screen.blit(title_surface, title_rectangle)

        # subtitle
        subtitle_surface = button_font.render('Choose Your Puzzle:', 0, (0, 0, 0))
        subtitle_rectangle = subtitle_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(subtitle_surface, subtitle_rectangle)

        # button text
        easy_text = button_font.render("Easy", 0, (255, 255, 255))
        medium_text = button_font.render("Medium", 0, (255, 255, 255))
        hard_text = button_font.render("Hard", 0, (255, 255, 255))

        # button BG color and text
        easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
        easy_surface.fill((0, 0, 0))
        easy_surface.blit(easy_text, (10, 10))

        medium_surface = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
        medium_surface.fill((0, 0, 0))
        medium_surface.blit(medium_text, (10, 10))

        hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
        hard_surface.fill((0, 0, 0))
        hard_surface.blit(hard_text, (10, 10))

        # button rectangle
        easy_rectangle = easy_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 25))
        medium_rectangle = medium_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        hard_rectangle = hard_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 175))

        # draw buttons
        screen.blit(easy_surface, easy_rectangle)
        screen.blit(medium_surface, medium_rectangle)
        screen.blit(hard_surface, hard_rectangle)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_rectangle.collidepoint(event.pos):
                        return "easy"
                    elif medium_rectangle.collidepoint(event.pos):
                        return "medium"
                    elif hard_rectangle.collidepoint(event.pos):
                        return "hard"

            pygame.display.update()

def draw_grid(screen):
    # Draws the Grid to the screen
    for i in range(0, 10):
        if i % 3 == 0:
            # every third line is bold to
            pygame.draw.line(screen, (0,0,0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(screen, (0,0,0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)

        else:
            # draw.line(window, color, start coodinate, end coodinate, width)
            # vertical lines
            pygame.draw.line(screen, (0,0,0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
            # horizontal lines
            pygame.draw.line(screen, (0,0,0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)


def main():

    pygame.init()
    screen_width = 550
    screen_height = 550
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Sudoku')
    screen.fill(bg_color)
    font = pygame.font.SysFont('Helvetica', 50)

    selected_difficulty = draw_start_screen(screen,screen_width,screen_height)

    if selected_difficulty == "easy":
        pygame.display.set_caption("Sudoku - Easy")
        board = generate_sudoku(81,30)

    elif selected_difficulty == "medium":
        pygame.display.set_caption("Sudoku - Medium")
        board = generate_sudoku(81,40)

    elif selected_difficulty == "hard":
        pygame.display.set_caption("Sudoku - Hard")
        board = generate_sudoku(81,50)
    screen.fill(bg_color)
    draw_grid(screen)

    # making a copy of the board beacuse we will be changing the values of the board
    # so at last it will help in checking the correctness
    original = [[board[i][j] for j in range(len(board[0]))] for i in range(len(board))]

    # placing digits on the Sudoku board
    for x in range(0, len(board[0])):
        for y in range(0, len(board[0])):

            # if it is a digit is between 1 and 9
            if (board[x][y] > 0 and board[x][y] < 10):
                # text rendering
                value = font.render(str(board[x][y]), True, (100, 100, 200))
                # print the digit on Sudoku Board
                screen.blit(value, ((y + 1) * 50 + 15, (x + 1) * 50 + 5))

    # again displaying updated window
    pygame.display.update()

    while True:
        for event in pygame.event.get():

            # Mouse button click on cell
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # obtaining the coordinate from Mouse button click
                coord = pygame.mouse.get_pos()
                # floor division by 50 to place digit in cell
                place(screen, (coord[0] // 50, coord[1] // 50),board,original)

            # allows user to quit
            if (event.type == pygame.QUIT):
                pygame.quit()
                return




if __name__ == '__main__':
    main()