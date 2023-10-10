import pygame
from sys import exit
import math
from enum import Enum
import json
from random import randint


def display_string(string, x, y):
    sting_surf = pygame.font.Font('font/Pixeltype.ttf', 50)
    sting_surf = sting_surf.render(string, False, (64, 64, 64))
    sting_rect = sting_surf.get_rect(center=(x, y))
    screen.blit(sting_surf, sting_rect)
    return sting_rect


def display_score():
    global current_time
    current_time = pygame.time.get_ticks()-start_time
    display_string(f'{math.floor((current_time/1000)%60)}', 400, 50)


def game_over_screen():
    screen.fill((94, 129, 162))
    display_string('Game Over', 400, 85)

    mainmenu = display_string('Main Menu', 400, 350)

    player_stand = pygame.image.load(
        'graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_rect = player_stand.get_rect(center=(400, 200))
    screen.blit(player_stand, player_stand_rect)
    return mainmenu


def main_menu_screen():
    screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 300))
    # screen.blit(snail_frame_surface, snail_rect)
    snail_rect.left -= 4
    if snail_rect.left <= -10:
        snail_rect.left = 800

    name = display_string('snaily', 400, 50)
    start = display_string('Start', 400, 85)
    exit = display_string('Exit', 400, 120)
    score = display_string('Score', 750, 30)

    # screen.blit(start_surf, start_rect)
    # screen.blit(exit_surf, exit_rect)
    return {'start': start, 'exit': exit, 'score': score}


def display_player_data(score, pixel):
    user_surf = pygame.font.Font('font/Pixeltype.ttf', 50)
    score_surf = pygame.font.Font('font/Pixeltype.ttf', 50)

    # user name display
    user_surf = user_surf.render("player:", False, (64, 64, 64))
    user_rect = user_surf.get_rect(center=(300, 200+pixel))
    screen.blit(user_surf, user_rect)
    # user score
    score_surf = score_surf.render(str(score), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(500, 200+pixel))
    screen.blit(score_surf, score_rect)


def score_screen():
    screen.fill((94, 129, 162))
    pixel = 0
    file = open('user_info.json')
    data = json.load(file)
    main = display_string('Main Menu', 720, 30)
    for i in data['users']:
        display_player_data(i['player'], pixel)
        pixel += 50
    file.close()


def calc_score():
    time = math.floor((current_time/1000) % 60)
    dict1 = {"users": [{
        "player": time,
    }
    ]
    }
    with open("user_info.json", "w") as outfile:
        json.dump(dict1, outfile)


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 5
            if obstacle.bottom == 300:
                screen.blit(snail_frame_surface, obstacle)
            else:
                screen.blit(fly_frame_surface, obstacle)
            obstacle_list = [
                obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collosion(palyer, obstacles):
    # print(len(obstacles))
    if obstacles:
        for obstacle in obstacles:
            if obstacle.colliderect(palyer):
                return False
            else:
                return True
    else:
        return True


def player_animation():
    global player_surface, player_walk_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_walk_index += 0.1
        if player_walk_index >= len(player_walks):
            player_walk_index = 0
        player_surface = player_walks[int(player_walk_index)]


pygame.init()


class Screen(Enum):
    main = 1
    gameOver = 2
    game = 3
    score = 4
    new_user = 5


global ScreenMode
ScreenMode = 1
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('SnailRunner')
clock = pygame.time.Clock()

game_is_active = False
start_time = 0
sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()


snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_frame_surface = snail_frames[snail_frame_index]
snail_rect = snail_frame_surface.get_rect(midbottom=(600, 300))

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_frame_surface = fly_frames[fly_frame_index]
fly_rect = fly_frame_surface.get_rect(midbottom=(600, 300))


obstacle_rect_list = []

menu_senor = game_over_screen()
mainATT_senor = main_menu_screen()
main = display_string('Main Menu', 720, 30)
# main_in_score = score_screen()


player_walk1 = pygame.image.load(
    'graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load(
    'graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load(
    'graphics/Player/jump.png').convert_alpha()
player_walk_index = 0
player_walks = [player_walk1, player_walk2]
player_surface = player_walks[player_walk_index]
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if player_rect.bottom == 300:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity -= 20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity -= 20

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mainATT_senor['start'].collidepoint(event.pos) and game_is_active == False:
                game_is_active = True
                ScreenMode = 3
                start_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mainATT_senor['exit'].collidepoint(event.pos) and game_is_active == False:
                pygame.quit()
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_senor.collidepoint(event.pos):
                game_is_active = False
                ScreenMode = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if main.collidepoint(event.pos) and ScreenMode == 4:
                ScreenMode = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mainATT_senor['score'].collidepoint(event.pos) and ScreenMode == 1:
                ScreenMode = 4
                print(ScreenMode)

        if game_is_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(
                        snail_frame_surface.get_rect(midbottom=(randint(900, 1100), 210)))
                else:
                    obstacle_rect_list.append(
                        fly_frame_surface.get_rect(midbottom=(randint(900, 1100), 300)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_frame_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_frame_surface = fly_frames[fly_frame_index]

    if game_is_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        # screen.blit(snail_frame_surface, snail_rect)
        time = display_score()
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_is_active = collosion(player_rect, obstacle_rect_list)
        player_animation()
        # snail_rect.left -= 4
        # if snail_rect.left <= -10:
        #     snail_rect.left = 800
        # if snail_rect.colliderect(player_rect):
        #     game_is_active = False
        #     ScreenMode = 2

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_gravity = 0
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)
        if game_is_active == False:
            ScreenMode = 2

    else:

        if ScreenMode == 1:
            main_menu_screen()
        if ScreenMode == 2:
            obstacle_rect_list.clear()
            game_over_screen()
            calc_score()

        if ScreenMode == 4:
            score_screen()

    pygame.display.update()
    clock.tick(60)
