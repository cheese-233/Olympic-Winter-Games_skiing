# -*- coding: utf-8 -*-

from turtle import title
import pygame
from pygame.locals import *
import sys
import random


Player_pic = pygame.image.load("./images/1.png")    #打开图片
Player_pic_with_flip = pygame.image.load("./images/flip_1.png")
Player_pic_hit = pygame.image.load("./images/hit_1.png")
Stone_pic = pygame.image.load("./images/stone.png")
win_pic = pygame.image.load("./images/win.png")
flag_pic = pygame.image.load("./images/flag.png")
background_pic = pygame.image.load("./images/background.png")
background_music = "./sounds/bgmusic.mp3"  # 打开mp3文件
handclap_music = "./sounds/handclap.mp3"


def again():
    screen.fill(color='white')  # 为窗口填充白色
    for sprite in snows:  # 显示整个精灵组中的精灵
        sprite.kill()
    for i in range(100):
        snow = Snow()
        snows.add(snow)
    for sprite in stones:  # 显示整个精灵组中的精灵
        sprite.kill()
    for sprite in flags:  # 显示整个精灵组中的精灵
        sprite.kill()
    if background_pic_show:
        screen.blit(background_pic, (screen_height/2-100, screen_width/2-100))
    for i in range(10):
        stone = Stone()
        hit = pygame.sprite.spritecollide(stone, stones, True)
        if hit:  # 如果重叠石头
            stone.kill()
            i -= 1
        stones.add(stone)
    for sprite in stones:  # 显示整个精灵组中的精灵
        screen.blit(sprite.image, sprite.rect)
    flagwidth = random.randrange(20, 80)
    flagheight = random.randrange(10, 100)
    flag = Flag(flagwidth,
                flagheight)
    flags.add(flag)
    hit = pygame.sprite.spritecollide(flag, stones, True)
    while hit:  # 如果重叠石头
            flag.kill()
            flagwidth = random.randrange(20, 80)
            flagheight = random.randrange(10, 100)
            flag = Flag(flagwidth,
                                flagheight)
            flags.add(flag)
            hit = pygame.sprite.spritecollide(flag, stones, True)
    for i in range(9):
        flagwidth = flagwidth+random.randrange(10, 100)
        flagheight = flagheight+random.randrange(0, 100)
        flag = Flag(flagwidth,
                flagheight)
        flags.add(flag)
        hit = pygame.sprite.spritecollide(flag, stones, True)
        if hit:
            flag.kill()
            i -= 1
    
class Player(pygame.sprite.Sprite):  # 继承pygame.sprite.Sprite精灵对象
    def __init__(self):
        super().__init__()
        self.image = Player_pic #人物图片
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.rect.x = screen_width-self.rect.width  # 重新设置X轴坐标
        self.rect.y = 0  # 重新设置Y轴坐标


    def update(self, pressed_keys):
        global player_speed,goes_to_win,player_round
        img_copy = Player_pic.copy()    #旋转人物图片
        flip_img_copy = Player_pic_with_flip.copy()
        if player_speed < 2:
            player_speed += 0.1  # 增加玩家速度
        elif player_speed < 4:
            player_speed += 0.05  # 增加玩家速度
        elif player_speed > 4:
            player_speed += 0.02  # 增加玩家速度
        if pressed_keys[K_UP]:  # 如果按下的是方向上键
            player_round = 0
            img_with_flip = pygame.transform.flip(  
                flip_img_copy, False, False)  # 旋转人物图片
            self.image = img_with_flip
            self.rect.move_ip(0, -(player_speed))  # 更新rect的X,Y
            player_round = 3
        elif pressed_keys[K_DOWN]:  # 如果按下的是方向下键
            player_round = 0
            img_with_flip = pygame.transform.flip(
                flip_img_copy, False, True)  # 旋转人物图片
            self.image = img_with_flip
            self.rect.move_ip(0, player_speed)  # 更新rect的X,Y
            player_round = 2
        elif pressed_keys[K_LEFT]:  # 如果按下的是方向左键
            player_round = 0
            goes_to_win = goes_to_win - player_speed  # 减少距离
            img_with_flip = pygame.transform.flip(
                img_copy, False, False)  # 旋转人物图片
            self.image = img_with_flip
            self.rect.move_ip(-(player_speed), 0)  # 更新rect的X,Y
            player_round = 1
        else:
            if int(player_speed) > 0:
                player_speed -= 0.15    #减少玩家速度
                if player_round == 1:
                    self.rect.move_ip(-(player_speed), 0)  # 更新rect的X,Y
                elif player_round == 2:
                    self.rect.move_ip(0, player_speed)  # 更新rect的X,Y
                elif player_round == 3:
                    self.rect.move_ip(0, -(player_speed))  # 更新rect的X,Y
        self.stay_inside()  # 保证一直在窗口里面


    def stay_inside(self):  # 保证一直在窗口里面
        global player_speed,rounds,goes_to_win
        if self.rect.top < 0:  # 如果上边界小于0
            self.rect.top = 0  # 设置上边界为0
            player_speed = 0
        if self.rect.bottom > screen.get_height():  # 如果下边界超过窗口高度
            self.rect.bottom = screen.get_height()  # 设置下边界为窗口高度
            player_speed = 0
        if self.rect.left < 0:  # 如果左边界小于0
            self.rect.left = screen.get_width()-100  # 设置左边界为0
            rounds += 1
            goes_to_win = (go_to_win-rounds+1)*screen.get_width()  # 减少一圈
            again() #重来
            player_speed = 0



