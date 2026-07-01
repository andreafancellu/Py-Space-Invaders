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
    BOSS_DAMAGE,
    BOSS_HIT_DAMAGE,
    BOSS_BULLET_SCALE,
    BULLET_SPEED,
    COLLISION_COOLDOWN_MS,
    FPS,
    INITIAL_BOSS_POSITION,
    INITIAL_SHUTTLE_POSITION,
    LEVELS,
    PLAYER_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHUTTLE_DAMAGE,
    SHUTTLE_HP,
    asset_path,
)


def create_aliens(level):
    aliens = []
    rows = [
        (0, SCREEN_HEIGHT - 650),
        (10, SCREEN_HEIGHT - 500),
        (20, SCREEN_HEIGHT - 350),
    ]

    for row_offset, y in rows:
        for column in range(10):
            alien_id = row_offset + column + 1
            aliens.append(
                Alien(
                    f"Alien {alien_id}",
                    [SCREEN_WIDTH - 77 * (column + 1), y],
                    level["alien_tint"],
                )
            )

    return aliens


def create_boss(level):
    return Boss(
        level["boss_name"],
        level["boss_hp"],
        INITIAL_BOSS_POSITION,
        level["boss_speed"],
        level["boss_texture"],
    )


def draw_status(screen, font, shuttle, level, phase, boss):
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

    level_label = font.render(f"level {level['number']}: {level['name']}", True, (255, 255, 255))
    screen.blit(level_label, (SCREEN_WIDTH / 2 - level_label.get_width() / 2, 10))

    score_label = font.render("score: ", True, (255, 255, 255))
    score_value = font.render(f"{shuttle.get_score()}", True, (0, 0, 255))
    screen.blit(score_label, (SCREEN_WIDTH - 95, 10))
    screen.blit(score_value, (SCREEN_WIDTH - 25, 10))

    if phase == "boss":
        boss_label = font.render(f"{boss.get_name()} hp: {boss.get_hp()}", True, (255, 190, 40))
        screen.blit(boss_label, (SCREEN_WIDTH / 2 - boss_label.get_width() / 2, 42))


def draw_centered_message(screen, background, title_font, text_font, title, subtitle=None, shuttle=None):
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    text = title_font.render(title, True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))

    if subtitle:
        subtitle_text = text_font.render(subtitle, True, (255, 220, 100))
        screen.blit(subtitle_text, (SCREEN_WIDTH / 2 - subtitle_text.get_width() / 2, SCREEN_HEIGHT / 2 + 90))

    if shuttle is not None:
        final_score_label = text_font.render("Final Score: ", True, (255, 255, 255))
        final_score = text_font.render(f"{shuttle.get_score() * max(0, shuttle.get_hp())}", True, (0, 255, 255))
        screen.blit(final_score_label, (SCREEN_WIDTH - 480, 500))
        screen.blit(final_score, (SCREEN_WIDTH - 370, 500))


def update_aliens(aliens, direction, level, dt):
    living_aliens = [alien for alien in aliens if not alien.get_is_dead()]
    if not living_aliens:
        return direction

    speed_multiplier = level["alien_speed_multiplier"]
    for alien in living_aliens:
        alien.move_down(ALIEN_VERTICAL_SPEED * speed_multiplier * dt)
        alien.move_horizontal(direction * ALIEN_HORIZONTAL_SPEED * speed_multiplier * dt)

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


def reset_bullet_to_shuttle(bullet, shuttle):
    bullet.set_pos([shuttle.get_position()[0] + 20, shuttle.get_position()[1] - 10])


def create_boss_bullet(boss, level):
    boss_rect = boss.get_rect()
    boss_bullet = Bullet(
        [boss_rect.centerx, boss_rect.bottom],
        level["boss_shot_speed"],
        direction=1,
        scale=BOSS_BULLET_SCALE,
    )
    boss_bullet.set_pos([boss_rect.centerx - boss_bullet.get_rect().width / 2, boss_rect.bottom])
    return boss_bullet


def update_bullet(bullet, shuttle, dt):
    if shuttle.get_shot():
        bullet.move_bullet(dt)
    else:
        reset_bullet_to_shuttle(bullet, shuttle)

    if bullet.get_pos()[1] < -bullet.get_rect().height:
        shuttle.set_shot(False)
        reset_bullet_to_shuttle(bullet, shuttle)


def handle_alien_collisions(aliens, bullet, shuttle):
    for alien in aliens:
        if bullet.collision(alien):
            alien.die()
            shuttle.set_shot(False)
            shuttle.score_up()
            reset_bullet_to_shuttle(bullet, shuttle)
            return


