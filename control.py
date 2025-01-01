import numpy as np

from typing import Iterable, Union


Real = Union[float | int]


class PIDController():
    
    def __init__(self, pid_coefs: Iterable[Real]):
        self.pid_coefs = np.array(pid_coefs).astype(np.float32)
    
    def step(self, current: Real, target: Real) -> Real:
        # maybe there's a better way to name this method idk
        # function returns how much should i step particular shit
        return
    
    def reset(self):
        pass
    
    def __call__(self):
        pass



