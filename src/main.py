import sys

import pygame

from Alien import Alien
from Boss import Boss
from Bullet import Bullet
from Shuttle import Shuttle
from constants import (
    ALIEN_EDGE_PADDING,
    ALIEN_HORIZONTAL_SPEED,
    ALIEN_VERTICAL_SPEED,
    BULLET_SPEED,
    COLLISION_COOLDOWN_MS,
    FPS,
    INITIAL_BOSS_POSITION,
    INITIAL_SHUTTLE_POSITION,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHUTTLE_DAMAGE,
    SHUTTLE_HP,
    asset_path,
)


def create_aliens():
    aliens = []
    rows = [
        (0, SCREEN_HEIGHT - 650),
        (10, SCREEN_HEIGHT - 500),
        (20, SCREEN_HEIGHT - 350),
    ]

    for row_offset, y in rows:
        for column in range(10):
            alien_id = row_offset + column + 1
            aliens.append(Alien(f"Alien {alien_id}", [SCREEN_WIDTH - 77 * (column + 1), y]))

    return aliens


def draw_status(screen, font, shuttle):
    hp = max(0, shuttle.get_hp())
    if hp >= 70:
        hp_color = (0, 255, 0)
    elif hp >= 40:
        hp_color = (255, 255, 0)
    else:
        hp_color = (255, 0, 0)

    hp_label = font.render("hp: ", True, (255, 255, 255))
    hp_value = font.render(f"{hp}", True, hp_color)
    screen.blit(hp_label, (10, 10))
    screen.blit(hp_value, (45, 10))

    score_label = font.render("score: ", True, (255, 255, 255))
    score_value = font.render(f"{shuttle.get_score()}", True, (0, 0, 255))
    screen.blit(score_label, (SCREEN_WIDTH - 95, 10))
    screen.blit(score_value, (SCREEN_WIDTH - 25, 10))


def draw_centered_message(screen, background, title_font, text_font, title, shuttle=None):
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    text = title_font.render(title, True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))

    if shuttle is not None:
        final_score_label = text_font.render("Final Score: ", True, (255, 255, 255))
        final_score = text_font.render(f"{shuttle.get_score() * max(0, shuttle.get_hp())}", True, (0, 255, 255))
        screen.blit(final_score_label, (SCREEN_WIDTH - 480, 500))
        screen.blit(final_score, (SCREEN_WIDTH - 370, 500))


def update_aliens(aliens, direction, dt):
    living_aliens = [alien for alien in aliens if not alien.get_is_dead()]
    if not living_aliens:
        return direction

    for alien in living_aliens:
        alien.move_down(ALIEN_VERTICAL_SPEED * dt)
        alien.move_horizontal(direction * ALIEN_HORIZONTAL_SPEED * dt)

    left_edge = min(alien.get_rect().left for alien in living_aliens)
    right_edge = max(alien.get_rect().right for alien in living_aliens)
    if left_edge <= ALIEN_EDGE_PADDING:
        return 1
    if right_edge >= SCREEN_WIDTH - ALIEN_EDGE_PADDING:
        return -1

    return direction


def handle_player_input(shuttle, dt):
    keys = pygame.key.get_pressed()
    dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

    if dx or dy:
        shuttle.move(dx, dy, dt)

    if keys[pygame.K_SPACE]:
        shuttle.shoot()

    return not keys[pygame.K_ESCAPE]


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Py-Space-Invaders")

    background = pygame.image.load(asset_path("background.png")).convert()
    font_game_over = pygame.font.SysFont("uroob", 180)
    font_text = pygame.font.SysFont("uroob", 30)
    clock = pygame.time.Clock()

    shuttle = Shuttle("Apollo13", SHUTTLE_HP, INITIAL_SHUTTLE_POSITION, PLAYER_SPEED)
    bullet = Bullet([shuttle.get_position()[0] + 20, shuttle.get_position()[1] - 10], BULLET_SPEED)
    boss = Boss("Alienoooo", 100, INITIAL_BOSS_POSITION)
    aliens = create_aliens()

    alien_direction = -1
    last_collision_time = 0
    game_state = "playing"
    running = True

    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_state == "playing":
            running = handle_player_input(shuttle, dt)
            alien_direction = update_aliens(aliens, alien_direction, dt)

            if shuttle.get_shot():
                bullet.move_bullet(dt)
            else:
                bullet.set_pos([shuttle.get_position()[0] + 20, shuttle.get_position()[1] - 10])

            if bullet.get_pos()[1] < -bullet.get_rect().height:
                shuttle.set_shot(False)

            for alien in aliens:
                if bullet.collision(alien):
                    alien.die()
                    shuttle.set_shot(False)
                    shuttle.score_up()
                    bullet.set_pos([shuttle.get_position()[0] + 20, shuttle.get_position()[1] - 10])
                    break

            now = pygame.time.get_ticks()
            if now - last_collision_time > COLLISION_COOLDOWN_MS:
                for alien in aliens:
                    if not alien.get_is_dead() and shuttle.get_rect().colliderect(alien.get_rect()):
                        shuttle.take_damage(SHUTTLE_DAMAGE)
                        last_collision_time = now
                        break

            if shuttle.get_is_dead():
                game_state = "game_over"
            elif shuttle.get_score() == len(aliens):
                game_state = "win"

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        if game_state == "playing":
            shuttle.draw_shuttle(screen)
            for alien in aliens:
                alien.draw_alien(screen)
            boss.draw_boss(screen)
            if shuttle.get_shot():
                bullet.draw_bullet(screen)
            draw_status(screen, font_text, shuttle)
        elif game_state == "win":
            draw_centered_message(screen, background, font_game_over, font_text, "You Win!!!", shuttle)
        else:
            draw_centered_message(screen, background, font_game_over, font_text, "Game Over :(")

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
