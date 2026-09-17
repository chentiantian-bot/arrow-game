import pygame
import sys
import random

# -------------------------- Constant --------------------------
WIDTH, HEIGHT = 650, 650
FPS = 60
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (200, 30, 30)
GREEN = (20, 160, 60)
GRAY = (160,160,160)
DARK_GRAY = (80,80,80)
LIGHT_GRAY = (220,220,220)
HOVER_GRAY = (130,130,130)
HOVER_GREEN = (0,140,40)

CELL_SIZE = 70
GRID_OFFSET_X = 45
GRID_OFFSET_Y = 45

# Direction UP DOWN LEFT RIGHT
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
DIR_DELTA = [(0, -1), (0, 1), (-1, 0), (1, 0)]
DIR_CHAR = ["U", "D", "L", "R"]

LEVELS = [
    # Level 1
    [
        {"x": 0, "y": 0, "dir": RIGHT},
        {"x": 2, "y": 0, "dir": RIGHT},
        {"x": 0, "y": 2, "dir": DOWN},
    ],
    # Level 2
    [
        {"x": 1, "y": 1, "dir": RIGHT},
        {"x": 3, "y": 1, "dir": DOWN},
        {"x": 1, "y": 3, "dir": RIGHT},
        {"x": 5, "y": 3, "dir": UP},
    ],
    # Level 3
    [
        {"x": 0, "y": 0, "dir": DOWN},
        {"x": 2, "y": 2, "dir": RIGHT},
        {"x": 4, "y": 2, "dir": UP},
        {"x": 6, "y": 4, "dir": LEFT},
        {"x": 3, "y": 5, "dir": RIGHT},
    ]
]

