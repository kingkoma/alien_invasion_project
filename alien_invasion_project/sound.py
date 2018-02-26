import pygame


def stero_pan(x_coord, screen_width):
    '''根据位置决定播放声音左右声道的音量'''
    right_volume = float(x_coord) / screen_width
    left_volume = 1.0 - right_volume
    return (left_volume, right_volume)

class Sound():
    '''游戏音效'''
    def __init__(self):
        '''初始化音效'''
        self.bullet_sound = pygame.mixer.Sound('./bullet.wav')
        self.bg_music = pygame.mixer.music.load('./bg_music.ogg')

    def bullet_sound(self):
        '''子弹发射音效'''
        pass
        # self.bullet_sound = pygame.mixer.Sound('./bullet.wav')

    def play_sound(self, bullets, ai_settings, stats):
        '''播放音效'''
        if stats.game_active:
            channel = self.bullet_sound.play()

    def play_bg_music(self, stats):
        '''播放背景音乐'''
        if stats.game_active:
            pygame.mixer.music.play()
