import pygame
import random

pygame.init()

WIDTH = 1080
HEIGHT = 720
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

background_img = pygame.image.load("background.png").convert()
bird_img = pygame.image.load("bird.png").convert_alpha()
pipe_img = pygame.image.load("pipe.png").convert_alpha()
base_img = pygame.image.load("base.png").convert_alpha()

# Variables
gravity = 0.7
bird_movement = 0
score = 0
high_score = 0
game_font = pygame.font.Font(None, 80) #BY Default Font for all

# Bird class
class Bird:
    def __init__(self):
        self.x = 300
        self.y = HEIGHT//2 - 100
        self.jump = -10
        self.bird_rect = bird_img.get_rect(center=(self.x, self.y))

    def update(self):
        self.bird_rect.centery += bird_movement

    def draw(self):
        window.blit(bird_img, self.bird_rect)

    def jump_bird(self):
        global bird_movement
        bird_movement = self.jump

    def reset_position(self):
        self.bird_rect.center = (self.x, self.y)

# Pipe class
class Pipe:
    def __init__(self):
        self.pipe_height = [300, 400, 500]
        self.pipe_pos = random.choice(self.pipe_height)
        self.pipe_rect_top = pipe_img.get_rect(midbottom=(WIDTH + 200, self.pipe_pos - 200))
        self.pipe_rect_bottom = pipe_img.get_rect(midtop=(WIDTH + 200, self.pipe_pos + 200))
        self.scored = False

    def update(self):
        self.pipe_rect_top.centerx -= 10
        self.pipe_rect_bottom.centerx -= 10

    def draw(self):
        window.blit(pygame.transform.flip(pipe_img, False, True), self.pipe_rect_bottom)
        window.blit(pipe_img, self.pipe_rect_top)

    def collision(self):
        if self.pipe_rect_top.colliderect(bird.bird_rect) or self.pipe_rect_bottom.colliderect(bird.bird_rect):
            return True
        return False

    def passed(self):
        if self.pipe_rect_top.right < bird.bird_rect.left and not self.scored:
            self.scored = True
            return True
        return False

# Base class
class Base:
    def __init__(self):
        self.x_pos = 0
        self.y_pos = HEIGHT - base_img.get_height()

    def update(self):
        self.x_pos -= 10

        if self.x_pos <= -base_img.get_width():
            self.x_pos = 0

    def draw(self):
        window.blit(base_img, (self.x_pos, self.y_pos))
        window.blit(base_img, (self.x_pos + base_img.get_width(), self.y_pos))

bird = Bird()
pipes = [Pipe()]
base = Base()

class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.button_font = pygame.font.Font(None, 35)

    def draw(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect)
        text = self.button_font.render("Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        window.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


restart_button = Button((WIDTH-150) // 2, HEIGHT // 2 - 60, 150, 50)



# Game loop
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird.jump_bird()
            if event.key == pygame.K_RETURN and game_over:
                game_over = False
                bird_movement = 0
                score = 0
                bird.reset_position()
                pipes = [Pipe()]


        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.is_clicked(mouse_pos):
                game_over = False
                bird_movement = 0
                score = 0
                bird.reset_position()
                pipes = [Pipe()]

    if not game_over:
        bird_movement += gravity
        bird.update()

        for pipe in pipes:
            pipe.update()
            if pipe.collision():
                game_over = True
                if score > high_score:
                    high_score = score

            if pipe.passed():
                score += 1

        # Check if pipes need to be added
        if pipes[-1].pipe_rect_top.centerx < WIDTH - 400:
            new_pipe = Pipe()
            pipes.append(new_pipe)

        # Remove pipes that are out of the screen
        if pipes[0].pipe_rect_top.right < 0:
            pipes.pop(0)

        base.update()



        # Check if bird hits the ground
        if bird.bird_rect.bottom >= HEIGHT - base_img.get_height():
            game_over = True
            if score > high_score:
                high_score = score


    # Draw objects
    window.blit(background_img, (0, 0))

    for pipe in pipes:
        pipe.draw()

    bird.draw()
    base.draw()

    # Display the score
    score_text = game_font.render(f"Score: {score}", True, (0, 0, 0))
    window.blit(score_text, (10, 10))

    high_score_text = game_font.render(f"High Score: {high_score}", True, (0, 0, 0))
    window.blit(high_score_text, (10, 70))

    if game_over:
        restart_button.draw()
        game_over_text = game_font.render("Game Over", True, (255, 0, 0))
        window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
