import sys
from time import sleep
import random
import pygame
import pandas as pd
from pygame.sprite import Sprite
import joblib  # For saving/loading models
from sklearn.ensemble import RandomForestRegressor
import os


from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien



class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.model = joblib.load('difficulty_model.pkl')  # Load the trained model here

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Load sound effects
        self.laser_sound = pygame.mixer.Sound('laser.wav')
        self.explosion_sound = pygame.mixer.Sound('explosion.wav')
        self.powerup_sound = pygame.mixer.Sound('powerup.wav')

        # Create an instance to store game statistics and a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Initialize powerups group

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")


    def update_difficulty(self):
        """Adjust the game difficulty based on player performance."""
        if len(self.stats.reaction_times) > 0:
            reaction_time = self.stats.reaction_times[-1]
            accuracy = self.stats.shots_hit / self.stats.shots_fired if self.stats.shots_fired > 0 else 0
            lives_lost = self.stats.lives_lost

            # Use the model to predict the new alien speed based on player metrics
            predicted_alien_speed = self.model.predict([[reaction_time, accuracy, lives_lost]])[0]
            self.settings.alien_speed = predicted_alien_speed

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.update_difficulty()  # Adjust difficulty in real-time
                self._update_powerups()  # Update power-ups

                # Save metrics periodically
                self.save_metrics()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _reset_game_elements(self):
        """Reset the game elements after the ship is hit."""
        self.bullets.empty()
        self.aliens.empty()
        self.powerups.empty()  # Clear power-ups as well
        self._create_fleet()
        self.ship.center_ship()
        sleep(0.5)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self.powerups.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()  # Play laser sound when firing

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.explosion_sound.play()  # Play explosion sound
            self.sb.prep_score()
            self.sb.check_high_score()

            # Chance to spawn a power-up
            if random.random() < 0.2:  # 20% chance to spawn
                self._create_powerup()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _create_powerup(self):
        """Create a power-up at a random position."""
        powerup = PowerUp(self)  # Assuming PowerUp class is defined
        self.powerups.add(powerup)

    def _update_powerups(self):
        """Update and check for power-up collisions."""
        self.powerups.update()
        for powerup in self.powerups.copy():
            if powerup.rect.top > self.settings.screen_height:
                self.powerups.remove(powerup)
            if pygame.sprite.spritecollideany(self.ship, self.powerups):
                self.powerup_sound.play()
                self.stats.shots_fired += 1  # Example power-up effect
                self.powerups.remove(powerup)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.stats.lives_lost += 1  # Increment lives lost
            self.sb.prep_ships()
            self._reset_game_elements()
        else:
            self.save_metrics()  # Save metrics when the game ends
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens with dynamic speed."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        new_alien.alien_speed = random.uniform(0.5, 2.0)  # Assign random speed
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def save_metrics(self):
        """Collect and save game metrics to a CSV file."""
        accuracy = [self.stats.shots_hit / self.stats.shots_fired if self.stats.shots_fired > 0 else 0]
        lives_lost = [self.stats.lives_lost]

        # Ensure all lists are of the same length
        max_length = max(len(self.stats.reaction_times), len(accuracy), len(lives_lost))
        reaction_times = self.stats.reaction_times + [None] * (max_length - len(self.stats.reaction_times))
        accuracy = accuracy + [None] * (max_length - len(accuracy))
        lives_lost = lives_lost + [None] * (max_length - len(lives_lost))

        metrics_data = {
            'reaction_time': reaction_times,
            'accuracy': accuracy,
            'lives_lost': lives_lost,
        }

        df = pd.DataFrame(metrics_data)
        df.to_csv('player_metrics.csv', mode='a', header=not os.path.exists('player_metrics.csv'), index=False)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


# Power-up class
class PowerUp(Sprite):
    """A class to represent a power-up in the game."""

    def __init__(self, ai_game):
        """Initialize the power-up."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('pup.png')  # Load your power-up image
        self.rect = self.image.get_rect()

        # Start each new power-up at a random position near the top of the screen
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = random.randint(50, 150)  # Adjust the height as needed

    def update(self):
        """Move the power-up down the screen."""
        self.rect.y += 1  # Move down; adjust speed as needed
        if self.rect.top >= self.settings.screen_height:
            self.kill()  # Remove power-up if it goes off screen

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
