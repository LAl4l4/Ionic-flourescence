import os, pygame
from glogic import Player
import glogic
import windowset

# 初始化 Pygame
pygame.init()


WIDTH, HEIGHT = 1200, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.SCALED | pygame.DOUBLEBUF,
    vsync =1
    )
pygame.display.set_caption("Ionic fluorescence")

base_path = os.path.dirname(os.path.abspath(__file__))  # 当前脚本所在目录
bg_img_path = os.path.join(base_path, "Materials", "map_background.png")



# 创建角色
playername = "Cosmos"
playeratk = 10
playerhp = 100
playerwidth = 150
playerheight = 150
user1 = Player(playername, playeratk, playerhp, playerwidth, playerheight)
pl_img_path = os.path.join(base_path, "Materials", "player_transcript.png")
PlayerImg = pygame.image.load(pl_img_path).convert_alpha()
PlayerImg = pygame.transform.scale(PlayerImg, (user1.player_width, user1.player_height))
PlayerImgRight = pygame.transform.flip(PlayerImg, True, False)

# create enemy
EnemyHP = 100
EnemyATK = 5
EnemySpeed = 5
EnemyRadius = 100
EnemyAtkRadius = 150
en_img_path = os.path.join(base_path, "Materials", "diren1.png")
EnemyImg = pygame.image.load(en_img_path).convert_alpha()
EnemyImg = pygame.transform.scale(EnemyImg, (EnemyRadius*2, EnemyRadius*2))
Enemies = [glogic.Enemy.getEnemy(
    EnemyATK, EnemyHP, EnemySpeed, EnemyRadius, EnemyAtkRadius, EnemyImg
    ) for _ in range(3)]



# 字体对象
font = pygame.font.SysFont("Arial", 30)
# 控制游戏帧率的时钟对象
clock = pygame.time.Clock()


window = windowset.interfaceManager(screen, base_path)

# 游戏主循环
running = True
while running:
    
    Events = pygame.event.get()
    #如果退出了就把游戏关了
    for event in Events:
        if event.type == pygame.QUIT:
            running = False

    # 填充背景颜色（RGB）
    screen.fill((0, 128, 255))
    
    
    #更新窗口事件
    window.LoadEvents(Events)
    window.updateWindow()
    window.drawWindow()
    if running == True:
        running = window.quitHandle()
    
    # 控制帧率
    clock.tick(60)
    # 更新显示内容
    pygame.display.flip()
    
# 退出 Pygame
pygame.quit()