class Stone(pygame.sprite.Sprite):  #石头
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = Stone_pic  # 石头图片
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.rect.x = random.randrange(0, screen_width-screen_width/8)
        self.rect.y = random.randrange(0,screen_height)


class Flag(pygame.sprite.Sprite):  # 旗
    def __init__(self,it_width,it_height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = flag_pic  # 旗图片
        self.rect = self.image.get_rect()  # 获取X,Y坐标和大小
        self.rect.x = it_width
        self.rect.y = it_height


class Snow(pygame.sprite.Sprite):   #雪花
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        # 将雪花缩放成随机生成的大小
        random_surface = random.randrange(5, 10)
        self.image = pygame.Surface((random_surface, random_surface))
        self.image.fill('lightgray')
        self.rect = self.image.get_rect()   # 获取X,Y坐标和大小
        self.rect.x = random.randrange(0, screen_width)
        self.rect.y = random.randrange(0, screen_height)


class Winner(pygame.sprite.Sprite):  # 胜利判定
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.Surface((50, screen_height))
        self.image.fill('red')
        self.rect = self.image.get_rect()   # 获取X,Y坐标和大小
        self.rect.x = 0
        self.rect.y = 0


def plus_points():  #记分规则
    global points
    if player_speed == 0:   #根据玩家速度记分
        pass
    elif player_speed < 2:
        points += 0.001
    elif player_speed < 3:
        points += 0.01
    elif player_speed < 5:
        points += 0.02
    elif player_speed == 5:
        points += 0.05


def how_to_win():  # 胜利规则
    global goes_to_win,tips_line
    if go_to_win == rounds:  # 最后一圈
        winners = pygame.sprite.Group()  # 定义精灵组,用于存放所有精灵
        winner = Winner()  # 创建winner对象
        winners.add(winner)  # 添加winner到精灵组
        screen.blit(winner.image, (0,0))
        font_surface = font.render('最后一圈！', True, 'black')  # 将文字生成 surface对象
        tips_line = 24
        screen.blit(font_surface, (0, 24*2))  # 将文字surface对象 放到背景surface上
        hit = pygame.sprite.spritecollide(player, winners, False)  # 设定赢事件
        if hit:
            screen.fill(color='white')  # 为窗口填充白色
            for i in range(10):  # 放烟花
                screen.blit(win_pic, (random.randrange(
                    0, screen.get_width()), random.randrange(0, screen.get_height())))
            font_surface = font.render(
                '恭喜你，你赢了！', True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                    3, screen.get_width()/3))
            font_surface = font.render(
                '共获得分数：', True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                    3, screen.get_width()/3-24))
            font_surface = font.render(
                str(int(points)), True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                    3+24*6, screen.get_width()/3-24))
            pygame.display.update()  # 刷新整个平面 或者 pygame.display.flip()
            pygame.mixer.init()  # 载入
            pygame.mixer.music.load(handclap_music)  # 加载MP3文件
            pygame.mixer.music.play()  # 播放mp3文件
            winrunning = True
            global running
            while winrunning:
                for event in pygame.event.get():  # 获取所有事件
                    if event.type == QUIT:  # 如果是QUIT事件,如点击关闭窗口按钮
                        running = False
                        winrunning = False
                        break
                    elif pygame.mixer.music.get_busy() == False:  # 获取播放状态
                        running = False
                        winrunning = False
                        break
    else:
        tips_line = 0


