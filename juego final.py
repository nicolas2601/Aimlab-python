import pygame
import random
import sys


WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
BACKGROUND_COLOR = (255, 255, 255) 


TARGET_IMAGE = pygame.image.load('ladron.png')

NEGATIVE_IMAGE = pygame.transform.scale(pygame.image.load('tombo.png'), (200, 200))


TARGET_LIFETIME = 1000  
MAX_TARGETS = 1  #
SCORE_DECREASE = 5  
GAME_SPEED_INCREASE = 0.00001 
GAME_FONT_SIZE = 36


CURSOR_IMAGE = pygame.transform.scale(pygame.image.load('custom_cursor.png'), (80, 80))


MARGIN_TOP = 50
MARGIN_LEFT = 50
MARGIN_BOTTOM = HEIGHT - 50
MARGIN_RIGHT = WIDTH - 50


pygame.init()

class Target:
    def __init__(self, image, score_value):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.active = True
        self.lifetime = TARGET_LIFETIME
        self.score_value = score_value

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.deactivate()

    def deactivate(self):
        self.active = False

    def reset(self):
        self.active = True
        self.lifetime = TARGET_LIFETIME
        self.rect.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))

def main_game():
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)  
    pygame.display.set_caption("Aim Lab")


    pygame.mouse.set_visible(False) 
    custom_cursor = CURSOR_IMAGE

    targets = [Target(TARGET_IMAGE, 1)]
    negative_targets = [Target(NEGATIVE_IMAGE, -5)]
    score = 1
    game_over = False
    game_speed = 1.0

    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                for target in targets:
                    if target.active and target.rect.collidepoint(x, y):
                        target.deactivate()
                        score += target.score_value
                        pygame.mouse.set_pos(WIDTH // 2, HEIGHT // 2)
                        break  

                for negative_target in negative_targets:
                    if negative_target.active and negative_target.rect.collidepoint(x, y):
                        negative_target.deactivate()
                        score += negative_target.score_value

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        dt = clock.tick(60)  
        game_speed += GAME_SPEED_INCREASE * score  

        for target in targets:
            target.update(int(dt * game_speed))

        for negative_target in negative_targets:
            negative_target.update(int(dt * game_speed))

        targets = [target for target in targets if target.active]
        negative_targets = [target for target in negative_targets if target.active]

        while len(targets) < MAX_TARGETS:
            targets.append(Target(TARGET_IMAGE, 1))
            if score > 1:  
                negative_targets.append(Target(NEGATIVE_IMAGE, -5))

        if score < 0:
            score = 0

        if score == 0:
            game_over = True

        screen.fill(BACKGROUND_COLOR)

        for target in targets:
            target.draw(screen)

        for negative_target in negative_targets:
            negative_target.draw(screen)

        font = pygame.font.Font(None, GAME_FONT_SIZE)
        text = font.render(f"Puntuación: {score}", True, (0, 0, 0)) 
        screen.blit(text, (10, 10))

        if game_over:
            text = font.render("Juego terminado. Presiona R para reiniciar o ESC para salir.", True, (255, 0, 0))  # Texto en rojo
            screen.blit(text, (WIDTH // 2 - 300, HEIGHT // 2))

            pygame.display.update()

            restart_timer = pygame.time.get_ticks()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_r:
                            return True
                if pygame.time.get_ticks() - restart_timer > 5000:  
                    return False


        cursor_x, cursor_y = pygame.mouse.get_pos()
        cursor_x = max(min(cursor_x, MARGIN_RIGHT), MARGIN_LEFT)
        cursor_y = max(min(cursor_y, MARGIN_BOTTOM), MARGIN_TOP)
        screen.blit(custom_cursor, (cursor_x, cursor_y))
        pygame.display.update()

if __name__ == "__main__":
    while True:
        main_game()
