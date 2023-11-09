import math
from copy import copy, deepcopy
from cmu_graphics import *


ground = Rect(0, 250, 4000000000000000, 400, border ="white", fill = "pink", borderWidth = 3)
Label("By Kihea Adams-Wilson and Heldana Yacob", 200, 40, size = 10)
Label("Esc to return to menu", 200, 100, size = 10)
everything = Group(ground)
everything.visible = False
app.background = "pink"
app.speed = 6
app.ready = False
app.baseSpeed = app.speed
app.wrappers = []
def roundToMultiple(num, multiple):
    return multiple * rounded(num / multiple)
def clamp(num, Min, Max):
    return max(Min, min(num, Max))
def map(n, im, iM, om, oM):
    return om + (float(n - im) / float(iM -im) * (oM -om))
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        return self
    def __mul__(self, v):
        if isinstance(v, Vector2):
            return Vector2(self.x * v.x, self.y * v.y)
        else:
            return Vector2(self.x * v, self.y * v)
app.GRAVITY = Vector2(0, .86)
class Player:
    def __init__(self):
        self.sprite = app.plrSprites["cube"]
        self.sprite.rotateAngle = 0
        self.sprite.visible = False
        self.sprite.left = 40
        
        self.sprite.bottom = ground.top
        self.mode = "cube"
        app.plr = self
        self.continuous = False
        self.isJumping = False
        self.onGround = True
        
        self.isAscending = False
        self.velocity = Vector2(app.speed)
        self.jumpStrength = 11
        self.speed = 6
        self.ignoreVelocity = False
        self.died = False
    def update(self):
        #self.collide(0)
        
        if self.mode == "cube":
            if self.isJumping and self.onGround:
                self.jump()
            if not self.onGround:
                self.sprite.rotateAngle += 7.5
                self.velocity += app.GRAVITY
            if self.velocity.y > 100: self.velocity.y = 100
        elif self.mode == "ship":
            #orig = deepcopy(self.sprite.centerY)
            
            if self.isAscending:
                self.velocity += Vector2(0, -.86) * .4
                
            elif not self.onGround:
                self.velocity += app.GRAVITY * .4
            angle  = angleTo(self.sprite.centerX, self.sprite.centerY, self.sprite.centerX + self.velocity.x, self.velocity.y + self.sprite.centerY)
            self.sprite.rotateAngle = angle - 90
        self.sprite.centerY += self.velocity.y
        #self.onGround = False
    def setMode(self, mode):
        self.mode = mode
        self.sprite.visible = False
        self.sprite = app.plrSprites[mode]
        self.sprite.visible = True
    def jump(self):
        self.velocity.y = -self.jumpStrength
    
app.plrSprites = {}
class Level:
    def __init__(self, enemies, blocks, background, collectibles):
        self.enemies = enemies
        self.blocks = blocks
        self.background = background
        self.collectibles = collectibles
        self.items = enemies.items + blocks.items + background.items + collectibles.items
        self.group = Group(enemies.group, blocks.group, background.group, collectibles.group)
        self.group.visible = False
class Button:
    def __init__(self, style, action, *arguments, hideOnClick = False):
        
        self.button = style
        self.action = action
        self.hideOnClick = hideOnClick
        app.wrappers.append(self)
        self.args = arguments
    def click(self):
        if self.hideOnClick:
            self.button.visible = False
        self.action(*self.args)
class ItemGroup:
    def __init__(self, items):
        self.group = Group()
        self.items = items
        for item in items:
            self.group.add(item.sprite)
class Enemy:
    def __init__(self, x, yoffset = 0, color = "black"):
        self.sprite = RegularPolygon(x, ground.top - yoffset - 8, 17, 3, fill = color)
        self.Type = Enemy
        setattr(self.sprite, "Type", Enemy)
class CustomEnemy:
    def __init__(self, x, style, yoffset = 0):
        self.sprite = cloneImage(style)
        self.sprite.bottom = ground.top - yoffset
        self.sprite.centerX = x
        self.Type = Enemy
        setattr(self.sprite, "Type", Enemy)
