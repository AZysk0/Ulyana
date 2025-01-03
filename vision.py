import numpy as np
import cv2 as cv

from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass, field


@dataclass
class ProcessingParams:
    maskColor: tuple = (0, 255, 0)
    hsvColor: tuple = (60, 255, 255)  # green hsv
    hsvMin: np.ndarray = field(default_factory=lambda: np.array([50, 210, 70]))
    hsvMax: np.ndarray = field(default_factory=lambda: np.array([70, 255, 255]))
    gaussianBlurSize: int = (21, 21)
    morphKernelSize: int = (3, 3)
    morphKernelShape: int = cv.MORPH_RECT

    def __post_init__(self):
        if not isinstance(self.hsvMin, np.ndarray):
            self.hsvMin = np.array(self.hsvMin)
        if not isinstance(self.hsvMax, np.ndarray):
            self.hsvMax = np.array(self.hsvMax)

    def __str__(self):
        return (f"ProcessingParams(hsvColor={self.hsvColor}, "
                f"hsvMin={self.hsvMin.tolist()}, "
                f"hsvMax={self.hsvMax.tolist()})")

    def to_dict(self):
        return {
            "hsvColor": self.hsvColor,
            "hsvMin": self.hsvMin.tolist(),
            "hsvMax": self.hsvMax.tolist()
        }


class FrameProcessorCV:
    
    def __init__(self, params: ProcessingParams=ProcessingParams()):
        self.params = params
    
    # ==== middle-transform methods/functions
    def hsvThresholding(self, image):
        '''-> hsv-thresholded mask for image'''
      
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        
        lower_bound = self.params.hsvMin
        upper_bound = self.params.hsvMax
        
        mask = cv.inRange(hsv_image, lower_bound, upper_bound)

        return mask
    
    def maskMorphologyPipeline(self, mask):
    
        maskCp = mask.copy()
        
        kernel = cv.getStructuringElement(self.params.morphKernelShape, self.params.morphKernelSize)
        
        openedMask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        closedMask = cv.morphologyEx(openedMask, cv.MORPH_CLOSE, kernel)
        dilatedMask = cv.morphologyEx(closedMask, cv.MORPH_DILATE, kernel, iterations=9)
        
        return dilatedMask
    
    def separateObjects(self, mask):
        # Ensure the mask is binary (0 or 255 values)
        _, binaryMask = cv.threshold(mask, 127, 255, cv.THRESH_BINARY)

        # Find connected components in the binary mask
        # 'cv.connectedComponents' returns the label matrix and the number of labels
        numLabels, labels = cv.connectedComponents(binaryMask)
        
        # Create a color image where each object is assigned a different color
        # This is optional but useful for visualization
        colorMask = cv.cvtColor(binaryMask, cv.COLOR_GRAY2BGR)
        for label in range(1, numLabels):
            # Assign a random color for each label (object)
            color = np.random.randint(0, 255, size=3).tolist()
            colorMask[labels == label] = color
        
        # Return the labeled mask (labels) and the color mask for visualization
        return labels, colorMask
        # return colorMask
        
    def getBoundingBoxesFromLabels(self, labels):
        bounding_boxes = []
        unique_labels = np.unique(labels)
        unique_labels = unique_labels[unique_labels != 0]  # omit bg
        
        for label in unique_labels:
            # Find coordinates of the current label
            y_coords, x_coords = np.where(labels == label)
            
            # Compute bounding box (x_min, y_min, width, height)
            x_min, x_max = x_coords.min(), x_coords.max()
            y_min, y_max = y_coords.min(), y_coords.max()
            bounding_boxes.append((x_min, y_min, x_max - x_min, y_max - y_min))
        
        return bounding_boxes
    
    # ====
    def __call__(self, image):
        '''main pipeline for frame transformation'''
        
        imageCp = image.copy()
        
        blur = cv.GaussianBlur(imageCp, self.params.gaussianBlurSize, 0)
        mask = self.hsvThresholding(blur)
        morphedMask = self.maskMorphologyPipeline(mask)
        labels, colorMask = self.separateObjects(morphedMask)
        
        bboxes = self.getBoundingBoxesFromLabels(labels)
        
        # return (cv.cvtColor(colorMask, cv.COLOR_BGR2RGB), bboxes)
        return (cv.cvtColor(morphedMask, cv.COLOR_BGR2RGB), bboxes)



class FrameDebugger:
    
    def __init__(self):
        pass
    
    def drawTextInfo(self, image: np.ndarray, info: Dict[str, Any]):
        '''Draw the textual debugging info (fps, object count, etc.) onto the image'''
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


