from hwnd import WindowHandler, WindowCapture
from vision import FrameProcessorCV, ProcessingParams, FrameDebugger
import cv2 as cv
from time import time

# 8591
def main():
    handler = WindowHandler(windowTitle='Quake 3')
    
    processingParams = ProcessingParams()
    frameDebugger = FrameDebugger()
    
    frameProc = FrameProcessorCV(params=processingParams)
    # windowCapturer = WindowCapture('Quake 3: Arena')

    while True:
        handler.focusCurrentWindow()
        
        prevTime = time()
        currentFrame = handler.takeScreenshot()
        # currentFrame = windowCapturer.get_screenshot()
        
        # handler.logWindowInfo()

        # Exit on pressing 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        currentTime = time()
        processedFrame = frameProc(currentFrame)
        
        deltaTime = currentTime - prevTime
        fps = int(1 / deltaTime)
        
        debugInfo = {
            'fps': fps
        }
        
        resFrame = frameDebugger(processedFrame, debugInfo)
        
        cv.imshow(f"Aimbot eyes", resFrame)

    cv.destroyAllWindows()


if __name__ == '__main__':
    
    main()

