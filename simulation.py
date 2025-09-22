import pygame

from objects.balls import Ball
from objects.container import Container
from video_writer import VideoWriter
from audio import init_audio
from collision_manager import CollisionManager

VIDEO_PATH = "output_videos/simulation_raw.mp4"
FINAL_VIDEO_PATH = "output_videos/simulation_final.mp4"
BG_MUSIC_PATH = "assets/background.mp3"
BOUNCE_SOUND_PATH = "assets/bounce.wav"



def run_simulation(output_file=FINAL_VIDEO_PATH,
                   duration=30, width=540, height=960,
                   fps=30):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # Initialize objects
    container = Container(width // 2, height // 2, shape="circle", size=200)
    balls = [Ball(width // 2, height // 2, gravity=(0, 0.5)) for _ in range(5)]
    objects = [container] + balls

    # Initialize collision manager
    collision_manager = CollisionManager(objects)

    # Video writer
    writer = VideoWriter(VIDEO_PATH, width, height, fps=fps)

    # Initialize audio
    init_audio(bg_music=None)

    elapsed = 0
    running = True
    while running and elapsed < duration * 1000:
        dt = clock.tick(fps)
        elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update objects
        for obj in objects:
            obj.update(dt / 16.0)

        # Handle collisions
        collision_manager.handle_collisions(elapsed)

        # Draw
        screen.fill((0, 0, 0))
        for obj in objects:
            obj.draw(screen)

        pygame.display.flip()
        writer.add_frame(screen)

    writer.close()
    pygame.quit()

    # Merge background music + bounce sounds using ffmpeg/pydub
#     merge_audio_with_video(VIDEO_PATH, BG_MUSIC_PATH, FINAL_VIDEO_PATH, collision_manager.bounce_events)


# def merge_audio_with_video(video_file, bg_music_file, output_file, bounce_events, bounce_wav=BOUNCE_SOUND_PATH):
#     """
#     Merge background music + bounce sound effects into the final video.
#     """
#     import tempfile
#     from pydub import AudioSegment

#     tmp_bounce_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
#     bg_music = AudioSegment.from_file(bg_music_file)
#     bounce = AudioSegment.from_file(bounce_wav)

#     total_duration_ms = int(bg_music.duration_seconds * 1000)
#     output_audio = AudioSegment.silent(duration=total_duration_ms)

#     # Overlay bounce sounds at correct timestamps
#     for t in bounce_events:
#         start_ms = int(t * 1000)
#         output_audio = output_audio.overlay(bounce, position=start_ms)

#     # Overlay background music
#     output_audio = output_audio.overlay(bg_music)
#     output_audio.export(tmp_bounce_wav, format="wav")

#     # Merge using ffmpeg
#     cmd = [
#         "ffmpeg", "-y", "-i", video_file, "-i", tmp_bounce_wav,
#         "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
#     ]
#     subprocess.run(cmd)

#     os.remove(tmp_bounce_wav)
