import numpy as np
import random
import pyautogui

from control import PIDController, PIDParams
from vision import FrameProcessorCV

class AutoAimBot:
    
    def __init__(self):
        self.yawController = PIDController()
        self.pitchController = PIDController()
        self.frameProcessor = FrameProcessorCV()
        self.prevTargetPos = (0, 0)  # pos on image
    
    def chooseTarget(self, targetCentroids):
        '''targets - list of centroids of bboxes of separated objects'''
        
        # sort by distance to the center
        
        # get random from 3 nearest (if more than 3 targets on the screen)
        
        return
    
    def updateCurrentTarget(self):
        '''get centroid that is nearest to target from previous state'''        
        
        return
    
    def lockTarget(self):
        '''rly idk if i need it'''
        raise NotImplementedError
    
    def resetTarget(self):
        '''choose new target that is not current and reset PID-controllers'''
        raise NotImplementedError
    
    def processFrame(self):
        return
    
    def update(self) -> None:
        '''step over PID-controllers'''
        return
    
    def moveMouse(self):
        return
    
    def mainLoop(self):
        
        return



class AutoFireBot:
    
    def __init__(self):
        pass
    
    def mainLoop(self):


    
    
