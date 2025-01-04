import time
import math
from events import Mouse, KeyboardInputHandler
import ctypes

from aim import AutoAimBot, AutoFireBot

# mouse = Mouse()
aimbot = AutoAimBot(windowTitle='Quake 3: Arena')
aimbot.mainLoop()

# autofire = AutoFireBot(windowTitle='Quake 3: Arena')
# autofire.mainLoop()

# keyboardListener = KeyboardInputHandler()

# def main():
#     try:
#         while True:
#             keysPressed = keyboardListener.getState()
#             if keysPressed:
#                 print(f"Keys pressed: {keysPressed}")
#             time.sleep(0.1)
#     except KeyboardInterrupt:
#         print("Exiting...")


# if __name__ == "__main__":
#     main()




