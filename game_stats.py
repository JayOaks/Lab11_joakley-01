"""
Alien Invasion - Slightly Altered
Jeroldine Oakley [author]
This is a slightly altered version of the Alien Invasion game from the 
CSCI 1511 class/textbook.
07/30/25
"""

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1