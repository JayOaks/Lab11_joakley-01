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

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien near the right edge of the screen.
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height

        # Store the alien’s exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien leftward across the screen."""
        # Towards the ship on the left side
        self.x -= self.settings.alien_speed
        self.rect.x = self.x

    def check_left_edge(self):
        """Return True if alien has reached the left edge of the screen."""
        # This will mean the ship has been hit by an alien
        return self.rect.left <= 0
