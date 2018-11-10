class Bullet(object):
    # Model
    def __init__(self, cx, cy, angle, speed):
        # A bullet has a position, a size, a direction, and a speed
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.angle = angle
        self.speed = speed
        
    # View
    def draw(self, canvas):
        canvas.create_oval(self.cx - self.r, self.cy - self.r, 
                           self.cx + self.r, self.cy + self.r,
                           fill="red", outline=None)

    # Controller
    def moveBullet(self):
        # Move according to the original trajectory
        self.cx += math.cos(math.radians(self.angle))*self.speed
        self.cy -= math.sin(math.radians(self.angle))*self.speed 
        
    def isOffscreen(self, width, height):
        # Check if the bullet has moved fully offscreen
        return (self.cx + self.r <= 0 or self.cx - self.r >= width) and \
               (self.cy + self.r <= 0 or self.cy - self.r >= height)

    
class BulletSpawner(object):
    import random
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def makeBullet(self, screenWidth, screenHeight):
       
        side = random.choice(["topbot","leftright"])
        if side == "topbot":
            x = random.randint(0,screenWidth)
            y = random.choice([0,screenHeight])
        elif side == "leftright":
            x = random.choice([0,screenWidth])
            y = random.randint(0,screenHeight)
        
        speed = random.randint(10,40)
    
        angle = math.degrees(math.atan((y *1. - screenHeight/2)/(screenWidth/2 - x)))
    
        
        if x > 300:
            angle = math.degrees(math.atan((x * 1. - screenWidth/2)/(y - screenHeight/2))) - 90
            if y > 300:
                angle += 180
        
        return Bullet(x, y, angle, speed)