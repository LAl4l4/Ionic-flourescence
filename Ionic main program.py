import os, pygame
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
    # 暗红色,但是开发过程还是用比较亮的颜色吧
    screen.fill((30, 80, 80))
    
    
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

