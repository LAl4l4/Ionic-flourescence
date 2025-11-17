import pygame
from abc import ABC, abstractmethod
import os, random, json
import glogic

class interfaceManager():
    def __init__(self, screen, basepath):
        self.screen = screen
        self.window = "menu"
        self.basepath = basepath
        self.font = pygame.font.SysFont("Arial", 40)
        self.menu = mainMenu(self.screen, self.font, self.basepath)
        self.loadPlayer()
    #玩家数据在不同地图间不能丢失，所以独立在地图外先创建再传进去    
    def loadPlayer(self):
        self.player = glogic.Player(self.basepath)
        
    def loadGameWindow(self):
        self.gamewindow = gameWindow(self.screen, "normal", self.basepath, self.player, self.font)
        
    def loadWin(self):
        self.winpage = winPage(self.font)
        
    def LoadEvents(self, events):
        self.event = events
        
    def quitHandle(self):#返回是否继续循环
        if self.window == "quit":
            return False
        return True
        
    def drawWindow(self):
        if self.window == "menu":
            self.menu.drawMenu()
        elif self.window == "game":
            if not hasattr(self, "gamewindow"):
                self.loadGameWindow()
            self.gamewindow.Refresh()
        elif self.window == "winpage":
            if not hasattr(self, "winpage"):
                self.loadWin()
            self.gamewindow.Draw()
            self.winpage.Draw(self.screen)
            
        
    def updateWindow(self):
        choice = None
        if self.window == "menu":
            choice = self.menu.clickHandle(self.event)   
        elif self.window == "game":
            choice = self.gamewindow.clickHandle(self.event)
        elif self.window == "winpage":
            choice = self.winpage.clickHandle(self.event)
                                  
        if choice == "start":
            self.window = "game"
        elif choice == "quit":
            self.window = "quit"
        elif choice == "menu":
            if self.window == "winpage":
                if hasattr(self, "gamewindow"):
                    del self.gamewindow
                    del self.winpage
                    del self.player
                    self.loadPlayer()
            self.window = "menu"
        elif choice == "win":
            self.window = "winpage"

class loadtexture(ABC):
    @abstractmethod
    def loadtex(self):
        pass
                    
