import pygame
import sys
import os
from itertools import product


pygame.init()

# Constants
SCREEN_SIZE = 800
SQUARE_SIZE = SCREEN_SIZE // 8
PIECE_SIZE_FACTOR = 0.9
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame window
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Schach')

# Define a 2D list to represent the chessboard with pixel coordinates
chessboard = [[None for _ in range(8)] for _ in range(8)]

# Assign pixel coordinates to each square in the chessboard
for row in range(8):
    for col in range(8):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        chessboard[row][col] = (x, y)

# Keep track of occupied squares with pieces
occupied_squares = {
    'a1': 'whiteRook',
    'b1': 'whiteKnight',
    'c1': 'whiteBishop',
    'd1': 'whiteQueen',
    'e1': 'whiteKing',
    'f1': 'whiteBishop',
    'g1': 'whiteKnight',
    'h1': 'whiteRook',
    'a2': 'whitePawn',
    'b2': 'whitePawn',
    'c2': 'whitePawn',
    'd2': 'whitePawn',
    'e2': 'whitePawn',
    'f2': 'whitePawn',
    'g2': 'whitePawn',
    'h2': 'whitePawn',
    'a7': 'blackPawn',
    'b7': 'blackPawn',
    'c7': 'blackPawn',
    'd7': 'blackPawn',
    'e7': 'blackPawn',
    'f7': 'blackPawn',
    'g7': 'blackPawn',
    'h7': 'blackPawn',
    'a8': 'blackRook',
    'b8': 'blackKnight',
    'c8': 'blackBishop',
    'd8': 'blackQueen',
    'e8': 'blackKing',
    'f8': 'blackBishop',
    'g8': 'blackKnight',
    'h8': 'blackRook'
}

# Load piece images
image_folder = "images"
piece_images = {}
piece_names = ['whitePawn', 'whiteRook', 'whiteKnight', 'whiteBishop', 'whiteQueen', 'whiteKing',
               'blackPawn', 'blackRook', 'blackKnight', 'blackBishop', 'blackQueen', 'blackKing']
for piece_name in piece_names:
    image_path = os.path.join(image_folder, f"{piece_name}.svg")
    piece_images[piece_name] = pygame.transform.scale(pygame.image.load(image_path),
                                                       (SQUARE_SIZE * PIECE_SIZE_FACTOR, SQUARE_SIZE * PIECE_SIZE_FACTOR))

selected_square = None
selected_piece = None

# Add this code before the main loop to calculate possible moves for each piece
possible_moves = {}  # Define possible_moves here

def get_pawn_moves(square):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Define the direction and the number of squares to move based on the color
    color = 'white' if square in occupied_squares and 'white' in occupied_squares[square] else 'black'
    direction = 1 if turn % 2 != 0 else -1
    initial_row = 2 if turn % 2 != 0 else 7
    current_row = int(square[1])

    # Check one square forward
    forward_square = f"{square[0]}{current_row + direction}"
    if 1 <= current_row + direction <= 8 and forward_square not in occupied_squares:
        moves.append(forward_square)

    # Check two squares forward (for the initial move)
    double_forward_square = f"{square[0]}{current_row + 2 * direction}"
    if current_row == initial_row and double_forward_square not in occupied_squares:
        moves.append(double_forward_square)

    if square == selected_square:
        print(f"Possible moves for {square}: {moves}")

    return moves

def get_rook_moves(square):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Check moves to the right
    for c in range(col + 1, 8):
        move = f"{chr(c + ord('a'))}{row}"
        if move not in occupied_squares:
            moves.append(move)
        else:
            break

    # Check moves to the left
    for c in range(col - 1, -1, -1):
        move = f"{chr(c + ord('a'))}{row}"
        if move not in occupied_squares:
            moves.append(move)
        else:
            break

    # Check moves upwards
    for r in range(row - 1, -1, -1):
        move = f"{chr(col + ord('a'))}{r}"
        if move not in occupied_squares:
            moves.append(move)
        else:
            break

    # Check moves downwards
    for r in range(row + 1, 8):
        move = f"{chr(col + ord('a'))}{r}"
        if move not in occupied_squares:
            moves.append(move)
        else:
            break

    if square == selected_square:
        print(f"Possible moves for {square}: {moves}")

    return moves

from itertools import product

def get_knight_moves(square):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Define all possible knight moves relative to the current position
    possible_moves = list(product([col - 1, col + 1], [row - 2, row + 2])) + \
                     list(product([col - 2, col + 2], [row - 1, row + 1]))

    # Filter out invalid moves
    moves = [(x, y) for x, y in possible_moves if 0 <= x < 8 and 1 <= y <= 8]

    # Convert moves to square names
    moves = [f"{chr(x + ord('a'))}{y}" for x, y in moves if f"{chr(x + ord('a'))}{y}" not in occupied_squares]

    if square == selected_square:
        print(f"Possible moves for {square}: {moves}")

    return moves


