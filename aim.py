import numpy as np
import random
import pyautogui

from control import PIDController
from vision import FrameProcessorCV

class AutoAimBot:
    
    def __init__(self):
        self.yawController = PIDController(np.array([0.1, 0.1, 0.1]))
        self.pitchController = PIDController(np.array([0.1, 0.1, 0.1]))
        self.frameProcessor = FrameProcessorCV()
        self.prevTargetPos = (0, 0)  # pos on image
    
    def chooseTarget(self, targets):
        '''targets - list of centroids of bboxes of separated objects'''
        
        
        
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


    
    
