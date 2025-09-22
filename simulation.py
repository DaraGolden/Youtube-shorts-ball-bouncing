import pygame
import math
import os
import subprocess
from objects.balls import Ball
from objects.container import Container
from plugins import color_change_on_bounce
from video_writer import VideoWriter
from audio import init_audio

# Paths
VIDEO_PATH = "output_videos/simulation_raw.mp4"
FINAL_VIDEO_PATH = "output_videos/simulation_final.mp4"
BG_MUSIC_PATH = "assets/background.mp3"
BOUNCE_SOUND_PATH = "assets/bounce.wav"

def run_simulation(output_file=FINAL_VIDEO_PATH,
                   duration=20, width=540, height=960,
                   fps=60):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Initialize objects
    container = Container(width // 2, height // 2, shape="circle", size=200)
    balls = [Ball(width // 2, height // 2, gravity=(0, 0.4)) for _ in range(3)]
    objects = [container] + balls

    # Initialize video writer
    writer = VideoWriter(VIDEO_PATH, width, height, fps=fps)

    # Initialize Pygame mixer (for bounce sound playback during simulation)
    init_audio(bg_music=None)
    bounce_sound = pygame.mixer.Sound(BOUNCE_SOUND_PATH)

    # Keep track of bounce sound timestamps (for ffmpeg mixing)
    bounce_events = []

    elapsed = 0
    running = True
    while running and elapsed < duration * 1000:
        dt = clock.tick(fps)
        elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update all objects
        for obj in objects:
            obj.update(dt / 16.0)

        # Collision detection
        for i, obj1 in enumerate(objects):
            for obj2 in objects[i+1:]:
                collision = obj1.check_collision(obj2)
                if not collision:
                    collision = obj2.check_collision(obj1)
                if collision:
                    ctype, nx, ny = collision

                    if ctype == "ball_container":
                        # Bounce and reposition inside container
                        obj2.bounce((nx, ny))
                        color_change_on_bounce(obj2)
                        bounce_sound.play()
                        bounce_events.append(elapsed / 1000.0)  # in seconds

                    elif ctype == "ball_ball":
                        obj1.bounce((nx, ny))
                        obj2.bounce((-nx, -ny))
                        color_change_on_bounce(obj1)
                        color_change_on_bounce(obj2)
                        bounce_sound.play()
                        bounce_events.append(elapsed / 1000.0)

        # Draw frame
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.draw(screen)

        pygame.display.flip()
        writer.add_frame(screen)

    writer.close()
    pygame.quit()

    # Merge background music + bounce sound events using ffmpeg
#     merge_audio_with_video(VIDEO_PATH, BG_MUSIC_PATH, FINAL_VIDEO_PATH, bounce_events)


# def merge_audio_with_video(video_file, bg_music_file, output_file, bounce_events, bounce_wav=BOUNCE_SOUND_PATH):
#     """
#     Merges background music and bounce sound effects into the video using ffmpeg.
#     bounce_events: list of timestamps (seconds) to play bounce sound
#     """
#     import tempfile

#     # 1. Create a temporary bounce track with correct timestamps
#     tmp_bounce_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
#     # Generate the bounce sound timeline with pydub
#     from pydub import AudioSegment
#     bg_music = AudioSegment.from_file(bg_music_file)
#     bounce = AudioSegment.from_file(bounce_wav)

#     total_duration_ms = int(bg_music.duration_seconds * 1000)
#     output_audio = AudioSegment.silent(duration=total_duration_ms)

#     for t in bounce_events:
#         start_ms = int(t * 1000)
#         output_audio = output_audio.overlay(bounce, position=start_ms)

#     # Overlay background music
#     output_audio = output_audio.overlay(bg_music)
#     output_audio.export(tmp_bounce_wav, format="wav")

#     # 2. Use ffmpeg to merge with video
#     cmd = [
#         "ffmpeg", "-y", "-i", video_file, "-i", tmp_bounce_wav,
#         "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
#     ]
#     subprocess.run(cmd)

#     # Clean up temporary file
#     os.remove(tmp_bounce_wav)
