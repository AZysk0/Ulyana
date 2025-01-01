import numpy as np

from typing import Iterable, Union


Real = Union[float | int]


class PIDController():
    
    def __init__(self, pid_coefs: Iterable[Real]):
        self.pid_coefs = np.array(pid_coefs).astype(np.float32)
        self.prop = 0
        self.prevError = 0
        self.integral = 0
    
    def step(self, dt: float, current: Real, target: Real) -> Real:
        """
        Compute the control action based on the current state and target.

        Args:
            dt (float): Time step.
            current (Real): Current value of the system variable.
            target (Real): Desired target value.

        Returns:
            Real: The computed control action.
        """
        # TODO: 
        # - Calculate the error (difference between target and current).
        # - Compute the proportional, integral, and derivative terms.
        # - Combine terms using PID coefficients.
        # - Return the control action value.
        return 0  # Placeholder

    def reset(self):
        """
        Reset the PID controller's internal state.
        """
        # TODO:
        # - Set proportional, integral, and previous error terms to zero.
        self.prop = 0
        self.prev_error = 0
        self.integral = 0

    def __call__(self, dt: float, current: Real, target: Real) -> Real:
        """
        Callable interface for the PID controller.

        Args:
            dt (float): Time step.
            current (Real): Current value of the system variable.
            target (Real): Desired target value.

        Returns:
            Real: The computed control action.
        """
        # TODO:
        # - Forward the call to the `step` method for easy usage.
        return self.step(dt, current, target)


