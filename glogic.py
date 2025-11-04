import pygame
import random
import math
from abc import ABC, abstractmethod
import os, json

#这是窗口的，不是地图的，地图的在self.width 和 self.height
WIDTH, HEIGHT = 1200, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
    
    

class GameWorld():
    def __init__(self, screen, mapname):
        self.mapname = mapname
        self.screen = screen
        
        self.font = pygame.font.SysFont("Arial", 40)
        self.tilesize = 150
        self.Initialize()
        
    
    def Initialize(self):
        self.totalObj = []
        self.removedObj = []
        
        self.basepath = os.path.dirname(os.path.abspath(__file__))
        self.loadjson()
        
        self.Map = Map(self.tilesize, self.mapname)
        self.totalObj.append(self.Map)
        
        self.player = Player(self.basepath)
        self.totalObj.append(self.player)
        self.CreateUI()
        
        
        
        
    def loadjson(self):
        filepath = f"{self.mapname}.json"
        jsonpath = os.path.join("Map", filepath)
        
        self.jsonpath = os.path.join(self.basepath, jsonpath)
        
        with open(self.jsonpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        mapinfo = data["map_info"]
        
        self.width = mapinfo["width"]
        self.height = mapinfo["height"]
        self.tilesize = mapinfo["tilesize"]

    def CreateUI(self):
        self.ingameui = InGameUI(self.player, self.font, self.screen)
        
    def GeneralUpdate(self):
        self.ingameui.Draw()

    
    def escapeHandle(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "menu"
        return None

    def Move(self):
        self.movable = []
        
        for obj in self.totalObj:
            if isinstance(obj, MoveSys):
                self.movable.append(obj)
                
        for obj in self.movable:
            obj.Move(self.Map, self.height, self.width)
        
            
    def updateDrawXY(self):
        self.DrawXYneeder = []
        for obj in self.totalObj:
            if isinstance(obj, ScreenXYUpdater):
                self.DrawXYneeder.append(obj)
                
        for obj in self.DrawXYneeder:
            obj.updateScreenXY(self.player)
    
    def Draw(self):
        self.updateDrawXY()
        
        self.drawable = []
        for obj in self.totalObj:
            if isinstance(obj, Drawable):
                self.drawable.append(obj)
        
        for obj in self.drawable:
            obj.Draw(self.screen)
    
                             
    def Attack(self):
        self.canAttack = []
        self.attackable = []
        for obj in self.totalObj:
            if isinstance(obj, CanAttack):
                self.canAttack.append(obj)
            if isinstance(obj, Attackable):
                self.attackable.append(obj)
            
        for obj in self.canAttack:
            obj.Atk(self.attackable, self.screen)
            for target in self.attackable:
                if target.hp <= 0 and not isinstance(target, Player):
                    self.removedObj.append(target)

        

    def updateRemoveObjects(self):
        for obj in self.removedObj:
            if obj in self.totalObj:
                self.totalObj.remove(obj)
            
        self.removedObj = []


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
    def Draw(self):
        pass
       
class MoveSys(HasCoordinate):
    def Move(self, map, mapheight, mapwidth):
        if isinstance(self, Player):
            self.MovePlayer(map, mapheight, mapwidth)
        elif isinstance(self, Enemy):
            self.MoveEnemy()
            
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

    def MoveEnemy(self):
        pass

class Player(MoveSys, CanAttack, Drawable, Attackable):
    def __init__(self, basepath):
        self.basepath = basepath
        self.loadjson()
        
        self.player_x, self.player_y = CENTER_X - self.width//2, CENTER_Y - self.height//2
        self.Drawx, self.Drawy = CENTER_X - self.width//2, CENTER_Y - self.height//2
        self.AtkCounter = 0
        self.facing_right = True 
        
        self.isdmgtick = False
        self.IsAttacking = False
        self.CanAtkWho = [barrier, Enemy]

        self.atkType = "player"
        
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.gravity = 1.2
        self.jump_power = 20
        self.on_ground = False
        
    def loadjson(self):
        filepath = "Player/player.json"
        jsonpath = os.path.join(self.basepath, filepath)
        
        with open(jsonpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.hp = data["hp"]
        self.atk = data["atk"]
        self.name = data["name"]
        self.height = data["height"]
        self.width = data["width"]
        self.speed = data["speed"]
        self.atkradius = data["atkradius"]
        
        imgpath = os.path.join(self.basepath, data["path"])
        self.imgleft = pygame.image.load(imgpath).convert_alpha()
        self.imgleft = pygame.transform.scale(self.imgleft, (self.height, self.width))
        self.imgright = pygame.transform.flip(self.imgleft, True, False)
        
        
    def getWidthHeight(self):
        return self.width, self.height

    def GetCoordinate(self):
        return self.player_x, self.player_y
    
    def GetScreenXY(self):
        return self.Drawx, self.Drawy
    
    def GetCenterCoordinate(self):    
        return self.player_x + self.width//2, self.player_y + self.height//2
         
    def Draw(self, screen):
        if  self.facing_right:
            screen.blit(self.imgright, (self.Drawx, self.Drawy))
        else:
            screen.blit(self.imgleft, (self.Drawx, self.Drawy))
    
    
    def AtkStatus(self, tglist):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.AtkCounter == 0:
            self.AtkCounter = 40
        if self.AtkCounter > 0:
            self.AtkCounter -= 1
        if self.AtkCounter == 35:
            self.isdmgtick = True
        else:
            self.isdmgtick = False
        if self.AtkCounter > 30:
            self.IsAttacking = True
            return
        self.IsAttacking = False
           
    def drawOnAtk(self, screen):
        pass
    
    def drawAtk(self,screen):
        attack_radius = self.atkradius
        player_center = self.GetCenterCoordinate()
        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (player_center[0] - attack_radius, player_center[1] - attack_radius))
    
    def IsDamageTick(self):
        return self.isdmgtick
    
    def loadXY(self, x, y):
        self.player_x = x
        self.player_y = y
            
       
class InGameUI(Drawable):
    def __init__(self, player, font, screen):
        self.player = player
        self.font = font
        self.screen = screen
        
    def Draw(self):
        name_text = self.font.render(f"{self.player.name}", True, (255, 255, 255))
        hp_text = self.font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
        self.screen.blit(name_text, (50, 50))
        self.screen.blit(hp_text, (50, 150))
        
    def GetCoordinate(self):
        return super().GetCoordinate()
    
    def GetScreenXY(self):
        return super().GetScreenXY()
        
    
class barrier(ScreenXYUpdater, Attackable, Drawable):
    def __init__(self,x,y,length, Img):
        self.x = x
        self.y = y
        self.length = length
        self.Img = Img
        self.ScreenX = self.x
        self.ScreenY = self.y
        
        self.IsCollidable = True
        self.hp = 1
      
    def create_barrier(length, player, Img):
        x=random.randint(0,int(2*WIDTH-length))
        y=random.randint(0,int(2*HEIGHT-length))
        if x > player.player_x - length and x < player.player_x + player.player_width:
            x = x + length + player.player_width
        if y > player.player_y - length and y < player.player_y + player.player_height:
            y = y + length + player.player_height
        bar = barrier(x,y,length, Img)
        return bar
    
    def BarGetCoodi(self, player):#传入玩家实例
        Bx = self.x - player.player_x + player.Drawx
        By = self.y - player.player_y + player.Drawy
        return Bx, By#返回障碍物在屏幕中的位置

    def drawOnAtk(self, screen):
        pass
    
    def LoadScreenCoordinate(self, X, Y):
        self.ScreenX = X
        self.ScreenY = Y
    
    def GetCoordinate(self):
        return self.x, self.y
        
    def GetScreenXY(self):
        return self.ScreenX, self.ScreenY
        
    def GetCenterCoordinate(self):
        x = self.x
        y = self.y
        return x + self.length//2, y + self.length//2
    
    #draw方法
    def Draw(self, screen, player):
        #出屏幕就不画
        if -self.length < self.ScreenX < WIDTH and -self.length < self.ScreenY < HEIGHT:
            screen.blit(self.Img, (self.ScreenX, self.ScreenY))
    
class Map(Drawable, ScreenXYUpdater):
    def __init__(self, TileSize, mapname):
        self.IsCollidable = False
        self.x = 0
        self.y = 0
        self.ScreenX = 0
        self.ScreenY = 0
        
        self.TileSize = TileSize
        self.basepath = os.path.dirname(os.path.abspath(__file__))
        
        self.Initialize(mapname)
        
    def Initialize(self, mapname):
        self.name = mapname
        self.read_from_json(mapname)
        self.loadmap()
        
        
    def read_from_json(self, mapname):    
        filepath = f"{mapname}.json"
        jsonpath = os.path.join("Map", filepath)
        
        self.jsonpath = os.path.join(self.basepath, jsonpath)
        
        with open(self.jsonpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        tileinfo = data["tile_info"]
        self.tile_info = {int(code): info for code, info in tileinfo.items()}
        
        self.tile_grid_codes = [[tile["code"] for tile in row] for row in data["map"]]
        self.rowlen = len(self.tile_grid_codes)
        self.collen = len(self.tile_grid_codes[0])
        
    def loadmap(self):
        self.map = []
        for r in range(self.rowlen):
            newrow = []
            for c in range(self.collen):
                code = self.tile_grid_codes[r][c]
                info = self.tile_info[code]
                
                thistile = maptile(
                    code = code,
                    path = info["path"],
                    walkable = info["walkable"],
                    up_throughable = info["upThroughable"],
                    size = self.TileSize,
                    basepath = self.basepath
                )
                thistile.loadtex()
                newrow.append(thistile)
            self.map.append(newrow)

    def getmap(self):
        return self.map

    def get_TileInfo(self):
        return self.tile_info
    
    def LoadScreenCoordinate(self, X, Y):
        self.ScreenX = X
        self.ScreenY = Y

    def GetScreenXY(self):
        return self.ScreenX, self.ScreenY
    
    def GetCoordinate(self):
        return self.x, self.y
    
    def Draw(self, screen):
        for row in range(self.rowlen):
            for col in range(self.collen):
                tile = self.map[row][col]
                if tile.texture is None:
                    continue

                world_x = col * self.TileSize
                world_y = row * self.TileSize
                screen_x = self.ScreenX + world_x
                screen_y = self.ScreenY + world_y

                tile.DrawTile(screen_x, screen_y, screen)
       
          
class maptile():
    def __init__(self, code, path, walkable, up_throughable, size, basepath):
        self.code = code
        self.path = path
        self.walkable = walkable          # 是否可走
        self.up_throughable = up_throughable  # 是否可从下穿过
        self.size = size                  # 格子大小（像素）
        self.basepath = basepath          # 工程根目录
        self.loadtex() 
        
    def getWalk(self):
        return self.walkable
        
    def loadtex(self):
        if not self.path:
            self.texture = None
            return

        texpath = os.path.join(self.basepath, self.path)
        self.texture = pygame.image.load(texpath).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.size, self.size))
        
    def DrawTile(self, screenX, screenY, screen):
        if -self.size < screenX < screen.get_width() and -self.size < screenY < screen.get_height():
            screen.blit(self.texture, (screenX, screenY))
        
              
class Enemy(ScreenXYUpdater, CanAttack, Attackable, MoveSys, Drawable):
    def __init__(self,atk,hp,speed,radius, atkradius, Img):
        self.hp = hp
        self.atk = atk
        self.speed = speed
        self.radius = radius
        self.x = random.randint(0, 2*WIDTH)
        self.y = random.randint(0, 2*HEIGHT)
        self.Img = Img
        self.screen_x = self.x
        self.screen_y = self.y
        
        self.Counter = 0
        self.atkradius = atkradius
        self.IsAttacking = False
        self.isdmgtick = False
        self.CanAtkWho = [Player]
        self.IsCollidable = False
        self.atkType = "enemynormal"
    
    def getEnemy(atk,hp,speed,radius,atkradius, Img):
        enemy = Enemy(atk,hp,speed,radius,atkradius, Img)
        return enemy
    
    def Move(self, notusedobst, player):
        # 计算敌人到玩家的方向向量
        dx = player.player_x - self.x
        dy = player.player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # 如果距离大于0，按比例移动
        if distance > 20:
            self.x += self.speed * dx / distance
            self.y += self.speed * dy / distance
            
    def GetCoordinate(self):
        return self.x, self.y
    
    def GetScreenXY(self):
        return self.screen_x, self.screen_y
    
    def LoadScreenCoordinate(self, X, Y):
        self.screen_x = X
        self.screen_y = Y
    
    def Draw(self, screen, player):
        if -self.radius < self.screen_x < WIDTH and -self.radius < self.screen_y < HEIGHT:
            screen.blit(self.Img, (self.screen_x, self.screen_y))
    
    def drawAtk(self, screen):
        attack_radius = self.atkradius
        x, y = self.GetScreenXY()
        x = x + self.radius
        y = y + self.radius
        # 半透明圆效果
        surface = pygame.Surface((2*attack_radius, 2*attack_radius), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 255, 80), (attack_radius, attack_radius), attack_radius)
        screen.blit(surface, (x - attack_radius, y - attack_radius))
    
    def AtkStatus(self, targetlist):
        Atk = False
        for target in targetlist:
            if not self.IsInRadius(target):
                continue
            for cawobj in self.CanAtkWho:
                if isinstance(target, cawobj):
                    Atk = True
        if self.Counter > 0:
            self.Counter -= 1
        if self.Counter == 55:
            self.isdmgtick = True
        elif True:
            self.isdmgtick = False
        if self.Counter > 50:
            self.IsAttacking = True
            return
        if self.Counter == 0 and Atk == True:
            self.Counter = 60
        self.IsAttacking = False
    
    def IsDamageTick(self):
        return self.isdmgtick
    
    def drawOnAtk(self, screen):
        pass
    
    def GetCenterCoordinate(self):
        return self.x + self.radius, self.y + self.radius
    
class statusbar():
    def __init__(self):
        pass


