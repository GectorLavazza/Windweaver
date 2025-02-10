from pygame import Surface

from settings import screen_size, DAY_TIME, HOUR


class Sky:
    def __init__(self, screen):
        self.screen = screen

        self.dark = False
        self.day = 0
        self.time = ''
        self.hour = 0
        self.minute = 0

        self.colors = [
            (0, 0, 0),  # Night (black)
            (255, 102, 0),  # Sunrise/Sunset (orange)
            (135, 206, 235)  # Day (sky blue)
        ]

        self.alphas = [150, 50, 0]  # Night, Sunrise/Sunset, Day

        self.phase_durations = {
            "night": DAY_TIME,  # Static night
            "sunrise": DAY_TIME,
            # Transition: night → day (black → orange → blue)
            "day": DAY_TIME,  # Static day
            "sunset": DAY_TIME
            # Transition: day → night (blue → orange → black)
        }

        self.phases = ['night', 'sunrise', 'day', 'sunset']

        self.current_phase = "day"
        self.tick = self.phase_durations[self.current_phase]
        self.surface = Surface(
            screen_size).convert_alpha()

        self.current_colors = [self.colors[2]]  # Static Blue
        self.current_alphas = [self.alphas[2]]  # Static 0

    def interpolate(self, start, end, t):
        return start + (end - start) * t

    def interpolate_color(self, color1, color2, t):
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t),
        )

    def update(self, dt):

        if self.current_phase == 'night' or self.current_phase == 'sunset' and self.tick <= \
                self.phase_durations[
                    'sunset'] // 4 or self.current_phase == 'sunrise' and self.tick >= \
                self.phase_durations['sunrise'] // 4 * 3:
            self.dark = True
        else:
            self.dark = False

        t = 1 - (self.tick / self.phase_durations[self.current_phase])

        if self.current_phase == "sunrise" or self.current_phase == "sunset":
            if t <= 0.5:  # First half of transition
                t_local = t * 2  # Map to [0, 1]
                self.current_color = self.interpolate_color(
                    self.current_colors[0], self.current_colors[1], t_local)
                self.current_alpha = int(
                    self.interpolate(self.current_alphas[0],
                                     self.current_alphas[1], t_local))

            else:  # Second half of transition
                t_local = (t - 0.5) * 2  # Map to [0, 1]
                self.current_color = self.interpolate_color(
                    self.current_colors[1], self.current_colors[2], t_local)
                self.current_alpha = int(
                    self.interpolate(self.current_alphas[1],
                                     self.current_alphas[2], t_local))
        else:
            self.current_color = self.current_colors[0]
            self.current_alpha = self.current_alphas[0]

        self.surface.fill((*self.current_color, self.current_alpha))
        self.screen.blit(self.surface, (0, 0))

        self.tick -= dt
        if self.tick <= 0:
            if self.current_phase == "night":
                self.current_phase = "sunrise"
                self.current_colors = [self.colors[0], self.colors[1],
                                       self.colors[2]]  # Black → Orange → Blue
                self.current_alphas = [self.alphas[0], self.alphas[1],
                                       self.alphas[2]]  # 150 → 100 → 0
            elif self.current_phase == "sunrise":
                self.current_phase = "day"
                self.current_colors = [self.colors[2]]  # Static Blue
                self.current_alphas = [self.alphas[2]]  # Static 0
            elif self.current_phase == "day":
                self.current_phase = "sunset"
                self.current_colors = [self.colors[2], self.colors[1],
                                       self.colors[0]]  # Blue → Orange → Black
                self.current_alphas = [self.alphas[2], self.alphas[1],
                                       self.alphas[0]]  # 0 → 100 → 150
            elif self.current_phase == "sunset":
                self.time = 0
                self.day += 1
                self.current_phase = "night"
                self.current_colors = [self.colors[0]]  # Static Black
                self.current_alphas = [self.alphas[0]]  # Static 150

            # Reset tick for the new phase
            self.tick = self.phase_durations[self.current_phase]

        self.hour = (DAY_TIME * self.phases.index(self.current_phase) + DAY_TIME - self.tick) / HOUR
        self.minute = (self.hour - round(self.hour) + 0.5) * 60
        f = 'AM' if 0 <= round(self.hour) < 13 else 'PM'
        h = round(self.hour) if f == 'AM' else round(self.hour) - 12
        self.time = (f'{str(round(h)).rjust(2, "0")}:'
                     f'{str(round(self.minute)).rjust(2, "0")} {f}')
