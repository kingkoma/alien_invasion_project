

class GameStats():
    '''跟踪游戏统计信息'''
    def __init__(self, ai_settings):
        '''初始化统计信息'''
        self.ai_settings = ai_settings
        self.reset_stats()
        # 游戏启动时处于活动状态
        self.game_active = False
        # 任何情况下都不重置最高分
        # self.high_score = 0

    def reset_stats(self):
        '''初始化游戏运行中可能发生变化的统计信息'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        try:
            with open('./high_score.txt', 'r') as f:
                self.high_score = f.read()
                self.high_score = int(self.high_score)
        except Exception as e:
            self.high_score = 0
