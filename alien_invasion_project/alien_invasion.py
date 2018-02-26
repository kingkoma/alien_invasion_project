import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from sound import Sound
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
import game_functions as gf


def run_game():
    '''游戏主程序'''
   
   # 初始化游戏并设置一个屏幕对象
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.set_num_channels(8)
    ai_settings = Settings()
    screen = pygame.display.set_mode(
            (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    # 创建 play 按钮
    play_button = Button(ai_settings, screen, 'Play')
    # 加载音效
    sound = Sound()
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储游戏统计信息的实例, 及记分牌
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)
    # 创建存储子弹,外星人的编组
    bullets = Group()
    aliens = Group()

    # 创建外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 游戏主循环
    while True:
        
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, 
                aliens, bullets, sound)
        if stats.game_active:
            ship.update()      
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, sound)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
                bullets,play_button)

run_game()
