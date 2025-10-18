import sys
import pygame #pip install pygame
from pygame.locals import QUIT
import random

pygame.display.set_caption("qwo的遊戲")

# 球
class Ball(object):
    def __init__(self, canvas, pos, radius):
        self.pygame = pygame
        self.canvas = canvas
        self.pos = pos
        self.radius = radius
        self.color = (100, 200, 200)
        self.visible = True
        self.rect = self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)
#更新
    def update(self):
        if self.visible:
            self.rect = self.pygame.draw.circle(self.canvas, self.color, self.pos, self.radius)


# 板子
class Paddle(object):
    def __init__(self, canvas, rect):
        self.pygame = pygame
        self.canvas = canvas
        self.rect = rect
        self.color = (255, 255, 255)
        self.visible = True
#更新
    def update(self):
        if self.visible:
            self.pygame.draw.rect(self.canvas, self.color, self.rect)

# 方塊
class Block(object):
    def __init__(self, canvas, rect):
        self.pygame = pygame
        self.canvas = canvas
        self.rect = rect
        self.color = (99, 184, 255)
        self.visible = True
#更新
    def update(self):
        if self.visible:
            self.pygame.draw.rect(self.canvas, self.color, self.rect)
#位置更新(刷新)
    def reset_position(self):
        self.rect[0] = random.randint(0, SCREEN_SIZEX - self.rect[2])
        self.rect[1] = random.randint(0, SCREEN_SIZEY // 2)

#等級選單
def draw_menu():
    window_surface.fill(SCREEN_COLOR)
    options = ["LV1", "LV2", "LV3"]
    speeds = [5, 6, 8]
    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        window_surface.blit(text, (SCREEN_SIZEX // 2 - 50, SCREEN_SIZEY // 2 - 60 + i * 50))
    pygame.display.flip()
    #等級接收
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i in range(len(options)):
                    if SCREEN_SIZEX // 2 - 50 <= x <= SCREEN_SIZEX // 2 + 50 and SCREEN_SIZEY // 2 - 60 + i * 50 <= y <= SCREEN_SIZEY // 2 - 60 + i * 50 + 36:
                        return speeds[i]

#分數
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window_surface.blit(score_text, (SCREEN_SIZEX - 150, 10))

#更新
def update_game(ball, paddle, blocks, score):
    ball.update()
    paddle.update()
    for block in blocks:  # 更新所有方塊
        block.update()
    draw_score(score)  # 更新分數顯示
    pygame.display.update()

#碰撞箱
def is_collision(rect1, rect2):
    return pygame.Rect.colliderect(rect1, rect2)

#字面意義
def reset_game():
    global game_mode, dx, dy
    game_mode = 0
    dx = BALL_SPEED
    dy = -BALL_SPEED

#結束選單
def game_over_menu(score):
    pygame.mouse.set_visible(True)  # 顯示鼠標
    pygame.event.set_grab(False)  # 釋放鼠標

    window_surface.fill(SCREEN_COLOR)
    text = font.render(f"            GG  Score: {score}", True, (99,184,255))
    window_surface.blit(text, (SCREEN_SIZEX // 2 - 200, SCREEN_SIZEY // 2 - 50))

    options = ["Play Again", "Exit"]
    for i, option in enumerate(options):
        text = font.render(option, True, (255, 255, 255))
        window_surface.blit(text, (SCREEN_SIZEX // 2 - 100, SCREEN_SIZEY // 2 + i * 50))

    pygame.display.flip()
#結束選單接收
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if SCREEN_SIZEX // 2 - 100 <= x <= SCREEN_SIZEX // 2 + 100:
                    if SCREEN_SIZEY // 2 <= y <= SCREEN_SIZEY // 2 + 36:
                        return True
                    elif SCREEN_SIZEY // 2 + 50 <= y <= SCREEN_SIZEY // 2 + 86:
                        pygame.quit()
                        sys.exit()


def main():
    global SCREEN_SIZEX, SCREEN_SIZEY, SCREEN_COLOR, window_surface, font, BALL_SPEED, game_mode, dx, dy #全域宣告

    # 雜七雜八
    SCREEN_SIZEX = 800
    SCREEN_SIZEY = 600
    SCREEN_COLOR = (0, 0, 0)

    pygame.init()
    font = pygame.font.SysFont(None, 40)

    # 顯示選單 設置速度
    window_surface = pygame.display.set_mode((SCREEN_SIZEX, SCREEN_SIZEY))
    BALL_SPEED = draw_menu()

    # 球位置
    dx = BALL_SPEED
    dy = -BALL_SPEED
    clock = pygame.time.Clock()

    # 分數
    score = 0
    GG = 0  

    # 雜七雜八
    paddle_x = 0
    paddle_y = SCREEN_SIZEY - 48
    paddle = Paddle(window_surface, [paddle_x, paddle_y, 100, 24])

    ball_x = paddle_x
    ball_y = paddle_y
    ball = Ball(window_surface, [ball_x, ball_y], 8)

    # speeds[i]
    lv = 0
    if BALL_SPEED == 5:
        lv = 5
    elif BALL_SPEED == 6:
        lv = 3
    elif BALL_SPEED == 8:
        lv = 2

    # 創建多個方塊
    blocks = [Block(window_surface, [random.randint(0, SCREEN_SIZEX - 60), random.randint(0, SCREEN_SIZEY // 2), 30, 30]) for _ in range(lv)]

    reset_game()
    pygame.display.update()

    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    # 主遊戲迴圈
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEMOTION:
                paddle_x = pygame.mouse.get_pos()[0] - 50

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode == 0:
                    game_mode = 1

        window_surface.fill(SCREEN_COLOR)

        paddle.rect[0] = paddle_x
        if is_collision(ball.rect, paddle.rect):
            dy = -dy

        # 檢查每個方塊的碰撞
        for block in blocks:
            if is_collision(ball.rect, block.rect):
                dy = -dy
                score += 1
                block.reset_position()

        if game_mode == 0:
            ball.pos[0] = ball_x = paddle.rect[0] + ((paddle.rect[2] - ball.radius) // 2)
            ball.pos[1] = ball_y = paddle.rect[1] - ball.radius
        else:
            ball_x += dx
            ball_y += dy
            if ball_y + dy > SCREEN_SIZEY - ball.radius:
                GG += 1
                if GG == 5:  # 進入結束選單
                    play_again = game_over_menu(score)
                    if play_again:
                        main()  # 重新開始 嗯這是個遞迴欸WW
                    else:
                        pygame.quit()
                        sys.exit()
                game_mode = 0
            if ball_x + dx > SCREEN_SIZEX - ball.radius or ball_x + dx < ball.radius:
                dx = -dx
            if ball_y + dy < ball.radius:
                dy = -dy
            ball.pos[0] = ball_x
            ball.pos[1] = ball_y

        update_game(ball, paddle, blocks, score)
        clock.tick(120)
if __name__ == "__main__":
    main()
