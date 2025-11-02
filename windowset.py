import pygame
from abc import ABC, abstractmethod
import os

class interfaceManager():
    def __init__(self, screen, basepath, gameworld):
        self.screen = screen
        self.window = "menu"
        self.basepath = basepath
        self.font = pygame.font.SysFont("Arial", 40)
        self.menu = mainMenu(self.screen, self.font, self.basepath)
        self.gameworld = gameworld
        self.gameworld.Initialize()
        
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
            self.gameworld.updateMove()
            self.gameworld.Draw()
            self.gameworld.Attack()
            self.gameworld.updateRemoveObjects()
            self.gameworld.updatePackageData()
            self.gameworld.updateDrawXY()
            self.gameworld.GeneralUpdate()
        
    def updateWindow(self):
        choice = None
        if self.window == "menu":
            choice = self.menu.clickHandle(self.event)   
        elif self.window == "game":
            choice = self.gameworld.escapeHandle(self.event)
                                  
        if choice == "start":
            self.window = "game"
        elif choice == "quit":
            self.window = "quit"
        elif choice == "menu":
            self.window = "menu"

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

        
        
class gameLoader(loadtexture):
    def __init__(self, screen, basepath):
        self.screen = screen
        self.basepath = basepath
    
    def iniGame(self):
        pass
    
    def loadtex(self):
        return super().loadtex()