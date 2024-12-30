import pygame
from settings import screen_width, screen_height

class Sky:
    def __init__(self, screen):
        self.screen = screen

        # Define the full gradient for transitions
        self.colors = [
            (0, 0, 0),       # Night (black)
            (255, 102, 0),   # Sunrise/Sunset (orange)
            (135, 206, 235)  # Day (sky blue)
        ]

        # Corresponding alpha values
        self.alphas = [150, 50, 0]  # Night, Sunrise/Sunset, Day

        # Phase durations (in ticks)
        self.phase_durations = {
            "night": 9000,      # Static night
            "sunrise": 9000,    # Transition: night → day (black → orange → blue)
            "day": 9000,        # Static day
            "sunset": 9000      # Transition: day → night (blue → orange → black)
        }

        # Initial state
        self.current_phase = "night"
        self.tick = self.phase_durations[self.current_phase]
        self.surface = pygame.Surface((screen_width, screen_height)).convert_alpha()

        # Track which colors to interpolate between
        self.current_colors = [self.colors[0], self.colors[1]]  # Default: night → orange
        self.current_alphas = [self.alphas[0], self.alphas[1]]  # Default: night → orange

    def interpolate(self, start, end, t):
        """Interpolate between two values based on t (0 to 1)."""
        return start + (end - start) * t

    def interpolate_color(self, color1, color2, t):
        """Interpolate between two colors based on t (0 to 1)."""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )

    def update(self, dt):
        t = 1 - (self.tick / self.phase_durations[self.current_phase])

        # Determine behavior based on the phase
        if self.current_phase == "sunrise" or self.current_phase == "sunset":
            # Transition through multiple steps: [black → orange → blue]
            if t <= 0.5:  # First half of transition
                # Interpolate between the first two colors (black → orange OR blue → orange)
                t_local = t * 2  # Map to [0, 1]
                self.current_color = self.interpolate_color(self.current_colors[0], self.current_colors[1], t_local)
                self.current_alpha = int(self.interpolate(self.current_alphas[0], self.current_alphas[1], t_local))
            else:  # Second half of transition
                # Interpolate between the second and third colors (orange → blue OR orange → black)
                t_local = (t - 0.5) * 2  # Map to [0, 1]
                self.current_color = self.interpolate_color(self.current_colors[1], self.current_colors[2], t_local)
                self.current_alpha = int(self.interpolate(self.current_alphas[1], self.current_alphas[2], t_local))
        else:
            # Static colors and alpha for day and night
            self.current_color = self.current_colors[0]
            self.current_alpha = self.current_alphas[0]

        # Draw the sky surface
        self.surface.fill(self.current_color)
        self.surface.set_alpha(self.current_alpha)
        self.screen.blit(self.surface, (0, 0))

        # Update tick and phase
        self.tick -= dt
        if self.tick <= 0:
            # Advance to the next phase
            if self.current_phase == "night":
                self.current_phase = "sunrise"
                self.current_colors = [self.colors[0], self.colors[1], self.colors[2]]  # Black → Orange → Blue
                self.current_alphas = [self.alphas[0], self.alphas[1], self.alphas[2]]  # 150 → 100 → 0
            elif self.current_phase == "sunrise":
                self.current_phase = "day"
                self.current_colors = [self.colors[2]]  # Static Blue
                self.current_alphas = [self.alphas[2]]  # Static 0
            elif self.current_phase == "day":
                self.current_phase = "sunset"
                self.current_colors = [self.colors[2], self.colors[1], self.colors[0]]  # Blue → Orange → Black
                self.current_alphas = [self.alphas[2], self.alphas[1], self.alphas[0]]  # 0 → 100 → 150
            elif self.current_phase == "sunset":
                self.current_phase = "night"
                self.current_colors = [self.colors[0]]  # Static Black
                self.current_alphas = [self.alphas[0]]  # Static 150

            # Reset tick for the new phase
            self.tick = self.phase_durations[self.current_phase]
