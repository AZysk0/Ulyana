import time
import math
from events import Mouse


mouse = Mouse()

theta = 0
x = y = 0

mouse.moveTo(200, 200)

while True:
    time.sleep(1 / 144)
    
    # x = int(100 * math.cos(theta)) + 200
    # y = int(100 * math.sin(theta)) + 200
      
    # mouse.click('left')
    # mouse.moveTo(x, y)
    # mouse.moveBy(int(10 * math.cos(theta)), int(10 * math.sin(theta)))
    mouse.moveBy(int(60 * math.cos(theta)), 0)
    
    theta = (theta + 1 / 60) % 6.28
    


