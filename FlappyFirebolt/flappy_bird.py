import pygame
import sys
import random
import time
from datetime import datetime
from firebolt.db import connect
from firebolt.client.auth.client_credentials import ClientCredentials
from dotenv import load_dotenv
import os

# Load Firebolt credentials from .env file
load_dotenv()
FIREBOLT_ENDPOINT = os.getenv("FIREBOLT_API_ENDPOINT")
FIREBOLT_ACCOUNT_ID = os.getenv("FIREBOLT_API_KEY")
FIREBOLT_ACCOUNT_SECRET = os.getenv("FIREBOLT_API_SECRET")
FIREBOLT_DATABASE = os.getenv("FIREBOLT_DATABASE")
FIREBOLT_ACCOUNT_NAME = os.getenv("FIREBOLT_ACCOUNT_NAME")
FIREBOLT_ENGINE = os.getenv("FIREBOLT_ENGINE")


# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 150
GRAVITY = 0.25
FLAP_STRENGTH = -5.0  # Decrease flap amount for less jump
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
BROWN = (222, 184, 135)
# Firebolt red color
FIREBOLT_RED = (255, 0, 51)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load bird image
BIRD_IMAGE = pygame.image.load("images/firebolt-logo.png").convert_alpha()
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))


def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def show_start_screen(player_name=None):
    screen.fill(BLUE)
    draw_text("Flappy Firebolt", 90, 100, BLACK)
    draw_text("Controls:", 140, 180, BLACK)
    draw_text("SPACE = Flap", 130, 220, BLACK)
    draw_text("R = Restart (after game over)", 60, 260, BLACK)
    if player_name:
        draw_text(f"Player: {player_name}", 120, 320, BLACK)
    draw_text("Press SPACE to start", 80, 400, BLACK)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(10)


def show_countdown():
    for count in ["3", "2", "1", "Go!"]:
        screen.fill(BLUE)
        draw_text(count, 180, 250, BLACK)
        pygame.display.flip()
        pygame.time.delay(700)