class mainMenu(loadtexture):
    def __init__(self, screen, font, basepath):
        self.screen = screen
        self.font = font
        self.basepath = basepath
        self.setbutton()
        self.loadtex()
        
        
    def setbutton(self):
        screen_w, screen_h = self.screen.get_size()
        button_w, button_h = screen_w//3, screen_h//10
        spacing = button_h
        
        total_height = 2 * button_h + spacing
        start_y = (screen_h - total_height) // 2
        
        midlength = (button_w // button_h) - 2 
        
        self.buttons = [
        button(self.basepath, midlength, button_h,  # tilesize=40
               (screen_w - button_w) // 2, start_y,
               self.screen, "start", self.font),
        button(self.basepath, midlength, button_h,
               (screen_w - button_w) // 2, start_y + button_h + spacing,
               self.screen, "quit", self.font)
        ]
        
    def loadtex(self):
        bgpath = os.path.join(self.basepath, "Materials", "background", "cavebackground.png")
        self.background = pygame.image.load(bgpath).convert()
        
        screen_w, screen_h = self.screen.get_size()
        img_w, img_h = self.background.get_size()
        scale = max(screen_w / img_w, screen_h / img_h)
        new_w = int(img_w * scale)
        new_h = int(img_h * scale)
        self.background = pygame.transform.smoothscale(self.background, (new_w, new_h))
        self.bg_rect = self.background.get_rect(center=(screen_w // 2, screen_h // 2))
        
    def drawMenu(self):
        self.screen.blit(self.background, self.bg_rect)
        for btn in self.buttons:
            btn.drawButton()
            
    def clickHandle(self, events):
        for btn in self.buttons:
            btn.loadEvents(events)
            e = btn.eventsHandle()
            if e != None:
                return e
    
class button(loadtexture):
    def __init__(self, basepath, midlength, tilesize, x, y, screen, btnname, font):
        self.basepath =  basepath
        self.midlength = midlength
        self.x = x
        self.y = y
        self.screen = screen
        self.tilesize = tilesize #单个图块边长
        self.btnname = btnname
        self.font = font
        self.loadtex()
        
    def loadEvents(self, events):
        self.events = events
    
    def eventsHandle(self):
        for e in self.events:
            if e.type != pygame.MOUSEBUTTONDOWN:
                return None
            mx, my = e.pos
            if self.getRect().collidepoint(mx, my):
                return self.btnname
    
    def getRect(self):
        width = (self.midlength + 2) * self.tilesize
        height = self.tilesize
        return pygame.Rect(self.x, self.y, width, height)
    
    def loadtex(self):
        leftpath = os.path.join(self.basepath, "Materials", "button", "buttononeleft.png")
        self.leftimg = pygame.image.load(leftpath).convert_alpha()
        self.leftimg = pygame.transform.smoothscale(self.leftimg, (self.tilesize, self.tilesize))
        middlepath = os.path.join(self.basepath, "Materials", "button", "buttononemiddle.png")
        self.middleimg = pygame.image.load(middlepath).convert_alpha()
        self.middleimg = pygame.transform.smoothscale(self.middleimg, (self.tilesize, self.tilesize))
        rightpath = os.path.join(self.basepath, "Materials", "button", "buttononeright.png")
        self.rightimg = pygame.image.load(rightpath).convert_alpha()
        self.rightimg = pygame.transform.smoothscale(self.rightimg, (self.tilesize, self.tilesize))
        
    def drawButton(self):
        self.screen.blit(self.leftimg, (self.x, self.y))
        for i in range(self.midlength - 1):
            self.screen.blit(self.middleimg, (self.x + (i + 1) * self.tilesize, self.y))
        self.screen.blit(self.rightimg, (self.x + self.midlength * self.tilesize, self.y))
        
        label = self.font.render(self.btnname.upper(), True, (255, 255, 255))
        label_rect = label.get_rect(center=self.getRect().center)
        self.screen.blit(label, label_rect)
        
        mx, my = pygame.mouse.get_pos()
        if self.getRect().collidepoint(mx, my):
            dark_surface = pygame.Surface((self.getRect().width, self.getRect().height), pygame.SRCALPHA)
            dark_surface.fill((0, 0, 0, 100))  # RGBA，最后一个是透明度
            self.screen.blit(dark_surface, (self.x, self.y))

class box():
    def __init__(self, font, basepath, imgsize, player, tag, type, value):
        self.font = font
        self.basepath = basepath
        self.imgsize = imgsize
        self.player = player
        self.tag = tag
        self.type = type
        self.value = value
        self.loadtex()
    
    def loadtex(self):
        bluebox = os.path.join(self.basepath, "Materials/bonus/lock_blue.png")
        greenbox = os.path.join(self.basepath, "Materials/bonus/lock_green.png")
        redbox = os.path.join(self.basepath, "Materials/bonus/lock_red.png")
        
        if self.type == "atk":
            self.img = pygame.image.load(redbox).convert_alpha()
        elif self.type == "hp":
            self.img = pygame.image.load(greenbox).convert_alpha()
        elif self.type == "spd":
            self.img = pygame.image.load(bluebox).convert_alpha()
            
        self.img = pygame.transform.smoothscale(self.img, (self.imgsize, self.imgsize))
            
    def loadXY(self, x, y):
        self.x = x
        self.y = y
            
    def clickHandle(self, events):
        if self.isClick(events):
            if self.type == "atk":
                self.player.atk += self.value
            elif self.type == "hp":
                self.player.hp += self.value
            elif self.type == "spd":
                self.player.speed += self.value
            return True
                
    
    def isClick(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                self.rect = pygame.Rect(self.x, self.y, self.imgsize, self.imgsize)
                if self.rect.collidepoint(mx, my):
                    return True
        return False
    
    def Draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        label = self.font.render(f"{self.tag}", True, (255, 255, 255))
        label_rect = label.get_rect(center=(self.x + self.imgsize // 2, self.y - 50))
        screen.blit(label, label_rect)

class bonusPage():
    def __init__(self, basepath, imgsize, player, font):
        self.basepath = basepath
        self.imgsize = imgsize
        self.player = player
        self.font = font

        self.loadbox(3)
        
    def loadbox(self, num):
        tagpath = os.path.join(self.basepath, "bonustag", "bonus.json")
        with open(tagpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        tagsnum = data["tagsnum"]
        keys = list(range(1, tagsnum + 1))
        selected_keys = random.sample(keys, num)
        
        self.box = []
        tags = data["tags"]
        for key in selected_keys:
            type = tags[f"{key}"]["type"]
            value = tags[f"{key}"]["value"]
            tag = tags[f"{key}"]["tag"]
            thisbox = box(self.font, self.basepath, self.imgsize, 
                          self.player, tag, type, value)
            self.box.append(thisbox)

        
    def Draw(self, screen):
        screen.fill((30, 80, 80))
        screen_width, screen_height = screen.get_size()
        
        gap = self.imgsize
        num_boxes = len(self.box)
        total_width = num_boxes*self.imgsize + (num_boxes-1)*gap
        start_x = (screen_width - total_width) / 2
        y = (screen_height - self.imgsize) / 2
        for i, b in enumerate(self.box):
            x = start_x + i*(self.imgsize + gap)
            self.box[i].loadXY(x, y)
            b.Draw(screen)
               
    def clickHandle(self, events):
        for b in self.box:
            if b.clickHandle(events):
                return "game"
        return None
        
        
class gameWindow():
    def __init__(self, screen, windowtype, basepath, player, font):
        self.screen = screen
        self.counter = 0
        self.window = windowtype
        self.basepath = basepath
        self.player = player
        self.font = font
        self.randomWindow()
        
    def randomWindow(self):
        self.counter += 1 
        if hasattr(self, "gameworld"):
            del self.gameworld
        self.mapname = "start_cave"
        self.iniGameWorld()
        
    def iniGameWorld(self):
        self.gameworld = glogic.GameWorld(self.screen, f"{self.mapname}", self.player)
        
    def iniBonus(self):
        self.bonus = bonusPage(self.basepath, 150, self.player, self.font)
    
    def clickHandle(self, events):
        choice = None
        if self.window == "normal":
            choice = self.gameworld.escapeHandle(events)
        elif self.window == "bonus":
            choice = self.bonus.clickHandle(events)
            
        if choice == "win" and self.counter >=3:
            return "win"
        elif choice == "win":
            if hasattr(self, "bonus"):
                del self.bonus
            self.iniBonus()
            self.window = "bonus"
        elif choice == "game" and self.counter <=3:
            self.window = "normal"
            if hasattr(self, "gameworld"):
                del self.gameworld
            self.randomWindow()
        elif choice == "game":
            self.window = "boss"
        elif choice == "menu":
            return "menu"
            
    
    #只绘制，用于最后的winpage 
    def Draw(self):
        self.gameworld.Draw()
       
    #执行游戏逻辑并绘制 
    def Refresh(self):
        if self.window == "normal":
            self.gameworld.Refresh()
        elif self.window == "bonus":          
            self.bonus.Draw(self.screen)
        
    
class winPage():
    def __init__(self, font):
        self.font = font
        self.timecounter = 0
        self.waittime = 120
    
    def Draw(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # 黑色半透明背景 (RGBA)
        screen.blit(overlay, (0, 0))
    
    # “通关”文字
        text = self.font.render("You Win!", True, (255, 255, 255))
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        
    def clickHandle(self, event):
        for e in event:
            if e.type == pygame.MOUSEBUTTONDOWN:
                return "menu"
        
        self.timecounter += 1
        if self.timecounter > self.waittime:
            return "menu"
        return None
    
    