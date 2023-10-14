import pygame
import cv2 as cv
from Classes.Object import Object as Obj

from icecream import ic


class UI:

  def __init__(self, w: int, h: int, img: cv.Mat) -> None:
    pygame.init()
    self.width = w
    self.height = h
    self.display = pygame.display.set_mode((w, h))

    rgb_frame = cv.cvtColor(
        cv.rotate(img, cv.ROTATE_90_CLOCKWISE), cv.COLOR_BGR2RGB)
    self.background = pygame.surfarray.make_surface(cv.flip(rgb_frame, 1))

  def drawObj(self, obj: Obj) -> None:
    if obj.shape == "Circle":
      pos = (obj.bBox['x'], obj.bBox['y'])
      radious = (obj.bBox['w'] + obj.bBox['h']) / 4
      pygame.draw.circle(self.window, (0, 0, 0), pos, radious)
    elif obj.shape == "Rectangle" or obj.shape == "Triangle":
      pygame.draw.polygon(self.display, (0, 0, 0), obj.vert)
    else:
      pass

  def checkClick(self, objs: list[Obj]) -> Obj:
    clickPos = pygame.mouse.get_pos()
    for obj in objs:
      if obj.collidesWith(clickPos):
        return Obj
      else:
        return None

  def clear(self) -> None:
    self.display.blit(self.background, (0, 0))
    pygame.display.update()

  def updateBg(self, img: cv.Mat) -> None:
    rgb_frame = cv.cvtColor(
        cv.rotate(img, cv.ROTATE_90_CLOCKWISE), cv.COLOR_BGR2RGB)
    self.background = pygame.surfarray.make_surface(cv.flip(rgb_frame, 1))

    self.display.blit(self.background, (0, 0))
    pygame.display.update()
