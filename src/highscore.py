# Este código foi feito por Azam Usman
import json
import os

class HighScoreManager:
    def __init__(self):
        self.file_path = os.path.expanduser("~/.snake_high_scores.json")   # Caminho do arquivo de pontuações
        self.scores = self._load_scores()   # Carrega as pontuações
    
    def _load_scores(self):
        # Carrega as pontuações do arquivo, se existir
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                return json.load(f)
        # Inicializa com zero para todos os modos
        return {
            "classic": 0, 
            "time_attack": 0, 
            "survival": 0
        }
    
    def save_scores(self):
        # Salva as pontuações no arquivo
        with open(self.file_path, 'w') as f:
            json.dump(self.scores, f)
    
    def update_score(self, mode, score):
        # Atualiza a pontuação de um modo se for maior que a atual
        if score > self.scores.get(mode, 0):
            self.scores[mode] = score
            self.save_scores()
    
    def get_scores(self):
        # Retorna todas as pontuações
        return self.scores