class Block:
    def __init__(self, x, yoffset = 0, color="black"):
        self.sprite = cloneImage(app.loadedImageAssets["Block"])
        self.sprite.bottom = ground.top - yoffset
        self.sprite.centerX = x
        self.Type = Block
        setattr(self.sprite, "Type", Block)
class CustomBlock:
    def __init__(self, x, sprite, yoffset = 0):
        self.sprite = cloneImage(sprite)
        self.sprite.bottom = ground.top - yoffset
        self.sprite.centerX = x
        self.Type = Block
        setattr(self.sprite, "Type", Block)
#app.ground = CustomBlock(ground)
class Collectible:
    def __init__(self, x, sprite, action, *params, yoffset = 0):
        
        self.sprite = cloneImage(sprite)
        self.sprite.centerX = x
        self.sprite.bottom = ground.top - yoffset
        setattr(self.sprite, "activated", self.activate)
        self.Type = Collectible
        setattr(self.sprite, "Type", Collectible)
        self.action = action
        self.params = params
    def activate(self):
        self.action(*self.params)
class Misc:
    def __init__(self, x, sprite, *params, yoffset = 0):
        self.sprite.left = x
        self.sprite.bottom = ground.top - yoffset
        self.Type = Misc
        setattr(self.sprite, "Type", Misc)
# class SpeedPortal(Collectible):
#     def __init__(self, x, sprite, action, *params, yoffset = 0):
#         super().__init__(x, sprite, action, *params, yoffset = 0)
#         setattr(self.sprite, "Type", SpeedPortal)
def spawnLevel(level):
    level.group.visible = True
    everything.add(level.group)
    app.collectibles = level.collectibles.group
    app.enemies = level.enemies.group
    app.blocks = level.blocks.group
    
app.enemies = Group()
app.blocks = Group()
app.running = False
app.stepsPerSecond = 60
app.plr = None
def Start(level):
    app.running = False
    app.stepsPerSecond = 60
    if hasattr(app, "level") and app.level:
        app.level.group.left = 300
        everything.remove(app.level.group)
        app.level = None
    app.level = level
    if hasattr(app, "plr") and app.plr:
        app.plr.sprite.visible = False
        app.plr = None
    setattr(app, "plr", Player())
    #app.plr = Player()
    app.plr.sprite.visible = True
    
    spawnLevel(level)
    app.speed = app.baseSpeed
    app.plr.velocity.x = app.speed
    ground.left = 0
    everything.visible = True
    app.running = True
def onStep():
    if app.running:
        
        
        everything.left -= app.plr.velocity.x
        app.plr.ignoreVelocity = False
        
        app.plr.update()
        #app.plr.update()
        # if app.plr.died:
        #     app.running = False
        #     Start(app.level)
        blockColliding = everything.hitTest(app.plr.sprite.right, app.plr.sprite.centerY)
        blockOnTop = app.blocks.hitTest(app.plr.sprite.left, app.plr.sprite.bottom)
        PadColliding = app.collectibles.hitTest(app.plr.sprite.right, app.plr.sprite.bottom)
        collectibleColliding = app.collectibles.hitTest(app.plr.sprite.right, app.plr.sprite.centerY)
        app.plr.onGround = False
        if PadColliding:
            PadColliding.activated()
            app.plr.ignoreVelocity = True
        if collectibleColliding and hasattr(collectibleColliding, "activated"):
            getattr(collectibleColliding, "activated")()
            app.plr.ignoreVelocity = True
            
        elif blockColliding and blockColliding != ground:
            Start(app.level)
        if app.plr.sprite.hitsShape(ground):
            blockOnTop = ground
        if blockOnTop and blockOnTop.top != 0:
            app.plr.onGround = True
            if not app.plr.ignoreVelocity:
                app.plr.velocity.y = 0
            if app.plr.mode == "cube":
                app.plr.sprite.rotateAngle = roundToMultiple(app.plr.sprite.rotateAngle, 90)
                app.plr.sprite.bottom = blockOnTop.top
            #app.plr.isJumping = False
        elif not blockOnTop:
            pass
            #app.plr.onGround = False
        if app.plr.sprite.top <= 0:
            app.plr.sprite.top = 0
            app.plr.velocity.y = 0
        #app.plr.update()
    
