import numpy as np

from control import PIDController
from vision import FrameProcessorCV

class Aimbot:
    
    def __init__(self):
        self.yawController = PIDController(np.array([0.1, 0.1, 0.1]))
        self.pitchController = PIDController(np.array([0.1, 0.1, 0.1]))
        self.frameProcessor = FrameProcessorCV()
    
    def lockTarget(self):
        pass
    

    
    
