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
import win32com.client

from typing import Optional, Dict, Any


# TODO:
# high-fps window capture (win32 api?)
# OpenGL q3-hook 
# 


class WindowCaptureAbstract:
    
    def __init__(self, windowTitle: str):
        self.windowTitle = windowTitle
        
        self.hWnd = win32gui.FindWindow(None, windowTitle)
        if not self.hWnd:
            raise Exception(f"Window with title '{windowTitle}' not found!")

        window_rect = win32gui.GetWindowRect(self.hWnd)
        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        
        win32gui.SetForegroundWindow(self.hWnd)
    
    def listWindowNames(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
        
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)


class WindowCaptureWin32(WindowCaptureAbstract):
    '''
    Issue:
    - Static window frame (quake 3)
    - To get another frame you need to re-launch window 
    and after this the same problem with static frame
    - Windows PowerShell - black image (with debug info)
    '''

    def __init__(self, windowTitle: str):
        super().__init__(windowTitle=windowTitle)

    def takeScreenshot(self):
        
        # windowDC = windll.user32.GetWindowDC(self.hWnd)
        
        win32gui.RedrawWindow(
            self.hWnd, None, None, 
            win32con.RDW_INVALIDATE | win32con.RDW_UPDATENOW
        )
        
        # get the window image data
        windowDC = win32gui.GetWindowDC(self.hWnd)
        dcObj = win32ui.CreateDCFromHandle(windowDC)
        memoryDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        memoryDC.SelectObject(dataBitMap)
        memoryDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0,0), win32con.SRCCOPY)
        
        #save the screenshot
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        # img = np.fromstring(signedIntsArray, dtype='uint8').reshape(self.h, self.w, 4)[..., :3]
        img = np.frombuffer(signedIntsArray, dtype='uint8').reshape(self.h, self.w, 4)[..., :3]
        img = np.ascontiguousarray(img)
        
        # Free Resources
        dcObj.DeleteDC()
        memoryDC.DeleteDC()
        win32gui.ReleaseDC(self.hWnd, windowDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        # print(img.shape)
        
        return img

    def _on_resize(self):
        # update window if resized
        
        pass

    def update(self):
        pass


class WindowCaptureMSS(WindowCaptureAbstract):
    
    def __init__(self, windowTitle: str):
        super().__init__(windowTitle=windowTitle)
    
    def focusCurrentWindow(self) -> None:
        '''Error for commented code on Alt+tab'''
        
        # if self.hWnd is None:
        #     raise RuntimeError("Window is not set. Unable to focus.")
        
        # foreground_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        
        # if foreground_window_title != self.windowTitle:
        #     win32gui.SetForegroundWindow(self.hWnd)
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self.hWnd)
    
    def takeScreenshot(self) -> np.ndarray:
        # ensure window is always focused
        
        # self.focusCurrentWindow()
        
        monitor = {
            "top": self.offset_y,
            "left": self.offset_x,
            "width": self.w,
            "height": self.h
        }
        
        with mss.mss() as sct:
            screenshot = sct.grab(monitor)
            
            img = np.array(screenshot)[:, :, :3]
            return img





# ===================== Some shit i probably will never use ==========

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
        # slow: 25 fps at most
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