def onKeyPress(key):
    if key == 'space' and hasattr(app, "plr") and app.plr:
        app.plr.isJumping = True
    elif key == "escape" and app.running:
        if hasattr(app, "level"):
            
            app.running = False
            app.plr.sprite.visible = False
            everything.visible = False
            everything.remove(app.level.group)
            levelSelectorUI.visible = True
            visibleButton.visible = True
            PlayerChanger.button.visible = True
            levelsArray[app.currentIndex].button.visible = True
def onKeyRelease(key):
    if key == 'space' and hasattr(app, "plr") and app.plr:
        app.plr.isJumping = False
def onKeyHold(keys):
    if 'space' in keys:
        onKeyPress('space')
def onMousePress(x, y):
    if app.running and hasattr(app, "plr"):
        if app.plr.mode == "ship":
            app.plr.isAscending = True
        elif app.plr.mode == "wave":
            app.plr.isAscending = not app.plr.isAscending
        elif app.plr.mode == "cube":
            app.plr.isJumping = True
            
    else:
        for button in app.wrappers:
            if button.button.visible and button.button.contains(x, y):
                button.click()
def onMouseRelease(x, y):
    if app.running and hasattr(app, "plr"):
        if app.plr.mode == "ship":
            app.plr.isAscending = False
        elif app.plr.mode == "cube":
            app.plr.isJumping = False
