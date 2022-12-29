import pygame
import sys
import traceback
import os
import CXK
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

# 初始化pygame
pygame.init()
# 初始化pygame的音频模块
pygame.mixer.init()
# 定义背景尺寸宽和高
bg_size = width, height = 480, 700
# 初始化窗口
screen = pygame.display.set_mode(bg_size)
# 设置显示在窗口上的名称
pygame.display.set_caption("雷霆篮球🏀🏀🏀")
# 初始化背景图片
background = pygame.image.load("images/background.png").convert()
# 定义RGB颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 载入背景音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
# 载入游戏音效
background_sound = pygame.mixer.Sound("sound/background_sound.wav")
background_sound.set_volume(0.1)
enemy3_fly_sound = pygame.mixer.Sound("sound/Organic Rhythm Assault.wav")
enemy3_fly_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/爆炸.wav")
enemy3_down_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/bomb_sound.wav")
bomb_sound.set_volume(0.2)
get_supply_sound = pygame.mixer.Sound("sound/get_bullet_sound.wav")
get_supply_sound.set_volume(0.2)


# 定义增加小型敌人的函数
def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


# 定义增加中型敌人的函数
def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


# 定义增加大型敌人的函数
def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


# 定义增加敌人移动速度的函数
def inc_speed(target, inc):
    for each in target:
        each.speed += inc


