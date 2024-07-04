import pygame
import random
from enum import Enum
import numpy as np


class COLOR(Enum):
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)
        YELLOW = (255, 255, 0)
        GRAY = (128, 128, 128)
        ORANGE = (255, 165, 0)
        PINK = (255, 192, 203)
        COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PINK]


class Env:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.WIDTH, self.HEIGHT = 750, 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mastermind")

        # Game variables
        self.CODE_LENGTH = 4
        self.MAX_GUESSES = 15

        # Game state
        self.reset()

    def generate_code(self):
        return [random.choice(self.COLOR.COLORS) for _ in range(self.CODE_LENGTH)]

    def draw_circle(self, x, y, color):
        pygame.draw.circle(self.screen, color.value, (x, y), 20)

    def draw_feedback(self, x, y, correct_position, correct_color):
        for i in range(correct_position):
            pygame.draw.circle(self.screen, self.COLOR.BLACK.value, (x + i * 25, y), 5)
        for i in range(correct_color):
            pygame.draw.circle(self.screen, self.COLOR.WHITE.value, (x + (i + correct_position) * 25, y), 5)

    def draw_button(self, x, y, width, height, color, text):
        pygame.draw.rect(self.screen, color.value, (x, y, width, height))
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, self.COLOR.BLACK.value)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)

    def get_last_guess_coordinates(self, num_guesses):
        y = 50 + (num_guesses - 1) * 40  # Vertical position of the last guess
        coordinates = [(75 + i * 50, y) for i in range(self.CODE_LENGTH)]
        return coordinates

    def reset(self):
        self.code = self.generate_code()
        self.guesses = []
        self.current_guess = []
        self.game_over = False
        self.win = False
        return self.code, self.guesses, self.current_guess, self.game_over, self.win

    def compute_reward(self, guess, code, game_over, win):
        if game_over:
            if win:
                return 100  # Large reward for winning
            else:
                return -100  # Large penalty for losing
        correct_position = sum(1 for a, b in zip(guess, code) if a == b)
        correct_color = sum(min(guess.count(c), code.count(c)) for c in set(guess)) - correct_position
        reward = correct_position * 10 + correct_color * 5  # Reward for correct positions and colors
        reward -= 1  # Small penalty for each guess to encourage fewer guesses
        return reward

    def play_step(self, action):
        reward = 0
        if action < self.CODE_LENGTH:
            if len(self.current_guess) < self.CODE_LENGTH:
                self.current_guess.append(self.COLOR.COLORS[action])
        elif action == self.CODE_LENGTH:
            if len(self.current_guess) == self.CODE_LENGTH:
                self.guesses.append(self.current_guess)
                if self.current_guess == self.code:
                    self.game_over = True
                    self.win = True
                elif len(self.guesses) == self.MAX_GUESSES:
                    self.game_over = True
                    self.win = False
                reward = self.compute_reward(self.current_guess, self.code, self.game_over, self.game_over and self.current_guess == self.code)
                self.current_guess = []
            else:
                reward = -0.1  # Penalty for invalid submission
        elif action == self.CODE_LENGTH + 1:
            self.current_guess = []
            reward = -0.1  # Penalty for clearing the guess

        # Drawing part
        self.screen.fill(self.COLOR.GRAY.value)
        for i, color in enumerate(self.COLOR.COLORS):
            self.draw_circle(75 + i * 50, 675, color)
        self.draw_button(400, 650, 100, 50, self.COLOR.GREEN, "Submit")
        self.draw_button(520, 650, 100, 50, self.COLOR.RED, "Clear")
        for i, guess in enumerate(self.guesses):
            for j, color in enumerate(guess):
                self.draw_circle(75 + j * 50, 50 + i * 40, color)
            correct_position = sum(1 for a, b in zip(guess, self.code) if a == b)
            correct_color = sum(min(guess.count(c), self.code.count(c)) for c in set(guess)) - correct_position
            self.draw_feedback(300, 50 + i * 40, correct_position, correct_color)
        for i, color in enumerate(self.current_guess):
            self.draw_circle(75 + i * 50, 50 + len(self.guesses) * 40, color)
        if self.game_over:
            font = pygame.font.Font(None, 36)
            if self.win:
                text = font.render("You win!", True, self.COLOR.BLACK.value)
            else:
                text = font.render("Game Over!", True, self.COLOR.BLACK.value)
            self.screen.blit(text, (50, 50 + len(self.guesses) * 40 + 20))
            text = font.render("Correct Code:", True, self.COLOR.BLACK.value)
            self.screen.blit(text, (50, 50 + len(self.guesses) * 40 + 60))
            for i, color in enumerate(self.code):
                self.draw_circle(250 + i * 50, 50 + len(self.guesses) * 40 + 60, color)
        pygame.display.flip()
        return self.code, self.guesses, self.current_guess, self.game_over, reward

    def play(self):
        self.reset()
        while True:
            action = np.random.choice(self.CODE_LENGTH + 2)  # Random action for now
            self.code, self.guesses, self.current_guess, self.game_over, reward = self.play_step(action)
            if self.game_over:
                break

# To play the game
game = Env()
game.play()
pygame.quit()
