import pygame
import random
import time

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE GAME')
clock = pygame.time.Clock()

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 변수 설정
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = 10
direction = 'RIGHT'
change_to = direction
score = 0
best_score = 0
apple_spawned = False
pill_spawned = False
apple_pos = [0, 0]
pill_pos = [0, 0]
apple_timer = 0
pill_timer = 0

# 폰트 설정
font = pygame.font.SysFont('consolas', 35)

# 시작 화면 함수
def show_start_screen():
    win.fill(WHITE)
    start_button = pygame.Rect(WIDTH//2 - 50, HEIGHT//2, 100, 40)
    exit_button = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 50, 100, 40)
    best_score_text = font.render(f'Best Score: {best_score}', True, BLUE)
    win.blit(best_score_text, (WIDTH//2 - best_score_text.get_width()//2, HEIGHT//2 - 50))
    pygame.draw.rect(win, GREEN, start_button)
    pygame.draw.rect(win, RED, exit_button)
    start_text = font.render('START', True, WHITE)
    exit_text = font.render('EXIT', True, WHITE)
    win.blit(start_text, (start_button.x + 10, start_button.y + 5))
    win.blit(exit_text, (exit_button.x + 20, exit_button.y + 5))
    pygame.display.update()
    return start_button, exit_button

# 사과와 알약 생성 함수
def spawn_apple():
    return [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]

def spawn_pill():
    return [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]

# 게임 오버 화면 함수
def show_game_over():
    win.fill(WHITE)
    game_over_text = font.render(f'Your Score: {score}', True, RED)
    win.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    main_menu_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 40)
    pygame.draw.rect(win, BLUE, main_menu_button)
    main_menu_text = font.render('MAIN MENU', True, WHITE)
    win.blit(main_menu_text, (main_menu_button.x + 10, main_menu_button.y + 5))
    pygame.display.update()
    return main_menu_button

# 메인 게임 루프
start_screen = True
game_over = False
running = True
while running:
    # 시작 화면
    if start_screen:
        start_button, exit_button = show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    start_screen = False
                    # 게임 시작 시 뱀의 위치를 초기화합니다.
                    snake_pos = [[WIDTH // 2, HEIGHT // 2], [WIDTH // 2 - 10, HEIGHT // 2], [WIDTH // 2 - 20, HEIGHT // 2]]
                    direction = 'RIGHT'
                    change_to = direction
                    score = 0
                    snake_speed = 10
                    apple_spawned = False
                    pill_spawned = False
                elif exit_button.collidepoint(mouse_pos):
                    running = False
        continue

    # 게임 오버 화면
    if game_over:
        main_menu_button = show_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if main_menu_button.collidepoint(mouse_pos):
                    game_over = False
                    start_screen = True
        continue

    # 게임 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 방향키 입력 처리
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # 방향 변경
    direction = change_to

    # 뱀 이동
    if direction == 'UP':
        snake_pos[0][1] -= 10
    elif direction == 'DOWN':
        snake_pos[0][1] += 10
    elif direction == 'LEFT':
        snake_pos[0][0] -= 10
    elif direction == 'RIGHT':
        snake_pos[0][0] += 10

    # 뱀 꼬리 이동
    snake_pos = [[snake_pos[0][0], snake_pos[0][1]]] + snake_pos[:-1]

    # 사과 생성
    if not apple_spawned or time.time() - apple_timer > random.randint(7, 15):
        apple_pos = spawn_apple()
        apple_spawned = True
        apple_timer = time.time()

    # 알약 생성
    if not pill_spawned or time.time() - pill_timer > 30:
        pill_pos = spawn_pill()
        pill_spawned = True
        pill_timer = time.time()

    # 사과 먹기
    if snake_pos[0] == apple_pos:
        snake_pos.append(snake_pos[-1])
        score += 100
        apple_spawned = False

    # 알약 먹기
    if snake_pos[0] == pill_pos:
        snake_pos.pop()
        pill_spawned = False

    # 화면 업데이트
    win.fill(WHITE)
    for pos in snake_pos:
        pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(win, RED, pygame.Rect(apple_pos[0], apple_pos[1], 10, 10))
    pygame.draw.rect(win, BLUE, pygame.Rect(pill_pos[0], pill_pos[1], 10, 10))

    # 점수 표시
    score_text = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_text, (5, 5))

    # 게임 오버 조건 확인
    if snake_pos[0][0] >= WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= HEIGHT or snake_pos[0][1] < 0 or snake_pos[0] in snake_pos[1:]:
        game_over = True
        if score > best_score:
            best_score = score

    pygame.display.update()
    clock.tick(snake_speed)

    # 속도 증가
    if pygame.time.get_ticks() % 10000 == 0:
        snake_speed += 1

pygame.quit()
