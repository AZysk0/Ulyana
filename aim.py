import numpy as np
import random
# import pyautogui
import cv2 as cv
import time

from hwnd import WindowHandler, WindowCaptureMSS
from events import Mouse, KeyboardInputHandler
from control import PIDController, PIDParams
from vision import FrameProcessorCV, ProcessingParams
import utils
from debug import FrameDebugger, DebugFPS

from typing import List, Tuple, Iterable, Any
from dataclasses import dataclass

# ==== some constants ===
RESET_TARGET_KEY = '1'
TRACK_TARGET_KEY = 'SHIFT'
CLOSE_KEY = '9'
# =======================

def debug(title, debugFrame, debugInfo):
    
    cv.imshow(title, debugFrame)
    
    return


class AutoAimBot:
    # bbox filtering params (valid is inside this rect)
    xCenterMin = 135
    xCenterMax = float('inf')
    yCenterMin = 0
    yCenterMax = float('inf')
    
    def __init__(
        self, 
        windowTitle: str, 
        processingParams: ProcessingParams=ProcessingParams(),
        pidParams=PIDParams(),
        debug=False,
    ) -> None:
        
        # same PID params for yaw and pitch
        self.yawController = PIDController(params=pidParams)
        self.pitchController = PIDController(params=pidParams)
        
        self.hWnd = WindowCaptureMSS(windowTitle=windowTitle)
        self.mouseController = Mouse()
        self.keyboardListener = KeyboardInputHandler()
        
        self.processingParams = ProcessingParams()
        self.frameProc = FrameProcessorCV(params=self.processingParams)
        
        self.debug = debug
        self.frameDebugger = FrameDebugger()
        self.fpsDebugger = DebugFPS(sz=20)
        
        self.prevTargetPos: Tuple[int, int] | None = None  # pos on image
    
    def getTargetCentroids(self, bboxes) -> List[Tuple[int, int]]:
        return [(x + w // 2, y + h // 2) for x, y, w, h in bboxes]
    
    def filterBboxes(self, bboxes):
        
        def isValid(bbox) -> bool:
            x, y, w, h = bbox
            cx, cy = x + w // 2, y + h // 2
            
            if self.xCenterMin <= cx <= self.xCenterMax and self.yCenterMin <= cy <= self.yCenterMax:
                return True
        
            return False
        
        return list(filter(isValid, bboxes))
    
    def chooseTarget(self, bboxes) -> None:  # side-effect
        
        if not bboxes:
            self.prevTargetPos = None
            return
        
        if self.prevTargetPos:
            return
        
        def bboxArea(bbox):
            _, _, w, h = bbox
            return w * h
        
        validBboxes = self.filterBboxes(bboxes)
        if not validBboxes:
            self.resetTarget()
            return
        
        # get random target from top 3 largest (nearest to player in-game) bboxes
        targetBboxesSorted = sorted(validBboxes, key=bboxArea, reverse=True)
        randomTargetBbox = random.choice(targetBboxesSorted[:3])
        targetCentroid = self.getTargetCentroids([randomTargetBbox])[0]
        self.prevTargetPos = targetCentroid
    
    def updateCurrentTarget(self, bboxes) -> None:
        '''get centroid that is nearest to target from previous state'''
        
        if self.prevTargetPos is None or not bboxes:
            return

        centroids = self.getTargetCentroids(bboxes)

        prevPos = np.array(self.prevTargetPos)
        distances = [utils.distL2(prevPos, np.array(centroid)) for centroid in centroids]

        nearestIdx = np.argmin(distances)
        self.prevTargetPos = centroids[nearestIdx]
    
    def lockTarget(self):
        '''rly idk if i need it'''
        raise NotImplementedError
    
    def resetTarget(self) -> None:
        '''choose new target that is not current and reset PID-controllers'''
        self.yawController.reset()
        self.pitchController.reset()
        self.prevTargetPos = None
    
    def update(self, dt, frame) -> None:
        '''step over PID-controllers and move mouse'''
        
        h, w = frame.shape[:2]
        pidTarget = np.array([w // 2, h // 2])

        if self.prevTargetPos is not None:
            targetOffset = np.array(self.prevTargetPos) - pidTarget

            yawAdjustment = self.yawController.step(dt, 0, targetOffset[0])
            pitchAdjustment = self.pitchController.step(dt, 0, targetOffset[1])

            self.mouseController.moveBy(int(yawAdjustment), int(pitchAdjustment))
    
    def debugDrawValidBboxArea(self, frame: np.ndarray):
        lineColor = (0, 255, 0)
        thickness = 2
        
        if self.yCenterMin != float('-inf'):
            cv.line(frame, (0, self.yCenterMin), (frame.shape[1], self.yCenterMin), lineColor, thickness)
        if self.yCenterMax != float('inf'):
            cv.line(frame, (0, self.yCenterMax), (frame.shape[1], self.yCenterMax), lineColor, thickness)
        
        if self.xCenterMin != float('-inf'):
            cv.line(frame, (self.xCenterMin, 0), (self.xCenterMin, frame.shape[0]), lineColor, thickness)
        if self.xCenterMax != float('inf'):
            cv.line(frame, (self.xCenterMax, 0), (self.xCenterMax, frame.shape[0]), lineColor, thickness)
    
    def debugFrame(
        self, 
        frame: np.ndarray, 
        bboxes: List
    ) -> None:
        '''pass output of the vision pipeline'''
        dtDebug = self.fpsDebugger.average
        fps = int(1 / dtDebug)
        
        debugInfo = {
            'fps': fps,
            'bboxes': bboxes
        }
        
        resFrame = self.frameDebugger(frame, debugInfo)
        self.debugDrawValidBboxArea(resFrame)
        cv.imshow(f"Aimbot eyes", resFrame)
    
    def mainLoop(self):
        
        self.hWnd.focusCurrentWindow()
        
        while True:
            # self.hWnd.focusCurrentWindow()
            
            currentPressedKeys = self.keyboardListener._currentState
            
            if (cv.waitKey(1) & 0xFF == ord('q')) or (CLOSE_KEY in currentPressedKeys):
                break
            
            prevTime = time.time()
            currentFrame = self.hWnd.takeScreenshot()
            processedFrame, bboxes = self.frameProc(currentFrame)
            
            if not bboxes:
                self.resetTarget()
                
            if RESET_TARGET_KEY in self.keyboardListener.releasedKeys:
                self.resetTarget()
                
            if not (TRACK_TARGET_KEY in currentPressedKeys):
                # next iteration
                
                currTime = time.time()
                dt = currTime - prevTime
                
                # self.chooseTarget(bboxes)
                # self.update(dt, currentFrame)
                self.updateCurrentTarget(bboxes)
                
                # self.fpsDebugger.append(dt)
                # dtDebug = self.fpsDebugger.average
                # fps = int(1 / dtDebug)
                
                # debugInfo = {
                #     'fps': fps,
                #     'bboxes': bboxes
                # }
                
                # resFrame = self.frameDebugger(processedFrame, debugInfo)
                # self.debugDrawValidBboxArea(resFrame)
                # cv.imshow(f"Aimbot eyes", resFrame)
                if self.debug:
                    self.fpsDebugger.append(dt)
                    self.debugFrame(processedFrame, bboxes)
                
                continue
            
            currTime = time.time()
            dt = currTime - prevTime
            
            self.chooseTarget(bboxes)
            self.update(dt, currentFrame)
            
            self.updateCurrentTarget(bboxes)
            self.keyboardListener.updateKeyboard()  # update keyboard state (prev)
            
            # self.fpsDebugger.append(dt)
            # dtDebug = self.fpsDebugger.average
            # fps = int(1 / dtDebug)
            # debugInfo = {
            #     'fps': fps,
            #     'bboxes': bboxes
            # }
            
            # resFrame = self.frameDebugger(processedFrame, debugInfo)
            # self.debugDrawValidBboxArea(resFrame)
            # cv.imshow(f"Aimbot eyes", resFrame)
            if self.debug:
                self.fpsDebugger.append(dt)
                self.debugFrame(processedFrame, bboxes)
        
        cv.destroyAllWindows()


class AutoFireBot:
    
    def __init__(
        self, 
        windowTitle, 
        processingParams=ProcessingParams(),
        pidParams=PIDParams(),
        debug=False
    ) -> None:
        
        self.windowTitle = windowTitle
        
        self.mouse = Mouse()
        self.keyboardHandler = KeyboardInputHandler()
        
        self.hWnd = WindowCaptureMSS(windowTitle=windowTitle)
        
        self.frameProc = FrameProcessorCV()
        
        self.debug = debug
        self.frameDebugger = FrameDebugger()
        self.fpsDebugger = DebugFPS(sz=20)
        
    def getTargetCentroids(self, bboxes) -> List[Tuple[int, int]]:
        return [(x + w // 2, y + h // 2) for x, y, w, h in bboxes]
    
    def shouldFire(self, frame: np.ndarray, bboxes: List[np.ndarray]) -> bool:
        
        fw, fh = frame.shape[:2]
        
        cursor = np.array([fw // 2, fh // 2])
        
        # if any of cursor pos (center of the frame) is inside bboxes (- random adjustment)
        def cursorInside(bbox) -> bool:
            x, y, w, h = bbox
            cy, cx = cursor
            epsX = h * 0.1 * random.random()
            epsY = h * 0.1 * random.random()
            return (x + epsX <= cx <= x + w - epsX) and (y + epsY <= cy <= y + h - epsY)
        
        return any(tuple(map(cursorInside, bboxes)))
    
    def debugFrame(
        self, 
        frame: np.ndarray, 
        debugInfo
    ) -> None:
        '''pass output of the vision pipeline'''
        dtDebug = self.fpsDebugger.average
        fps = int(1 / dtDebug)
        
        # debugInfo = {
        #     'fps': fps,
        #     'shouldFire': 
        #     'bboxes': bboxes,
        # }
        
        resFrame = self.frameDebugger(frame, debugInfo)
        # self.debugDrawValidBboxArea(resFrame)
        cv.imshow(f"Aimbot eyes", resFrame)
    
    def mainLoop(self):
        self.hWnd.focusCurrentWindow()
        
        while True:
            
            currentPressedKeys = self.keyboardHandler._currentState
            
            if (cv.waitKey(1) & 0xFF == ord('q')) or (CLOSE_KEY in currentPressedKeys):
                break
            
            prevTime = time.time()
            
            currentFrame = self.hWnd.takeScreenshot()
            processedFrame, bboxes = self.frameProc.simpleVisionPipeline(currentFrame)
            
            _shouldFire = self.shouldFire(processedFrame, bboxes)
            if _shouldFire:
                self.mouse.click('left')
            
            currTime = time.time()
            
            dt = currTime - prevTime
            
            if self.debug:
                self.fpsDebugger.append(dt)
                fps = int(1 / self.fpsDebugger.average)
                debugInfo = {
                    'fps': fps,
                    'shouldFire': _shouldFire,
                    'bboxes': bboxes
                }
                self.debugFrame(processedFrame, debugInfo)
            
            # debugging pipeline
            # self.fpsDebugger.append(dt)
                
            # dtDebug = self.fpsDebugger.average
            # fps = int(1 / dtDebug)
            
            # debugInfo = {
            #     'fps': fps,
            #     'bboxes': bboxes
            # }
            
            # resFrame = self.frameDebugger(processedFrame.copy(), debugInfo)
            # cv.imshow(f"Aimbot eyes", resFrame)

        cv.destroyAllWindows()
    



