"""
Alien Invasion - Slightly Altered
Jeroldine Oakley [author]
This is a slightly altered version of the Alien Invasion game from the 
CSCI 1511 class/textbook.
07/16/25
"""
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_speed = 1.5

        # Bullet settings - changed width and height to show direction
        self.bullet_speed = 2.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3