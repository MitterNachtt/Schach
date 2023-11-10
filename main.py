import pygame
import sys
import os  # Import the os module to work with file paths

pygame.init()

# Constants
SCREEN_SIZE = 800
SQUARE_SIZE = SCREEN_SIZE // 8
PIECE_SIZE_FACTOR = 0.9  # Adjust the size factor as needed
# Defining colors, change these as necessary
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
image_name = "whitePawn.svg"
image_path = os.path.join(image_folder, image_name)
piece_names = ['whitePawn', 'whiteRook', 'whiteKnight', 'whiteBishop', 'whiteQueen', 'whiteKing',
               'blackPawn', 'blackRook', 'blackKnight', 'blackBishop', 'blackQueen', 'blackKing']
for piece_name in piece_names:
    image_path = os.path.join(image_folder, f"{piece_name}.svg")
    piece_images[piece_name] = pygame.transform.scale(pygame.image.load(image_path),
                                                       (SQUARE_SIZE * PIECE_SIZE_FACTOR, SQUARE_SIZE * PIECE_SIZE_FACTOR))

selected_square = None

# Add this code before the main loop to calculate possible moves for each piece

def get_pawn_moves(square, color):
    col, row = ord(square[0]) - ord('a'), int(square[1])
    moves = []

    # Check one square forward
    if color == 'white' and row < 8:
        moves.append(f"{chr(col + ord('a'))}{row + 1}")
    elif color == 'black' and row > 1:
        moves.append(f"{chr(col + ord('a'))}{row - 1}")

    # Check two squares forward (for the initial move)
    if ((color == 'white' and row == 2) or (color == 'black' and row == 7)) and 1 <= row + 2 <= 8:
        moves.append(f"{chr(col + ord('a'))}{row + 2}")

    return moves

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

    # Draw chessboard using pixel coordinates
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK

            # Highlight the selected square
            if selected_square:
                selected_col = ord(selected_square[0]) - ord('a')
                selected_row = 8 - int(selected_square[1])
                if row == selected_row and col == selected_col:
                    pygame.draw.rect(screen, RED,
                                     (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE), 0)

            pygame.draw.rect(screen, color,
                             (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE))

            if selected_square:
                # Draw a red overlay with 50% opacity for the selected piece
                selected_col = ord(selected_square[0]) - ord('a')
                selected_row = 8 - int(selected_square[1])
                if row == selected_row and col == selected_col:
                    red_overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    red_overlay.fill((255, 0, 0, 128))  # 128 for 50% opacity
                    screen.blit(red_overlay, (chessboard[row][col][0], chessboard[row][col][1]))

    # Draw the piece on the occupied square (centered and enlarged)
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

    pygame.display.flip()




