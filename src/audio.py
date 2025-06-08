# Este código foi feito por Azam Usman
import pygame

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.0  # Som desligado
    
    def play(self, name):
        # Som desligado porque não há assets
        pass
    
    def set_volume(self, volume):
        # Controle de volume desligado
        pass