import numpy as np


def distL2(p1: np.ndarray, p2: np.ndarray):
    if p1.shape != p2.shape:
        raise ValueError(f"Shapes of p1 {p1.shape} and p2 {p2.shape} must be the same.")
    
    return np.linalg.norm(p2 - p1)


