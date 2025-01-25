class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1000
        self.screen_height = 700
        self.bg_color = (10, 10, 30)  # A deep navy blue for space theme

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5  # Increased width for better visibility
        self.bullet_height = 20  # Increased height for better visibility
        self.bullet_color = (255, 0, 0)  # Bright red bullets
        self.bullets_allowed = 5  # Increased allowed bullets for a more dynamic gameplay

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Power-up settings
        self.powerup_duration = 5  # Duration of power-ups in seconds

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0  # Increased bullet speed for a faster-paced game
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
