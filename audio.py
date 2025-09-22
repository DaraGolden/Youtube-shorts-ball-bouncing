import pygame

def init_audio(bg_music=None):
    pygame.mixer.init()
    if bg_music:
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.play(-1)  # Loop forever

def play_bounce_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()
