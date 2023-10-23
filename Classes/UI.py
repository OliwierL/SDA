import pygame
import cv2 as cv
from Classes.Object import Object as Obj


class UI:

  def __init__(self, w: int, h: int, img: cv.Mat) -> None:
    pygame.init()
    self.width = w
    self.height = h
    self.display = pygame.display.set_mode((w, h))

    rgb_frame = cv.cvtColor(
        cv.rotate(img, cv.ROTATE_90_CLOCKWISE), cv.COLOR_BGR2RGB)
    self.background = pygame.surfarray.make_surface(cv.flip(rgb_frame, 1))

  def drawObjs(self, objs: list[Obj]) -> None:
    for obj in objs:
      if obj.shape == "Circle":
        radious = (obj.bBox['w'] + obj.bBox['h']) / 4
        pos = (obj.bBox['x'] + radious, obj.bBox['y'] + radious)
        pygame.draw.circle(self.display, obj.color, pos, radious)
      elif obj.shape == "Rectangle" or obj.shape == "Triangle":
        pygame.draw.polygon(self.display, obj.color, obj.vert)
      else:
        pass
    pygame.display.update()

  def checkClick(self, objs: list[Obj]) -> Obj:
    clickPos = pygame.mouse.get_pos()
    for obj in objs:
      if obj.collidesWith(clickPos):
        return obj

  def clear(self) -> None:
    self.display.blit(self.background, (0, 0))
    pygame.display.update()

  def updateBg(self, img: cv.Mat) -> None:
    rgb_frame = cv.cvtColor(
        cv.rotate(img, cv.ROTATE_90_CLOCKWISE), cv.COLOR_BGR2RGB)
    self.background = pygame.surfarray.make_surface(cv.flip(rgb_frame, 1))

    self.display.blit(self.background, (0, 0))
    pygame.display.update()
