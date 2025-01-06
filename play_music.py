import pygame
def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("diskoteka_avariya_song.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass

