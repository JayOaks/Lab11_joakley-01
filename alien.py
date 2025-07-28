"""
Alien Invasion - Slightly Altered
Jeroldine Oakley [author]
This is a slightly altered version of the Alien Invasion game from the 
CSCI 1511 class/textbook to match/reflect the changes made in the base code.
07/23/25
"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien."""

    def __init__(self, ai_game, x=None, y=None):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect.
        self.image = pygame.image.load('Assets/images/enemy_4.png')
        self.rect = self.image.get_rect()

        # Start each alien near the right edge of the screen.
        self.rect.x = x if x is not None else self.screen.get_rect().right
        self.rect.y = y if y is not None else 0

        # Store the alien’s exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.vertical_direction = 1

    def update(self):
        """Move the alien rightward across the screen."""
        # Towards the ship on the left side
        self.y += self.settings.alien_speed * self.vertical_direction
        self.x -= self.settings.alien_left_movement

        # Update the rect position
        self.rect.y = self.y
        self.rect.x = self.x

        # Change direction if the alien reaches the top or bottom of the screen
        if self.rect.bottom >= self.screen.get_rect().bottom or self.rect.top <= 0:
            self.vertical_direction *= -1

    def check_left_edge(self):
        """Return True if alien has reached the left edge of the screen."""
        # This will mean the ship has been hit by an alien
        return self.rect.left <= 0
