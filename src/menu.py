# Este código foi feito por Azam Usman
import pygame
from config import Config

class MenuSystem:
    def __init__(self):
        self.config = Config()   # Configurações
        self.main_menu = [   # Itens do menu principal
            "Play Classic",
            "Time Attack",
            "Survival Mode",
            "Options",
            "High Scores",
            "Quit"
        ]
        self.update_options_menu()   # Atualiza o menu de opções
        self.current_menu = "main"   # Menu atual
        self.selected_index = 0   # Índice do item selecionado
        self.menu_items_rects = []   # Retângulos dos itens para interação com mouse
    
    def update_options_menu(self):
        # Atualiza os itens do menu de opções com os valores atuais
        self.options_menu = [
            "Difficulty: " + self.config.difficulty.capitalize(),
            "Theme: " + self.config.theme.capitalize(),
            f"Volume: {int(self.config.volume * 100)}%",
            "Back"
        ]
        self.menus = {
            "main": self.main_menu,
            "options": self.options_menu
        }
    
    def handle_input(self, event, mouse_pos=None):
        # Trata entrada do mouse
        if mouse_pos:
            for i, rect in enumerate(self.menu_items_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_index = i   # Seleciona o item sob o mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return self._handle_selection()   # Clicou
        
        # Trata entrada do teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menus[self.current_menu])   # Move para cima
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menus[self.current_menu])   # Move para baixo
            elif event.key == pygame.K_RETURN:
                return self._handle_selection()   # Seleciona
            elif event.key == pygame.K_ESCAPE and self.current_menu != "main":
                self.current_menu = "main"   # Volta ao menu principal
                self.selected_index = 0
        return None
    
    def _handle_selection(self):
        # Executa a ação do item selecionado
        if self.current_menu == "main":
            if self.selected_index == 0:  # Play Classic
                return {"action": "start_game", "mode": "classic"}
            elif self.selected_index == 1:  # Time Attack
                return {"action": "start_game", "mode": "time_attack"}
            elif self.selected_index == 2:  # Survival
                return {"action": "start_game", "mode": "survival"}
            elif self.selected_index == 3:  # Options
                self.current_menu = "options"
                self.selected_index = 0
            elif self.selected_index == 4:  # High Scores
                return {"action": "show_scores"}
            elif self.selected_index == 5:  # Quit
                return {"action": "quit"}
        
        elif self.current_menu == "options":
            if self.selected_index == 0:  # Difficulty
                difficulties = ["easy", "medium", "hard"]
                current_index = difficulties.index(self.config.difficulty)
                self.config.difficulty = difficulties[(current_index + 1) % len(difficulties)]   # Cicla dificuldades
            elif self.selected_index == 1:  # Theme
                themes = list(self.config.available_themes)
                current_index = themes.index(self.config.theme)
                self.config.theme = themes[(current_index + 1) % len(themes)]   # Cicla temas
            elif self.selected_index == 2:  # Volume
                self.config.volume = (self.config.volume + 0.1) % 1.1   # Aumenta volume (módulo 1.1 para voltar a 0)
            elif self.selected_index == 3:  # Back
                self.current_menu = "main"
                self.selected_index = 3
                self.config.save()   # Salva configurações
            
            self.update_options_menu()   # Atualiza o menu de opções com novos valores
            return {"action": "theme_changed"}   # Indica que o tema pode ter mudado
    
    def get_current_menu(self):
        return self.menus[self.current_menu]   # Retorna os itens do menu atual
    
    def get_selected_index(self):
        return self.selected_index   # Retorna o índice selecionado