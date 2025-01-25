import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('alien.png')  # Ensure this is a high-quality image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize for better visibility
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)  # Random x position
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

        # Set a random vertical speed to make movements more dynamic
        self.vertical_speed = random.uniform(0.5, 1.5)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien right or left, and make it move down periodically."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

        # Randomly change the alien's vertical position for dynamic movement
        if random.randint(0, 100) < 5:  # 5% chance to move down
            self.rect.y += self.vertical_speed
