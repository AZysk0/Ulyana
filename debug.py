import cv2 as cv
import numpy as np

from collections import deque
from typing import Dict, Any, List, Tuple


class DebugFPS(deque):
    def __init__(self, sz: int):
        super().__init__(maxlen=sz)

    @property
    def average(self):
        if len(self) == 0:
            return 0
        return sum(self) / len(self)


class FrameDebugger:
    
    def __init__(self):
        pass
    
    def drawTextInfo(self, image: np.ndarray, info: Dict[str, Any]):
        position = (10, 30)
        imageCp = image.copy()
        for key, value in info.items():
            if isinstance(value, (str, int, float)):
                text = f"{key}: {value}"
                cv.putText(imageCp, text, position, cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
                position = (position[0], position[1] + 40)
        
        return imageCp
    
    def drawBoundingBoxes(self, image: np.ndarray, bboxes: List[Tuple[int, int, int, int]]):
        '''Draw bounding boxes on the image'''
        imageCp = image.copy()
        for bbox in bboxes:
            x, y, w, h = bbox
            cv.rectangle(imageCp, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box
        return imageCp
    
    def drawBboxCentroids(self, image: np.ndarray, bboxes: List[Tuple[int, int, int, int]]):
        '''Draw centroids of bounding boxes on the image'''
        imageCp = image.copy()
        for bbox in bboxes:
            x, y, w, h = bbox
            cx, cy = x + w // 2, y + h // 2  # Calculate the centroid
            cv.circle(imageCp, (cx, cy), 5, (0, 0, 255), -1)  # Red dot
        return imageCp
    
    def __call__(self, image, info: Dict[str, Any]):
        '''draw debuggin info onto screentshot'''
        bboxes = info.get('bboxes', [])
        
        resImage = self.drawTextInfo(image.copy(), info)
        resImage = self.drawBoundingBoxes(resImage, bboxes)
        resImage = self.drawBboxCentroids(resImage, bboxes)
        
        return resImage