app.MusicAssets = {}
app.ImageAssets = {
    "plr": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/d/d9/Cube001.png/revision/latest/scale-to-width-down/185?cb=20141208151754",
        "left": 200,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr2": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/9/99/Cube002.png/revision/latest/scale-to-width-down/185?cb=20150219061001",
        "left": 230,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr3": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/3/3f/Cube019.png/revision/latest/scale-to-width-down/185?cb=20150220065207",
        "left": 260,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr4": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/7/7b/Cube051.png/revision/latest/scale-to-width-down/185?cb=20150829171312",
        "left": 290,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr5": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/4/47/Cube062.png/revision/latest/scale-to-width-down/185?cb=20160402083631",
        "left": 290,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr6": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/7/7c/Cube074.png/revision/latest/scale-to-width-down/185?cb=20170206113610",
        "left": 290,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr7": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/1/1a/Cube113.png/revision/latest/scale-to-width-down/185?cb=20180506025254",
        "left": 290,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "plr8": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/2/21/Cube126.png/revision/latest/scale-to-width-down/185?cb=20180504223025",
        "left": 290,
        "top": 200,
        "width": 30,
        "height": 30
    },
    "ship": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/d/df/Ship01.png/revision/latest/scale-to-width-down/185?cb=20150724110610",
        "left": 320,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "ship2": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/e/e0/Ship06.png/revision/latest/scale-to-width-down/185?cb=20150724090841",
        "left": 320,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "ship3": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/5/51/Ship10.png/revision/latest/scale-to-width-down/185?cb=20150724104542",
        "left": 320,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "ship4": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/5/50/Ship22.png/revision/latest/scale-to-width-down/185?cb=20150830090036",
        "left": 320,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "ship5": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/7/7c/Ship42.png/revision/latest/scale-to-width-down/185?cb=20180505010013",
        "left": 390,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "ship6": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/c/c5/Ship48.png/revision/latest/scale-to-width-down/185?cb=20180512040019",
        "left": 390,
        "top": 240,
        "width": 40,
        "height": 25
    },
    "wave": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/2/27/Wave01.png/revision/latest/scale-to-width-down/150?cb=20160926044816",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave1": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/6/60/Wave10.png/revision/latest/scale-to-width-down/147?cb=20160926052702",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave2": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/e/ee/Wave19.png/revision/latest/scale-to-width-down/179?cb=20170320085222",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave3": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/d/de/Wave29.png/revision/latest/scale-to-width-down/136?cb=20180324233326",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave4": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/3/38/Wave31.png/revision/latest/scale-to-width-down/136?cb=20180830210724",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave5": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/6/64/Wave27.png/revision/latest/scale-to-width-down/125?cb=20180324000105",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    },
    "wave6": {
        "url": "https://static.wikia.nocookie.net/geometry-dash/images/3/3f/Wave13.png/revision/latest/scale-to-width-down/164?cb=20160926055232",
        "left": 390,
        "top": 280,
        "width": 30,
        "height": 30
    }
}
app.levels = {
    "Ship Test": "e>9ee>9>6b>4b2>5S>9>9b2^5b4>5b4>6^6b4C>8b2>2b3",
    "Jump Pad Test": "j0>6j1>6j2>6J2",
    "Block Test": ">9>9^h>^h>^h>^h>^h>"
}
app.loadedMusicAssets = {}
app.loadedImageAssets = {
    "BlockTop": Image("https://static.wikia.nocookie.net/geometry-dash/images/0/01/RegularBlock01.png/revision/latest?cb=20160604070948", 0,0, width = 30, height = 30, visible = False),
    "BlockBottom": Image("https://static.wikia.nocookie.net/geometry-dash/images/c/cb/GridBlock08.png/revision/latest?cb=20160515081424", 0, 0, width = 30, height = 30, visible = False),
    "Block": Image("https://static.wikia.nocookie.net/geometry-dash/images/c/c3/GridBlock03.png/revision/latest?cb=20160515081423", 0, 0, width = 30, height = 30, visible = False),
    "Spike": Image("https://static.wikia.nocookie.net/geometry-dash/images/8/8a/RegularSpike01.png/revision/latest?cb=20160604071118", 0, 0, width = 30, height = 30, fill = None, visible = False),
    "shipMode": Image("https://static.wikia.nocookie.net/geometry-dash/images/e/e1/ShipPortal.png/revision/latest/scale-to-width-down/60?cb=20160806091442", 0, 0, width = 30, height = 45, visible = False),
    "cubeMode": Image("https://static.wikia.nocookie.net/geometry-dash/images/d/de/CubePortal.png/revision/latest/scale-to-width-down/60?cb=20160806091441", 0, 0, width = 30, height = 45, visible = False),
    "Speed1": Image("https://static.wikia.nocookie.net/geometry-dash/images/c/ce/SpeedPortalS.png/revision/latest/scale-to-width-down/55?cb=20180602110238", 0,0,width = 30, height = 45, visible = False),
    "Speed2": Image("https://static.wikia.nocookie.net/geometry-dash/images/4/46/SpeedPortalN.png/revision/latest/scale-to-width-down/45?cb=20180602110237", 0,0,width = 30, height = 45, visible = False),
    "Speed3": Image("https://static.wikia.nocookie.net/geometry-dash/images/b/b9/SpeedPortalF.png/revision/latest/scale-to-width-down/70?cb=20180602110236", 0,0,width = 60, height = 45, visible = False),
    "Speed4": Image("https://static.wikia.nocookie.net/geometry-dash/images/9/9f/SpeedPortalVF.png/revision/latest/scale-to-width-down/95?cb=20180602110238", 0,0,width = 60, height = 45, visible = False),
    "Speed5": Image("https://static.wikia.nocookie.net/geometry-dash/images/8/82/SpeedPortalEF.png/revision/latest/scale-to-width-down/95?cb=20171206212613", 0,0,width = 70, height = 45, visible = False),
    "JumpOrb1": Image("https://static.wikia.nocookie.net/geometry-dash/images/a/ab/YellowRing.png/revision/latest/scale-to-width-down/100?cb=20160722142856", 0, 0, width = 30, height = 30, visible = False),
    "JumpOrb2": Image("https://static.wikia.nocookie.net/geometry-dash/images/7/7d/MagentaRing.png/revision/latest/scale-to-width-down/100?cb=20160722144515", 0, 0, width = 30, height = 30, visible = False),
    "JumpOrb3": Image("https://static.wikia.nocookie.net/geometry-dash/images/e/ed/RedRing.png/revision/latest/scale-to-width-down/100?cb=20180613101510", 0, 0, width = 30, height = 30, visible = False),
    "JumpOrb4": Image("https://static.wikia.nocookie.net/geometry-dash/images/1/11/BlackRing.png/revision/latest/scale-to-width-down/100?cb=20180613101505", 0, 0, width = 30, height = 30, visible = False),
    "JumpPad1": Image("https://static.wikia.nocookie.net/geometry-dash/images/3/3d/YellowPad.png/revision/latest?cb=20180725100142", 0, 0, width = 30, height = 8, visible = False),
    "JumpPad2": Image("https://static.wikia.nocookie.net/geometry-dash/images/4/4c/MagentaPad.png/revision/latest?cb=20180725095949", 0, 0, width = 30, height = 8, visible = False),
    "JumpPad3": Image("https://static.wikia.nocookie.net/geometry-dash/images/e/ec/RedPad.png/revision/latest/scale-to-width-down/100?cb=20180613101509", 0, 0, width = 30, height = 8, visible = False),
}
app.loadedLevels = {}
def changeMode(mode):
    if hasattr(app, "plr") and app.plr:
        app.plrSprites[mode].centerX = app.plr.sprite.centerX
        app.plrSprites[mode].centerY = app.plr.sprite.centerY
        app.plr.setMode(mode)
