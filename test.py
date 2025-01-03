import time
import math
from events import Mouse

from aim import AutoAimBot

mouse = Mouse()

aimbot = AutoAimBot(windowTitle='Quake 3: Arena')

aimbot.mainLoop()


