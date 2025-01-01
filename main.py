from hwnd import WindowHandler, WindowCapture
import cv2 as cv
from time import time


def main():
    handler = WindowHandler(windowTitle='Quake 3')
    
    # windowCapturer = WindowCapture('Quake 3: Arena')

    while True:
        handler.focusCurrentWindow()
        
        prevTime = time()
        currentFrame = handler.takeScreenshot()
        # currentFrame = windowCapturer.get_screenshot()
        
        handler.logWindowInfo()

        # Exit on pressing 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        currentTime = time()
        deltaTime = currentTime - prevTime
        fps = int(1 / deltaTime)
        print(fps)
        
        cv.imshow(f"Aimbot eyes", currentFrame)


    cv.destroyAllWindows()


if __name__ == '__main__':
    
    main()

