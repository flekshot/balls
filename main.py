import pygame
import random
import time

# pygame start
pygame.init()

# windows
window_width = 1700
window_height = 880

# display
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Arcade Ball Game')

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

# fps
fps = 60
clock = pygame.time.Clock()

# ball properties
ball_radius = 10
ball_x = window_width // 2
ball_y = window_height // 2
ball_dx = 5
ball_dy = -5  # ball always start going up

# player paddle properties
paddle_width = 150  # increased paddle width
paddle_height = 15  # increased paddle height
paddle_x = (window_width - paddle_width) // 2
paddle_y = window_height - paddle_height - 10
paddle_dx = 10

# state
game_over = False
score = 0
start_time = time.time()
difficulty_increase_interval = 10  # speed up every 10 sec
last_difficulty_increase_time = start_time
photo_appearance_interval = 10  # photos every 10 sec
photo_disappearance_interval = 5  # photos disappear every 5 sec
last_photo_appearance_time = start_time

# font
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)

# sounds
bounce_sound = pygame.mixer.Sound('assets/bounce.wav')
pygame.mixer.music.load('assets/background_music.mp3')

# images load
background_image = pygame.image.load('assets/background_image.jpg')
background_image = pygame.transform.scale(background_image, (window_width, window_height))
photo1 = pygame.image.load('assets/photo1.png')
photo2 = pygame.image.load('assets/photo2.png')
photo_size = (100, 100)  # increased image size to 100x100
photo1 = pygame.transform.scale(photo1, photo_size)
photo2 = pygame.transform.scale(photo2, photo_size)
photo_positions = []
photos_visible = False

# particle
particles = []

def show_game_over():
    game_over_text = font.render('Game Over', True, red)
    restart_button_text = font.render('Restart', True, green)
    window.blit(game_over_text, (window_width // 2 - game_over_text.get_width() // 2, window_height // 2 - 50))
    restart_button_rect = restart_button_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
    window.blit(restart_button_text, restart_button_rect)
    # outline for button
    pygame.draw.rect(window, green, restart_button_rect.inflate(20, 10), 2)
    return restart_button_rect

# game restart
def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, game_over, score, start_time, particles, last_difficulty_increase_time, photo_positions, photos_visible, last_photo_appearance_time
    ball_x = window_width // 2
    ball_y = window_height // 2
    ball_dx = random.choice([-5, 5])
    ball_dy = -5
    paddle_x = (window_width - paddle_width) // 2
    game_over = False
    score = 0
    start_time = time.time()
    last_difficulty_increase_time = start_time
    last_photo_appearance_time = start_time
    particles = []
    photo_positions = []
    photos_visible = False

# score and timer
def draw_score_and_timer():
    elapsed_time = int(time.time() - start_time)
    score_text = small_font.render(f'Score: {score}', True, white)
    timer_text = small_font.render(f'Time: {elapsed_time}s', True, white)
    window.blit(score_text, (10, 10))
    window.blit(timer_text, (10, 50))

def create_particles(x, y):
    for _ in range(10):
        particles.append([x, y, random.randint(1, 4), random.randint(-3, 3), random.randint(-3, 3)])

def draw_particles():
    for particle in particles[:]:
        pygame.draw.circle(window, yellow, (particle[0], particle[1]), particle[2])
        particle[0] += particle[3]
        particle[1] += particle[4]
        particle[2] -= 0.1
        if particle[2] <= 0:
            particles.remove(particle)

def increase_difficulty():
    global ball_dx, ball_dy
    ball_dx *= 1.2
    ball_dy *= 1.2

def add_photos():
    global photo_positions, photos_visible
    x1, y1 = random.randint(0, window_width - photo_size[0]), random.randint(0, window_height - photo_size[1])
    x2, y2 = random.randint(0, window_width - photo_size[0]), random.randint(0, window_height - photo_size[1])
    photo_positions = [(photo1, (x1, y1)), (photo2, (x2, y2))]
    photos_visible = True

def remove_photos():
    global photos_visible
    photos_visible = False

def menu():
    menu_text = font.render('Arcade Ball Game', True, black)
    start_button_text = font.render('Start', True, green)
    quit_button_text = font.render('Quit', True, red)
    start_button_rect = start_button_text.get_rect(center=(window_width // 2, window_height // 2))
    quit_button_rect = quit_button_text.get_rect(center=(window_width // 2, window_height // 2 + 100))

    while True:
        window.fill(white)
        window.blit(menu_text, (window_width // 2 - menu_text.get_width() // 2, window_height // 2 - 200))
        window.blit(start_button_text, start_button_rect)
        window.blit(quit_button_text, quit_button_rect)
        pygame.draw.rect(window, green, start_button_rect.inflate(20, 10), 2)
        pygame.draw.rect(window, red, quit_button_rect.inflate(20, 10), 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    return
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()

# start background music
pygame.mixer.music.play(-1)  # play indefinitely

# game loop
menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = event.pos
            if restart_button_rect.collidepoint(mouse_x, mouse_y):
                restart_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_dx
    if keys[pygame.K_RIGHT] and paddle_x < window_width - paddle_width:
        paddle_x += paddle_dx

    if not game_over:
        # ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # ball collision w walls
        if ball_x <= ball_radius or ball_x >= window_width - ball_radius:
            ball_dx = -ball_dx
            bounce_sound.play()
        if ball_y <= ball_radius:
            ball_dy = -ball_dy
            bounce_sound.play()

        # ball collision w paddle
        if (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and
                paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_dy = -ball_dy
            score += 1  # score +1 when ball hit paddle
            bounce_sound.play()
            create_particles(ball_x, ball_y)

        # ball collision w photos
        if photos_visible:
            for photo, pos in photo_positions:
                photo_rect = pygame.Rect(pos[0], pos[1], photo_size[0], photo_size[1])
                if photo_rect.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                    if ball_x - ball_radius < photo_rect.right and ball_dx > 0:
                        ball_dx = -ball_dx
                    elif ball_x + ball_radius > photo_rect.left and ball_dx < 0:
                        ball_dx = -ball_dx
                    if ball_y - ball_radius < photo_rect.bottom and ball_dy > 0:
                        ball_dy = -ball_dy
                    elif ball_y + ball_radius > photo_rect.top and ball_dy < 0:
                        ball_dy = -ball_dy
                    bounce_sound.play()

        # ball things
        if ball_y >= window_height - ball_radius:
            game_over = True

        # difficulty over time
        current_time = time.time()
        if current_time - last_difficulty_increase_time >= difficulty_increase_interval:
            increase_difficulty()
            last_difficulty_increase_time = current_time

        # photo appearance
        if current_time - last_photo_appearance_time >= photo_appearance_interval:
            add_photos()
            last_photo_appearance_time = current_time
        elif current_time - last_photo_appearance_time >= photo_disappearance_interval:
            remove_photos()

    # screen
    window.blit(background_image, (0, 0))

    if game_over:
        restart_button_rect = show_game_over()
    else:
        # ball
        pygame.draw.circle(window, red, (ball_x, ball_y), ball_radius)

        # paddle
        pygame.draw.rect(window, blue, (paddle_x, paddle_y, paddle_width, paddle_height))

        # score and timer
        draw_score_and_timer()

        # particles
        draw_particles()

        # photos
        if photos_visible:
            for photo, pos in photo_positions:
                window.blit(photo, pos)

    # updates the display
    pygame.display.update()

    # cap for frame rate
    clock.tick(fps)

# stop background music and quit
pygame.mixer.music.stop()
pygame.quit()