def get_player_name():
    name = ""
    active = True
    input_box = pygame.Rect(80, 300, 240, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 20 and event.unicode.isprintable():
                    name += event.unicode
        screen.fill(BLUE)
        draw_text("Enter your player name:", 60, 220, BLACK)
        txt_surface = font.render(name, True, BLACK)
        width = max(240, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text("Press Enter to continue", 80, 360, BLACK)
        pygame.display.flip()
        clock.tick(30)
    return name.strip()


def main():
    # Prompt for player name in the game window
    player_name = get_player_name()
    while True:
        show_start_screen(player_name)
        show_countdown()
        # Bird
        bird_x = 50
        bird_y = SCREEN_HEIGHT // 2
        bird_vel = 0
        score = 0
        pipes = []
        frame_count = 0
        running = True
        game_over = False
        result_saved = False
        pipe_speed = 3
        pipe_spawn_rate = 90
        min_pipe_gap = 110
        pipe_gap = PIPE_GAP
        # Stats
        total_flaps = 0
        flap_times = []
        last_flap_time = None
        min_y = bird_y
        max_y = bird_y
        max_speed = bird_vel
        min_speed = bird_vel
        start_time = time.time()
        total_obstacles_flapped = 0

        def reset():
            nonlocal bird_y, bird_vel, score, pipes, frame_count, running, game_over, result_saved
            nonlocal total_flaps, flap_times, last_flap_time, min_y, max_y, max_speed, min_speed, start_time, total_obstacles_flapped
            bird_y = SCREEN_HEIGHT // 2
            bird_vel = 0
            score = 0
            pipes = []
            frame_count = 0
            running = True
            game_over = False
            result_saved = False
            total_flaps = 0
            flap_times = []
            last_flap_time = None
            min_y = bird_y
            max_y = bird_y
            max_speed = bird_vel
            min_speed = bird_vel
            start_time = time.time()
            total_obstacles_flapped = 0

        while running:
            clock.tick(FPS)
            # Increase difficulty over time
            if frame_count % (FPS * 10) == 0 and frame_count > 0:  # Every 10 seconds
                pipe_speed += 1 if pipe_speed < 10 else 0
                pipe_spawn_rate = max(50, pipe_spawn_rate - 10)
                pipe_gap = max(min_pipe_gap, pipe_gap - 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not game_over:
                        bird_vel = FLAP_STRENGTH
                        total_flaps += 1
                        now = time.time()
                        if last_flap_time is not None:
                            flap_times.append(now - last_flap_time)
                        last_flap_time = now
                    if event.key == pygame.K_r and game_over:
                        running = False  # Return to start screen
                    if event.key == pygame.K_DELETE and game_over:
                        # Confirm reset
                        confirm = False
                        confirming = True
                        while confirming:
                            screen.fill((255,255,255))
                            draw_text("Are you sure you want to reset?", 30, 250, FIREBOLT_RED)
                            draw_text("Press Y to confirm, N to cancel", 30, 300, FIREBOLT_RED)
                            pygame.display.flip()
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if e.type == pygame.KEYDOWN:
                                    if e.key == pygame.K_y:
                                        confirm = True
                                        confirming = False
                                    elif e.key == pygame.K_n:
                                        confirming = False
                        if confirm:
                            reset_results_table()
            if not game_over:
                bird_vel += GRAVITY
                bird_y += bird_vel

                # Add pipes (more frequent as difficulty increases)
                if frame_count % pipe_spawn_rate == 0:
                    if pipes:
                        prev_gap_y = pipes[-1]["gap_y"]
                        max_delta = int(pipe_gap * 0.7)  # Allow at most 70% of the gap as vertical jump
                        min_y = max(100, prev_gap_y - max_delta)
                        max_y = min(SCREEN_HEIGHT - GROUND_HEIGHT - 100 - pipe_gap, prev_gap_y + max_delta)
                        gap_y = random.randint(min_y, max_y)
                    else:
                        gap_y = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100 - pipe_gap)
                    pipes.append({
                        "x": SCREEN_WIDTH,
                        "gap_y": gap_y
                    })
                # Occasionally add a second pipe for more obstacles
                if frame_count % (pipe_spawn_rate * 2) == 0 and frame_count > 0:
                    if pipes:
                        prev_gap_y = pipes[-1]["gap_y"]
                        max_delta = int(pipe_gap * 0.7)
                        min_y = max(100, prev_gap_y - max_delta)
                        max_y = min(SCREEN_HEIGHT - GROUND_HEIGHT - 100 - pipe_gap, prev_gap_y + max_delta)
                        gap_y2 = random.randint(min_y, max_y)
                    else:
                        gap_y2 = random.randint(100, SCREEN_HEIGHT - GROUND_HEIGHT - 100 - pipe_gap)
                    pipes.append({
                        "x": SCREEN_WIDTH + SCREEN_WIDTH // 2,
                        "gap_y": gap_y2
                    })

                # Move pipes
                for pipe in pipes:
                    pipe["x"] -= pipe_speed

                # Remove off-screen pipes
                pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]

                # Collision detection
                for pipe in pipes:
                    if (bird_x + BIRD_WIDTH > pipe["x"] and bird_x < pipe["x"] + PIPE_WIDTH):
                        if (bird_y < pipe["gap_y"] or bird_y + BIRD_HEIGHT > pipe["gap_y"] + pipe_gap):
                            game_over = True
                if bird_y < 0 or bird_y + BIRD_HEIGHT > SCREEN_HEIGHT - GROUND_HEIGHT:
                    game_over = True

                min_y = min(min_y, bird_y)
                max_y = max(max_y, bird_y)
                max_speed = max(max_speed, bird_vel)
                min_speed = min(min_speed, bird_vel)

                # Score
                for pipe in pipes:
                    if pipe["x"] + PIPE_WIDTH == bird_x:
                        score += 1
                        total_obstacles_flapped += 1
                frame_count += 1

            # Draw
            screen.fill((255,255,255))  # White background for contrast
            # Draw ground
            pygame.draw.rect(screen, FIREBOLT_RED, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
            # Draw bird (Firebolt logo)
            screen.blit(BIRD_IMAGE, (bird_x, int(bird_y)))
            # Draw pipes as Firebolt-red cylinder databases
            for pipe in pipes:
                # Top cylinder
                x = pipe["x"]
                y = 0
                h = pipe["gap_y"]
                w = PIPE_WIDTH
                # Draw cylinder body
                pygame.draw.rect(screen, FIREBOLT_RED, (x, y+10, w, h-10))
                # Draw top ellipse
                pygame.draw.ellipse(screen, FIREBOLT_RED, (x, y, w, 20))
                # Draw bottom ellipse (shaded)
                pygame.draw.ellipse(screen, (200,0,40), (x, y+h-20, w, 20))
                # Bottom cylinder
                y2 = pipe["gap_y"] + pipe_gap
                h2 = SCREEN_HEIGHT - GROUND_HEIGHT - y2
                if h2 > 0:
                    pygame.draw.rect(screen, FIREBOLT_RED, (x, y2+10, w, h2-10))
                    pygame.draw.ellipse(screen, FIREBOLT_RED, (x, y2, w, 20))
                    pygame.draw.ellipse(screen, (200,0,40), (x, y2+h2-20, w, 20))
            # Draw score
            draw_text(f"Score: {score}", 10, 10, FIREBOLT_RED)

            if game_over:
                draw_text("Game Over!", 120, SCREEN_HEIGHT // 2 - 30)
                draw_text(f"Final Score: {score}", 120, SCREEN_HEIGHT // 2)
                draw_text("Press R to return to start", 60, SCREEN_HEIGHT // 2 + 40)
                pygame.display.flip()
                if not result_saved:
                    total_game_time = time.time() - start_time
                    fastest_flap_speed = min(flap_times) if flap_times else 0
                    average_flap_speed = sum(flap_times)/len(flap_times) if flap_times else 0
                    save_result(player_name, score, total_game_time, total_flaps, total_obstacles_flapped, fastest_flap_speed, average_flap_speed, min_y, max_y, max_speed, min_speed)
                    result_saved = True
            else:
                pygame.display.flip()


def ensure_results_table(cursor):
    # Try to create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flappy_bird_results (
            player_name VARCHAR,
            score INT,
            created_at TIMESTAMP,
            total_game_time FLOAT,
            total_flaps INT,
            total_obstacles_flapped INT,
            fastest_flap_speed FLOAT,
            average_flap_speed FLOAT,
            min_y FLOAT,
            max_y FLOAT,
            max_speed FLOAT,
            min_speed FLOAT
        )
    ''')


def reset_results_table():
    try:
        auth = ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID, client_secret=FIREBOLT_ACCOUNT_SECRET)
        conn = connect(
            auth=auth,
            account_name=FIREBOLT_ACCOUNT_NAME,
            database=FIREBOLT_DATABASE,
            engine_name=FIREBOLT_ENGINE,
            api_endpoint=FIREBOLT_ENDPOINT
        )
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS flappy_bird_results')
        ensure_results_table(cursor)
        conn.commit()
        cursor.close()
        conn.close()
        print("Results table reset!")
    except Exception as e:
        print(f"Failed to reset results table: {e}")


def save_result(player_name, score, total_game_time, total_flaps, total_obstacles_flapped, fastest_flap_speed, average_flap_speed, min_y, max_y, max_speed, min_speed):
    try:
        auth = ClientCredentials(client_id=FIREBOLT_ACCOUNT_ID, client_secret=FIREBOLT_ACCOUNT_SECRET)
        conn = connect(
            auth=auth,
            account_name=FIREBOLT_ACCOUNT_NAME,
            database=FIREBOLT_DATABASE,
            engine_name=FIREBOLT_ENGINE,
            api_endpoint=FIREBOLT_ENDPOINT
        )
        cursor = conn.cursor()
        ensure_results_table(cursor)
        cursor.execute(
            "INSERT INTO flappy_bird_results (player_name, score, created_at, total_game_time, total_flaps, total_obstacles_flapped, fastest_flap_speed, average_flap_speed, min_y, max_y, max_speed, min_speed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (player_name, score, datetime.now(), total_game_time, total_flaps, total_obstacles_flapped, fastest_flap_speed, average_flap_speed, min_y, max_y, max_speed, min_speed)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Result saved to Firebolt!")
    except Exception as e:
        print(f"Failed to save result: {e}")


if __name__ == "__main__":
    main()