import math

def print_board(board):
    """Display the Tic Tac Toe board"""
    for row in board:
        print(" | ".join(row))
        print("-" * 5)


def check_winner(board, player):
    """Check all winning conditions for a player"""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_full(board):
    """Check if the board is full"""
    return all(cell != " " for row in board for cell in row)


def minimax(board, depth, is_maximizing):
    """Minimax algorithm for optimal AI moves"""
    if check_winner(board, "O"):  # AI wins
        return 1
    if check_winner(board, "X"):  # Human wins
        return -1
    if is_full(board):  # Draw
        return 0

    if is_maximizing:  # AI's turn
        best_score = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False)
                    board[r][c] = " "
                    best_score = max(score, best_score)
        return best_score
    else:  # Human's turn
        best_score = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True)
                    board[r][c] = " "
                    best_score = min(score, best_score)
        return best_score


def best_move(board):
    """Find the best move for AI using minimax"""
    best_score = -math.inf
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == " ":
                board[r][c] = "O"
                score = minimax(board, 0, False)
                board[r][c] = " "
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move


def tic_tac_toe():
    """Main game loop"""
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic Tac Toe!")
    print("You are X. Computer is O.")
    print_board(board)

    while True:
        # Human turn
        print("Your turn (X).")
        try:
            row = int(input("Enter row (1-3): ")) - 1
            col = int(input("Enter column (1-3): ")) - 1
        except ValueError:
            print("Invalid input! Enter numbers between 1 and 3.")
            continue

        if row not in range(3) or col not in range(3):
            print("Invalid move! Try again.")
            continue
        if board[row][col] != " ":
            print("Cell already taken! Try again.")
            continue

        board[row][col] = "X"
        print_board(board)

        if check_winner(board, "X"):
            print("🎉 You win!")
            break
        if is_full(board):
            print("It's a Draw!")
            break

        # Computer turn
        print("Computer's turn (O)...")
        move = best_move(board)
        if move:
            board[move[0]][move[1]] = "O"
        print_board(board)

        if check_winner(board, "O"):
            print("💻 Computer wins!")
            break
        if is_full(board):
            print("It's a Draw!")
            break


# Run the game
if __name__ == "__main__":
    tic_tac_toe()