def changeSpeed(speed):
    if speed == 1:
        app.plr.velocity.x = app.baseSpeed * .807
    elif speed == 2:
        app.plr.velocity.x = app.baseSpeed * 1
    elif speed == 3:
        app.plr.velocity.x = app.baseSpeed * 1.243
    elif speed == 4:
        app.plr.velocity.x = app.baseSpeed * 1.502
    elif speed == 5:
        app.plr.velocity.x = app.baseSpeed * 1.849
    app.speed = app.plr.velocity.x
def customJump(strength, mustJump):
    if hasattr(app, "plr") and app.plr and (app.plr.isJumping if mustJump else True):
        if strength == 1:
            app.plr.jumpStrength = 11
            app.plr.jump()
            app.plr.jumpStrength = 11
        elif strength == 2:
            app.plr.jumpStrength = 9
            app.plr.jump()
            app.plr.jumpStrength = 11
        elif strength == 3:
            app.plr.jumpStrength = 16
            app.plr.jump()
            app.plr.jumpStrength = 11
        elif strength == 4:
            app.plr.jumpStrength = -400
            app.plr.jump()
            app.plr.jumpStrength = 11
def decodeLevel(string): # Takes a string and creates a level: b3 creates a stack of 3 blocks at x = 300 and b2>3e creates a stack of 2 blocks, skips 3 spaces then creates an enemie
    place = 0
    startingGrid = 300
    creating = None
    creatingNumber = 0
    start = 0
    mode = 0
    
    blocks = []
    enemies = []
    collectibles = []
    li = None
    special = False
    args = []
    for char in string:
        
        if char == "b" and creating == None:
            creating = CustomBlock
            li = blocks
            creatingNumber = 1
        elif char == "h" and creating == None:
            creating = Block
            li = blocks
            creatingNumber = 1
        elif char == ">" and creating == None:
            creating = "Blank"
            creatingNumber = 1
        elif char == "^" and creating == None:
            creating = "VerticalBlank"
            creatingNumber = 1
        elif char == "e" and creating == None:
            creating = CustomEnemy
            args.append(app.loadedImageAssets["Spike"])
            li = enemies
            creatingNumber = 1
        elif char == "S" and creating == None:
            creating = Collectible
            li = collectibles
            creatingNumber = 1
            args.append(app.loadedImageAssets["shipMode"])
            args.append(changeMode)
            args.append("ship")
        elif char == "C" and creating == None:
            creating = Collectible
            li = collectibles
            creatingNumber = 1
            args.append(app.loadedImageAssets["cubeMode"])
            args.append(changeMode)
            args.append("cube")
        elif char == "s" and creating == None:
            creating = Collectible
            mode = 2 #default speed
            creatingNumber = 1
            args.append(app.loadedImageAssets["Speed" + str(mode)])
            args.append(changeSpeed)
            args.append(mode)
            special = "Speed"
            li = collectibles
        elif char == "j" and creating == None:
            creating = Collectible
            mode = 1 #default jump
            creatingNumber = 1
            args.append(app.loadedImageAssets["JumpPad" + str(mode)])
            args.append(customJump)
            args.append(mode)
            args.append(False)
            special = "JumpPad"
            li = collectibles
        elif char == "J" and creating == None:
            creating = Collectible
            mode = 1 #default jump
            creatingNumber = 1
            args.append(app.loadedImageAssets["JumpOrb" + str(mode)])
            args.append(customJump)
            args.append(mode)
            args.append(True)
            special = "JumpOrb"
            li = collectibles
        elif char.isdigit() and creating != None:
            if creating == Collectible and special != False:
                mode = clamp(int(char), 0, 4) + 1
                args[0] = app.loadedImageAssets[special + str(mode)]
                #args[1] = len(args) == 3 and changeSpeed or customJump
                args[2] = mode
            else:
                creatingNumber = int(char)
            
        elif not char.isdigit() and creating != None:
            if creating == "Blank":
                place += creatingNumber
                creatingNumber = 0
            elif creating == "VerticalBlank":
                start = creatingNumber
                place -= 1
            else:
                for creation in range(start, creatingNumber + start):
                    if creating == CustomBlock:
                        sprite = app.loadedImageAssets["BlockBottom"]
                        if (start == 0 and creation == creatingNumber - 1) or (start != 0 and creation == start):
                            sprite = app.loadedImageAssets["BlockTop"]
                        li.append(CustomBlock(startingGrid + place * 30, sprite, yoffset = creation * 30))
                    else:
                        
                        li.append(creating(startingGrid + place * 30, *args, yoffset = creation * 30))
                creatingNumber = 0
                start = 0
                place += 1
            creating = None
            
            mode = 0
            special = False
            args.clear()
            if char == "b" and creating == None:
                creating = CustomBlock
                li = blocks
                creatingNumber = 1
            elif char == "h" and creating == None:
                creating = Block
                li = blocks
                creatingNumber = 1
            elif char == ">" and creating == None:
                creating = "Blank"
                creatingNumber = 1
            elif char == "^" and creating == None:
                creating = "VerticalBlank"
                creatingNumber = 1
            elif char == "e" and creating == None:
                creating = CustomEnemy
                args.append(app.loadedImageAssets["Spike"])
                li = enemies
                creatingNumber = 1
            elif char == "S" and creating == None:
                creating = Collectible
                li = collectibles
                creatingNumber = 1
                args.append(app.loadedImageAssets["shipMode"])
                args.append(changeMode)
                args.append("ship")
            elif char == "C" and creating == None:
                creating = Collectible
                li = collectibles
                creatingNumber = 1
                args.append(app.loadedImageAssets["cubeMode"])
                args.append(changeMode)
                args.append("cube")
            elif char == "s" and creating == None:
                creating = Collectible
                mode = 2 #default speed
                creatingNumber = 1
                args.append(app.loadedImageAssets["Speed" + str(mode)])
                args.append(changeSpeed)
                args.append(mode)
                special = "Speed"
                li = collectibles
            elif char == "j" and creating == None:
                creating = Collectible
                mode = 1 #default jump
                creatingNumber = 1
                args.append(app.loadedImageAssets["JumpPad" + str(mode)])
                args.append(customJump)
                args.append(mode)
                args.append(False)
                special = "JumpPad"
                li = collectibles
            elif char == "J" and creating == None:
                creating = Collectible
                mode = 1 #default jump
                creatingNumber = 1
                args.append(app.loadedImageAssets["JumpOrb" + str(mode)])
                args.append(customJump)
                args.append(mode)
                args.append(True)
                special = "JumpOrb"
                li = collectibles
            elif char.isdigit() and creating != None:
                creatingNumber = int(char)
    if creating != None:
        if creating == "Blank":
            place += creatingNumber
        elif creating == "VerticalBlank":
            start = creatingNumber
            place -= 1
        else:
            for creation in range(start, creatingNumber + start):
                if creating == CustomBlock:
                    sprite = app.loadedImageAssets["BlockBottom"]
                    if (start == 0 and creation == creatingNumber - 1) or (start != 0 and creation == start):
                        args = [app.loadedImageAssets["BlockTop"]]
                    li.append(CustomBlock(startingGrid + place * 30, sprite, yoffset = creation * 30))
                else:
                        
                    li.append(creating(startingGrid + place * 30, *args, yoffset = creation * 30))
    return Level(ItemGroup(enemies), ItemGroup(blocks), ItemGroup([]), ItemGroup(collectibles))


