import sys
import time
import random
import pygame
from pygame.constants import MOUSEBUTTONDOWN, QUIT, USEREVENT

import json
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WHITE = (255, 255, 255)
IMAGEWIDTH = 150
IMAGEHEIGHT = 100
FPS = 60
TIME_PERIOD = 500
IMG = 'hater.jpg'
TIMELEFT = 20


def get_random_position(widow_width, window_height, image_width, image_height):
    random_x = random.randint(0, widow_width - image_width)
    random_y = random.randint(50, window_height - image_height)

    return random_x, random_y


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (0, 0, 0)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface(
            (max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color,
                         self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()


class Mosquito(pygame.sprite.Sprite):
    def __init__(self, IMG, width, height, random_x, random_y, window_width, window_height) -> None:
        super().__init__()

        # 載入圖片
        self.raw_image = pygame.image.load(
            IMG).convert_alpha()
        # 縮小圖片
        self.image = pygame.transform.scale(self.raw_image, (width, height))
        # 回傳位置
        self.rect = self.image.get_rect()
        # 定位
        self.rect.topleft = (random_x, random_y)
        self.width = width
        self.height = height
        self.window_width = window_width

        self.window_height = window_height

        self.iskill = False

    def kill(self):
        self.iskill = True

    def hit(self):
        if self.iskill:
            self.raw_image = self.images[1].convert_alpha()
        else:
            self.raw_image = self.images[0].convert_alpha()


def extract_time(json):
    try:
        # Also convert to int since update_time will be string. When comparing
        # strings, "10" is smaller than "2".
        return json['score']
    except KeyError:
        return 0

# lines.sort() is more efficient than lines = lines.sorted()


def main():

    fetch = False
    list_record = ()
    # 初始化pygame
    pygame.init()
    # 初始化視窗
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # 視窗名稱
    pygame.display.set_caption('打蚊子')
    # 初始化蚊子位置
    random_x, random_y = get_random_position(
        WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
    mosquito = Mosquito(IMG, IMAGEWIDTH, IMAGEHEIGHT, random_x,
                        random_y, WINDOW_WIDTH, WINDOW_HEIGHT)

    # 設定載入蚊子計時器
    reload_mosquito_event = USEREVENT + 1
    pygame.time.set_timer(reload_mosquito_event, TIME_PERIOD)
    # 設定載入時間計時器
    reload_time_event = USEREVENT + 2
    pygame.time.set_timer(reload_time_event, 1000)

    # 玩家分數
    points = 0
    # 剩餘時間
    time_left = TIMELEFT

    # 設定字體
    my_font = pygame.font.SysFont("Arial", 30)

    # 設定物件
    hit_text_surface = None

    # 設定遊戲偵數
    main_clock = pygame.time.Clock()

    page_id = 0
    gamername = ""

    pygame.mixer.music.load('hit.wav')
    while True:

        for event in pygame.event.get():

            if page_id == 0:
                list_record = ()
                fetch = False
                # 初始化蚊子位置
                random_x, random_y = get_random_position(
                    WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                mosquito = Mosquito(IMG, IMAGEWIDTH, IMAGEHEIGHT, random_x,
                                    random_y, WINDOW_WIDTH, WINDOW_HEIGHT)

                # 設定載入蚊子計時器
                reload_mosquito_event = USEREVENT + 1
                pygame.time.set_timer(reload_mosquito_event, TIME_PERIOD)
                # 設定載入時間計時器
                reload_time_event = USEREVENT + 2
                pygame.time.set_timer(reload_time_event, 1000)

                # 玩家分數
                points = 0
                # 剩餘時間
                time_left = TIMELEFT

                # 設定字體
                my_font = pygame.font.SysFont("Arial", 30)

                # 設定物件
                hit_text_surface = None

                # 設定遊戲偵數
                main_clock = pygame.time.Clock()

                page_id = 0
                gamername = ""
                # 輸入框
                font = pygame.font.SysFont("Arial", 100)

                text_input_box = TextInputBox(170, 150, 400, font)
                text_input_box2 = TextInputBox(170, 350, 400, font)
                group = pygame.sprite.Group(text_input_box)
                run = True
                while run:
                    event_list = pygame.event.get()
                    for event in event_list:
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                if text_input_box.text != "":
                                    run = False
                                    gamername = text_input_box.text
                                    page_id = 1

                    group.update(event_list)
                    window_surface.fill(WHITE)
                    text_count_time = my_font.render(
                        '{}'.format("Input You NickName"), True, (0, 0, 0))
                    window_surface.blit(text_count_time, (170, 100))
                    text_count_time = my_font.render(
                        '{}'.format("Put your hater image at th same folder and rename to hater.jpg"), True, (0, 0, 0))
                    window_surface.blit(text_count_time, (100, 450))
                    group.draw(window_surface)
                    text_count_time = my_font.render(
                        '{}'.format("Input You NickName and Press 'Enter' to start"), True, (255, 0, 0))
                    window_surface.blit(text_count_time, (150, 550))
                    pygame.display.flip()
            elif page_id == 1:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == USEREVENT + 2:
                    time_left -= 1
                    if time_left == 0:
                        with open("record.json", "r") as f:
                            data = json.load(f)
                        with open("record.json", "w") as f:
                            data += [{'name': gamername, 'score': points}]
                            json.dump(data, f)
                        page_id = 2
                elif event.type == reload_mosquito_event:
                    # 偵測到重新整理事件，固定時間移除蚊子，換新位置
                    random_x, random_y = get_random_position(
                        WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                    mosquito = Mosquito(IMG, IMAGEWIDTH, IMAGEHEIGHT, random_x,
                                        random_y, WINDOW_WIDTH, WINDOW_HEIGHT)
                    # 蚊子新位置
                elif event.type == MOUSEBUTTONDOWN:
                    # 當使用者點擊滑鼠時，檢查是否滑鼠位置 x, y 有在蚊子圖片上
                    if random_x < pygame.mouse.get_pos()[0] < random_x + IMAGEWIDTH and random_y < pygame.mouse.get_pos()[1] < random_y + IMAGEHEIGHT:
                        pygame.mixer.music.play()
                        pygame.mixer.stop()
                        random_x, random_y = get_random_position(
                            WINDOW_WIDTH, WINDOW_HEIGHT, IMAGEWIDTH, IMAGEHEIGHT)
                        mosquito = Mosquito(IMG, IMAGEWIDTH, IMAGEHEIGHT, random_x,
                                            random_y, WINDOW_WIDTH, WINDOW_HEIGHT)

                        hit_text_surface = my_font.render(
                            'Hit!!', True, (0, 0, 0))
                        points += 5
                # 背景顏色，清除畫面
                window_surface.fill(WHITE)

                # 遊戲分數儀表板
                text_surface = my_font.render(
                    'Point:{}'.format(points), True, (0, 0, 0))

                # 遊戲時間倒數計時器
                text_count = my_font.render(
                    'TimeLeft:', True, (0, 0, 0))
                text_count_time = my_font.render(
                    '{}s'.format(time_left), True, (255, 0, 0))

                window_surface.blit(mosquito.image, mosquito.rect)
                window_surface.blit(text_surface, (10, 0))
                window_surface.blit(text_count, (650, 0))
                window_surface.blit(text_count_time, (750, 0))
                if hit_text_surface:
                    window_surface.blit(hit_text_surface, (10, 10))
                    hit_text_surface = None

                pygame.display.update()
                main_clock.tick(FPS)
            elif page_id == 2:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        page_id = 0
                # 背景顏色，清除畫面
                window_surface.fill(WHITE)
                tmp = []
                tmp = list(list_record)

                # 取得資料庫data
                width = 10
                if fetch == False:
                    with open("record.json", "r") as f:
                        docs = json.load(f)
                    docs.sort(key=extract_time, reverse=True)
                    index = 0
                    for doc in docs:
                        if index < 10:
                            index += 1
                            tmp.append(
                                (doc['name'], str(doc['score'])))
                    fetch = True

                list_record = tuple(tmp)

                # 顯示data
                text_count_time = my_font.render(
                    '{}'.format("name"), True, (255, 0, 0))
                window_surface.blit(text_count_time, (250, 0))
                text_count_time = my_font.render(
                    '{}'.format("score"), True, (255, 0, 0))
                window_surface.blit(text_count_time, (400, 0))

                for i in range(len(list_record)):

                    test_text = ("{}".format(
                        list_record[i][0].ljust(width)))
                    text_count_time = my_font.render(
                        'No.{}   {}'.format(i+1, test_text), True, (255, 0, 0))
                    window_surface.blit(text_count_time, (190, 50*(i+1)))
                    test_text = ("{}".format(
                        list_record[i][1].ljust(width)))
                    text_count_time = my_font.render(
                        '{}'.format(test_text), True, (255, 0, 0))
                    window_surface.blit(text_count_time, (400, 50*(i+1)))

                text_count_time = my_font.render(
                    '{}'.format("Press 'P' to restart"), True, (255, 0, 0))
                window_surface.blit(text_count_time, (350, 550))
                # 更新畫面
                pygame.display.update()
                main_clock.tick(FPS)


if __name__ == '__main__':
    main()