def how_to_hit(doing_what): #doing_what：因为什么死亡
        global points,running,player,rounds,points,goes_to_win
        player.image = Player_pic_hit
        if background_pic_show:
            screen.blit(background_pic, (screen_height/2-100, screen_width/2-100))
        for sprite in snows:  # 显示整个精灵组中的精灵
            screen.blit(sprite.image, sprite.rect)
        for sprite in stones:  # 显示整个精灵组中的精灵
            screen.blit(sprite.image, sprite.rect)
        for sprite in all_sprite:  # 显示整个精灵组中的精灵
            screen.blit(sprite.image, sprite.rect)
        for sprite in flags:  # 显示整个精灵组中的精灵
            screen.blit(sprite.image, sprite.rect)
        font_surface = font.render(
                '你'+str(doing_what)+'！', True, 'red')  # 将文字生成 surface对象
        screen.blit(font_surface, (0, 0))  # 将文字surface对象 放到背景surface上
        pygame.display.flip()  # 刷新整个平面
        clock.tick(0.5)
        screen.fill(color='white')
        this_running = True
        for i in range(6):
            if this_running != True:
                break
            font_surface = font.render(
                '你'+str(doing_what)+'！', True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3, screen.get_width()/3))
            font_surface = font.render('当前分数：', True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3, screen.get_width()/3+24))
            font_surface = font.render(
                str(int(points)), True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3+24*5, screen.get_width()/3+24))
            font_surface = font.render(
                "你将在", True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3, screen.get_width()/3+24*2))
            font_surface = font.render(
                str(int(5-i)), True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3+24*3, screen.get_width()/3+24*2))
            font_surface = font.render(
                "秒后重生", True, 'black')  # 将文字生成 surface对象
            # 将文字surface对象 放到背景surface上
            screen.blit(font_surface, (screen.get_height() /
                                       3+24*4, screen.get_width()/3+24*2))
            pygame.display.flip()   # 刷新整个平面
            for event in pygame.event.get():  # 获取所有事件
                if event.type == QUIT:  # 如果是QUIT事件,如点击关闭窗口按钮
                    running = False
                    this_running = False
                    break
            clock.tick(1)
            pygame.display.flip()
            screen.fill(color='white')
        player.rect.x = screen_width-player.rect.width  # 重新设置X轴坐标
        player.rect.y = 0  # 重新设置Y轴坐标
        rounds = 0  # 圈数
        points = 0  #重置分数
        goes_to_win = (go_to_win+1)*screen_width    #重置距离
        again()
        player.image = Player_pic
        

'''主程序'''
pygame.init()  # 初始化pygame

'''参数设置'''
screen_width = 1280 #窗口长度
screen_height = 720 #窗口宽度
player_round = 0    #玩家方向
points = 0  #初始化分数
player_speed = 0
screen = pygame.display.set_mode((screen_width, screen_height))  # 创建窗口
pygame.display.set_caption("冬奥会作品")
player = Player()  # 创建Player对象
running = False
background_pic_show = True  #是否显示背景图片
font_name = pygame.font.match_font('SimHei')  # 获得字体文件
font = pygame.font.Font(font_name, 24)  # 获取font对象（需要字体文件）
speed = 100 #游戏速度
go_to_win = 5  #距终点距离（圈数）
rounds = 0  #圈数
tips_line = 0   #左上角变化文字
goes_to_win = (go_to_win+1)*screen_width  # 当前距终点距离（像素）
clock = pygame.time.Clock()  # 创建Clock用于跟踪时间
all_sprite = pygame.sprite.Group()  # 定义精灵组,用于存放所有精灵
all_sprite.add(player)  # 添加player到精灵组
snows = pygame.sprite.Group()  # 定义精灵组,用于存放所有精灵
stones = pygame.sprite.Group()  # 定义精灵组,用于存放所有精灵
flags = pygame.sprite.Group()  # 定义精灵组,用于存放所有精灵


'''新手教程'''
screen.fill(color='white')  # 为窗口填充白色
pygame.display.update()  # 刷新整个平面 或者 pygame.display.flip()
font_surface = font.render(  
    '教程：', True, 'black')  # 将文字生成 surface对象
# 将文字surface对象 放到背景surface上
screen.blit(font_surface, (screen.get_height() /
                           3, screen.get_width()/3-24*2))
font_surface = font.render(
    '按方向上、下、左键移动人物', True, 'black')  # 将文字生成 surface对象
