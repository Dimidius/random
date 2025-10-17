import pygame as pg
from random import randrange
import json, os

# I now need to make the scores save to the new_tricks file and read it out and store it as dabloons? 
# Or should I make it check if the score is over 20 and then give 5 dabloons or something?

# === CONFIG ===
WINDOW = 1000
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
SAVE_FILE = "FinalProject/files/highscore.json"

# === HELPER FUNCTIONS ===
def get_random_position():
    return [randrange(*RANGE), randrange(*RANGE)]

def load_high_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (json.JSONDecodeError, FileNotFoundError):
            return 0
    return 0

def save_high_score(score):
    with open(SAVE_FILE, "w") as f:
        json.dump({"high_score": score}, f)


# === GAME LOOP ===
def start_game(screen):
    snake = pg.rect.Rect([0, 0], [TILE_SIZE - 2, TILE_SIZE - 2])
    snake.center = get_random_position()
    snake_dir = (0, 0)
    time, timestep = 0, 110
    food = snake.copy()
    food.center = get_random_position()
    length = 1
    segments = [snake.copy()]
    clock = pg.time.Clock()
    dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}

    score = 0
    high_score = load_high_score()  # Load saved high score

    pg.font.init()
    font = pg.font.Font(None, 36)
    go_font = pg.font.Font(None, 80)
    game_over = False

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return "quit"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return "menu"
                if not game_over:
                    if event.key == pg.K_UP and dirs[pg.K_UP]:
                        snake_dir = (0, -TILE_SIZE)
                        dirs = {pg.K_UP: 1, pg.K_DOWN: 0, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                    if event.key == pg.K_DOWN and dirs[pg.K_DOWN]:
                        snake_dir = (0, TILE_SIZE)
                        dirs = {pg.K_UP: 0, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 1}
                    if event.key == pg.K_LEFT and dirs[pg.K_LEFT]:
                        snake_dir = (-TILE_SIZE, 0)
                        dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 1, pg.K_RIGHT: 0}
                    if event.key == pg.K_RIGHT and dirs[pg.K_RIGHT]:
                        snake_dir = (TILE_SIZE, 0)
                        dirs = {pg.K_UP: 1, pg.K_DOWN: 1, pg.K_LEFT: 0, pg.K_RIGHT: 1}

        # === Move the snake ===
        time_now = pg.time.get_ticks()
        if time_now - time > timestep:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]

            # Food collision
            if snake.center == food.center:
                food.center = get_random_position()
                length += 1
                score += 1

                # Update high score
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)

            # Wall collision resets the game
            if (
                snake.left < 0 or snake.right > WINDOW
                or snake.top < 0 or snake.bottom > WINDOW
            ):
                # Reset snake
                snake.center = get_random_position()
                snake_dir = (0, 0)
                length = 1
                score = 0
                segments = [snake.copy()]

        # === Draw everything ===
        screen.fill("black")
        pg.draw.rect(screen, "red", food)
        [pg.draw.rect(screen, "green", segment) for segment in segments]

        # Score display
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 50))

        pg.display.flip()
        clock.tick(60)

# === MENU SCREEN ===
def main_menu():
    pg.init()
    screen = pg.display.set_mode([WINDOW] * 2)
    pg.display.set_caption("Snake Menu")
    font = pg.font.Font(None, 80)
    small_font = pg.font.Font(None, 50)
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if start_rect.collidepoint(mouse_pos):
                    result = start_game(screen)
                    if result == "quit":
                        return
                if quit_rect.collidepoint(mouse_pos):
                    pg.quit()
                    return

        screen.fill((20, 20, 20))
        title = font.render("Snake", True, (0, 255, 0))
        title_rect = title.get_rect(center=(WINDOW // 2, WINDOW // 2 - 150))
        screen.blit(title, title_rect)

        start_rect = pg.Rect(WINDOW // 2 - 150, WINDOW // 2 - 20, 300, 60)
        pg.draw.rect(screen, (0, 120, 0), start_rect, border_radius=10)
        start_text = small_font.render("START GAME", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=start_rect.center))

        quit_rect = pg.Rect(WINDOW // 2 - 150, WINDOW // 2 + 70, 300, 60)
        pg.draw.rect(screen, (120, 0, 0), quit_rect, border_radius=10)
        quit_text = small_font.render("QUIT", True, (255, 255, 255))
        screen.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
