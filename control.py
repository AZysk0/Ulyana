import numpy as np

from dataclasses import dataclass, field
from typing import Iterable, Union

Real = Union[float | int]


@dataclass(frozen=True)
class PIDParams:
    kp: float = 5.0
    ki: float = 0.6
    kd: float = 0.07
    intMinLimit: float = -30
    intMaxLimit: float = 30
    derMinLimit: float = -50
    derMaxLimit: float = 50


class PIDController:
    def __init__(self, params: PIDParams=PIDParams()):
        """
        Initialize the PID controller with parameters.

        Args:
            params (PIDParams): An instance of PIDParams containing PID coefficients and integral limits.
        """
        self.params = params
        
        self.pTerm = 0
        self.iTerm = 0
        self.dTerm = 0
        
        self.prevError = 0  # for derivative term

    def step(self, dt: float, current: Real, target: Real) -> Real:

        if dt == 0:
            raise ValueError("dt cannot be zero")

        error = target - current
        
        self.pTerm = error

        # integral with windup clamping
        self.iTerm += error * dt
        self.iTerm = max(min(self.iTerm, self.params.intMaxLimit), self.params.intMinLimit)

        # self.dTerm = (error - self.prevError) / dt
        raw_dTerm = (error - self.prevError) / dt
        self.dTerm = max(min(raw_dTerm, self.params.derMaxLimit), self.params.derMinLimit)

        self.prevError = error

        resP = self.params.kp * self.pTerm
        resI = self.params.ki * self.iTerm
        resD = self.params.kd * self.dTerm
        
        return resP + resI + resD

    def reset(self):
        self.pTerm = 0
        self.iTerm = 0
        self.dTerm = 0
        self.prevError = 0

    def __call__(self, dt: float, current: Real, target: Real) -> Real:
        # TODO:
        # - Forward the call to the `step` method for easy usage.
        return self.step(dt, current, target)


