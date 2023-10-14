import pygame
import math
from shapes.Shape import Shape


class Circle(Shape):

  def __init__(self, window, x, y, radious, color):
    self.radious = radious
    self.pos = (x + radious, y + radious)
    super().__init__(window, color, pygame.Rect(x, y, radious * 2, radious * 2),
                     "Circle")

  def getArea(self):
    return math.pi * self.radious**2

  def draw(self):
    pygame.draw.circle(self.window, self.color, self.pos, self.radious)

  def clickedInside(self, clickPos):

    if super().clickedInside(clickPos):
      if (math.sqrt(
          abs(self.pos[0] - clickPos[0])**2 + abs(self.pos[0] - clickPos[0])**2)
          < self.radious):
        return True
    else:
      return False
