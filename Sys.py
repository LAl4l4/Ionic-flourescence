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
            target.OnAtk()
            
            # 为敌人添加击退效果（根据攻击者位置计算方向）
            from glogic import Enemy
            if isinstance(target, Enemy):
                selfX, selfY = self.GetCenterCoordinate()
                targetX, targetY = target.GetCenterCoordinate()
                dx = targetX - selfX
                dy = targetY - selfY
                # 归一化方向并应用击退力度
                distance = (dx*dx + dy*dy) ** 0.5
                if distance > 0:
                    knockback_strength = 12
                    target.knockback_vx = (dx / distance) * knockback_strength
                    target.knockback_vy = (dy / distance) * knockback_strength - 8  # 额外向上分量
        
    def AtkEnemyNormal(self, target, screen):  #need: IsAttacking，CanAtkWho，atk，hp
        CanAtk = False
        for obj in self.CanAtkWho:
            if isinstance(target, obj):
                CanAtk = True
        if self.IsInRadius(target) and CanAtk:  
            target.hp = target.hp - self.atk
            target.OnAtk()
    
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
    def OnAtk(self):
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
        x, y = self.GetCoordinate()
        px, py = player.GetCoordinate()
        
        # 如果有击退速度，优先应用击退
        if abs(self.knockback_vx) > 0.5 or abs(self.knockback_vy) > 2:
            # 应用击退速度
            self.vx = self.knockback_vx
            # knockback_vy 会被重力影响，所以直接加到vy上
            self.vy = self.knockback_vy
            # 衰减击退速度
            self.knockback_vx *= self.knockback_decay
            self.knockback_vy *= self.knockback_decay
        else:
            # 没有击退时，正常追踪玩家
            self.knockback_vx = 0
            self.knockback_vy = 0
            
            self.vx = 0
            if x - px > 20:
                self.vx = -self.speed
            elif x - px < -20:
                self.vx = self.speed
        
        # 应用重力（无论是否在击退中）
        self.vy += self.gravity
        if self.vy > 20:
            self.vy = 20
            
        newx = x + self.vx
        newy = y + self.vy
        
        if self.CanMoveTo(map, mapheight, mapwidth, newx, y):
            x = newx
        else:
            # 碰到墙壁，停止水平击退
            self.knockback_vx = 0
        
        if self.CanMoveTo(map, mapheight, mapwidth, x, newy):
            y = newy
            self.on_ground = False
        else:
            self.vy = 0
            self.on_ground = True
            # 落地时停止垂直击退
            self.knockback_vy = 0
            
        self.loadXY(x, y)
    
    