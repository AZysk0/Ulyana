import time
import math
import ctypes
import cv2 as cv

from hwnd import WindowHandler, WindowCaptureWin32, WindowCaptureMSS
from events import Mouse, KeyboardInputHandler
from aim import AutoAimBot, AutoFireBot
from debug import DebugFPS, FrameDebugger

# mouse = Mouse()
# aimbot = AutoAimBot(windowTitle='Quake 3: Arena')
# aimbot.mainLoop()

autofire = AutoFireBot(windowTitle='Quake 3: Arena')
autofire.mainLoop()

# windowCapture = WindowCaptureWin32(windowTitle='Quake 3: Arena')
# windowCapture = WindowCaptureWin32(windowTitle='Windows PowerShell')
# windowCapture = WindowCaptureMSS(windowTitle='Quake 3: Arena')

# frameDebugger = FrameDebugger()
# fpsDebugger = DebugFPS(sz=20)

# windowCapture.listWindowNames()

# while True:
    
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break
    
#     prevTime = time.time()
    
#     currentFrame = windowCapture.takeScreenshot()

#     currTime = time.time()
    
#     dt = currTime - prevTime
#     fpsDebugger.append(dt)
#     dtAvg = fpsDebugger.average()
    
#     fps = int(1 / dtAvg)
#     # shapeX, shapeY, channels = currentFrame.shape
#     debugInfo = {
#         'fps': fps,
#         'frameShape': str(tuple(currentFrame.shape))
#     }
    
#     debugFrame = frameDebugger(currentFrame, debugInfo)
    
#     cv.imshow(f"WindowCapture", debugFrame)

# cv.destroyAllWindows()

