import Sys, math
import os, json, pygame

class Door(Sys.Drawable, Sys.ScreenXYUpdater):
    def __init__(self, x, y, basepath, id, tilesize):
        self.basepath = basepath
        self.x = x
        self.y = y
        self.screenX = x
        self.screenY = y
        self.id = id
        self.width = tilesize
        self.height = 2*tilesize
        
        self.isopen = False
        self.loadjson()
        
    def isOpen(self):
        return self.isopen
        
    def isCollide(self, x, y):
        door_center_x = self.x + self.width / 2
        door_center_y = self.y + self.height / 2

        dx = door_center_x - x
        dy = door_center_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        threshold = self.width * 0.5
        return distance <= threshold
        
    def loadjson(self):
        jsonpath = os.path.join(self.basepath, "Entity/entity.json")
        with open(jsonpath, "r", encoding="utf-8") as d:
            data = json.load(d)
        
        thisinfo = data[f"{self.id}"]
        
        self.uppath = os.path.join(self.basepath, thisinfo["uppath"])
        self.downpath = os.path.join(self.basepath, thisinfo["downpath"])
        self.uppath_open = os.path.join(self.basepath, thisinfo["uppath_unlock"])
        self.downpath_open = os.path.join(self.basepath, thisinfo["downpath_unlock"])
        
        self.imgUp = pygame.image.load(self.uppath).convert_alpha()
        self.imgUp = pygame.transform.scale(self.imgUp, (self.width, self.width))
        self.imgDown = pygame.image.load(self.downpath).convert_alpha()
        self.imgDown = pygame.transform.scale(self.imgDown, (self.width, self.width))
    
    def setOpen(self, open):
        self.isopen = open
        if self.isopen:
            self.imgUp = pygame.image.load(self.uppath_open).convert_alpha()
            self.imgUp = pygame.transform.scale(self.imgUp, (self.width, self.width))
            self.imgDown = pygame.image.load(self.downpath_open).convert_alpha()
            self.imgDown = pygame.transform.scale(self.imgDown, (self.width, self.width))
    
    def GetCoordinate(self):
        return self.x, self.y
    
    def LoadScreenCoordinate(self, X, Y):
        self.screenX = X
        self.screenY = Y
    
    def GetScreenXY(self):
        return self.screenX, self.screenY
    
    def Draw(self, screen):
        screen.blit(self.imgUp, (self.screenX, self.screenY))
        screen.blit(self.imgDown, (self.screenX, self.screenY + self.height//2))