PlayerChangerUI = Group(
    
    )

SelectorShip = Rect(0,0, 40, 25, fill = None, border = "yellow", visible = False)
SelectorCube = Rect(0, 0, 33, 33, fill = None, border = "yellow", visible=False)
SelectorWave = Rect(0,0,32,32, fill=None, border = "yellow", visible=False)
def ShowPlayerChangerUI():
    PlayerChangerUI.visible = True
    SelectorShip.visible = True
    SelectorWave.visible = True
    SelectorCube.visible = True
    levelSelectorUI.visible = False
    
def HidePlayerChangerUI(t = False):
    PlayerChangerUI.visible = False
    SelectorShip.visible = False
    SelectorWave.visible = False
    SelectorCube.visible = False
    if t:
        levelSelectorUI.visible = True

HidePlayerChangerUI()

def changeCharacter(character, typ):
    app.plrSprites[typ] = cloneImage(character)
    app.plrSprites[typ].visible = False
    if typ == "cube":
        SelectorCube.centerX = character.centerX
        SelectorCube.centerY = character.centerY
        SelectorCube.visible = not PlayerChanger.button.visible
    elif typ == "ship":
        SelectorShip.centerX = character.centerX
        SelectorShip.centerY = character.centerY
        SelectorShip.visible = not PlayerChanger.button.visible
    elif typ == "wave":
        SelectorWave.centerX = character.centerX
        SelectorWave.centerY = character.centerY
        SelectorWave.visible = not PlayerChanger.button.visible
