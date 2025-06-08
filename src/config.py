# Este código foi feito por Azam Usman
import json
import os

class Config:
    def __init__(self):
        # Configurações iniciais
        self.screen_width = 1200
        self.screen_height = 800
        self.grid_size = 20
        self.theme = "forest"   # Tema padrão
        self.difficulty = "medium"   # Dificuldade padrão
        self.volume = 0.0   # Volume inicial (mudo)
        self.high_scores = {"classic": 0, "time_attack": 0, "survival": 0}   # Pontuações altas iniciais
        self.config_path = os.path.expanduser("~/.snake_game_config.json")   # Caminho para salvar configurações
        self.available_themes = ["forest", "neon", "sunset", "ocean"]   # Temas disponíveis
        self.base_speed = {   # Velocidade base por dificuldade
            "easy": 8,
            "medium": 12,
            "hard": 16
        }
        self.speed_increment = 0.2   # Incremento de velocidade por comida
        self.max_speed = 30   # Velocidade máxima
        self.load()   # Carregar configurações salvas
    
    def load(self):
        # Carrega configurações de um arquivo se existir
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                # Atualiza os atributos com os valores carregados, exceto available_themes
                for key, value in data.items():
                    if key == "available_themes": 
                        continue  # Pula este, não carrega
                    setattr(self, key, value)
    
    def save(self):
        # Salva as configurações atuais no arquivo
        with open(self.config_path, 'w') as f:
            json.dump({
                "theme": self.theme,
                "difficulty": self.difficulty,
                "volume": self.volume,
                "high_scores": self.high_scores
            }, f)