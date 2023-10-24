# import
import pygame
import cv2 as cv
import sys
import time
from serial.tools import list_ports

from Classes.UI import UI
from Classes.Vision import Vision
from Classes.Movement import Movement


def main():

  # define constants:
  __iwidth__ = 1920 / 2
  __iHeight__ = 1080 / 2
  __camID__ = 0

  available_ports = list_ports.comports()
  for i, port in enumerate(available_ports):
    print(f"  {i}: {port.description}")

  choice = int(input('Choose port by typing a number followed by [Enter]: '))
  __port__ = available_ports[choice].device

  # Initialize objects
  vi = Vision(cv.VideoCapture(__camID__), (__iwidth__, __iHeight__))
  mv = Movement(__port__)
  mv.setBCord(vi.frame)
  ui = UI(__iwidth__, __iHeight__, vi.frame)

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

    # get objects
    objs = vi.GetObjects()

    # update the image in pygame and draw the objects
    ui.updateBg(vi.frame)
    ui.drawObjs(objs)

    selectedObj = None

    timeSnip = time.time()

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

      if time.time() - timeSnip > 15:  # in secconds
        break

    # do movement here
    print(f"clicked {selectedObj}")

    mv.moveObj(selectedObj)


# run the main function
if __name__ == "__main__":
  main()
  print("program stop")
  pygame.quit()
  cv.destroyAllWindows()
  sys.exit()