LoaderBase = Rect(80, 240, 240, 40, fill = "black")
Loader = Rect(80, 240, 1, 40, fill = "blue")
Title = Label("TRIGONOMETRY RUN", 200, 80, fill = "blue", border = "black", borderWidth = 1, size = 30, font="orbitron")
PlayerChanger = Button(Rect(120, 160, 120, 60, fill = "blue"), ShowPlayerChangerUI, hideOnClick = True)
visibleButton = Group(
        PlayerChanger.button,
        Label("Character", PlayerChanger.button.centerX, PlayerChanger.button.centerY, size = 24, fill = "white")
        )

LoadScreen = Group(
    Title,
    LoaderBase,
    Loader,
    visibleButton
    )
def fullHide():
    HidePlayerChangerUI(t = True)
    PlayerChanger.button.visible = True
    SelectorShip.visible = False
    SelectorCube.visible = False
    SelectorWave.visible = False
exitB = Button(Label("X", 20, 20, fill = "red", size = 15), fullHide)
PlayerChangerUI.add(exitB.button)
def loadAssets():
    LoadScreen.visible = True
    totalAssets = len(app.levels) + len(app.MusicAssets) + len(app.ImageAssets)
    numberLoaded = 0
    CONSTANT = 1 / totalAssets * LoaderBase.width
    for key, levelstring in app.levels.items():
        app.loadedLevels[key] = decodeLevel(levelstring)
        numberLoaded += 1
        Loader.width += CONSTANT
    for key, musicAsset in app.MusicAssets.items():
        app.loadedMusicAssets[key] = Sound(musicAsset)
        numberLoaded += 1
        Loader.width += CONSTANT
    for key, imageAsset in app.ImageAssets.items():
        app.loadedImageAssets[key] = Image(imageAsset["url"], imageAsset["left"], imageAsset["top"], height = imageAsset["height"], width = imageAsset["width"], visible = False, fill = None)
        app.loadedImageAssets[key].name = key
        numberLoaded += 1
        Loader.width += CONSTANT
    LoadScreen.remove(LoaderBase)
    LoadScreen.remove(Loader)
    
def cloneImage(image):
    return Image(image.url, image.left, image.top, height = image.height, width = image.width, fill = image.fill, visible = image.visible)
loadAssets()

levelSelectorUI = Group()
levelsArray = []
app.currentIndex = 0
def goRight():
    levelsArray[app.currentIndex].button.visible = False
    app.currentIndex += 1
    if app.currentIndex >= len(levelsArray):
        app.currentIndex = 0
    levelsArray[app.currentIndex].button.visible = True
def goLeft():
    levelsArray[app.currentIndex].button.visible = False
    app.currentIndex -= 1
    if app.currentIndex < 0:
        app.currentIndex = len(levelsArray) - 1
    levelsArray[app.currentIndex].button.visible = True
    
