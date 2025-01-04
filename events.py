import ctypes

from typing import Tuple, Any, Literal, Set


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


class KeyboardInputHandler:
    VK_CODES = {
        "BACKSPACE": 0x08,
        "TAB": 0x09,
        "ENTER": 0x0D,
        "SHIFT": 0x10,
        "CTRL": 0x11,
        "ALT": 0x12,
        "ESC": 0x1B,
        "SPACE": 0x20,
        "LEFT_ARROW": 0x25,
        "UP_ARROW": 0x26,
        "RIGHT_ARROW": 0x27,
        "DOWN_ARROW": 0x28,
        **{chr(i): i for i in range(0x30, 0x5A + 1)},  # alphanumeric
    }
    
    INVERSE_MAP = {v: k for k, v in VK_CODES.items()}

    def __init__(self):
        self.prevState: Set[str] = set()  # human-readable
        self._previousStateHex = set()

    @property
    def _currentState(self) -> Set[str]:
        '''
        get keys that are currently pressed
        human-readable ver
        '''
        pressed_keys = set()
        for name, vk in self.VK_CODES.items():
            if ctypes.windll.user32.GetAsyncKeyState(vk) & 0x8000:
                pressed_keys.add(name)
        return pressed_keys

    @property
    def _currentStateHex(self) -> Set[int]:
        """not-human-readable"""
        pressed_keys = set()
        for vk_code in range(0x08, 0xFE):
            if ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000:
                key_name = self.INVERSE_MAP.get(vk_code, f"VK_{vk_code}")
                pressed_keys.add(vk_code)  # Add the key code, not the key name
        return pressed_keys

    @property
    def pressedKeys(self) -> Set[str]:
        '''Returns the set of keys pressed since the last update (human-readable)'''
        return self._currentState.difference(self.prevState)
    
    @property
    def releasedKeys(self) -> Set[str]:
        '''Returns the set of keys released since the last update (human-readable)'''
        return self.prevState.difference(self._currentState)

    @property
    def pressedKeysHex(self) -> Set[int]:
        '''Returns the set of keys pressed since the last update (hex codes)'''
        return self._currentStateHex.difference(self._previousStateHex)
    
    @property
    def releasedKeysHex(self) -> Set[int]:
        '''Returns the set of keys released since the last update (hex codes)'''
        return self._previousStateHex.difference(self._currentStateHex)
    
    def updateKeyboard(self) -> None:
        self.prevState = self._currentState
        self._previousStateHex = self._currentStateHex



