"""
Alien Invasion - Slightly Altered
Jeroldine Oakley [author]
This is a slightly altered version of the Alien Invasion game from the 
CSCI 1511 class/textbook.
07/23/25
"""

import sys

import pygame

from alien import Alien
from settings import Settings
from ship import Ship
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from time import sleep


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Create a group to hold aliens
        self.aliens = pygame.sprite.Group()

        # Create an alien fleet
        alien = Alien(self)
        self.current_column_count = 1
        self._create_fleet()

        # Call button class to draw play button
        self.play_button = Button(self, "Play")

        # Game state
        self.game_active = False

        # Storing game statistics
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

    def _start_game(self):
        """Initialize game settings when Play is clicked."""
        self.game_active = True
        pygame.mouse.set_visible(False)
        
        # Reset dynamic game elements
        self.bullets.empty()
        self.aliens.empty()
        
        # Position the ship
        self.ship.rect.midleft = self.screen.get_rect().midleft
        
        # Recreate alien fleet
        self.current_column_count = 1
        self._create_fleet()
        
        # Reset scoreboard, level and lives
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_ships()



    def run_game(self):
        # Call the event handler
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()
                self._delete_bullets()
            
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
                    self._start_game()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()            

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    

    # Create a vertical column of aliens
    def _create_alien_column(self, column_x, alien_height):
        """Create a vertical column of aliens."""
        for row_number in range(5):
            alien_y = alien_height + 2 * alien_height * row_number
            alien = Alien(self, column_x, alien_y)
            self.aliens.add(alien)

    # Create a fleet of aliens
    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        total_width = self.current_column_count * 2 * alien_width
        start_x = (self.screen.get_width() - total_width) // 2
        
        for column_number in range(self.current_column_count):
            column_x = start_x + column_number * 2 * alien_width
            self._create_alien_column(column_x, alien_height)

    
    def _update_aliens(self):
        """Tracks and updates alien(s) count/actions."""
        self.aliens.update()

        # Check for when the alien(s) hits the ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Check for when the alien(s) reaches the left edge of the screen
        self._check_aliens_left()

    def _check_aliens_left(self):
        """Checks if alien(s) has reached the left edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                self._ship_hit()
                break
    
    
    def _ship_hit(self):
        """Respond to ship being hit by alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _reset_game(self):
        """Resets the game."""
        self.game_active = False
        pygame.mouse.set_visible(True)
        self.aliens.empty()
        self.bullets.empty()
        self.current_column_count = 1
        self._create_fleet()
        self.ship.rect.midleft = self.screen.get_rect().midleft

    def _delete_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        
        # Check for collisions between bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.aliens:
            self.current_column_count = min(self.current_column_count + 1, 6)
            self._create_fleet()
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
