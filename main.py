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
    pidParams: PIDParams=PIDParams(),
    debug: bool=False,
) -> None:
    
    autoAimBot = AutoAimBot(
        windowTitle='Quake 3: Arena', 
        processingParams=procParams,
        pidParams=pidParams,
        debug=debug,
    )
    autoAimBot.mainLoop()


def runAutoFire(
    procParams: ProcessingParams=ProcessingParams(),
    debug: bool=False,
):
    
    autoFireBot = AutoFireBot(
        windowTitle='Quake 3: Arena', 
        processingParams=procParams,
        debug=debug,
    )
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
    print({
        'mode': mode,
        'debug': debug,
        'hsvmin': hsvmin,
        'hsvmax': hsvmax,
        'gaussianBlurSize': gaussianBlurSize,
        'morphKernelSize': morphKernelSize,
        'pid': pid,
    })
    frameProcDict = {
        'hsvmin': hsvmin,
        'hsvmax': hsvmax,
        'gaussianBlurSize': gaussianBlurSize,
        'morphKernelSize': morphKernelSize,
    }
    
    frameProcParams = cmd_helper.constructProcessingParams(**frameProcDict)
    
    if mode.lower() == 'autoaim':
        pidParams = cmd_helper.constructPIDParams(pidCoefs=pid)
        runAutoAim(procParams=frameProcParams, pidParams=pidParams, debug=debug)
        return
        
    elif mode.lower() == 'autofire':
        runAutoFire(procParams=frameProcParams, debug=debug)
        return
    
    raise ValueError('Mode must ne one of these: autoaim, autofire')
    

if __name__ == '__main__':
    
    main()

