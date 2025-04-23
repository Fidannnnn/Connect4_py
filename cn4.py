# this code belongs to Ismayilova Asiman, Jafarzade Madina, Ashrafova Gunay and Alizada Fidan

import random, math  # Import the random and math module for generating random moves
EMPTY, YELLOW, RED = 0, 1, 2  # Constants representing the different states of cells in the grid
grid = [[EMPTY for _ in range(7)] for _ in range(6)]  # Initialize a 6x7 grid with all cells set to EMPTY


def clearing_grid():
    """Clears the Connect Four grid, resetting all cells to EMPTY."""
    for row in grid:
        for i in range(len(row)):
            row[i] = EMPTY

def move_possibility(column, grid):
    """Checks if a move is possible in the specified column."""
    return grid[0][column] == EMPTY


def current_grid():
    """Displays the current state of the Connect Four grid with numbers on all sides."""
    # Print the top row with column numbers
    print("  1 2 3 4 5 6 7")

    # Print the grid with row numbers on the left and right sides
    for i, row in enumerate(grid, start=1):
        print(f"{7-i}", end=' ')
        for cell in row:
            if cell == YELLOW:
                print('o', end=' ')
            elif cell == RED:
                print('*', end=' ')
            else:
                print('.', end=' ')
        print(f"{7-i}")

    # Print the bottom row with column numbers
    print("  1 2 3 4 5 6 7")
    if longest_alignment(grid) == 0:
        print("No winning move possible.")

    elif move_possibility(i, grid):
        print("Recommended column : " + str(random_move(grid)))
    else:
        print("Recommended column : " + str(int(longest_alignment(grid))))

def random_move(grid):
    """Selects a column to play at random."""
    possible_moves = [col for col in range(7) if grid[0][col] == EMPTY]
    return random.choice(possible_moves)

def disc(column, disc, grid):
    """places disc into given column of the grid."""
    for row in reversed(grid):
        if row[column] == EMPTY:
            row[column] = disc
            return True
    return False

def check_alignment(disc, grid_to_check=None):
    """Verifies whether the designated disc type achieves a winning state on the grid.."""
    if grid_to_check is None:
        grid_to_check = grid
    # Check horizontal lines
    for row in range(6):
        for col in range(4):
            if all(grid_to_check[row][col + i] == disc for i in range(4)):
                return True

    # Check vertical lines
    for col in range(7):
        for row in range(3):
            if all(grid_to_check[row + i][col] == disc for i in range(4)):
                return True

    # Check diagonal (down-right) lines
    for row in range(3):
        for col in range(4):
            if all(grid_to_check[row + i][col + i] == disc for i in range(4)):
                return True

    # Check diagonal (up-right) lines
    for row in range(3, 6):
        for col in range(4):
            if all(grid_to_check[row - i][col + i] == disc for i in range(4)):
                return True

    return False