# -------------------------- Game Class --------------------------
class ArrowGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Arrow Game")
        self.clock = pygame.time.Clock()

        # Default font
        self.font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)

        # Buttons
        self.restart_rect = pygame.Rect(480, 570, 130, 50)
        self.hint_rect = pygame.Rect(40, 570, 110, 50)
        self.volume_rect = pygame.Rect(200, 570, 130, 50)
        self.start_btn_rect = pygame.Rect(220, 380, 210, 70)

        self.is_mute = False
        self.origin_volume_bgm = 0.4
        self.origin_volume_sfx = 0.6
        self.game_state = "start"  # start / playing

        # Animation
        self.shake_arrow = None
        self.shake_timer = 0
        self.fade_arrow = None
        self.fade_alpha = 255

        # ===== 小熊背景设置 =====
        try:
            self.bear_img = pygame.image.load("bear.jpg").convert_alpha()
            # 缩放小熊大小，你可以调整这个数字
            self.bear_img = pygame.transform.scale(self.bear_img, (180, 180))
        except Exception as e:
            print("⚠️ 找不到 bear.jpg，背景将使用渐变", e)
            self.bear_img = None
        self.bear_x = 0
        self.bear_speed = 1.2
        self.bear_direction = 1

        # Load sound
        self.bgm_sound = None
        self.sound_success = None
        self.sound_fail = None
        try:
            self.bgm_sound = pygame.mixer.Sound("bgm.wav")
            self.bgm_sound.set_volume(self.origin_volume_bgm)
            self.bgm_sound.play(-1)
        except Exception as e:
            print("bgm.wav not found, no background music", e)
        try:
            self.sound_success = pygame.mixer.Sound("success.wav")
            self.sound_success.set_volume(self.origin_volume_sfx)
        except:
            print("success.wav not found")
        try:
            self.sound_fail = pygame.mixer.Sound("fail.wav")
            self.sound_fail.set_volume(self.origin_volume_sfx)
        except:
            print("fail.wav not found")

        self.reset_game()
        self.hint_arrow = None

    # 绘制动态小熊背景
    def draw_bear_bg(self):
        # 底层浅底色
        self.screen.fill((242,245,255))
        if self.bear_img is not None:
            # 更新小熊位置，左右来回移动
            self.bear_x += self.bear_speed * self.bear_direction
            # 边界反弹
            if self.bear_x > WIDTH - 180:
                self.bear_direction = -1
            if self.bear_x < 0:
                self.bear_direction = 1
            # 绘制小熊
            self.screen.blit(self.bear_img, (self.bear_x, 220))

    def toggle_mute(self):
        self.is_mute = not self.is_mute
        if self.is_mute:
            if self.bgm_sound:
                self.bgm_sound.set_volume(0)
            if self.sound_success:
                self.sound_success.set_volume(0)
            if self.sound_fail:
                self.sound_fail.set_volume(0)
        else:
            if self.bgm_sound:
                self.bgm_sound.set_volume(self.origin_volume_bgm)
            if self.sound_success:
                self.sound_success.set_volume(self.origin_volume_sfx)
            if self.sound_fail:
                self.sound_fail.set_volume(self.origin_volume_sfx)

    def reset_game(self):
        self.current_level = 0
        self.load_level(self.current_level)
        self.hint_arrow = None
        self.score = 0
        self.fade_arrow = None

    def load_level(self, level_idx):
        self.arrows = [item.copy() for item in LEVELS[level_idx]]
        self.mistake_count = 3
        self.hint_arrow = None
        self.fade_arrow = None

    def find_hint_arrow(self):
        for arrow in self.arrows:
            if self.check_path_clear(arrow):
                return arrow
        return None

    def draw_grid(self):
        for x in range(9):
            w = 3 if x ==0 else 2
            pygame.draw.line(self.screen, DARK_GRAY,
                             (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y),
                             (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + 8 * CELL_SIZE), w)
        for y in range(9):
            w = 3 if y ==0 else 2
            pygame.draw.line(self.screen, DARK_GRAY,
                             (GRID_OFFSET_X, GRID_OFFSET_Y + y * CELL_SIZE),
                             (GRID_OFFSET_X + 8 * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE), w)

    def draw_arrows(self):
        for arrow in self.arrows:
            if arrow == self.fade_arrow:
                continue
            off_x = 0
            off_y = 0
            if self.shake_arrow == arrow and self.shake_timer > 0:
                off_x = random.randint(-4, 4)
                off_y = random.randint(-2, 2)

            ax = GRID_OFFSET_X + arrow["x"] * CELL_SIZE + 18 + off_x
            ay = GRID_OFFSET_Y + arrow["y"] * CELL_SIZE + 15 + off_y
            if arrow == self.hint_arrow:
                text = self.font.render(DIR_CHAR[arrow["dir"]], True, GREEN)
            else:
                text = self.font.render(DIR_CHAR[arrow["dir"]], True, BLACK)
            self.screen.blit(text, (ax, ay))

        # Fade animation for removed arrow
        if self.fade_arrow is not None:
            surf = pygame.Surface((60,60), pygame.SRCALPHA)
            text = self.font.render(DIR_CHAR[self.fade_arrow["dir"]], True, GREEN)
            surf.blit(text, (18,15))
            surf.set_alpha(self.fade_alpha)
            ax = GRID_OFFSET_X + self.fade_arrow["x"] * CELL_SIZE + 18
            ay = GRID_OFFSET_Y + self.fade_arrow["y"] * CELL_SIZE +15
            self.screen.blit(surf, (ax, ay))
            self.fade_alpha -= 8
            if self.fade_alpha <= 0:
                self.fade_arrow = None
                self.fade_alpha = 255

    def check_path_clear(self, arrow):
        dx, dy = DIR_DELTA[arrow["dir"]]
        cx, cy = arrow["x"], arrow["y"]
        while True:
            cx += dx
            cy += dy
            if cx < 0 or cy < 0 or cx >= 8 or cy >= 8:
                return True
            for a in self.arrows:
                if a is arrow:
                    continue
                if a["x"] == cx and a["y"] == cy:
                    return False

    def get_arrow_at_mouse(self, mx, my):
        gx = (mx - GRID_OFFSET_X) // CELL_SIZE
        gy = (my - GRID_OFFSET_Y) // CELL_SIZE
        if 0 <= gx < 8 and 0 <= gy < 8:
            for arrow in self.arrows:
                if arrow["x"] == gx and arrow["y"] == gy:
                    return arrow
        return None

    def draw_buttons(self, mouse_pos):
        # Restart
        col = HOVER_GRAY if self.restart_rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(self.screen, col, self.restart_rect, border_radius=8)
        txt = self.font.render("Restart", True, BLACK)
        self.screen.blit(txt, (self.restart_rect.x + 10, self.restart_rect.y + 8))

        # Hint
        col = HOVER_GRAY if self.hint_rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(self.screen, col, self.hint_rect, border_radius=8)
        txt_hint = self.font.render("Hint", True, BLACK)
        self.screen.blit(txt_hint, (self.hint_rect.x + 25, self.hint_rect.y + 8))

        # Volume
        col = HOVER_GRAY if self.volume_rect.collidepoint(mouse_pos) else GRAY
        pygame.draw.rect(self.screen, col, self.volume_rect, border_radius=8)
        vol_text = "Mute" if self.is_mute else "Sound"
        txt_vol = self.font.render(vol_text, True, BLACK)
        self.screen.blit(txt_vol, (self.volume_rect.x + 20, self.volume_rect.y + 8))

    def draw_start_screen(self, mouse_pos):
        self.draw_bear_bg()
        title = self.title_font.render("Arrow Game", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)

        tip_text = self.font.render("Click arrow, remove if path is clear", True, DARK_GRAY)
        tip_rect = tip_text.get_rect(center=(WIDTH//2, 160))
        self.screen.blit(tip_text, tip_rect)

        # Start button hover
        btn_color = HOVER_GREEN if self.start_btn_rect.collidepoint(mouse_pos) else GREEN
        pygame.draw.rect(self.screen, btn_color, self.start_btn_rect, border_radius=10)
        start_text = self.big_font.render("Start Game", True, WHITE)
        start_rect = start_text.get_rect(center=self.start_btn_rect.center)
        self.screen.blit(start_text, start_rect)

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.game_state == "start":
                        if self.start_btn_rect.collidepoint(mx, my):
                            self.game_state = "playing"
                            self.reset_game()
                    elif self.game_state == "playing":
                        if self.restart_rect.collidepoint(mx, my):
                            self.reset_game()
                            continue
                        if self.hint_rect.collidepoint(mx, my):
                            self.hint_arrow = self.find_hint_arrow()
                            continue
                        if self.volume_rect.collidepoint(mx, my):
                            self.toggle_mute()
                            continue
                        if self.mistake_count <= 0 or self.current_level >= len(LEVELS):
                            continue
                        clicked_arrow = self.get_arrow_at_mouse(mx, my)
                        if clicked_arrow is not None:
                            self.hint_arrow = None
                            if self.check_path_clear(clicked_arrow):
                                self.fade_arrow = clicked_arrow
                                self.arrows.remove(clicked_arrow)
                                self.score += 10
                                if self.sound_success:
                                    self.sound_success.play()
                                if len(self.arrows) == 0:
                                    self.current_level += 1
                                    if self.current_level < len(LEVELS):
                                        self.load_level(self.current_level)
                            else:
                                self.mistake_count -= 1
                                self.shake_arrow = clicked_arrow
                                self.shake_timer = 15
                                self.score -= 5
                                if self.score < 0:
                                    self.score = 0
                                if self.sound_fail:
                                    self.sound_fail.play()

            if self.game_state == "start":
                self.draw_start_screen(mouse_pos)
            else:
                # 游戏页面也绘制动态小熊背景
                self.draw_bear_bg()

                if self.shake_timer > 0:
                    self.shake_timer -= 1
                else:
                    self.shake_arrow = None

                self.draw_grid()
                self.draw_arrows()
                self.draw_buttons(mouse_pos)

                info_text = self.font.render(f"Level:{self.current_level+1} | Mistakes:{self.mistake_count} | Score:{self.score}", True, BLACK)
                self.screen.blit(info_text, (10, 10))

                if self.mistake_count <= 0:
                    lose_text = self.big_font.render("Game Over!", True, RED)
                    lose_rect = lose_text.get_rect(center=(WIDTH//2, 320))
                    self.screen.blit(lose_text, lose_rect)
                if self.current_level >= len(LEVELS):
                    win_text = self.big_font.render("You Win!", True, GREEN)
                    win_rect = win_text.get_rect(center=(WIDTH//2, 320))
                    self.screen.blit(win_text, win_rect)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = ArrowGame()
    game.run()
