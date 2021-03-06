import sys
from time import sleep
import pygame

from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # 创建子弹，并加入组中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        with open('./high_score.txt', 'w') as f:
            f.write(str(stats.high_score))
        sys.exit()

def check_keyup_events(event, ship):
    '''响应松键'''
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, sound):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('./high_score.txt', 'w') as f:
                f.write(str(stats.high_score))
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sound)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            
def check_play_button(ai_settings, screen, sb, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sound):
    '''在玩家单击 play 按钮时开始新游戏'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌
        sb.prep_image()
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建新外星人群，飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    sound.play_bg_music(stats)


def check_high_score(stats, sb):
    '''检查是否诞生最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def fire_bullet(ai_settings, screen, ship, bullets):
    '''限制子弹数量'''
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳的外星人数量'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳外星人行数'''
    availble_space_y = (ai_settings.screen_height - 
                            (3 * alien_height) - ship_height)
    number_rows = int(availble_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''创建一个外星人并将其放在当前行'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''创建一群外星人'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
            alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, 
                    row_number)


def check_fleet_edges(ai_settings, aliens):
    '''外星人碰到屏幕边缘时的处理'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_dirction(ai_settings, aliens)
            break


def change_fleet_dirction(ai_settings, aliens):
    '''将外星人下移并改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_dirction *= -1

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
    '''删除子弹和外星人碰撞'''    
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            sound.play_sound(bullets, ai_settings, stats)
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        start_new_level(bullets, ai_settings, stats, sb, screen, ship, aliens)

def start_new_level(bullets, ai_settings, stats, sb, screen, ship, aliens):
    '''升级'''
    bullets.empty()
    ai_settings.increase_speed()
    # 提高等级
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''响应外星人撞到飞船'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建新的外星人群，并把新的飞船放到正中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''检查外星人是否到底端'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
        play_button):
    '''更新屏幕图像'''
    screen.fill(ai_settings.bg_color)    
    # 更新子弹页面
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
    '''更新子弹位置，删除消失的子弹'''
    bullets.update()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, sound)

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''更新外星人群中所有外星人的位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings,  screen, stats, sb, ship, aliens, bullets)


