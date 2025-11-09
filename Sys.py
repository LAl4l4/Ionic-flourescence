from abc import ABC, abstractmethod
import pygame

class AtkSystem(ABC):
    def Atk(self, target, screen):
        self.AtkStatus(target)
        if not self.IsAttacking:
            return
        self.drawAtk(screen)
        if not self.IsDamageTick():
            return
        for TargetObj in target:
            if self.atkType == "player":
                self.AtkPlayer(TargetObj, screen)
            if self.atkType == "enemynormal":
                self.AtkEnemyNormal(TargetObj, screen)
            
    def AtkPlayer(self, target, screen):    #need: IsAttacking，CanAtkWho，atk，hp
        CanAtk = False
        for obj in self.CanAtkWho:
            if isinstance(target, obj):
                CanAtk = True
        if self.IsInRadius(target) and CanAtk:  
            target.hp = target.hp - self.atk
            target.drawOnAtk(screen)
        
    def AtkEnemyNormal(self, target, screen):  #need: IsAttacking，CanAtkWho，atk，hp
        CanAtk = False
        for obj in self.CanAtkWho:
            if isinstance(target, obj):
                CanAtk = True
        if self.IsInRadius(target) and CanAtk:  
            target.hp = target.hp - self.atk
            target.drawOnAtk(screen)
    
    def IsInRadius(self, target): #need：x, y, atkradius
        selfX, selfY = self.GetCenterCoordinate()
        targetX, targetY = target.GetCenterCoordinate()
        dx = selfX - targetX
        dy = selfY - targetY
        return dx*dx + dy*dy <= self.atkradius * self.atkradius
    
    @abstractmethod
    def GetCenterCoordinate(self):    
        pass
    
class Attackable(AtkSystem):
    @abstractmethod
    def drawOnAtk(self, screen):
        pass
    
class CanAttack(AtkSystem):
    @abstractmethod
    def drawAtk(self, screen):
        pass
    
    @abstractmethod
    def AtkStatus(self, targetlist):#更新攻击状态
        pass
    
    @abstractmethod
    def IsDamageTick(self):
        pass
    
class HasCoordinate(ABC):
    @abstractmethod
    def GetScreenXY(self):
        pass
    
    @abstractmethod
    def GetCoordinate(self):
        pass
    
class ScreenXYUpdater(HasCoordinate):
    def updateScreenXY(self, player):
        playerScreenX, playerScreenY = player.GetScreenXY()
        playerX, playerY = player.GetCoordinate()
        selfX, selfY = self.GetCoordinate()
        screenX = selfX - playerX + playerScreenX
        screenY = selfY - playerY + playerScreenY
        self.LoadScreenCoordinate(screenX, screenY)

    @abstractmethod
    def LoadScreenCoordinate(self, X, Y):
        pass
    
class Drawable(HasCoordinate):
    @abstractmethod
    def Draw(self, screen):
        pass
    
class MoveSys(HasCoordinate):
    def Move(self, map, mapheight, mapwidth, player):
        from glogic import Player, Enemy
        if isinstance(self, Player):
            self.MovePlayer(map, mapheight, mapwidth)
        elif isinstance(self, Enemy):
            self.MoveEnemy(map, mapheight, mapwidth, player)
            
    @abstractmethod
    def loadXY(self, x, y):
        pass
    
    @abstractmethod
    def getWidthHeight(self):
        pass
    
            
    def MovePlayer(self, map, height, width):
        keys = pygame.key.get_pressed()
        #水平速度
        self.vx = 0
        if keys[pygame.K_a]:
            self.vx = -self.speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.vx = self.speed
            self.facing_right = True
        #垂直速度 
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_power
            self.on_ground = False
        self.vy += self.gravity
        if self.vy > 20:  # 限制最大下落速度
            self.vy = 20    
        
        newx, newy = self.GetCoordinate()
        
        if self.CanMoveTo(map, height, width, newx + self.vx, newy):
            newx += self.vx
        
        if self.CanMoveTo(map, height, width, newx, newy + self.vy):
            newy += self.vy
            self.on_ground = False
        else:
            # 被挡住 -> 如果是往下落说明落地了
            if self.vy > 0:
                self.on_ground = True
            self.vy = 0  # 重置竖直速度
        
        self.loadXY(newx, newy)

        
    def CanMoveTo(self, map, height, width, newx, newy):
        if newx < 0 or newy < 0:
            return False
        w, h = self.getWidthHeight()
        if newx + w > width or newy + h > height:
            return False

        MoveObj_rect = pygame.Rect(newx, newy, w, h)
        
        map_tiles = map.getmap()
        
        for row_idx, row in enumerate(map_tiles):
            for col_idx, tile in enumerate(row):
                if not tile.getWalk():
                    continue
                tile_rect = pygame.Rect(col_idx * tile.size , row_idx * tile.size, tile.size, tile.size)
                if MoveObj_rect.colliderect(tile_rect):
                    return False
        return True

    def MoveEnemy(self, map, mapheight, mapwidth, player):
        self.vx = 0
        x, y = self.GetCoordinate()
        px, py = player.GetCoordinate()
        
        if x - px > 20:
            self.vx -= self.speed
        elif x - px < -20:
            self.vx +=self.speed
            
        self.vy += self.gravity
        if self.vy > 20:
            self.vy = 20
            
        newx = x + self.vx
        newy = y + self.vy
        
        if self.CanMoveTo(map, mapheight, mapwidth, newx, y):
            x = newx
        
        if self.CanMoveTo(map, mapheight, mapwidth, x, newy):
            y = newy
            self.on_ground = False
        else:
            self.vy = 0
            self.on_ground = True
            
        self.loadXY(x, y)
    
    