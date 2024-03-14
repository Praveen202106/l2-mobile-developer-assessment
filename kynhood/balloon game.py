import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALLOON_RADIUS = 30
TIMER_SECONDS = 4  # 2 minutes
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BALLOON_SPEED_RANGE = (0, 1)  # Adjust the speed range here

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Pop Mania")

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
score = 0
balloons_popped = 0
balloons_missed = 0
timer = TIMER_SECONDS
game_over = False
start_screen = True
end_screen = False

# Balloon class
class Balloon(pygame.sprite.Sprite):
    def __init__(self, speed, color):
        super().__init__()
        self.speed = speed
        self.color = color
        self.image = pygame.Surface((BALLOON_RADIUS * 2, BALLOON_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (BALLOON_RADIUS, BALLOON_RADIUS), BALLOON_RADIUS)
        self.rect = self.image.get_rect(center=(random.randint(BALLOON_RADIUS, SCREEN_WIDTH - BALLOON_RADIUS), SCREEN_HEIGHT))

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            global balloons_missed
            balloons_missed += 1
            global score
            score -= 1
            self.kill()

    def blast(self):
        # Add blasting effect here
        self.kill()
        global score
        score += 10  # Increase the score when blasting a balloon

# Create sprite groups
all_sprites = pygame.sprite.Group()
balloons = pygame.sprite.Group()

# Timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Start screen
def draw_start_screen():
    screen.fill(WHITE)
    title_text = font.render("Balloon Pop Mania", True, RED)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    start_text = font.render("Click to Start", True, BLUE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    

    pygame.display.flip()

# End screen
def draw_end_screen():
    screen.fill(WHITE)
    final_score_text = font.render(f"Final Score: {score}", True, RED)
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    
    balloons_text = font.render(f"Balloons Popped: {balloons_missed - (-score)}", True, RED)
    screen.blit(balloons_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

    missed_text = font.render(f"Balloons Missed: {balloons_missed}", True, RED)
    screen.blit(missed_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))

    play_again_text = font.render("Click to Play Again", True, BLUE)
    screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50 + 50))

    


    pygame.display.flip()

# Game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            timer -= 1
            if timer <= 0:
                game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [sprite for sprite in balloons if sprite.rect.collidepoint(pos)]
            for balloon in clicked_sprites:
                balloon.blast()  # Blast the balloon when clicked

    # Create new balloons with random speed within the adjusted speed range
    if random.randint(0, 100) < 5:
        colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE]
        color = random.choice(colors)
        new_speed = random.randint(BALLOON_SPEED_RANGE[1], BALLOON_SPEED_RANGE[1])
        new_balloon = Balloon(new_speed, color)
        all_sprites.add(new_balloon)
        balloons.add(new_balloon)

    # Update sprites
    all_sprites.update()

    # Clear screen
    screen.fill(WHITE)

    # Draw sprites
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    # Display timer
    timer_text = font.render(f"Time Left: {timer // 60}:{timer % 60:02}", True, BLUE)
    screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))

    # Update display
    pygame.display.flip()

    # Check if time is up
    if timer <= 0:
        game_over = True

# Display end screen
draw_end_screen()



# Delay before returning to start screen
time.sleep(10)

# End screen loop
while end_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Reset game variables
            score = 0
            balloons_popped = 0
            balloons_missed = 0
            timer = TIMER_SECONDS
            game_over = False
            start_screen = True
            end_screen = False
            # Clear sprites
            all_sprites.empty()
            balloons.empty()
            # Return to start screen
            while start_screen:
                draw_start_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        start_screen = False
