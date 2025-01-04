import numpy as np
import cv2 as cv
from PIL import Image
import pygetwindow as gw
import mss
import pyautogui

from ctypes import windll, create_unicode_buffer
import win32gui
import win32ui
import win32con
import win32api

from typing import Optional, Dict, Any


# TODO:
# high-fps window capture (win32 api?)
# OpenGL q3-hook 
# 


class WindowHandler:
    '''
    class for capturing frames from chosen window
    '''
    
    def __init__(self, windowTitle: str) -> None:
        self.windowTitle = windowTitle
        self.hwnd = self._findWindow()
    
    def _findWindow(self) -> Optional[gw.Window]:
        '''method for setting up an object of this class'''
        
        windows = gw.getWindowsWithTitle(self.windowTitle)
        if not windows:
            raise ValueError(f"Window with title '{self.windowTitle}' not found")
        return windows[0]

    @staticmethod
    def getForegroundWindowTitle() -> Optional[str]:
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        buf = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    
        # 1-liner alternative: 
        return buf.value if buf.value else None

    def focusCurrentWindow(self) -> None:
        if self.hwnd is None:
            raise RuntimeError("Window is not set. Unable to focus.")
        
        if WindowHandler.getForegroundWindowTitle() != self.windowTitle:
            self.hwnd.activate()

    def takeScreenshot(self) -> np.ndarray:
        if not self.hwnd:
            raise RuntimeError("Window is not set. Unable to take screenshot.")
        
        region = (
            self.hwnd.left,
            self.hwnd.top,
            self.hwnd.width,
            self.hwnd.height
        )
        screenshot = np.array(pyautogui.screenshot(region=region))
        # return cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        return screenshot

    def windowIsFocused(self):
        
        return
    
    def isWindowValid(self) -> bool:
        try:
            return self._findWindow() is not None
        except ValueError:
            return False

    def logWindowInfo(self) -> None:
        if self.hwnd:
            print(f"Window Title: {self.hwnd.title}")
            print(f"Position: ({self.hwnd.left}, {self.hwnd.top})")
            print(f"Size: {self.hwnd.width}x{self.hwnd.height}")
        else:
            print("No window is currently selected.")
            
    def getLogWindowInfo(self) -> Dict[str, Any]:
        if self.hwnd:
            return {
                "title": self.hwnd.title,
                "position": {"x": self.hwnd.left, "y": self.hwnd.top},
                "size": {"width": self.hwnd.width, "height": self.hwnd.height},
            }
        else:
            return {}

    def debugScreenshot(self, save_path: str = "screenshot.png") -> None:
        raise NotImplementedError



class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        
        win32gui.InvalidateRect(self.hwnd, None, True)
        win32gui.UpdateWindow(self.hwnd)


        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        saveDC = dcObj.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        
        saveDC.SelectObject(saveBitMap)
        
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 0)
        
        # saveDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        
        # convert the raw data into a format opencv can read
        
        img = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        
        imgArray = np.array(img)

        # free resources
        dcObj.DeleteDC()
        saveDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(saveBitMap.GetHandle())

        # some shit for debugging
        print(result, imgArray.shape, sep='\n')

        return cv.cvtColor(imgArray, cv.COLOR_BGR2RGB)
        # return imgArray

    # find the name of the window you're interested in.
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)




