import ctypes
from typing import Tuple, Any, Literal


class Mouse:
    # init some constans for mouse events
    # source https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    
    def __init__(self):
        self.pressedButtons = set()
        
        # use these guys later
        # self.movementVelocity = (0, 0)
    
    def moveBy(self, dx, dy):
        ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
    
    def moveTo(self, x, y):
        ctypes.windll.user32.SetCursorPos(x, y)

    def click(self, mouseBtn: str | Literal[64]) -> None:
        self.pressBtn(mouseBtn)
        self.releaseBtn(mouseBtn)

    def pressBtn(self, mouseBtn: str | Literal[64]) -> None:
        if mouseBtn == "left":
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.pressedButtons.add("left")
        elif mouseBtn == "right":
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            self.pressedButtons.add("right")
        elif mouseBtn == "middle":
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            self.pressedButtons.add("middle")
        else:
            raise ValueError(f"Unsupported button: {mouseBtn}")

    def releaseBtn(self, mouseBtn: str | Literal[64]) -> None:
        if mouseBtn == "left" and "left" in self.pressedButtons:
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.pressedButtons.remove("left")
        elif mouseBtn == "right" and "right" in self.pressedButtons:
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            self.pressedButtons.remove("right")
        elif mouseBtn == "middle" and "middle" in self.pressedButtons:
            ctypes.windll.user32.mouse_event(self.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            self.pressedButtons.remove("middle")
        else:
            raise ValueError(f"Unsupported or unpressed button: {mouseBtn}")

    def moveSmoothlyTo(self, x, y, timeElapse):
        raise NotImplementedError
    
    def setVelocity(self, vx, vy):
        raise NotImplementedError
    
    def update(self):
        '''
        method that will update state of the mouse 
        (mostly for smooth implementations of movement)
        '''
        raise NotImplementedError


class Keyboard:
    
    def __init__(self):
        raise NotImplementedError
    
    def pressBtn(self, btn: str) -> None:
        raise NotImplementedError


class KeyboardInputHandler:
    
    def __init__(self):
        raise NotImplementedError
    
    def currentKey(self):
        raise NotImplementedError
    
    def getState(self):
        raise NotImplementedError


