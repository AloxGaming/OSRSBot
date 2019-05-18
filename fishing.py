import win32gui
import pyautogui
import random
import time
import numpy as np
import cv2
import subprocess as sp
import getpass
from datetime import datetime
from win32api import GetSystemMetrics

#Global variables
gameRect = []
gameWindow = None

pswd = ''

botActivated = False
coldStart = False

def main():
    global pswd
    pswd = getpass.getpass()
    tmp = sp.call('cls',shell=True)

    win32gui.EnumWindows(findWindow, None)

    if gameWindow == None:
        openRuneLite()

def findWindow(hwnd, extra):
    if 'RuneLite' in win32gui.GetWindowText(hwnd):
        print("Window found: (%s)" % (win32gui.GetWindowText(hwnd)))
        global gameWindow
        gameWindow = hwnd
        beginBot()

def openRuneLite():
    global coldStart
    coldStart = True
    runeLite = imagesearch_region_loop('images/runeLite.png', 1, 0, 0, GetSystemMetrics(0), GetSystemMetrics(1), 0.8)

    clickx = runeLite[0] + random.randint(0,30)
    clicky = runeLite[1] + random.randint(0,30)
    pyautogui.moveTo(clickx, clicky, random.randint(8,15) / 100)
    pyautogui.click(button='left')
    time.sleep(9)
    win32gui.EnumWindows(findWindow, None)

def beginBot():
    print("\tInitializing Bot...")

    cleanCoordinates()

    print("\tLocation: (%d, %d)" % (gameRect[0], gameRect[1]))
    print("\tWindow Size: (width:%d, height:%d)" % (gameRect[2] - gameRect[0], gameRect[3] - gameRect[1]))
       
    counter = 0
    try:
        while True:
            if not isLoggedIn() or coldStart:
                logIn()
            elif isFullInventory():
                print("\t\tEmptying inventory")
                emptyInventory()
            elif not isFishing() or hasLeveledUp():
                attemptToFish()
            time.sleep(random.randint(18,80) / 10)

            #Random mouse movement if away from keyboard since 
            #RuneLite will log you out if you're not at least moving the cursor
            counter = counter + 1
            if counter > 20:
                pyautogui.moveTo(random.randint(0,1920), random.randint(0,1080), 0.6)
                counter = 0
    except KeyboardInterrupt:
        pass

def cleanCoordinates():
    global gameRect
    gameRect = win32gui.GetWindowRect(gameWindow)

def isLoggedIn():
    login = imagesearcharea('images/existingUser.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)
    return login[0] == -1

def logIn():
    global pswd
    global coldStart

    coldStart = False

    print("\t" + datetime.now().strftime('%H:%M:%S')+ " Logging in...")
    existingUser = findInGameWindow('images/existingUser.png', 1, 0.8)

    clickx = existingUser[0] + gameRect[0] + random.randint(0,30)
    clicky = existingUser[1] + gameRect[1] + random.randint(0,30)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='left')

    pyautogui.typewrite(pswd) 
    time.sleep(random.randint(18,60) / 100)
    pyautogui.press('Enter')

    switchWorld()

    login = findInGameWindow('images/login.png', 1, 0.8)

    clickx = login[0] + gameRect[0] + random.randint(0,120)
    clicky = login[1] + gameRect[1] + random.randint(0,30)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='left')

    play = findInGameWindow('images/play.png', 1, 0.8)

    clickx = play[0] + gameRect[0] + random.randint(0,120)
    clicky = play[1] + gameRect[1] + random.randint(0,40)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='left')

    attemptToFish()
    
def switchWorld():
    clickHere = findInGameWindow('images/worldSwitch.png', 1, 0.8)

    clickx = clickHere[0] + gameRect[0] + random.randint(0,80)
    clicky = clickHere[1] + gameRect[1] + random.randint(0,15)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='left')

    clickHere = findInGameWindow('images/w469.png', 1, 0.9)

    clickx = clickHere[0] + gameRect[0] + random.randint(0,10)
    clicky = clickHere[1] + gameRect[1] + random.randint(0,80)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='left')

