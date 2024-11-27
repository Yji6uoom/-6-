#스네이크 게임

import pygame
import time
import random

pygame.init()

# 해상도
window_x = 720
window_y = 480

# 색깔
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# 게임 초기화
pygame.display.set_caption('스네이크 게임')
game_window = pygame.display.set_mode((window_x, window_y))

# 프레임
fps = pygame.time.Clock()

# 스네이크 몸
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]

# 목표 위치
food_position = [random.randrange(1, (window_x // 10)) * 10,
                 random.randrange(1, (window_y // 10)) * 10]
food_spawn = True

# 방향 설정
direction = 'RIGHT'
change_to = direction

# 점수 초기화
score = 0

# 글꼴
font_path = "C:/Windows/Fonts/malgun.ttf"  # 경로를 본인의 시스템에 맞게 변경하세요
font_size = 20
game_font = pygame.font.Font(font_path, font_size)

# 점수 표시 함수
def show_score(choice, color, font, size):
    score_surface = font.render(f'점수 : {score}', True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (window_x / 10, 15)
    game_window.blit(score_surface, score_rect)

# 게임 오버 함수
def game_over():
    my_font = pygame.font.Font(font_path, 50)
    game_over_surface = my_font.render(f'최종 점수 : {score}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)

    main_menu_font = pygame.font.Font(font_path, 35)
    main_menu_surface = main_menu_font.render('Main Menu', True, green)
    main_menu_rect = main_menu_surface.get_rect()
    main_menu_rect.midtop = (window_x / 2, window_y / 2)
    game_window.blit(main_menu_surface, main_menu_rect)
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_rect.collidepoint(event.pos):
                    main_menu()

# 메인 메뉴 함수
def main_menu():
    while True:
        game_window.fill(black)
        title_font = pygame.font.Font(font_path, 50)
        menu_font = pygame.font.Font(font_path, 35)
        
        title_surface = title_font.render('스네이크 게임', True, white)
        title_rect = title_surface.get_rect()
        title_rect.midtop = (window_x / 2, window_y / 4)
        game_window.blit(title_surface, title_rect)
        
        start_surface = menu_font.render('Start', True, green)
        start_rect = start_surface.get_rect()
        start_rect.midtop = (window_x / 2, window_y / 2)
        game_window.blit(start_surface, start_rect)
        
        exit_surface = menu_font.render('Exit', True, red)
        exit_rect = exit_surface.get_rect()
        exit_rect.midtop = (window_x / 2, window_y / 2 + 50)
        game_window.blit(exit_surface, exit_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    game_loop()
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# 게임 루프 함수
def game_loop():
    global snake_position, snake_body, food_position, food_spawn, direction, change_to, score
    
    # 일시정지 상태
    pause = False

    # 초기화
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    food_position = [random.randrange(1, (window_x // 10)) * 10,
                     random.randrange(1, (window_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                # P키로 일시정지 및 계속하기
                if event.key == pygame.K_p:
                    pause = not pause
                if not pause:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'

        # 일시정지 상태일 경우 점수표시와 나머지 게임 로직을 건너뛰고 계속
        if pause:
            game_window.fill(black)  # 배경 색상
            pause_font = pygame.font.Font(font_path, 50)
            pause_surface = pause_font.render('일시정지', True, white)
            pause_rect = pause_surface.get_rect()
            pause_rect.midtop = (window_x / 2, window_y / 4)
            game_window.blit(pause_surface, pause_rect)

            resume_surface = game_font.render('계속하려면 P키를 누르세요', True, white)
            resume_rect = resume_surface.get_rect()
            resume_rect.midtop = (window_x / 2, window_y / 2)
            game_window.blit(resume_surface, resume_rect)
            
            show_score(1, white, game_font, font_size)
            pygame.display.update()
            continue

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_position = [random.randrange(1, (window_x // 10)) * 10,
                             random.randrange(1, (window_y // 10)) * 10]
        food_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_position[0], food_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x-10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y-10:
            game_over()
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(1, white, game_font, font_size)
        pygame.display.update()
        fps.tick(15)

# 메인 메뉴 호출
main_menu()
