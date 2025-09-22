class SimObject:
    def update(self, dt):
        """Update object state each frame"""
        pass

    def draw(self, surface):
        """Draw object on screen"""
        pass

    def check_collision(self, other):
        """Return collision info if collides with other"""
        return None
