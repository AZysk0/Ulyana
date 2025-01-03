import numpy as np
import random
# import pyautogui
import cv2 as cv
import time

from hwnd import WindowHandler
from events import Mouse
from control import PIDController, PIDParams
from vision import FrameProcessorCV, ProcessingParams, FrameDebugger
import utils

from typing import List, Tuple, Iterable, Any


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
            
            prevTime = time.time()
            
            currentFrame = self.hWnd.takeScreenshot()
            
            processedFrame, bboxes = self.frameProc(currentFrame)
            
            if not bboxes:
                self.resetTarget()
            
            currTime = time.time()
            dt = currTime - prevTime
            
            self.chooseTarget(bboxes)
            self.update(dt, currentFrame)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            
            dtDebug = time.time() - prevTime
            fps = int(1 / dtDebug)
            
            debugInfo = {
                'fps': fps,
                'bboxes': bboxes
            }
            
            resFrame = self.frameDebugger(processedFrame, debugInfo)
            self.updateCurrentTarget(bboxes)
            
            cv.imshow(f"Aimbot eyes", resFrame)
        
        cv.destroyAllWindows()


class AutoFireBot:
    
    def __init__(self):
        raise NotImplementedError
    
    def mainLoop(self):
        raise NotImplementedError



