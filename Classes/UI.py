import pygame
import cv2 as cv
from math import sqrt, pi
from Classes.Object import Object as Obj


class UI:

  def __init__(self, w: int, h: int, img: cv.Mat) -> None:
    pygame.init()
    self.width = w
    self.height = h
    self.display = pygame.display.set_mode((w, h))
    self.background = img

    pass

  def drawObj(self, object: Obj) -> None:
    if object.shape == "Circle":
      pos = (object.bBox['x'], object.bBox['y'])
      radious = (object.bBox['w'] + object.bBox['h']) / 4
      pygame.draw.circle(self.window, object.color, pos, radious)
    elif object.shape == "Rectangle" or object.shape == "Triangle":
      pygame.draw.polygon(self.display, object.color, object.vert)

  def checkClick(self, objects: list[Obj]) -> Obj:
    pass
