import cv2
import numpy as np
import pygame

class VideoWriter:
    def __init__(self, filename, width, height, fps=60):
        self.filename = filename
        self.width = width
        self.height = height
        self.fps = fps
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))

    def add_frame(self, surface):
        frame = pygame.surfarray.array3d(surface)
        frame = frame.swapaxes(0, 1)  # (w, h, c) → (h, w, c)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.writer.write(frame)

    def close(self):
        self.writer.release()
