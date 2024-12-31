import numpy as np
import cv2 as cv
import pygetwindow as gw
import mss
import pyautogui
import win32gui
import win32ui
import win32con
import win32api

from typing import Optional, Dict, Any


class WindowHandler:
    '''
    class for capturing frames from chosen window
    '''
    
    def __init__(self, windowTitle: str) -> None:
        self.windowTitle = windowTitle
        self.window = self._find_window()
    
    def _find_window(self) -> Optional[gw.Window]:
        '''method for setting up an object of this class'''
        
        windows = gw.getWindowsWithTitle(self.windowTitle)
        
        if not windows:
            raise ValueError(f"Window with title '{self.windowTitle}' not found")
        return windows[0]

    def focusCurrentWindow(self) -> None:
        if self.window:
            self.window.activate()
        else:
            raise RuntimeError("Window is not set. Unable to focus.")

    def takeScreenshot(self) -> np.ndarray:
        if not self.window:
            raise RuntimeError("Window is not set. Unable to take screenshot.")
        
        region = (
            self.window.left,
            self.window.top,
            self.window.width,
            self.window.height
        )
        screenshot = np.array(pyautogui.screenshot(region=region))
        return cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)

    def isWindowValid(self) -> bool:
        try:
            return self._find_window() is not None
        except ValueError:
            return False

    def logWindowInfo(self) -> None:
        if self.window:
            print(f"Window Title: {self.window.title}")
            print(f"Position: ({self.window.left}, {self.window.top})")
            print(f"Size: {self.window.width}x{self.window.height}")
        else:
            print("No window is currently selected.")
            
    def getLogWindowInfo(self) -> Dict[str, Any]:
        if self.window:
            return {
                "title": self.window.title,
                "position": {"x": self.window.left, "y": self.window.top},
                "size": {"width": self.window.width, "height": self.window.height},
            }
        else:
            return {}

    def debugScreenshot(self, save_path: str = "screenshot.png") -> None:
        raise NotImplementedError

