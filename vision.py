import numpy as np
import cv2 as cv

from typing import Optional, Dict, Any


def hsvThresholding(image, hsvMin, hsvMax):    
    return


def maskImage(image, mask, maskColorRGB):
    return


def separateMaskObjects(mask):
    return


def computeCentroid(obj):
    
    return



class FrameProcessorCV:
    
    def __init__(self):
        pass
    
    def __call__(self, *args, **kwds):
        '''main pipeline for frame transformation'''
        pass


class FrameDebugger:
    
    def __init__(self):
        pass
    
    def __call__(image, info: Dict[str, Any]):
        '''draw debuggin info onto screentshot'''
        return    
