import click
import ast
import numpy as np
import cv2 as cv

from vision import ProcessingParams
from control import PIDParams

#  ====== Click helper namespace
class ClickLiteralOption(click.Option):
    '''helper to pass list to '''
    
    def type_cast_value(self, ctx, value):
        ''''''
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)


def constructProcessingParams(**kwargs) -> ProcessingParams:
    # maskColor: tuple = (0, 255, 0)  # unused 
    # hsvColor: tuple = (60, 255, 255)  # green hsv
    # hsvMin: np.ndarray = field(default_factory=lambda: np.array([50, 210, 70]))
    # hsvMax: np.ndarray = field(default_factory=lambda: np.array([70, 255, 255]))
    # gaussianBlurSize: tuple = (21, 21)
    # morphKernelSize: tuple = (3, 3)
    # morphKernelShape: int = cv.MORPH_RECT
    
    # defaults = {
    #     'maskColor': (0, 255, 0),
    #     'morphKernelShape': cv.MORPH_RECT,
    # }
    
    hsvMin = np.array(kwargs['hsvmin'])
    hsvMax = np.array(kwargs['hsvmax'])
    
    convertedParams = {
        'hsvMin': hsvMin,
        'hsvMin': hsvMax,
        'gaussianBlurSize': (21, 21),
        'morphKernelSize': (3, 3),
    }
    
    return ProcessingParams(**convertedParams)


def constructPIDParams(pidCoefs) -> PIDParams:
    # kp: float = 4.0
    # ki: float = 0.2
    # kd: float = 0.3
    # intMinLimit: float = -20
    # intMaxLimit: float = 20
    # derMinLimit: float = -100
    # derMaxLimit: float = 100
    
    # defaults = {
    #     'intMinLimit': -20,
    #     'intMaxLimit': 20,
    #     'derMinLimit': -100,
    #     'derMaxLimit': 100,
    # }
    kp, ki, kd = pidCoefs
    
    convertedParams = {
        'kp': kp,
        'ki': ki,
        'kd': kd,
    }
    
    # params = {**kwargs}
    return PIDParams(**{**convertedParams})

