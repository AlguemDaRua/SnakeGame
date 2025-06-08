# Este código foi feito por Azam Usman
import pygame
import random
import time
import math
from config import Config

class SnakeGame:
    def __init__(self):
        self.config = Config()   # Carrega configurações
        self.reset("classic")   # Inicia o jogo no modo clássico
    
    def reset(self, mode):
        # Reinicia o jogo com o modo especificado
        self.mode = mode
        # Inicializa a cobra no centro da tela
        self.snake = [
            (self.config.screen_width//2, self.config.screen_height//2),
            (self.config.screen_width//2 - self.config.grid_size, self.config.screen_height//2),
            (self.config.screen_width//2 - 2*self.config.grid_size, self.config.screen_height//2)
        ]
        self.direction = (1, 0)   # Direção inicial (direita)
        self.next_direction = (1, 0)   # Próxima direção (para suavizar entrada)
        self.score = 0   # Pontuação
        self.food = self._spawn_food()   # Gera a primeira comida
        self.game_over = False   # Estado do jogo
        
        # Dificuldade progressiva
        self.base_speed = self.config.base_speed[self.config.difficulty]   # Velocidade base
        self.current_speed = self.base_speed   # Velocidade atual
        self.foods_eaten = 0   # Contador de comidas comidas
        
        # Modo Time Attack - tempo dinâmico
        self.time_remaining = 20.0   # Tempo inicial para a primeira comida
        self.max_time = 60.0   # Tempo máximo possível para qualquer comida
        self.min_time = 5.0    # Tempo mínimo para qualquer comida
        self.time_set = False  # Flag para indicar se o tempo foi definido para a comida atual
        
        # Modo Survival (sobrevivência)
        self.lives = 3   # Vidas
        self.bombs = []  # Lista de bombas (x, y, tempo_de_nascimento)
        self.bomb_lifetime = 10   # Tempo de vida da bomba em segundos
        self.bomb_spawn_timer = 0   # Temporizador para gerar bombas
        self.waiting_for_respawn = False   # Estado de espera por renascimento
    
    def _spawn_food(self, away_from_snake=False):
        # Tenta gerar comida em uma posição válida (não na cobra)
        attempts = 0
        while attempts < 100:
            food = (
                random.randrange(0, self.config.screen_width - self.config.grid_size, self.config.grid_size),
                random.randrange(0, self.config.screen_height - self.config.grid_size, self.config.grid_size)
            )
            
            # Verifica se a comida não está na cobra
            if food in self.snake:
                attempts += 1
                continue
            
            return food
        
        # Fallback: se não encontrar posição válida em 100 tentativas, gera aleatório
        return (
            random.randrange(0, self.config.screen_width - self.config.grid_size, self.config.grid_size),
            random.randrange(0, self.config.screen_height - self.config.grid_size, self.config.grid_size)
        )
    
    def _spawn_bomb(self):
        # Gera uma bomba em uma posição válida (não na cobra, comida ou outra bomba)
        attempts = 0
        while attempts < 50:
            # 70% de chance de colocar a bomba perto da comida, 30% aleatório
            if random.random() < 0.7 and self.food:
                # Coloca perto da comida
                offset_x = random.randint(-3, 3) * self.config.grid_size
                offset_y = random.randint(-3, 3) * self.config.grid_size
                bomb = (
                    max(0, min(self.config.screen_width - self.config.grid_size, self.food[0] + offset_x)),
                    max(0, min(self.config.screen_height - self.config.grid_size, self.food[1] + offset_y))
                )
            else:
                # Posição aleatória
                bomb = (
                    random.randrange(0, self.config.screen_width - self.config.grid_size, self.config.grid_size),
                    random.randrange(0, self.config.screen_height - self.config.grid_size, self.config.grid_size)
                )
            
            # Garante que a bomba não sobreponha cobra, comida ou outras bombas
            if (bomb not in self.snake and 
                bomb != self.food and 
                not any(b[0] == bomb[0] and b[1] == bomb[1] for b in self.bombs)):
                return (*bomb, time.time())   # Retorna com o tempo atual
            
            attempts += 1
        
        return None   # Retorna None se não conseguir
    
    def handle_input(self, event):
        # Trata entrada do teclado para mudar direção
        if event.type == pygame.KEYDOWN:
            # Teclas de seta e WASD
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.direction != (0, 1):
                self.next_direction = (0, -1)   # Cima
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.direction != (0, -1):
                self.next_direction = (0, 1)    # Baixo
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.direction != (1, 0):
                self.next_direction = (-1, 0)   # Esquerda
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.direction != (-1, 0):
                self.next_direction = (1, 0)    # Direita
    
    def update(self, dt):
        # Atualiza o estado do jogo
        if self.game_over or self.waiting_for_respawn:
            return
        
        # Atualiza o tempo no modo Time Attack
        if self.mode == "time_attack":
            # Define o tempo apenas uma vez por comida
            if not self.time_set:
                # Calcula a distância até a comida para alocar tempo inteligente
                head_x, head_y = self.snake[0]
                distance = math.sqrt((self.food[0] - head_x)**2 + (self.food[1] - head_y)**2)
                
                # Normaliza a distância (0-1) baseado na diagonal da tela
                max_distance = math.sqrt(self.config.screen_width**2 + self.config.screen_height**2)
                normalized_distance = distance / max_distance
                
                # Escala o tempo baseado na distância (comida mais perto = menos tempo)
                # Usa escala quadrática para diferenças mais dramáticas
                self.time_remaining = self.min_time + (self.max_time - self.min_time) * (1 - normalized_distance**2)
                self.time_set = True
                
                # Ajusta baseado no tamanho da cobra (cobra maior = menos tempo)
                size_factor = len(self.snake) / 50
                self.time_remaining *= max(0.5, 1.0 - size_factor)
            
            # Diminui o tempo normalmente
            self.time_remaining -= dt
            
            if self.time_remaining <= 0:
                self.game_over = True
                return
        
        # Atualiza bombas (modo survival)
        if self.mode == "survival":
            # Remove bombas expiradas
            current_time = time.time()
            self.bombs = [bomb for bomb in self.bombs if current_time - bomb[2] < self.bomb_lifetime]
            
            # Gera novas bombas
            self.bomb_spawn_timer += dt
            # Gera bombas mais frequentemente conforme o jogo progride
            if self.bomb_spawn_timer > max(2, 6 - (self.foods_eaten / 10)):
                new_bomb = self._spawn_bomb()
                if new_bomb:
                    self.bombs.append(new_bomb)
                self.bomb_spawn_timer = 0
        
        self.direction = self.next_direction   # Atualiza a direção
        
        # Move a cobra
        head_x = self.snake[0][0] + self.direction[0] * self.config.grid_size
        head_y = self.snake[0][1] + self.direction[1] * self.config.grid_size
        new_head = (head_x, head_y)
        
        # Colisão com paredes baseada no modo
        if self.mode in ["classic", "time_attack"]:
            # Teletransporta a cobra pelas paredes
            if new_head[0] < 0:
                new_head = (self.config.screen_width - self.config.grid_size, new_head[1])
            elif new_head[0] >= self.config.screen_width:
                new_head = (0, new_head[1])
            if new_head[1] < 0:
                new_head = (new_head[0], self.config.screen_height - self.config.grid_size)
            elif new_head[1] >= self.config.screen_height:
                new_head = (new_head[0], 0)
        else:  # Modo survival: paredes sólidas
            if (new_head[0] < 0 or 
                new_head[0] >= self.config.screen_width or
                new_head[1] < 0 or 
                new_head[1] >= self.config.screen_height):
                self.handle_collision()   # Trata colisão
                return
        
        # Colisão consigo mesma
        if new_head in self.snake:
            self.handle_collision()
            return
        
        # Colisão com bomba (apenas survival)
        bomb_positions = [(b[0], b[1]) for b in self.bombs]
        if self.mode == "survival" and new_head in bomb_positions:
            self.handle_collision()
            # Remove a bomba
            self.bombs = [b for b in self.bombs if (b[0], b[1]) != new_head]
            return
        
        self.snake.insert(0, new_head)   # Adiciona nova cabeça
        
        # Colisão com comida
        if new_head == self.food:
            self.score += 10
            self.foods_eaten += 1
            
            # Dificuldade progressiva - aumenta a velocidade
            self.current_speed = min(
                self.base_speed + (self.foods_eaten * self.config.speed_increment),
                self.config.max_speed
            )
            
            # Gera nova comida
            self.food = self._spawn_food()
            
            # Reseta a flag de tempo para nova comida (time attack)
            if self.mode == "time_attack":
                self.time_set = False
        else:
            self.snake.pop()   # Remove a cauda se não comeu
    
    def handle_collision(self):
        # Trata colisões (paredes, si mesma, bombas)
        if self.mode == "survival":
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.waiting_for_respawn = True
                # Reseta a posição da cobra
                self.snake = [
                    (self.config.screen_width//2, self.config.screen_height//2),
                    (self.config.screen_width//2 - self.config.grid_size, self.config.screen_height//2),
                    (self.config.screen_width//2 - 2*self.config.grid_size, self.config.screen_height//2)
                ]
                self.direction = (1, 0)
                self.next_direction = (1, 0)
        else:
            self.game_over = True   # Fim de jogo em outros modos
    
    def trigger_respawn(self):
        # Reinicia o jogo após colisão no modo survival (quando tem vidas)
        if self.waiting_for_respawn:
            self.waiting_for_respawn = False
    
    def get_state(self):
        # Retorna o estado atual do jogo para renderização
        return {
            "snake": self.snake,
            "food": self.food,
            "bombs": [(b[0], b[1]) for b in self.bombs],  # Apenas posições
            "score": self.score,
            "game_over": self.game_over,
            "mode": self.mode,
            "time_remaining": self.time_remaining if self.mode == "time_attack" else 0,
            "max_time": self.max_time if self.mode == "time_attack" else 0,
            "lives": self.lives if self.mode == "survival" else 0,
            "waiting_for_respawn": self.waiting_for_respawn,
            "current_speed": self.current_speed
        }