def isFullInventory():
    isFull = imagesearcharea('images/isFull.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.6)
    return isFull[0] != -1

def isFishing():
    cleanCoordinates()
    isCurrentlyFish = imagesearcharea('images/fishing/isFishing.png', gameRect[0] + 6, gameRect[1] + 46, gameRect[0] + 140, gameRect[1] + 108, 0.95)
    return isCurrentlyFish[0] != -1

def emptyInventory():
    cleanCoordinates()
    openBag()
    emptyBag()
    attemptToFish()

def recenter():
    mapIcon = imagesearcharea('images/mapIcon.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.97)

    if mapIcon[0] != -1:
        clickx = mapIcon[0] + gameRect[0] - 140 + random.randint(0,20)
        clicky = mapIcon[1] + gameRect[1] - 120 + random.randint(0,20)
        pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
        
    pyautogui.click(button='left')
     
    pyautogui.keyDown('down')
    time.sleep(random.randint(28,40) / 100)
    pyautogui.keyUp('down')
    
    pyautogui.hotkey('up', 'up', 'up', 'up', 'up')

def closeBag():
    openBag = imagesearcharea('images/backpackOpen.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)

    if openBag[0] != -1:
        clickx = openBag[0] + gameRect[0] + random.randint(10,28)
        clicky = openBag[1] + gameRect[1] + random.randint(4,10)
        pyautogui.moveTo(clickx, clicky, random.randint(2,7) / 10)
        pyautogui.click(button='left')

def openBag():
    bag = imagesearcharea('images/backpack.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)

    if bag[0] != -1:
        clickx = bag[0] + gameRect[0] + random.randint(10,28)
        clicky = bag[1] + gameRect[1] + random.randint(4,10)
        pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    else:
        pyautogui.moveTo(gameRect[0] + 20, gameRect[1] + 4)
    
    pyautogui.click(button='left')

def emptyBag():
    pyautogui.keyDown('shift')

    openBag = imagesearcharea('images/backpackOpen.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)
    if openBag[0] != -1:
        topLeft = [openBag[0] - 51, openBag[0] - 400]
        #topLeft = [663, 314]
        itemSize = 25
        itemHeight = 37
        itemWidth = 42

        for y in range(7):

            decision = random.randint(0,2)
            if decision == 0:
                pyautogui.hotkey('left', 'left', 'left', 'left', 'left')
            elif decision == 1:
                pyautogui.hotkey('right', 'right', 'right', 'right', 'right')

            for x in range(4):
                if x != 0 or y != 0:
                    clickx = topLeft[0] + (itemWidth * x) + random.randint(0,itemSize)
                    clicky = topLeft[1] + (itemHeight * y) + random.randint(0,itemSize)

                    pyautogui.moveTo(gameRect[0] + clickx, gameRect[1] + clicky, random.randint(11,23) / 100)
                    pyautogui.click(button='left')

    pyautogui.keyUp('shift')
    
    decision = random.randint(0,3)
    if decision == 1:
        recenter()

def hasLeveledUp():
    fishUp = imagesearcharea('images/fishing/fishUp.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)
    return fishUp[0] != -1
    
def attemptToFish():
    print("\t\tAttempting to fish")
    closeBag()
    
    #Right click on fishing spot
    fishLoc = findInGameWindow('images/fishing/lobster.png', 1, 0.9)
    clickx = fishLoc[0] + gameRect[0] + random.randint(1,8)
    clicky = fishLoc[1] + gameRect[1] + random.randint(4,18)
    pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
    pyautogui.click(button='right')

    time.sleep(random.randint(12,84) / 100)

    #Click on harpooning
    harpoonLoc = imagesearcharea('images/fishing/harpoon.png', gameRect[0], gameRect[1], gameRect[2], gameRect[3], 0.8)

    if harpoonLoc[0] != -1:
        clickx = harpoonLoc[0] + gameRect[0] + random.randint(5,100)
        clicky = harpoonLoc[1] + gameRect[1] + random.randint(0,8)

        pyautogui.moveTo(clickx, clicky, random.randint(12,40) / 100)
        pyautogui.click(button='left')

        time.sleep(random.randint(12,40) / 100)
        if isFullInventory():
            emptyInventory()
    else:
        print("\t\t\tFailed to find harpoon")
        pyautogui.moveTo(gameRect[0] - 20, gameRect[1], random.randint(12,40) / 100)
        attemptToFish()

def findInGameWindow(image, timesample, precision=0.8):
    pos = imagesearcharea(image, gameRect[0], gameRect[1], gameRect[2], gameRect[3], precision)

    while pos[0] == -1:
        cleanCoordinates()
        time.sleep(timesample)
        pos = imagesearcharea(image, gameRect[0], gameRect[1], gameRect[2], gameRect[3], precision)
    
    return pos

############################## Imported Region ##############################
def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1

    return pyautogui.screenshot(region=(x1,y1,width,height))

def imagesearcharea(image, x1,y1,x2,y2, precision=0.8, takeScreenShot = False) :
    
    #print("\t\t\t IMAGE LOC: (%d, %d, %d, %d)" % (x1, y1, x2, y2))
    im = region_grabber(region=(x1, y1, x2, y2))
    if takeScreenShot:
        im.save('capture_' + image)
        
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]

    if takeScreenShot:
        locx = x1 + max_loc[0]
        locy = y1 + max_loc[1]
        found = region_grabber(region=(locx, locy, locx + 60, locy + 30))
        found.save('capture_loc_' + image)

    return max_loc

#Search until image found
def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1,y1,x2,y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        cleanCoordinates()
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    
    return pos

if __name__ == '__main__':
    main()