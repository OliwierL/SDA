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
  __camID__ = 1

  # Initialize objects
  vi = Vision(cv.VideoCapture(__camID__), (__iwidth__, __iHeight__))
  ui = UI(__iwidth__, __iHeight__, vi.frame)
  mv = Movement()

  # loop forever
  while True:
    #check if the user closed the window
    for event in pygame.event.get():
      #clicked the close button?
      #Quit pygame and end the program
      if event.type == pygame.QUIT:
        vi.cam.release()
        return -1

    # refresh the camera
    vi.refresh()

    # get objects
    objs = vi.GetObjects()

    # drop grey objects
    objects = []
    for obj in objs:
      if obj.notGray():
        objects.append(obj)

    # update the image in pygame and draw the objects
    ui.updateBg(vi.frame)
    ui.drawObj(objects)

    selectObj = None

    # wait for user to select the shape
    while selectObj is None:
      # check if the user closed the window
      for event in pygame.event.get():
        #Quit pygame and end the program
        if event.type == pygame.QUIT:
          vi.cam.release()
          return -1

      # check if the user clicked the window
      for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          clickedObj = ui.checkClick(objects)


# run the main function
if __name__ == "__main__":
  main()
  print("program stop")
  # dobot.dobotDisconnect()
  pygame.quit()
  cv.destroyAllWindows()
  sys.exit()
