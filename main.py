import pygame
import sys
import os  # Import the os module to work with file paths

pygame.init()

# Constants
SCREEN_SIZE = 800
SQUARE_SIZE = SCREEN_SIZE // 8
PIECE_SIZE_FACTOR = 0.9  # Adjust the size factor as needed
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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



# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw chessboard using pixel coordinates
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color,
                             (chessboard[row][col][0], chessboard[row][col][1], SQUARE_SIZE, SQUARE_SIZE))

            # Draw the piece on the occupied square (centered and enlarged)
            square_name = chr(ord('a') + col) + str(8 - row)
            if square_name in occupied_squares:
                piece_name = occupied_squares[square_name]
                image = piece_images.get(piece_name)
                if image:
                    image_rect = image.get_rect(
                        center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                    screen.blit(image, image_rect)

    pygame.display.flip()
