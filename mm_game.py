import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Game variables
COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PINK]
CODE_LENGTH = 4
MAX_GUESSES = 15


# Function to generate a random code
def generate_code():
    return [random.choice(COLORS) for _ in range(CODE_LENGTH)]


# Function to draw a colored circle
def draw_circle(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 20)


# Function to draw feedback pegs
def draw_feedback(x, y, correct_position, correct_color):
    for i in range(correct_position):
        pygame.draw.circle(screen, BLACK, (x + i * 25, y), 5)
    for i in range(correct_color):
        pygame.draw.circle(screen, WHITE, (x + (i + correct_position) * 25, y), 5)


# Function to draw a button
def draw_button(x, y, width, height, color, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)


# Function to get the coordinates of the last guess drawn
def get_last_guess_coordinates(num_guesses):
    y = 50 + (num_guesses - 1) * 40  # Vertical position of the last guess
    coordinates = [(75 + i * 50, y) for i in range(CODE_LENGTH)]
    return coordinates


# Main game function
# Main game function
# Main game function
# Main game function
def play_game():
    code = generate_code()
    print(code)
    guesses = []
    current_guess = []
    game_over = False
    win = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if not game_over:
                    if 50 <= x <= 350 and 650 <= y <= 700:
                        color_index = (x - 50) // 50
                        if len(current_guess) < CODE_LENGTH:
                            current_guess.append(COLORS[color_index])
                    elif 400 <= x <= 500 and 650 <= y <= 700:
                        if len(current_guess) == CODE_LENGTH:
                            guesses.append(current_guess)
                            if current_guess == code:
                                game_over = True
                                win = True
                            elif len(guesses) == MAX_GUESSES:
                                game_over = True
                            current_guess = []
                    elif 520 <= x <= 620 and 650 <= y <= 700:
                        current_guess = []
                else:
                    # Check if restart button is clicked
                    if WIDTH // 2 - 50 <= x <= WIDTH // 2 + 50 and HEIGHT - 50 <= y <= HEIGHT - 10:
                        return True  # Restart the game

        screen.fill(GRAY)

        # Draw color options
        for i, color in enumerate(COLORS):
            draw_circle(75 + i * 50, 675, color)

        # Draw submit button
        draw_button(400, 650, 100, 50, GREEN, "Submit")

        # Draw clear button
        draw_button(520, 650, 100, 50, RED, "Clear")

        # Draw guesses and feedback
        for i, guess in enumerate(guesses):
            for j, color in enumerate(guess):
                draw_circle(75 + j * 50, 50 + i * 40, color)

            correct_position = sum(1 for a, b in zip(guess, code) if a == b)
            correct_color = sum(min(guess.count(c), code.count(c)) for c in set(guess)) - correct_position
            draw_feedback(300, 50 + i * 40, correct_position, correct_color)

        # Draw current guess
        for i, color in enumerate(current_guess):
            draw_circle(75 + i * 50, 50 + len(guesses) * 40, color)

        # Draw game over message, correct code, and restart button
        if game_over:
            font = pygame.font.Font(None, 36)
            if win:
                text = font.render("You win!", True, BLACK)
            else:
                text = font.render("Game Over!", True, BLACK)
            screen.blit(text, (50, 50 + len(guesses) * 40 + 20))

            # Draw the correct code below the game over message
            text = font.render("Correct Code:", True, BLACK)
            screen.blit(text, (50, 50 + len(guesses) * 40 + 60))
            for i, color in enumerate(code):
                draw_circle(250 + i * 50, 50 + len(guesses) * 40 + 60, color)

            # Draw restart button below the correct code
            draw_button(WIDTH // 2 - 50, 50 + len(guesses) * 40 + 100, 100, 40, YELLOW, "Restart")

        pygame.display.flip()


# Game loop
def main_game_loop():
    while True:
        restart = play_game()
        if not restart:
            break


main_game_loop()
pygame.quit()
