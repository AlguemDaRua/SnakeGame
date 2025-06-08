# Este código foi feito por Azam Usman
import pygame
import random
import math
from config import Config
from particle import ParticleSystem

class Renderer:
    def __init__(self, screen):
        self.screen = screen   # Superfície para desenhar
        self.config = Config()   # Configurações
        self.particle_system = ParticleSystem()   # Sistema de partículas
        self.themes = self._load_themes()   # Carrega temas
        self.current_theme = self.config.theme   # Tema atual
        self.background = self._create_background()   # Cria o fundo
        self.fonts = self._create_fonts()   # Cria as fontes
    
    def _create_fonts(self):
        # Cria dicionário de fontes
        return {
            "title": pygame.font.SysFont("arial", 72, bold=True),
            "menu": pygame.font.SysFont("arial", 36),
            "score": pygame.font.SysFont("courier", 24, bold=True),
            "game_over": pygame.font.SysFont("arial", 48, bold=True)
        }
    
    def _load_themes(self):
        # Define as cores para cada tema
        return {
            "forest": {
                "snake": (34, 139, 34),   # Verde floresta
                "head": (0, 100, 0),       # Verde escuro (cabeça)
                "food": (220, 20, 60),     # Vermelho (comida)
                "bomb": (139, 0, 0),       # Vermelho escuro (bomba)
                "bg": (11, 30, 15),        # Fundo verde escuro
                "grid": (20, 50, 25),      # Grade
                "ui": (180, 210, 150),     # UI (verde claro)
                "accent": (255, 215, 0)    # Destaque (ouro)
            },
            "neon": {
                "snake": (0, 255, 255),    # Ciano
                "head": (0, 150, 255),      # Azul
                "food": (255, 20, 147),     # Rosa
                "bomb": (255, 0, 0),        # Vermelho
                "bg": (5, 5, 15),           # Fundo preto azulado
                "grid": (20, 20, 40),       # Grade
                "ui": (200, 50, 255),      # UI (roxo)
                "accent": (255, 255, 0)     # Destaque (amarelo)
            },
            "sunset": {
                "snake": (255, 140, 0),    # Laranja
                "head": (220, 80, 20),      # Laranja escuro
                "food": (255, 215, 0),      # Amarelo (comida)
                "bomb": (178, 34, 34),      # Vermelho tijolo
                "bg": (25, 15, 35),         # Fundo roxo escuro
                "grid": (40, 20, 50),       # Grade
                "ui": (255, 150, 100),      # UI (laranja claro)
                "accent": (255, 50, 150)    # Destaque (rosa)
            },
            "ocean": {
                "snake": (64, 224, 208),    # Turquesa
                "head": (25, 150, 200),      # Azul turquesa
                "food": (255, 105, 180),     # Rosa (comida)
                "bomb": (220, 20, 60),       # Vermelho carmesim
                "bg": (5, 15, 30),           # Fundo azul escuro
                "grid": (10, 30, 50),        # Grade
                "ui": (170, 220, 255),       # UI (azul claro)
                "accent": (0, 255, 200)      # Destaque (verde água)
            }
        }
    
    def _create_background(self):
        # Cria uma superfície de fundo com grade
        bg = pygame.Surface((self.config.screen_width, self.config.screen_height))
        theme = self.themes[self.config.theme]
        bg.fill(theme["bg"])
        
        # Desenha padrão de grade
        for y in range(0, self.config.screen_height, self.config.grid_size):
            for x in range(0, self.config.screen_width, self.config.grid_size):
                if (x//self.config.grid_size + y//self.config.grid_size) % 2 == 0:
                    pygame.draw.rect(
                        bg, 
                        theme["grid"], 
                        (x, y, self.config.grid_size, self.config.grid_size),
                        1
                    )
        return bg
    
    def check_theme_change(self):
        # Verifica se o tema mudou e recria o fundo
        if self.config.theme != self.current_theme:
            self.current_theme = self.config.theme
            self.background = self._create_background()
    
    def draw_game(self, snake, food, bombs, score, mode, time_remaining=0, max_time=0, lives=0):
        # Desenha o estado do jogo
        self.check_theme_change()
        self.screen.blit(self.background, (0, 0))   # Fundo
        theme = self.themes[self.config.theme]
        
        # Desenha bombas (modo survival)
        for bomb in bombs:
            pygame.draw.rect(
                self.screen, 
                theme["bomb"], 
                (bomb[0], bomb[1], self.config.grid_size, self.config.grid_size),
                border_radius=10
            )
            # Pavio
            pygame.draw.line(
                self.screen, 
                (255, 255, 0), 
                (bomb[0] + self.config.grid_size//2, bomb[1] - 5),
                (bomb[0] + self.config.grid_size//2, bomb[1] - 15),
                3
            )
        
        # Desenha comida
        center_x = food[0] + self.config.grid_size//2
        center_y = food[1] + self.config.grid_size//2
        pygame.draw.circle(
            self.screen, 
            theme["food"], 
            (center_x, center_y), 
            self.config.grid_size//2
        )
        # Brilho
        pygame.draw.circle(
            self.screen, 
            (255, 255, 255, 100), 
            (center_x - 3, center_y - 3), 
            self.config.grid_size//4
        )
        
        # Desenha cobra com gradiente
        for i, segment in enumerate(snake):
            # Gradiente da cabeça (verde escuro) para a cauda (verde)
            color = self._gradient_color(
                theme["head"],
                theme["snake"],
                i / max(1, len(snake))
            )
            pygame.draw.rect(
                self.screen, 
                color, 
                (segment[0], segment[1], self.config.grid_size, self.config.grid_size),
                border_radius=8
            )
            
            # Brilho na cabeça
            if i == 0:
                pygame.draw.circle(
                    self.screen, 
                    (255, 255, 255, 180), 
                    (segment[0] + self.config.grid_size//4, segment[1] + self.config.grid_size//4), 
                    self.config.grid_size//6
                )
        
        # Desenha pontuação
        score_text = self.fonts["score"].render(f"Pontuação: {score}", True, theme["ui"])
        text_rect = score_text.get_rect(topleft=(20, 20))
        # Fundo escuro para legibilidade
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0, 150), 
            (text_rect.x - 10, text_rect.y - 5, text_rect.width + 20, text_rect.height + 10),
            border_radius=5
        )
        self.screen.blit(score_text, (20, 20))
        
        # Desenha UI específica do modo
        if mode == "time_attack":
            # Barra de tempo
            timer_width = 400
            timer_height = 20
            timer_x = self.config.screen_width // 2 - timer_width // 2
            timer_y = 20
            
            # Fundo da barra
            pygame.draw.rect(self.screen, (100, 100, 100), (timer_x, timer_y, timer_width, timer_height), border_radius=10)
            
            # Preenchimento da barra (tempo restante)
            if max_time > 0:
                remaining_ratio = time_remaining / max_time
                remaining_width = max(0, int(timer_width * remaining_ratio))
                pygame.draw.rect(self.screen, theme["accent"], (timer_x, timer_y, remaining_width, timer_height), border_radius=10)
            
            # Texto do tempo
            time_text = self.fonts["score"].render(f"Tempo: {int(time_remaining)}s", True, theme["ui"])
            self.screen.blit(time_text, (timer_x + timer_width + 10, timer_y))
        
        elif mode == "survival":
            # Desenha vidas (corações)
            heart_text = self.fonts["score"].render("Vidas: ", True, theme["ui"])
            self.screen.blit(heart_text, (self.config.screen_width - 150, 20))
            for i in range(lives):
                x = self.config.screen_width - 70 + i * 25
                y = 30
                # Dois círculos e um triângulo formando um coração
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 8)
                pygame.draw.circle(self.screen, (255, 0, 0), (x+8, y), 8)
                pygame.draw.polygon(self.screen, (255, 0, 0), [(x-4, y+4), (x+12, y+4), (x+4, y+12)])
        
        # Desenha partículas
        self.particle_system.update()
        self.particle_system.draw(self.screen)
    
    def draw_menu(self, menu_items, selected_index):
        # Desenha o menu
        self.check_theme_change()
        theme = self.themes[self.config.theme]
        self.screen.fill(theme["bg"])
        
        # Limpa a lista de retângulos
        self.menu_items_rects = []
        
        # Atualiza e desenha partículas
        self.particle_system.update()
        self.particle_system.draw(self.screen)
        
        # Adiciona partículas aleatórias
        if random.random() > 0.9:
            self.particle_system.add_particles(
                random.randint(0, self.config.screen_width),
                random.randint(0, self.config.screen_height),
                color=theme["accent"],
                count=3
            )
        
        # Título
        title = self.fonts["title"].render("SNAKE GAME", True, theme["accent"])
        title_rect = title.get_rect(center=(self.config.screen_width//2, 150))
        # Fundo escuro para o título
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0, 150), 
            (title_rect.x - 20, title_rect.y - 15, title_rect.width + 40, title_rect.height + 30),
            border_radius=15
        )
        self.screen.blit(title, title_rect)
        
        # Itens do menu
        for i, item in enumerate(menu_items):
            # Cor diferente para o item selecionado
            color = theme["accent"] if i == selected_index else theme["ui"]
            text = self.fonts["menu"].render(item, True, color)
            text_rect = text.get_rect(center=(self.config.screen_width//2, 350 + i*70))
            
            # Define o retângulo para interação com o mouse
            item_rect = pygame.Rect(
                self.config.screen_width//2 - 200,
                350 + i*70 - 25,
                400,
                50
            )
            self.menu_items_rects.append(item_rect)
            
            # Destaca o item selecionado
            if i == selected_index:
                pygame.draw.rect(
                    self.screen, 
                    (0, 0, 0, 100), 
                    item_rect,
                    border_radius=10
                )
            
            self.screen.blit(text, text_rect)
        
        # Rodapé com instruções
        footer = self.fonts["score"].render("Usa as teclas de seta ou o rato para navegar • Pressiona ENTER para selecionar", True, theme["ui"])
        self.screen.blit(footer, (self.config.screen_width//2 - footer.get_width()//2, self.config.screen_height - 50))
    
    def draw_game_over(self, score, high_score, mode):
        # Tela de game over
        self.check_theme_change()
        theme = self.themes[self.config.theme]
        self.screen.fill(theme["bg"])
        
        # Texto "Game Over"
        game_over = self.fonts["game_over"].render("GAME OVER", True, (220, 20, 60))   # Vermelho
        self.screen.blit(game_over, (self.config.screen_width//2 - game_over.get_width()//2, 200))
        
        # Modo
        mode_text = self.fonts["menu"].render(f"Modo: {mode.replace('_', ' ').title()}", True, theme["ui"])
        self.screen.blit(mode_text, (self.config.screen_width//2 - mode_text.get_width()//2, 270))
        
        # Pontuação
        score_text = self.fonts["menu"].render(f"Pontuação: {score}", True, theme["ui"])
        self.screen.blit(score_text, (self.config.screen_width//2 - score_text.get_width()//2, 340))
        
        # Pontuação máxima
        high_score_text = self.fonts["menu"].render(f"Pontuação Máxima: {high_score}", True, theme["accent"])
        self.screen.blit(high_score_text, (self.config.screen_width//2 - high_score_text.get_width()//2, 410))
        
        # Instrução
        restart = self.fonts["menu"].render("Pressiona ENTER para continuar", True, theme["ui"])
        self.screen.blit(restart, (self.config.screen_width//2 - restart.get_width()//2, 500))
        
        # Partículas
        self.particle_system.update()
        self.particle_system.draw(self.screen)
    
    def draw_high_scores(self, scores):
        # Tela de pontuações máximas
        self.check_theme_change()
        theme = self.themes[self.config.theme]
        self.screen.fill(theme["bg"])
        
        # Título
        title = self.fonts["title"].render("PONTUAÇÕES MÁXIMAS", True, theme["accent"])
        self.screen.blit(title, (self.config.screen_width//2 - title.get_width()//2, 100))
        
        # Cabeçalhos
        header_font = pygame.font.SysFont("Arial", 36, bold=True)
        mode_header = header_font.render("MODO", True, theme["ui"])
        score_header = header_font.render("PONTUAÇÃO", True, theme["accent"])
        
        self.screen.blit(mode_header, (self.config.screen_width//2 - 200, 180))
        self.screen.blit(score_header, (self.config.screen_width//2 + 100, 180))
        
        # Divisor
        pygame.draw.line(
            self.screen, 
            theme["ui"], 
            (self.config.screen_width//2 - 200, 220),
            (self.config.screen_width//2 + 200, 220),
            2
        )
        
        # Lista de pontuações
        y_pos = 240
        for mode, score in scores.items():
            mode_text = self.fonts["menu"].render(f"{mode.replace('_', ' ').title()}", True, theme["ui"])
            score_text = self.fonts["menu"].render(f"{score}", True, theme["accent"])
            
            self.screen.blit(mode_text, (self.config.screen_width//2 - 180, y_pos))
            self.screen.blit(score_text, (self.config.screen_width//2 + 120, y_pos))
            y_pos += 60
        
        # Rodapé
        footer = self.fonts["score"].render("Pressiona ENTER para voltar ao menu", True, theme["ui"])
        self.screen.blit(footer, (self.config.screen_width//2 - footer.get_width()//2, self.config.screen_height - 100))
    
    def draw_waiting_for_respawn(self, lives):
        # Tela de espera por renascimento (modo survival)
        theme = self.themes[self.config.theme]
        
        # Overlay escuro
        overlay = pygame.Surface((self.config.screen_width, self.config.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Mensagem
        font = pygame.font.SysFont("Arial", 48, bold=True)
        text = font.render("Pressiona qualquer tecla para renascer", True, theme["accent"])
        self.screen.blit(text, (self.config.screen_width//2 - text.get_width()//2, 
                              self.config.screen_height//2 - text.get_height()//2))
        
        # Vidas restantes
        lives_text = font.render(f"Vidas: {lives}", True, theme["ui"])
        self.screen.blit(lives_text, (self.config.screen_width//2 - lives_text.get_width()//2, 
                                     self.config.screen_height//2 + 50))
    
    def _gradient_color(self, start, end, progress):
        # Calcula uma cor intermediária no gradiente
        return (
            int(start[0] + (end[0] - start[0]) * progress),
            int(start[1] + (end[1] - start[1]) * progress),
            int(start[2] + (end[2] - start[2]) * progress)
        )