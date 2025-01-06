import cv2 as cv
from time import time
import click

import cmd_helper
from vision import ProcessingParams
from control import PIDParams
from aim import AutoAimBot, AutoFireBot

# TODO:
# fullscale console app (click)

# ====== Main functions =========
def runAutoAim(
    procParams: ProcessingParams=ProcessingParams(),
    pidParams: PIDParams=PIDParams()
) -> None:
    
    autoAimBot = AutoAimBot(
        windowTitle='Quake 3: Arena', 
        processingParams=procParams,
        pidParams=pidParams
    )
    autoAimBot.mainLoop()


def runAutoFire(procParams: ProcessingParams=ProcessingParams()):
    
    autoFireBot = AutoFireBot(windowTitle='Quake 3: Arena', processingParams=procParams)
    autoFireBot.mainLoop()



@click.command()
@click.option('--mode', default=None, help='autoaim / autofire')
@click.option('--debug', default=False, help='enables debug mode: FPS, ROI-lines for autoAim detection area')
@click.option('--hsvmin', cls=cmd_helper.ClickLiteralOption, default='[50, 210, 70]')
@click.option('--hsvmax', cls=cmd_helper.ClickLiteralOption, default='[70, 255, 255]')
@click.option('--gaussianBlurSize', 'gaussianBlurSize', cls=cmd_helper.ClickLiteralOption, default='(21, 21)')
@click.option('--morphKernelSize', 'morphKernelSize', cls=cmd_helper.ClickLiteralOption, default='(3, 3)')
@click.option('--pid', cls=cmd_helper.ClickLiteralOption, default='[4.0, 0.2, 0.3]')
def main(
    mode: str, 
    debug: bool, 
    hsvmin: list,
    hsvmax: list,
    gaussianBlurSize: tuple,
    morphKernelSize: tuple,
    pid: list,
) -> None:
    
    frameProcDict = {
        'hsvmin': hsvmin,
        'hsvmax': hsvmax,
        'gaussianBlurSize': gaussianBlurSize,
        'morphKernelSize': morphKernelSize,
    }
    
    frameProcParams = cmd_helper.constructProcessingParams(**frameProcDict)
    
    if mode.lower() == 'autoaim':
        pidParams = cmd_helper.constructPIDParams(pidCoefs=pid)
        runAutoAim(procParams=frameProcParams, pidParams=pidParams)
        return
        
    elif mode.lower() == 'autofire':
        runAutoFire()
        return
    
    raise ValueError('Mode must ne one of these: autoaim, autofire')
    

if __name__ == '__main__':
    
    main()

