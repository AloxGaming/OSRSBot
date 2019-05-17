import win32gui
import pyautogui
import random
import time
import numpy as np
import cv2

def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]-x1
    height = region[3]-y1

    return pyautogui.screenshot(region=(x1,y1,width,height))

def imagesearcharea(image, x1,y1,x2,y2, precision=0.8, im=None) :
    if im is None :
        im = region_grabber(region=(x1, y1, x2, y2))
    
    #im.save('testarea.png') # usefull for debugging purposes, this will save the captured region as "testarea.png"

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]

    found = region_grabber(region=(x1 + max_loc[0], y1 + max_loc[1], x1 + max_loc[0] + 60, y1 + max_loc[1] + 30))
    found.save('found.png')
    return max_loc

def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    pos = imagesearcharea(image, x1,y1,x2,y2, precision)

    while pos[0] == -1:
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision)
    
    return pos

def doFishing(x1, y1, x2, y2):

    fishUp = imagesearcharea('fishUp.png', x1, y1, x2, y2, 0.8)
    isFull = imagesearcharea('isFull.png', x1, y1, x2, y2, 0.6)
    notFishing = imagesearcharea('notFishing.png', x1, y1, x2, y2, 0.90)

    if isFull[0] != -1:
        print("\t\tEmptying inventory")
        bag = imagesearcharea('backpack.png', x1, y1, x2, y2, 0.8)

        if bag[0] != -1:
            clickx = bag[0] + x1 + random.randint(10,28)
            clicky = bag[1] + y1 + random.randint(4,10)
            pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
            pyautogui.click(button='left')
        else:
            pyautogui.moveTo(x1 + 20, y1 + 4)
            pyautogui.click(button='left')
    
        pyautogui.keyDown('shift')

        topLeft = [663, 314]
        itemSize = 25
        itemHeight = 37
        itemWidth = 42

        for y in range(7):
            for x in range(4):
                if x != 0 or y != 0:
                    clickx = topLeft[0] + (itemWidth * x) + random.randint(0,itemSize)
                    clicky = topLeft[1] + (itemHeight * y) + random.randint(0,itemSize)

                    pyautogui.moveTo(x1 + clickx, y1 + clicky, random.randint(11,23) / 100)
                    pyautogui.click(button='left')

        pyautogui.keyUp('shift')
        doFishing(x1, y1, x2, y2)

    elif notFishing[0] != -1 or fishUp[0] != -1:
        print("\t\tStarting To Fish")
        openBag = imagesearcharea('backpackOpen.png', x1, y1, x2, y2, 0.8)

        if openBag[0] != -1:
            clickx = openBag[0] + x1 + random.randint(10,28)
            clicky = openBag[1] + y1 + random.randint(4,10)
            pyautogui.moveTo(clickx, clicky, random.randint(2,7) / 10)
            pyautogui.click(button='left')

        fishLoc = imagesearch_region_loop('anchovy.png', 1, x1, y1, x2, y2, 0.8)

        clickx = fishLoc[0] + x1 + random.randint(10,28)
        clicky = fishLoc[1] + y1 + random.randint(4,10)

        pyautogui.moveTo(clickx, clicky, random.randint(2,12) / 10)
        pyautogui.click(button='left')

        time.sleep(0.3)
        isFull = imagesearcharea('isFull.png', x1, y1, x2, y2, 0.6)
        if isFull[0] != -1:
            doFishing(x1, y1, x2, y2)


def beginBot(window):
    print("\tBot initializing...")
    rect = win32gui.GetWindowRect(window)
    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    w = x2 - x1
    h = y2 - y1
    print("\tLocation: (%d, %d)" % (x1, y1))
    print("\tSize: (%d, %d)" % (w, h))
    
    try:
        while True:
            doFishing(x1, y1, x2, y2)
            time.sleep(random.randint(48,80) / 10)
    except KeyboardInterrupt:
        pass

def callback(hwnd, extra):
    if 'RuneLite' in win32gui.GetWindowText(hwnd):
        print("Window found: (%s)" % (win32gui.GetWindowText(hwnd)))
        beginBot(hwnd)

def main():
    win32gui.EnumWindows(callback, None)

if __name__ == '__main__':
    main()