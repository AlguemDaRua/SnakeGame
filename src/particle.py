# Este código foi feito por Azam Usman
import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color   # Cor base
        self.size = random.randint(2, 5)   # Tamanho inicial
        self.life = random.randint(20, 40)   # Tempo de vida (frames)
        self.vx = random.uniform(-2, 2)   # Velocidade x
        self.vy = random.uniform(-2, 2)   # Velocidade y
        self.gravity = 0.1   # Gravidade (puxa para baixo)
    
    def update(self):
        # Atualiza a posição e estado da partícula
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        self.size = max(0, self.size - 0.05)   # Diminui o tamanho
        return self.life > 0   # Retorna se ainda está viva
    
    def draw(self, screen):
        # Desenha a partícula com transparência baseada na vida
        alpha = min(255, self.life * 6)   # Alpha diminui com a vida
        color = (*self.color, int(alpha))
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []   # Lista de partículas
    
    def add_particles(self, x, y, color, count=5):
        # Adiciona novas partículas
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        # Atualiza todas as partículas e remove as mortas
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        # Desenha todas as partículas
        for p in self.particles:
            p.draw(screen)