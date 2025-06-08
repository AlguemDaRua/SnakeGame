# Este código foi feito por Azam Usman
import pygame
import sys
import time
from game import SnakeGame
from menu import MenuSystem
from renderer import Renderer
from audio import AudioManager
from highscore import HighScoreManager
from config import Config

def main():
    pygame.init()
    pygame.display.set_caption("Ultimate Snake Game")
    
    config = Config()   # Configurações
    screen = pygame.display.set_mode((config.screen_width, config.screen_height))   # Tela
    clock = pygame.time.Clock()   # Relógio para controlar FPS
    
    game = SnakeGame()   # Inicializa o jogo
    menu = MenuSystem()   # Sistema de menu
    renderer = Renderer(screen)   # Renderizador
    audio = AudioManager()   # Áudio (desligado)
    high_scores = HighScoreManager()   # Gerenciador de pontuações
    
    game_state = "menu"   # Estado inicial: menu
    current_mode = "classic"   # Modo atual
    last_time = time.time()   # Tempo do último frame
    
    while True:
        # Calcula delta time (tempo entre frames)
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        mouse_pos = pygame.mouse.get_pos()   # Posição do mouse
        
        # Trata eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                config.save()   # Salva configurações
                pygame.quit()
                sys.exit()
            
            if game_state == "menu":
                # Trata entrada no menu
                action = menu.handle_input(event, mouse_pos)
                if action:
                    if action.get("action") == "start_game":
                        game.reset(action["mode"])   # Começa o jogo no modo escolhido
                        game_state = "playing"
                        current_mode = action["mode"]
                    elif action.get("action") == "quit":
                        config.save()
                        pygame.quit()
                        sys.exit()
                    elif action.get("action") == "show_scores":
                        game_state = "scores"   # Mostra pontuações
                    elif action.get("action") == "theme_changed":
                        # Tema mudou, não precisa de ação especial
                        pass
            
            elif game_state == "playing":
                state = game.get_state()
                if state["waiting_for_respawn"]:
                    # Esperando renascer: qualquer tecla reinicia
                    if event.type == pygame.KEYDOWN:
                        game.trigger_respawn()
                else:
                    game.handle_input(event)   # Passa entrada para o jogo
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        game_state = "menu"   # Volta ao menu
            
            elif game_state in ["game_over", "scores"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        game_state = "menu"   # Volta ao menu
        
        # Atualiza estado do jogo
        if game_state == "playing":
            state = game.get_state()
            if not state["waiting_for_respawn"]:
                game.update(dt)   # Atualiza o jogo
                state = game.get_state()
                if state["game_over"]:
                    # Atualiza pontuação e vai para tela de game over
                    high_scores.update_score(current_mode, state["score"])
                    game_state = "game_over"
                    audio.play("game_over")   # Som de game over (desligado)
        
        # Renderiza
        if game_state == "menu":
            renderer.draw_menu(menu.get_current_menu(), menu.get_selected_index())
        elif game_state == "playing":
            state = game.get_state()
            if state["waiting_for_respawn"]:
                # Desenha o jogo pausado e mensagem de renascimento
                renderer.draw_game(
                    state["snake"], 
                    state["food"], 
                    state["bombs"],
                    state["score"],
                    state["mode"],
                    state["time_remaining"],
                    state["max_time"],
                    state["lives"]
                )
                renderer.draw_waiting_for_respawn(state["lives"])
            else:
                # Desenha o jogo normalmente
                renderer.draw_game(
                    state["snake"], 
                    state["food"], 
                    state["bombs"],
                    state["score"],
                    state["mode"],
                    state["time_remaining"],
                    state["max_time"],
                    state["lives"]
                )
        elif game_state == "game_over":
            state = game.get_state()
            renderer.draw_game_over(
                state["score"], 
                high_scores.get_scores()[current_mode],
                current_mode
            )
        elif game_state == "scores":
            renderer.draw_high_scores(high_scores.get_scores())
        
        pygame.display.flip()   # Atualiza a tela
        
        # Controla a velocidade do jogo
        if game_state == "playing":
            state = game.get_state()
            clock.tick(state["current_speed"])   # Usa a velocidade atual da cobra
        else:
            clock.tick(60)   # 60 FPS no menu

if __name__ == "__main__":
    main()