# 将文字surface对象 放到背景surface上
screen.blit(font_surface, (screen.get_height() /
                           3, screen.get_width()/3-24))
font_surface = font.render(
    '祝你好运！', True, 'black')  # 将文字生成 surface对象
# 将文字surface对象 放到背景surface上
screen.blit(font_surface, (screen.get_height() /
                           3, screen.get_width()/3))
font = pygame.font.Font(font_name, 36)  # 获取font对象（需要字体文件）
font_surface = font.render(
    '冬奥会作品——滑雪', True, 'dimgray')  # 将文字生成 surface对象
# 将文字surface对象 放到背景surface上
screen.blit(font_surface, (screen.get_height() /
                           3+3, screen.get_width()/3-24*5+3))
font_surface = font.render(
    '冬奥会作品——滑雪', True, 'darkcyan')  # 将文字生成 surface对象
# 将文字surface对象 放到背景surface上
screen.blit(font_surface, (screen.get_height() /
                           3, screen.get_width()/3-24*5))
font = pygame.font.Font(font_name, 24)  # 获取font对象（需要字体文件）
pygame.display.update()  # 刷新整个平面 或者 pygame.display.flip()
for i in range(3):  
    clock.tick(1)   #计时3秒
    pressed_key = pygame.key.get_pressed()
running = True  #允许运行
screen.fill(color='white')  # 为窗口填充白色
pygame.display.update()  # 刷新整个平面 或者 pygame.display.flip()

'''创建场地'''
again()


'''正式开始'''
while running: 
    screen.fill(color='white')  # 为窗口填充白色
    if(player_speed > 5):
        player_speed = 5  # 保持玩家速度
    if pygame.mixer.music.get_busy() == False:  #获取播放状态
        pygame.mixer.init() #载入
        pygame.mixer.music.load(background_music)  # 加载MP3文件
        pygame.mixer.music.play()  # 播放mp3文件
    for event in pygame.event.get():  # 获取所有事件
        if event.type == QUIT:  # 如果是QUIT事件,如点击关闭窗口按钮
            running = False
    clock.tick(speed)  # 每秒刷新多少帧,不设置按键后移动的飞快
    pressed_key = pygame.key.get_pressed()  # 获取按键
    plus_points()   #记分
    hit = pygame.sprite.spritecollide(player, stones, False) #设定撞击事件
    if hit: #撞击石头
        how_to_hit("撞上了石头")
    hit = pygame.sprite.spritecollide(player, flags, True)  # 设定撞击事件
    if hit:  # 碰到小旗
        points += 1 #加一分
    if background_pic_show:
        screen.blit(background_pic,(screen_height/2-100,screen_width/2-100))
    for sprite in snows:  # 显示整个精灵组中的精灵
        screen.blit(sprite.image, sprite.rect)
    for sprite in stones:  # 显示整个精灵组中的精灵
        screen.blit(sprite.image, sprite.rect)
    for sprite in flags:  # 显示整个精灵组中的精灵
        screen.blit(sprite.image, sprite.rect)
    for sprite in all_sprite:  # 显示整个精灵组中的精灵
        screen.blit(sprite.image, sprite.rect)
        player.update(pressed_key)  # 更新位置
    how_to_win()  # 赢
    if int(player_speed) == 0:
        if int(points) > 0:
            points -= 0.05
        font_surface = font.render(
            '因为你没有移动，已经减分！', True, 'red')  # 将文字生成 surface对象
        # 将文字surface对象 放到背景surface上
        screen.blit(font_surface, (0, 48+tips_line))
    font_surface = font.render('当前分数：', True, 'black')  # 将文字生成 surface对象
    screen.blit(font_surface, (0, 0))  # 将文字surface对象 放到背景surface上
    font_surface = font.render(str(int(points)), True, 'black')  # 将文字生成 surface对象
    screen.blit(font_surface, (5*24, 0))  # 将文字surface对象 放到背景surface上
    font_surface = font.render('距终点还有：', True, 'black')  # 将文字生成 surface对象
    screen.blit(font_surface, (0, 24))  # 将文字surface对象 放到背景surface上
    font_surface = font.render(
        str(int(goes_to_win)), True, 'black')  # 将文字生成 surface对象
    screen.blit(font_surface, (6*24, 24))  # 将文字surface对象 放到背景surface上
    pygame.display.update()  # 刷新整个平面 或者 pygame.display.flip()


pygame.quit()  # 退出pygame
sys.exit() #退出程序
