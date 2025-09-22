import pygame
import math
from plugins import color_change_on_bounce

VIDEO_PATH = "output_videos/simulation_raw.mp4"
FINAL_VIDEO_PATH = "output_videos/simulation_final.mp4"
BG_MUSIC_PATH = "assets/background.mp3"
BOUNCE_SOUND_PATH = "assets/bounce.wav"

class CollisionManager:
    def __init__(self, objects, bounce_sound_path=BOUNCE_SOUND_PATH):
        self.objects = objects
        self.bounce_sound = pygame.mixer.Sound(bounce_sound_path)
        self.bounce_events = []  # timestamps for later audio merging

    def handle_collisions(self, elapsed_time):
        handled = set()

        for i, obj1 in enumerate(self.objects):
            for obj2 in self.objects[i + 1:]:
                pair_id = (id(obj1), id(obj2))
                if pair_id in handled:
                    continue

                collision = obj1.check_collision(obj2)
                if not collision:
                    collision = obj2.check_collision(obj1)
                if collision:
                    ctype, nx, ny = collision

                    if ctype == "ball_container":
                        obj2.bounce((nx, ny))
                        # reposition ball inside container
                        obj2.x = obj2.x if math.hypot(obj2.x - obj1.x, obj2.y - obj1.y) < obj1.size else \
                            obj1.x + nx * (obj1.size - obj2.radius)
                        obj2.y = obj2.y if math.hypot(obj2.x - obj1.x, obj2.y - obj1.y) < obj1.size else \
                            obj1.y + ny * (obj1.size - obj2.radius)
                        color_change_on_bounce(obj2)
                        self.bounce_sound.play()
                        self.bounce_events.append(elapsed_time / 1000.0)

                    elif ctype == "ball_ball":
                        self.resolve_ball_ball_collision(obj1, obj2, nx, ny)
                        color_change_on_bounce(obj1)
                        color_change_on_bounce(obj2)
                        self.bounce_sound.play()
                        self.bounce_events.append(elapsed_time / 1000.0)

                    handled.add(pair_id)

    @staticmethod
    def resolve_ball_ball_collision(ball1, ball2, nx, ny):
        # Push balls apart to prevent overlap
        dist = math.hypot(ball2.x - ball1.x, ball2.y - ball1.y)
        overlap = (ball1.radius + ball2.radius) - dist
        if overlap > 0:
            ball1.x -= nx * overlap / 2
            ball1.y -= ny * overlap / 2
            ball2.x += nx * overlap / 2
            ball2.y += ny * overlap / 2

        # Simple elastic collision (1D along collision normal)
        v1n = ball1.vx * nx + ball1.vy * ny
        v2n = ball2.vx * nx + ball2.vy * ny
        ball1.vx += (v2n - v1n) * nx
        ball1.vy += (v2n - v1n) * ny
        ball2.vx += (v1n - v2n) * nx
        ball2.vy += (v1n - v2n) * ny