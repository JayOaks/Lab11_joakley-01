"""
Alien Invasion - Slightly Altered
Jeroldine Oakley [author]
This is a slightly altered version of the Alien Invasion game from the 
CSCI 1511 class/textbook.
07/16/25
"""

import pygame
from pygame.sprite import Sprite

# Create the Bullet class to handle the bullets
class Bullet(Sprite):
    def __init__(self, ai_game):
        # Create a bullet object at the ship's current position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midleft = ai_game.ship.rect.midright

        # Store the bullet's position as a float.
        self.x = float(self.rect.x)

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """Move the bullet with the ship."""
        # Update the exact position of the bullet.
        self.x += self.settings.bullet_speed
        # Update the rect position.
        self.rect.x = self.x
