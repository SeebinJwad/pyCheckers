import pygame

pygame.init()
pygame.display.set_caption('Checkers')
gameDisplay = pygame.display.set_mode((400, 400))

light_black = (50, 50, 50)
black = (0, 0, 0)

white = (255, 255, 255)
yellow = (245, 245, 5)

light_red = (220, 0, 0)
red = (180, 0, 0)

dark_brown = (145, 95, 40)
light_brown = (230, 200, 170)

move_color = "w"

board = [['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
         [' ', 'b', ' ', 'b', ' ', 'b', ' ', 'b'],
         ['b', ' ', 'b', ' ', 'b', ' ', 'b', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', 'w', ' ', 'w', ' ', 'w', ' ', 'w'],
         ['w', ' ', 'w', ' ', 'w', ' ', 'w', ' '],
         [' ', 'w', ' ', 'w', ' ', 'w', ' ', 'w']]


def switch_color():
    global move_color
    if move_color == 'w':
        move_color = 'b'
    else:
        move_color = 'w'


def flip_board():
    global board
    flipped_board = []
    for x in range(8):
        flipped_board.append(board[len(board) - (x + 1)])
    board = flipped_board


def draw_board():
    tile_color = dark_brown
    # background is black so only white squares need to be drawn
    # every other row is displaced to the right for checker pattern
    # draws the white squares on the board
    for y in range(8):
        for x in range(8):
            if y % 2 == 0:
                if x % 2 == 0:
                    pygame.draw.rect(gameDisplay, tile_color, [x * 50, y * 50, 50, 50])

    # draws the white squares on the board offset right
    for y in range(8):
        for x in range(8):
            if y % 2 != 0:
                if x % 2 != 0:
                    pygame.draw.rect(gameDisplay, tile_color, [x * 50, y * 50, 50, 50])

    # pygame.draw.circle(gameDisplay, black, [25 + 100, 25], 15)


def gameLoop():
    # creates list of x and y positions
    x_pos = []
    y_pos = []
    for y in range(8):
        for x in range(8):
            x_pos.append((x * 50) + 25)
            y_pos.append((y * 50) + 25)
    # print(x_pos)
    # print(y_pos)

    global move_color

    # shortened y_pos list which is just the x_pos list
    short_y = x_pos

    # which piece is being selected
    selection = []

    bg_color = light_brown
    gameOver = False

    while not gameOver:

        mouse_pos = pygame.mouse.get_pos()

        gameDisplay.fill(bg_color)
        draw_board()

        selection_true_x = False
        selection_true_y = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    for x in board:
                        print(x)
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the piece is selected and the selection to move is the correct direction of the piece (-7 going up)
                # king functionality somehow

                possible_x_pos = []
                possible_y_pos = []

                for x in range(8):
                    if mouse_pos[0] >= x_pos[x] - 25:
                        possible_x_pos.append(x)

                for y in range(8):
                    if mouse_pos[1] <= y_pos[y * 8] + 25:
                        possible_y_pos.append(y)

                # the max of all possible x and min of all y is your selected position
                selected_x_pos = max(possible_x_pos)
                selected_y_pos = min(possible_y_pos)

                print("(" + str(selected_x_pos + 1) + ", " + str(selected_y_pos + 1) + ")", end=" ")

                # if board is equal to white while whites turn and black during blacks turn
                if board[selected_y_pos][selected_x_pos] == move_color:
                    if len(selection) != 0:
                        selection[0], selection[1] = selected_x_pos, selected_y_pos
                    else:
                        selection.append(selected_x_pos)
                        selection.append(selected_y_pos)

                    print("selection on " + str(selection[0] + 1) + ", " + str(selection[1] + 1) + "\n")

                if board[selected_y_pos][selected_x_pos] != ' ':
                    print(board[selected_y_pos][selected_x_pos])
                else:
                    print('empty' + "\n")
                    # move_color = ''
                    # MOVE MADE HERE
                    if len(selection) != 0:
                        # MOVE CODE

                        final_x = selected_x_pos
                        final_y = selected_y_pos

                        original_x = selection[0]
                        original_y = selection[1]

                        # difference in position between original and final
                        diff_in_pos = (final_x + final_y * 8) - (original_x + original_y * 8)

                        # white can only -9 -7
                        # black can only 9 7
                        move_color = board[original_y][original_x]
                        print(diff_in_pos)
                        # if color is white and it is moving up
                        if (move_color == "w" and (diff_in_pos == -9 or diff_in_pos == -7)) or\
                                (move_color == "b" and (diff_in_pos == 9 or diff_in_pos == 7)):

                            board[original_y][original_x] = " "
                            board[final_y][final_x] = move_color
                            print(move_color)
                            switch_color()

                            # FLIPS THE BOARD AFTER EACH MOVE OR BY CLICKING EMPTY SQUARE
                            # flip_board()

                            print("(" + str(original_x + 1) + ", " + str(original_y + 1) + ") -> (" + str(final_x + 1) +
                                  ", " + str(final_y + 1) + ")")
                            # if you moved two diagonal
                            print(str(final_x) + " + " + str(final_y) + " - " + str(original_x) + " + " + str(original_y))
                            print((final_x + final_y * 8) - (original_x + original_y * 8))

                        # capture hop event handler
                        # issue is that it deletes the position but doesnt replace the moved piece
                        if abs(diff_in_pos) == 14:

                            if final_x > original_x:
                                # up right
                                board[original_y - 1][original_x + 1] = " "
                            else:
                                # down left
                                board[original_y + 1][original_x - 1] = " "
                            # switches the color to negate the previous color switch, so same color makes another move

                            board[original_y][original_x] = " "
                            board[final_y][final_x] = move_color
                            print(move_color)

                        elif abs(diff_in_pos) == 18:

                            if final_y < original_y:
                                # up left
                                board[original_y - 1][original_x - 1] = " "

                            else:
                                # down right
                                board[original_y + 1][original_x + 1] = " "

                            board[original_y][original_x] = " "
                            board[final_y][final_x] = move_color
                            print(move_color)

        for y in range(8):
            for x in range(8):

                if len(selection) > 0:
                    # if the selection is true for the x selected
                    selection_true_x = (selection[0] == x)
                    selection_true_y = (selection[1] == y)

                # if the board has a b for black piece on it
                if board[y][x] == "b":
                    # draw a circle there
                    # if this piece was selected, change the outline color to yellow
                    if len(selection) > 0 and selection_true_x and selection_true_y:
                        pygame.draw.circle(gameDisplay, yellow, [x_pos[x], short_y[y]], 15)
                    else:
                        pygame.draw.circle(gameDisplay, black, [x_pos[x], short_y[y]], 15)

                    pygame.draw.circle(gameDisplay, light_black, [x_pos[x], short_y[y]], 12)

                # if the board has a w for white piece on it
                if board[y][x] == "w":
                    # draw a circle there
                    if len(selection) > 0 and selection_true_x and selection_true_y:
                        pygame.draw.circle(gameDisplay, yellow, [x_pos[x], short_y[y]], 15)
                    else:
                        pygame.draw.circle(gameDisplay, red, [x_pos[x], short_y[y]], 15)

                    pygame.draw.circle(gameDisplay, light_red, [x_pos[x], short_y[y]], 12)

        count_b = 0
        count_w = 0

        for x in board:
            for y in x:
                if y == "b":
                    count_b += 1
                elif y == "w":
                    count_w += 1

        if count_b == 0:
            print("RED WINS")
            gameOver = True
        elif count_w == 0:
            print("BLACK WINS")
            gameOver = True

        pygame.display.update()
    pygame.quit()
    quit()


gameLoop()