def handle_boss_collision(boss, bullet, shuttle):
    if shuttle.get_shot() and bullet.collision(boss):
        boss.take_damage(BOSS_DAMAGE)
        shuttle.set_shot(False)
        reset_bullet_to_shuttle(bullet, shuttle)


def update_boss_bullets(boss_bullets, dt):
    for boss_bullet in boss_bullets:
        boss_bullet.move_bullet(dt)

    return [
        boss_bullet
        for boss_bullet in boss_bullets
        if boss_bullet.get_pos()[1] <= SCREEN_HEIGHT + boss_bullet.get_rect().height
    ]


def handle_boss_bullet_collisions(boss_bullets, shuttle, damage):
    remaining_bullets = []
    for boss_bullet in boss_bullets:
        if boss_bullet.collision(shuttle):
            shuttle.take_damage(damage)
        else:
            remaining_bullets.append(boss_bullet)

    return remaining_bullets


def handle_player_damage(shuttle, enemies, now, last_collision_time, damage):
    if now - last_collision_time <= COLLISION_COOLDOWN_MS:
        return last_collision_time

    for enemy in enemies:
        if not enemy.get_is_dead() and shuttle.get_rect().colliderect(enemy.get_rect()):
            shuttle.take_damage(damage)
            return now

    return last_collision_time


def start_level(level_index):
    level = LEVELS[level_index]
    return {
        "level": level,
        "aliens": create_aliens(level),
        "boss": create_boss(level),
        "boss_bullets": [],
        "last_boss_shot_time": 0,
        "alien_direction": -1,
        "boss_direction": 1,
        "phase": "aliens",
    }


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
    level_index = 0
    level_state = start_level(level_index)

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
            update_bullet(bullet, shuttle, dt)

            if level_state["phase"] == "aliens":
                level_state["alien_direction"] = update_aliens(
                    level_state["aliens"],
                    level_state["alien_direction"],
                    level_state["level"],
                    dt,
                )
                handle_alien_collisions(level_state["aliens"], bullet, shuttle)
                last_collision_time = handle_player_damage(
                    shuttle,
                    level_state["aliens"],
                    pygame.time.get_ticks(),
                    last_collision_time,
                    SHUTTLE_DAMAGE,
                )

                if all(alien.get_is_dead() for alien in level_state["aliens"]):
                    level_state["phase"] = "boss"
                    level_state["boss_bullets"].clear()
                    level_state["last_boss_shot_time"] = pygame.time.get_ticks()
                    reset_bullet_to_shuttle(bullet, shuttle)
            else:
                now = pygame.time.get_ticks()
                level_state["boss_direction"] = level_state["boss"].move(level_state["boss_direction"], dt)
                if now - level_state["last_boss_shot_time"] >= level_state["level"]["boss_shot_cooldown_ms"]:
                    level_state["boss_bullets"].append(create_boss_bullet(level_state["boss"], level_state["level"]))
                    level_state["last_boss_shot_time"] = now

                level_state["boss_bullets"] = update_boss_bullets(level_state["boss_bullets"], dt)
                level_state["boss_bullets"] = handle_boss_bullet_collisions(
                    level_state["boss_bullets"],
                    shuttle,
                    level_state["level"]["boss_shot_damage"],
                )
                handle_boss_collision(level_state["boss"], bullet, shuttle)
                last_collision_time = handle_player_damage(
                    shuttle,
                    [level_state["boss"]],
                    now,
                    last_collision_time,
                    BOSS_HIT_DAMAGE,
                )

                if level_state["boss"].get_is_dead():
                    shuttle.score_up()
                    level_index += 1
                    if level_index >= len(LEVELS):
                        game_state = "win"
                    else:
                        level_state = start_level(level_index)
                        reset_bullet_to_shuttle(bullet, shuttle)
                        level_state["boss_bullets"].clear()

            if shuttle.get_is_dead():
                game_state = "game_over"

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        if game_state == "playing":
            shuttle.draw_shuttle(screen)
            for alien in level_state["aliens"]:
                alien.draw_alien(screen)

            if level_state["phase"] == "boss":
                level_state["boss"].draw_boss(screen)
                for boss_bullet in level_state["boss_bullets"]:
                    boss_bullet.draw_bullet(screen)

            if shuttle.get_shot():
                bullet.draw_bullet(screen)

            draw_status(screen, font_text, shuttle, level_state["level"], level_state["phase"], level_state["boss"])
        elif game_state == "win":
            draw_centered_message(
                screen,
                background,
                font_game_over,
                font_text,
                "You Win!!!",
                "Three invasions survived.",
                shuttle,
            )
        else:
            draw_centered_message(screen, background, font_game_over, font_text, "Game Over :(")

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
