class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reaction_times = []  # Initialize reaction times here
        self.shots_fired = 0  # Count total shots fired
        self.shots_hit = 0  # Count total hits
        self.lives_lost = 0  # Track lives lost
        self.powerups_collected = 0  # Count total power-ups collected

        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.reaction_times.clear()  # Clear reaction times
        self.shots_fired = 0
        self.shots_hit = 0
        self.lives_lost = 0
        self.powerups_collected = 0  # Reset power-ups collected
