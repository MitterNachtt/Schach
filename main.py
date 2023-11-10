import pygame
import sys
import os

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

# Add this code before the main loop to calculate possible moves for each piece

def get_pawn_moves(square, color):
    moves = []

    # Define the direction and the number of squares to move based on the color
    direction = 1 if color == 'white' else -1
    initial_row = 2 if color == 'white' else 7
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


    return moves

def draw_chessboard():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color,
                             (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE))

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
                    pygame.draw.rect(screen, GREEN,
                                     (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE), 0)

# Add a dictionary to store possible moves for each piece
possible_moves = {}
# Calculate and store possible moves for each pawn
for square, piece in occupied_squares.items():
    color = piece.split()[0]
    if 'Pawn' in piece:
        possible_moves[square] = get_pawn_moves(square, color)
    # Add similar logic for other pieces



# Main game loop
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

            if selected_square == current_selected_square:
                # Toggle selection if clicking on the same square
                selected_square = None
            else:
                selected_square = current_selected_square

                # Print possible moves for the selected piece (for debugging)
                print(f"Possible moves for {selected_square}: {possible_moves.get(selected_square, [])}")

    # Draw chessboard using pixel coordinates
    draw_chessboard()

    # Draw highlights
    draw_highlights()

    # Draw the piece on the occupied square (centered and enlarged)
    draw_pieces()

    pygame.display.flip()