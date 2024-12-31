from hwnd import WindowHandler
import cv2 as cv
from time import time


def main():
    handler = WindowHandler(windowTitle='Quake 3')
    handler.focusCurrentWindow()

    while True:
        prevTime = time()
        currentFrame = handler.takeScreenshot()
        handler.logWindowInfo()


        # Exit on pressing 'q'
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        currentTime = time()
        deltaTime = currentTime - prevTime
        fps = int(1 / deltaTime)
        print(fps)
        
        cv.imshow(f"FPS: {fps}", currentFrame)


    cv.destroyAllWindows()


if __name__ == '__main__':
    
    main()

