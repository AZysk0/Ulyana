import numpy as np
import random
# import pyautogui
import cv2 as cv
import time

from hwnd import WindowHandler
from events import Mouse, KeyboardInputHandler
from control import PIDController, PIDParams
from vision import FrameProcessorCV, ProcessingParams, FrameDebugger
import utils

from typing import List, Tuple, Iterable, Any
from dataclasses import dataclass

# ==== some constants ===
RESET_TARGET_KEY = '1'
TRACK_TARGET_KEY = 'SHIFT'
# =======================


class AutoAimBot:
    
    def __init__(
        self, 
        windowTitle: str, 
        processingParams: ProcessingParams=ProcessingParams()
    ) -> None:
        
        self.yawController = PIDController()
        self.pitchController = PIDController()
        
        self.hWnd = WindowHandler(windowTitle=windowTitle)
        self.mouseController = Mouse()
        self.keyboardListener = KeyboardInputHandler()
        
        self.processingParams = ProcessingParams()
        self.frameProc = FrameProcessorCV(params=self.processingParams)
        
        self.frameDebugger = FrameDebugger()
        
        self.prevTargetPos: Tuple[int, int] | None = None  # pos on image

    def getTargetCentroids(self, bboxes) -> List[Tuple[int, int]]:
        return [(x + w // 2, y + h // 2) for x, y, w, h in bboxes]
    
    def chooseTarget(self, bboxes) -> None:  # side-effect
        
        if not bboxes:
            self.prevTargetPos = None
            return
        
        if self.prevTargetPos:
            return
        
        def bboxArea(bbox):
            _, _, w, h = bbox
            return w * h
        
        # get random target from top 3 largest (nearest to player in-game) bboxes
        targetBboxesSorted = sorted(bboxes, key=bboxArea, reverse=True)
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
    
    def mainLoop(self):
        
        self.hWnd.focusCurrentWindow()
        
        while True:
            # self.hWnd.focusCurrentWindow()
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            currentPressedKeys = self.keyboardListener._currentState
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
                
                dtDebug = time.time() - prevTime
                fps = int(1 / dtDebug)
                
                debugInfo = {
                    'fps': fps,
                    'bboxes': bboxes
                }
                
                resFrame = self.frameDebugger(processedFrame, debugInfo)
                cv.imshow(f"Aimbot eyes", resFrame)
                
                continue
            
            currTime = time.time()
            dt = currTime - prevTime
            
            self.chooseTarget(bboxes)
            self.update(dt, currentFrame)
            
            dtDebug = time.time() - prevTime
            fps = int(1 / dtDebug)
            
            debugInfo = {
                'fps': fps,
                'bboxes': bboxes
            }
            
            resFrame = self.frameDebugger(processedFrame, debugInfo)
            self.updateCurrentTarget(bboxes)
            self.keyboardListener.updateKeyboard()  # update keyboard state (prev)
            
            cv.imshow(f"Aimbot eyes", resFrame)
        
        cv.destroyAllWindows()


class AutoFireBot:
    
    def __init__(self, windowTitle):
        self.windowTitle = windowTitle
        self.mouse = Mouse()
        
        self.hWnd = WindowHandler(windowTitle=windowTitle)
        
        self.frameProc = FrameProcessorCV()
        self.frameDebugger = FrameDebugger()
        
    def getTargetCentroids(self, bboxes) -> List[Tuple[int, int]]:
        return [(x + w // 2, y + h // 2) for x, y, w, h in bboxes]
    
    def shouldFire(self, frame: np.ndarray, bboxes: List[np.ndarray]) -> bool:
        
        fw, fh = frame.shape[:2]
        
        cursor = np.array([fw // 2, fh // 2])
        
        # if any of cursor pos (center of the frame) is inside bboxes (- random adjustment)
        def cursorInside(bbox) -> bool:
            x, y, w, h = bbox
            cy, cx = cursor
            return (x <= cx <= x + w) and (y <= cy <= y + h)
        
        return any(tuple(map(cursorInside, bboxes)))
        
    
    def mainLoop(self):
        self.hWnd.focusCurrentWindow()
        
        while True:
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            prevTime = time.time()
            
            currentFrame = self.hWnd.takeScreenshot()
            processedFrame, bboxes = self.frameProc.simpleVisionPipeline(currentFrame)
            
            _shouldFire = self.shouldFire(processedFrame, bboxes)
            if _shouldFire:
                self.mouse.click('left')
            
            currTime = time.time()
            
            dt = currTime - prevTime
            fps = int(1 / dt)
            debugInfo = {
                'fps': fps,
                'shouldFire': _shouldFire,
                'bboxes': bboxes
            }
            
            resFrame = self.frameDebugger(processedFrame.copy(), debugInfo)
            
            cv.imshow(f"Aimbot eyes", resFrame)

        cv.destroyAllWindows()
    