# 游戏主界面
def ui():
    # 循环播放背景音乐
    pygame.mixer.music.play(-1)

    # 初始化界面按键图片并获取图片的矩形位置
    start_game_image = pygame.image.load("images/start_game.png").convert_alpha()
    start_game_image_rect = start_game_image.get_rect()
    game_rules_image = pygame.image.load("images/game_rules.png").convert_alpha()
    game_rules_image_rect = game_rules_image.get_rect()
    game_quit_image = pygame.image.load("images/game_quit.png").convert_alpha()
    game_quit_image_rect = game_quit_image.get_rect()

    # 初始化游戏规则图片并获取图片的矩形位置
    rules_image = pygame.image.load("images/游戏玩法.png").convert_alpha()
    back_image = pygame.image.load("images/back.png").convert_alpha()
    back_image_rect = back_image.get_rect()

    # 标志是否在主界面
    is_ui = True

    # 帧率
    clock = pygame.time.Clock()

    # 主界面循环
    while True:
        # 获取事件信息
        for event in pygame.event.get():
            # 如果点击右上角退出
            if event.type == QUIT:
                # 退出程序
                pygame.quit()
                sys.exit()

        # 如果是主界面
        if is_ui:
            # 绘制背景
            screen.blit(background, (0, 0))

            # 更改主界面按键图片的矩形位置并绘制主界面按键
            start_game_image_rect.left, start_game_image_rect.top = (
                                                                                width - start_game_image_rect.width) // 2, height - 500
            screen.blit(start_game_image, start_game_image_rect)

            game_rules_image_rect = game_rules_image.get_rect()
            game_rules_image_rect.left, game_rules_image_rect.top = (
                                                                                width - game_rules_image_rect.width) // 2, start_game_image_rect.bottom + 50
            screen.blit(game_rules_image, game_rules_image_rect)

            game_quit_image_rect.left, game_quit_image_rect.top = (
                                                                              width - game_quit_image_rect.width) // 2, game_rules_image_rect.bottom + 50
            screen.blit(game_quit_image, game_quit_image_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击”开始游戏“
                if start_game_image_rect.left < pos[0] < start_game_image_rect.right and start_game_image_rect.top < \
                        pos[1] < start_game_image_rect.bottom:
                    # 调用主函数
                    main()
                # 如果用户点击”退出游戏“
                if game_quit_image_rect.left < pos[0] < game_quit_image_rect.right and game_quit_image_rect.top < pos[
                    1] < game_quit_image_rect.bottom:
                    pygame.quit()
                    sys.exit()
                # 如果用户点击”游戏规则“
                if game_rules_image_rect.left < pos[0] < game_rules_image_rect.right and game_rules_image_rect.top < \
                        pos[1] < game_rules_image_rect.bottom:
                    # 离开主界面
                    is_ui = False

        # 进入游戏规则界面
        else:
            # 绘制游戏规则图片
            screen.blit(rules_image, (0, 0))

            # 停止播放背景音乐
            pygame.mixer.music.stop()
            # 循环播放游戏规则音效
            background_sound.play(-1)

            # 更改返回按键图片的矩形位置并绘制返回按键
            back_image_rect.left, game_quit_image_rect.top = width - back_image_rect.width - 10, 10
            screen.blit(back_image, (width - back_image_rect.width - 10, 10))

            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击返回图片
                if back_image_rect.left < pos[0] < back_image_rect.right and back_image_rect.top < pos[
                    1] < back_image_rect.bottom:
                    # 背景音乐停止并进入主界面
                    pygame.mixer.stop()
                    ui()

        # 刷新屏幕
        pygame.display.flip()

        # 设置帧率为60帧
        clock.tick(60)


# 游戏主函数
def main():
    # 循环播放背景音乐
    pygame.mixer.music.play(-1)

    # 用于计算未暂停时经过的时间
    TIME = 0

    # 生成CXK
    me = CXK.CXK(bg_size)

    # 用于存放敌人
    enemies = pygame.sprite.Group()

    # 生成小型敌人
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 40)

    # 生成中型敌人
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 10)

    # 生成大型敌人
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 6)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 10, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 10, me.rect.centery)))

    clock = pygame.time.Clock()

    # 爆炸图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # 暂停
    paused = False
    pause_nor_image = pygame.image.load("images/pause_1.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_2.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/start_1.png").convert_alpha()
    resume_pressed_image = pygame.image.load("images/start_2.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf", 48)
    bomb_num = 3

    # 护盾
    shield_image = pygame.image.load("images/shield.png").convert_alpha()
    shield_rect = shield_image.get_rect()

    # 每10秒发放一个补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    shield_supply = supply.Shield_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 10 * 1000)

    # 超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 无敌时间计时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 暂停计时器
    PAUSE_TIME = USEREVENT + 3
    pygame.time.set_timer(PAUSE_TIME, 1 * 1000)

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 标志是否有护盾
    is_protected = False

    # 生命数量
    life_image = pygame.image.load("images/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 用于切换图片
    CXK_switch_image = 1
    enemy_switch_image = 1

    # 用于延迟
    delay = 100
    enemy_delay = 15

    # 用于限制重复打开记录文件
    recorded = False

    # 标志是否暂停过
    is_pause_time = False

    # 主函数循环
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # 如果有鼠标点击事件
            elif event.type == MOUSEBUTTONDOWN:
                # 如果是鼠标左键点击暂停按键
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    # 更改暂停状态
                    paused = not paused
                    # 如果当前为暂停
                    if paused:
                        # 标志暂停过
                        is_pause_time = True
                        # 暂停补给投放
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        # 背景音乐暂停
                        pygame.mixer.music.pause()
                        # 音效暂停
                        pygame.mixer.pause()
                    # 如果当前不是暂停状态
                    else:
                        # 如果曾经暂停过
                        if is_pause_time:
                            # 设置补给投放时间为10秒减去之前未暂停时经过的时间
                            pygame.time.set_timer(SUPPLY_TIME, (10 - TIME) * 1000)
                        # 从新标志位未暂停
                        is_pause_time = False
                        # 继续播放背景音乐
                        pygame.mixer.music.unpause()
                        # 继续播放音效
                        pygame.mixer.unpause()

            # 检测鼠标移动事件
            elif event.type == MOUSEMOTION:
                # 根据鼠标位置更改暂停/继续按键的样式
                if pause_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            # 检测键盘按下的事件
            elif event.type == KEYDOWN:
                # 如果按下空格键
                if event.key == K_SPACE:
                    # 如果炸弹数量不为0
                    if bomb_num:
                        # 炸弹数量-1
                        bomb_num -= 1
                        # 使用炸弹音效播放
                        bomb_sound.play()
                        # 屏幕内所有敌人暴毙
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            # 如果为用户自定义事件发放补给
            elif event.type == SUPPLY_TIME:
                # 随机选择一个补给发放
                Choice = int(choice([1, 2, 3]))
                if Choice == 1:
                    bomb_supply.reset()
                if Choice == 2:
                    bullet_supply.reset()
                if Choice == 3:
                    shield_supply.reset()
                # 发放补给后计时清零
                TIME = 0

            # 双倍子弹结束
            elif event.type == DOUBLE_BULLET_TIME:
                # 双倍子弹失效
                is_double_bullet = False
                # 取消双倍子弹计时器
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            # 无敌时间结束
            elif event.type == INVINCIBLE_TIME:
                # 不无敌
                me.invincible = False
                # 取消无敌时间计时器
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

            # 非暂停时间自动30秒内计时
            elif event.type == PAUSE_TIME:
                if not paused:
                    if TIME < 29:
                        TIME += 1
                    else:
                        TIME = 0

        # 根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            # 增加10小型敌人，6个中型敌人，4个大型敌人
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升小型敌人的速度
            inc_speed(small_enemies, 1)

        if level == 2 and score > 300000:
            level = 3
            # 增加10小型敌人，6个中型敌人，4个大型敌人
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升小型敌人的速度
            inc_speed(small_enemies, 1)
            # 提升中型敌人的速度
            inc_speed(mid_enemies, 1)

        if level == 3 and score > 600000:
            level = 4
            # 增加10小型敌人，6个中型敌人，4个大型敌人
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升小型敌人的速度
            inc_speed(small_enemies, 1)
            # 提升中型敌人的速度
            inc_speed(mid_enemies, 1)

        if level == 4 and score > 1000000:
            level = 5
            # 增加10小型敌人，6个中型敌人，4个大型敌人
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升小型敌人的速度
            inc_speed(small_enemies, 1)
            # 提升中型敌人的速度
            inc_speed(mid_enemies, 1)

        screen.blit(background, (0, 0))

        if life_num and not paused:

            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUP()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDOWN()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLEFT()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRIGHT()

            # 绘制炸弹补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                # 碰撞检测
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_supply_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                # 碰撞检测
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_supply_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # 绘制护盾补给
            if shield_supply.active:
                shield_supply.move()
                # 碰撞检测
                screen.blit(shield_supply.image, shield_supply.rect)
                if pygame.sprite.collide_mask(shield_supply, me):
                    get_supply_sound.play()
                    is_protected = True
                    shield_supply.active = False

            # 绘制子弹
            if not (delay % 10):
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 10, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 10, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌人
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    # 碰撞检测
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制大型敌人
            for each in big_enemies:
                if each.active:
                    each.move()

                    if enemy_switch_image == 1:
                        screen.blit(each.image1, each.rect)
                    if enemy_switch_image == 2:
                        screen.blit(each.image2, each.rect)
                    if enemy_switch_image == 3:
                        screen.blit(each.image3, each.rect)
                    if enemy_switch_image == 4:
                        screen.blit(each.image4, each.rect)
                    if enemy_switch_image == 5:
                        screen.blit(each.image5, each.rect)
                    if enemy_switch_image == 6:
                        screen.blit(each.image6, each.rect)
                    if enemy_switch_image == 7:
                        screen.blit(each.image7, each.rect)
                    if enemy_switch_image == 8:
                        screen.blit(each.image8, each.rect)
                    if enemy_switch_image == 9:
                        screen.blit(each.image9, each.rect)
                    if enemy_switch_image == 10:
                        screen.blit(each.image10, each.rect)
                    if enemy_switch_image == 11:
                        screen.blit(each.image11, each.rect)
                    if enemy_switch_image == 12:
                        screen.blit(each.image12, each.rect)
                    if enemy_switch_image == 13:
                        screen.blit(each.image13, each.rect)
                    if enemy_switch_image == 14:
                        screen.blit(each.image14, each.rect)
                    if enemy_switch_image == 15:
                        screen.blit(each.image15, each.rect)
                    if enemy_switch_image == 16:
                        screen.blit(each.image16, each.rect)
                    if enemy_switch_image == 17:
                        screen.blit(each.image17, each.rect)
                    if enemy_switch_image == 18:
                        screen.blit(each.image18, each.rect)
                    if enemy_switch_image == 19:
                        screen.blit(each.image19, each.rect)
                        enemy_switch_image = 1

                    # 每15帧切换一次图片
                    if not enemy_delay:
                        enemy_switch_image += 1
                        enemy_delay = 15
                    else:
                        enemy_delay -= 1

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                    # 载入音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        # 绘制毁灭画面
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 3
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌人
            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                else:
                    # 毁灭
                    # enemy3_down_sound.play()
                    if not (delay % 3):
                        # 绘制毁灭画面
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 3
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制小型敌人
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    # enemy3_down_sound.play()
                    if not (delay % 3):
                        # 绘制毁灭画面
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 3
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            anemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if anemies_down and not me.invincible:
                if is_protected:
                    is_protected = False
                    me.invincible = True
                    # 无敌状态计时
                    pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
                else:
                    me.active = False
                    for e in anemies_down:
                        e.active = False

            # 绘制CXK
            if me.active:
                if CXK_switch_image == 1:
                    screen.blit(me.image1, me.rect)
                    me.mask = pygame.mask.from_surface(me.image1)
                if CXK_switch_image == 2:
                    screen.blit(me.image2, me.rect)
                    me.mask = pygame.mask.from_surface(me.image2)
                if CXK_switch_image == 3:
                    screen.blit(me.image3, me.rect)
                    me.mask = pygame.mask.from_surface(me.image3)
                if CXK_switch_image == 4:
                    screen.blit(me.image4, me.rect)
                    me.mask = pygame.mask.from_surface(me.image4)
                if CXK_switch_image == 5:
                    screen.blit(me.image5, me.rect)
                    me.mask = pygame.mask.from_surface(me.image5)
                if CXK_switch_image == 6:
                    screen.blit(me.image6, me.rect)
                    me.mask = pygame.mask.from_surface(me.image6)
                if CXK_switch_image == 7:
                    screen.blit(me.image7, me.rect)
                    me.mask = pygame.mask.from_surface(me.image7)
                if CXK_switch_image == 8:
                    screen.blit(me.image8, me.rect)
                    me.mask = pygame.mask.from_surface(me.image8)
                if CXK_switch_image == 9:
                    screen.blit(me.image9, me.rect)
                    me.mask = pygame.mask.from_surface(me.image9)
                if CXK_switch_image == 10:
                    screen.blit(me.image10, me.rect)
                    me.mask = pygame.mask.from_surface(me.image10)
                if CXK_switch_image == 11:
                    screen.blit(me.image11, me.rect)
                    me.mask = pygame.mask.from_surface(me.image11)
                if CXK_switch_image == 12:
                    screen.blit(me.image12, me.rect)
                    me.mask = pygame.mask.from_surface(me.image12)
                if CXK_switch_image == 13:
                    screen.blit(me.image13, me.rect)
                    me.mask = pygame.mask.from_surface(me.image13)
                if CXK_switch_image == 14:
                    screen.blit(me.image14, me.rect)
                    me.mask = pygame.mask.from_surface(me.image14)
                if CXK_switch_image == 15:
                    screen.blit(me.image15, me.rect)
                    me.mask = pygame.mask.from_surface(me.image15)
                if CXK_switch_image == 16:
                    screen.blit(me.image16, me.rect)
                    me.mask = pygame.mask.from_surface(me.image16)
                if CXK_switch_image == 17:
                    screen.blit(me.image17, me.rect)
                    me.mask = pygame.mask.from_surface(me.image17)
                if CXK_switch_image == 18:
                    screen.blit(me.image18, me.rect)
                    me.mask = pygame.mask.from_surface(me.image18)
                    CXK_switch_image = 1
                else:
                    if not (delay % 6):
                        CXK_switch_image += 1
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        enemy3_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制护盾
            if is_protected:
                screen.blit(shield_image, (me.rect.left - 20, me.rect.top - 5))

            if not delay:
                delay = 100
            else:
                delay -= 1

            # 剩余炸弹数量
            bomb_text = bomb_font.render("X%d" % bomb_num, True, BLACK)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 11 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))

            # 绘制得分
            score_text = score_font.render("Score: %s" % str(score), True, BLACK)
            screen.blit(score_text, (10, 5))

        # 绘制游戏结束画面
        elif life_num == 0:

            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # 读取历史最高得分记录
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    record_score = score
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束界面
            record_score_text = score_font.render("Best:%d" % record_score, True, BLACK)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, BLACK)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height - 500
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, BLACK)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (
                                                                            width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (width - again_rect.width) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击”重新开始“
                if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                    main()
                # 如果用户点击”结束游戏“
                if gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[
                    1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image, pause_rect)

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    try:
        ui()
    except SystemExit:
        pass
    # 异常处理
    except:
        traceback.print_exc()
        pygame.quit()
        os.system("pause")