rightSelectorUI = Group(
    Rect(360, 280, 40, 80, fill = "black"),
    Label(">", 380, 320, fill = "white")
    )
rightSelector = Button(
    rightSelectorUI,
    goRight
    )
LeftSelectorUI = Group(
    Rect(0, 280, 40, 80, fill = "black"),
    Label("<", 20, 320, fill = "white")
    )
LeftSelector = Button(
    LeftSelectorUI,
    goLeft
    )
levelSelectorUI.add(LeftSelector.button)
levelSelectorUI.add(rightSelector.button)
def hide(ui):
    ui.visible = False
def hideAndStart(ui, level):
    hide(ui)
    fullHide()
    visibleButton.visible = False
    PlayerChanger.button.visible = False
    Start(level)
for name, level in app.loadedLevels.items():
    base = Rect(80, 280, 240, 80, fill = "black")
    Leveltext = Label("Level: " + str(len(levelsArray) + 1), 200, 300, size = 15, fill = "white")
    mainNameText = Label(name, base.centerX, base.centerY, size = 30, fill = "white")
    style = Group(base, Leveltext, mainNameText)
    levelButton = Button(
        style,
        hideAndStart,
        style,
        level
        )
    
    levelsArray.append(levelButton)
    levelSelectorUI.add(style)
    if len(levelsArray) > 1:
        levelButton.button.visible = False

plrs = [app.loadedImageAssets["plr"], app.loadedImageAssets["plr2"], app.loadedImageAssets["plr3"], app.loadedImageAssets["plr4"],app.loadedImageAssets["plr5"], app.loadedImageAssets["plr6"], app.loadedImageAssets["plr7"], app.loadedImageAssets["plr8"]]
ships = [app.loadedImageAssets["ship"], app.loadedImageAssets["ship2"], app.loadedImageAssets["ship3"], app.loadedImageAssets["ship5"], app.loadedImageAssets["ship4"], app.loadedImageAssets["ship6"]]
waves = [app.loadedImageAssets["wave"], app.loadedImageAssets["wave2"], app.loadedImageAssets["wave3"], app.loadedImageAssets["wave4"], app.loadedImageAssets["wave5"], app.loadedImageAssets["wave6"]]

    #Start(app.loadedLevels["stack"])
PlayerChangerUI.characters = 0
for character in plrs:
    clone = cloneImage(character)
    
    PlayerChangerUI.add(clone)
    clone.left = 30 + PlayerChangerUI.characters * 30
    if PlayerChangerUI.characters > 0 and PlayerChangerUI.characters < len(plrs):
        pass
        clone.left += 10 * PlayerChangerUI.characters
    if not "cube" in app.plrSprites:
        changeCharacter(clone, "cube")    
    ui = Button(clone, changeCharacter, clone, "cube")
    PlayerChangerUI.add(ui.button)
    PlayerChangerUI.characters += 1
PlayerChangerUI.characters = 0
for character in ships:
    clone = cloneImage(character)
    
    PlayerChangerUI.add(clone)
    clone.left = 40 + PlayerChangerUI.characters * 40
    if PlayerChangerUI.characters > 0 and PlayerChangerUI.characters < len(ships):
        clone.left += 10 * PlayerChangerUI.characters
    if not "ship" in app.plrSprites:
        changeCharacter(clone, "ship")    
    ui = Button(clone, changeCharacter, clone, "ship")
    PlayerChangerUI.add(ui.button)
    PlayerChangerUI.characters += 1
PlayerChangerUI.characters = 0
for character in waves:
    clone = cloneImage(character)
    
    PlayerChangerUI.add(clone)
    clone.left = 30 + PlayerChangerUI.characters * 30
    if PlayerChangerUI.characters > 0 and PlayerChangerUI.characters < len(waves):
        clone.left += 10 * PlayerChangerUI.characters
    if not "wave" in app.plrSprites:
        changeCharacter(clone, "wave")    
    ui = Button(clone, changeCharacter, clone, "wave")
    PlayerChangerUI.add(ui.button)
    PlayerChangerUI.characters += 1


app.ready = True
cmu_graphics.run()