def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color,
                             (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE))

def get_bishop_moves(square):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Define possible moves for a bishop
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for direction in directions:
        x, y = col, row
        while True:
            x += direction[0]
            y += direction[1]
            if 0 <= x < 8 and 1 <= y <= 8:
                new_square = f"{chr(x + ord('a'))}{y}"
                if new_square in occupied_squares:
                    break  # Stop if the bishop encounters a piece
                moves.append(new_square)
            else:
                break  # Stop if the bishop goes out of the board

    # Filter moves based on the bishop's starting square color
    moves = [move for move in moves if (ord(move[0]) - ord('a') + int(move[1])) % 2 == (col + row) % 2]

    if square == selected_square:
        print(f"Possible moves for {square}: {moves}")

    return moves

def get_queen_moves(square):
    rook_moves = get_rook_moves(square)
    bishop_moves = get_bishop_moves(square)
    queen_moves = rook_moves + bishop_moves

    if square == selected_square:
        print(f"Possible moves for {square}: {queen_moves}")

    return queen_moves
def get_king_moves(square):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Define all possible king moves relative to the current position
    king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for move in king_moves:
        new_col, new_row = col + move[0], row + move[1]
        new_square = f"{chr(new_col + ord('a'))}{new_row}"

        # Check if the move is within the board boundaries
        if 0 <= new_col < 8 and 1 <= new_row <= 8 and new_square not in occupied_squares:
            moves.append(new_square)

    if square == selected_square:
        print(f"Possible moves for {square}: {moves}")

    return moves

def draw_pieces():
    for row in range(8):
        for col in range(8):
            square_name = chr(ord('a') + col) + str(8 - row)
            if square_name in occupied_squares:
                piece_name = occupied_squares[square_name]
                image = piece_images.get(piece_name)
                if image:
                    image_rect = image.get_rect(
                        center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    screen.blit(image, image_rect)

def draw_highlights():
    for row in range(8):
        for col in range(8):
            square_name = chr(ord('a') + col) + str(8 - row)
            if selected_square:
                selected_col = ord(selected_square[0]) - ord('a')
                selected_row = 8 - int(selected_square[1])
                if row == selected_row and col == selected_col:
                    pygame.draw.rect(screen, RED,
                                     (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE), 0)
                elif square_name in possible_moves.get(selected_square, []):
                    # Create a surface with an alpha channel
                    green_highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    # Set the alpha value to 128 for 50% transparency
                    green_highlight_surface.fill((0, 255, 0, 128))
                    screen.blit(green_highlight_surface, (chessboard[row][col][0], chessboard[row][col][1]))

# Main game loop
turn = 1  # 1 for white, 2 for black
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the coordinates of the mouse click
            mouseX, mouseY = event.pos

            # Determine the selected square based on the mouse click
            selected_col = mouseX // SQUARE_SIZE
            selected_row = mouseY // SQUARE_SIZE
            current_selected_square = f"{chr(ord('a') + selected_col)}{8 - selected_row}"

            if selected_square is None:
                # First click - select the piece
                selected_piece = occupied_squares.get(current_selected_square, None)
                if selected_piece:
                    selected_square = current_selected_square
                    if 'Rook' in selected_piece:
                        possible_moves[selected_square] = get_rook_moves(selected_square)
                    if 'Knight' in selected_piece:
                        possible_moves[selected_square] = get_knight_moves(selected_square)
                    elif 'Bishop' in selected_piece:
                        possible_moves[selected_square] = get_bishop_moves(selected_square)
                    elif 'Queen' in selected_piece:
                        possible_moves[selected_square] = get_queen_moves(selected_square)
                    elif 'King' in selected_piece:
                        possible_moves[selected_square] = get_king_moves(selected_square)
                    else:
                        possible_moves[selected_square] = get_pawn_moves(selected_square)
                else:
                    selected_piece = None  # Reset selected_piece if no piece is clicked
            elif current_selected_square in possible_moves.get(selected_square, []):
                # Second click - move the piece to the new square
                occupied_squares[current_selected_square] = selected_piece
                del occupied_squares[selected_square]
                selected_square = None
                selected_piece = None
                turn += 1  # Update the turn
            elif current_selected_square == selected_square:
                # Deselect by clicking on the same square again
                selected_square = None
                selected_piece = None

    # Draw chessboard using pixel coordinates
    draw_chessboard()

    # Draw highlights
    draw_highlights()

    # Draw the piece on the occupied square (centered and enlarged)
    draw_pieces()

    pygame.display.flip()