def player_move():
    """Gets a valid column input from the player."""
    while True:
        try:
            column = int(input("Choose a column (1-7): ")) - 1
            if 0 <= column < 7:
                return column
            else:
                print("Column must be between 1 and 7.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def evaluate_column(grid, column):
    """Evaluates the potential alignment length for a given column."""
    temp_grid = [row.copy() for row in grid]
    disc(column, RED, temp_grid)

    # Count the length of the alignment for the given column
    alignment_lengths = [count_alignment(temp_grid, row, column) for row in range(6)]

    # Return the maximum alignment length
    return max(alignment_lengths)

def count_alignment(grid, row, col):
    """Counts the length of the alignment for a given position."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    max_length = 0

    for dir in directions:
        length = 1
        for i in range(1, 4):
            r, c = row + i * dir[0], col + i * dir[1]
            if 0 <= r < 6 and 0 <= c < 7 and grid[r][c] == RED:
                length += 1
            else:
                break

        for i in range(1, 4):
            r, c = row - i * dir[0], col - i * dir[1]
            if 0 <= r < 6 and 0 <= c < 7 and grid[r][c] == RED:
                length += 1
            else:
                break

        max_length = max(max_length, length)

    return max_length

def longest_alignment(grid):
    """Provides advice on the column that allows the longest alignment."""
    possible_moves = [col for col in range(7) if move_possibility(col, grid)]

    # Sorts the columns based on the length of alignment they can achieve
    sorted_moves = sorted(possible_moves, key=lambda col: evaluate_column(grid, col), reverse=True)

    # Returns the column that has the longest potential alignment
    return sorted_moves[0]

def computer_move(grid):
    """Generates a smart move for the computer using the minimax algorithm with alpha-beta pruning."""
    def is_move_possible(column, grid):
        """Checks if a move is possible in the specified column."""
        return grid[0][column] == EMPTY

    def drop_disc(column, color, grid):
        """puts a disc into the given column of the grid."""
        for row in range(5, -1, -1):
            if grid[row][column] == EMPTY:
                grid[row][column] = color
                break

    def is_terminal_node(grid):
        """Checks if the current grid is a terminal node."""
        return check_alignment(YELLOW, grid) or check_alignment(RED, grid) or all(grid[0][col] != EMPTY for col in range(7))

    def evaluate_window(window, color):
        """Evaluates the score for given cells in the grid."""
        score = 0
        opp_color = YELLOW if color == RED else RED

        if window.count(color) == 4:
            score += 100
        elif window.count(color) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(color) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_color) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(grid, color):
        """Scores the overall position of the grid for a given color."""
        score = 0

        # Score center column
        center_array = [int(i == 3) for i in range(7)]
        center_count = sum([1 for col in grid for i, cell in enumerate(col) if cell == color and center_array[i] == 1])
        score += center_count * 3

        # Score horizontal
        for row in grid:
            for col in range(4):
                window = row[col:col + 4]
                score += evaluate_window(window, color)

        # Score vertical
        for col in range(7):
            for row in range(3):
                window = [grid[row + i][col] for i in range(4)]
                score += evaluate_window(window, color)

        # Score diagonal
        for row in range(3):
            for col in range(4):
                window = [grid[row + i][col + i] for i in range(4)]
                score += evaluate_window(window, color)

        for row in range(3, 6):
            for col in range(4):
                window = [grid[row - i][col + i] for i in range(4)]
                score += evaluate_window(window, color)

        return score

    def minimax(depth, alpha, beta, maximizing_player, grid):
        """Determines the best move."""
        valid_moves = [col for col in range(7) if is_move_possible(col, grid)]

        if depth == 0 or is_terminal_node(grid):
            return None, score_position(grid, RED)

        if maximizing_player:
            value = -math.inf
            best_move = random.choice(valid_moves)
            for col in valid_moves:
                temp_grid = [row.copy() for row in grid]
                drop_disc(col, RED, temp_grid)
                _, child_score = minimax(depth - 1, alpha, beta, False, temp_grid)
                if child_score > value:
                    value = child_score
                    best_move = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_move, value
        else:
            value = math.inf
            best_move = longest_alignment(grid)
            for col in valid_moves:
                temp_grid = [row.copy() for row in grid]
                drop_disc(col, YELLOW, temp_grid)
                _, child_score = minimax(depth - 1, alpha, beta, True, temp_grid)
                if child_score < value:
                    value = child_score
                    best_move = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_move, value

    depth = 4  # Adjust the depth of the search as needed
    best_move, _ = minimax(depth, -math.inf, math.inf, True, grid)

    return best_move

def play_game(starting_player):
    """function to play onr game."""
    clearing_grid()
    current_player = starting_player

    while True:
        current_grid()
        if current_player == YELLOW:
            print("Player Yellow's turn.")
            column = player_move()
        else:
            print("Computer (Red) is making a move.")
            if current_player == RED:
                # Use the minimax algorithm
                column = computer_move(grid)
            else:
                # Use advice for the longest alignment
                column = longest_alignment(grid)

        if not move_possibility(column, grid):
            print("Column is full. Try another one.")
            continue

        disc(column, current_player, grid)

        if check_alignment(current_player):
            current_grid()
            winner = 'Player Yellow' if current_player == YELLOW else 'Computer (Red)'
            print(f"{winner} wins!")
            break

        if all(grid[0][col] != EMPTY for col in range(7)):
            print("The game is a draw.")
            break

        current_player = RED if current_player == YELLOW else YELLOW

def the_game():
    """Manages multiple games, changing the starting player."""
    starting_player = YELLOW
    while True:
        play_game(starting_player)
        starting_player = RED if starting_player == YELLOW else YELLOW
        if input("if u want to play again enter y? ").lower() != 'y':
            break

the_game() # Start playing games
