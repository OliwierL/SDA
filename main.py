# import
import pygame
import cv2 as cv
import sys

from Classes.UI import UI
from Classes.Vision import Vision
from Classes.Movement import Movement


def main():

  # define constants:
  __iwidth__ = 1920 / 2
  __iHeight__ = 1080 / 2
  __camID__ = 0

  __homePos__ = (250, 0, 50)
  __dropPos__ = (250, 100, 50)

  # Initialize objects
  vi = Vision(cv.VideoCapture(__camID__), (__iwidth__, __iHeight__))
  ui = UI(__iwidth__, __iHeight__, vi.frame)
  mv = Movement(__homePos__, __dropPos__)

  # loop forever
  while True:
    #check if the user closed the window
    for event in pygame.event.get():
      #clicked the close button?
      #Quit pygame and end the program
      if event.type == pygame.QUIT:
        vi.cam.release()
        mv.dobot.dobotDisconnect()
        return -1

    # refresh the camera
    vi.refresh()
    imgHeight, imgWidth, _ = vi.frame.shape
    res = (imgWidth, imgHeight)

    # get objects
    objs = vi.GetObjects()

    # update the image in pygame and draw the objects
    ui.updateBg(vi.frame)
    ui.drawObjs(objs)

    selectedObj = None

    # wait for user to select the shape
    while selectedObj is None:
      # check if the user closed the window
      for event in pygame.event.get():
        #Quit pygame and end the program
        if event.type == pygame.QUIT:
          vi.cam.release()
          mv.dobot.dobotDisconnect()
          return -1

      # check if the user clicked the window
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          selectedObj = ui.checkClick(objs)

    # do movement here
    print(f"clicked {selectedObj}")

    mv.moveObj(selectedObj, res)


# run the main function
if __name__ == "__main__":
  main()
  print("program stop")
  pygame.quit()
  cv.destroyAllWindows()
  sys.exit()
