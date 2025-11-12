import math

# ----- Game functions -----

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def is_moves_left(board):
    return any(' ' in row for row in board)

# ----- Minimax algorithm -----

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif not is_moves_left(board):
        return 0

    if is_maximizing:  # AI's turn
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, False)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
        return best_score
    else:  # Human's turn
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, True)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
        return best_score

def find_best_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# ----- Game loop -----

def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic Tac Toe!")
    print("You are 'O' and the AI is 'X'")
    print_board(board)

    while True:
        # Human move
        move = input("Enter your move (row and column: 1 1 for top-left): ").split()
        if len(move) != 2:
            print("Invalid input, try again.")
            continue
        i, j = int(move[0]) - 1, int(move[1]) - 1
        if board[i][j] != ' ':
            print("That spot is taken! Try again.")
            continue
        board[i][j] = 'O'

        print_board(board)
        if check_winner(board) == 'O':
            print("You win! 🎉")
            break
        if not is_moves_left(board):
            print("It's a draw!")
            break

        # AI move
        print("AI is thinking...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = 'X'
        print_board(board)

        if check_winner(board) == 'X':
            print("AI wins! 🤖")
            break
        if not is_moves_left(board):
            print("It's a draw!")
            break

# Run the game
if __name__ == "__main__":
    play_game()
