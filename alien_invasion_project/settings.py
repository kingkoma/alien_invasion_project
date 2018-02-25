'''游戏配置'''

class Settings():
    '''存储《外星人入侵》的所有设置的类'''
    
    def __init__(self):
        '''初始化游戏的设置'''
        # 屏幕设置
        self.screen_width = 750  # 600
        self.screen_height = 550  # 400
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.fleet_drop_speed = 10
        # 加快游戏速度
        self.speedup_scale = 1.1
        # 升级评分点数提高
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # fleet_dirction [-1 为向左移 1 为向右移]
        self.fleet_dirction = 1
        # 子弹设置
        self.bullet_width = 6  
        self.bullet_height = 5
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

    def initialize_dynamic_settings(self):
        '''初始化随游戏过关变化的设置'''
        self.ship_speed_factor = 1.5
        self.alien_speed_factor = 3
        self.bullet_speed_factor = 3
        self.fleet_dirction = 1
        self.alien_points = 50

    def increase_speed(self):
        '''提高速度设置和外星人点数'''
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
