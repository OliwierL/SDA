import pygame
from shapes.Shape import Shape


class Rectangle(Shape):

  def __init__(self, window, x, y, a, b, color):
    self.pos = (x, y)
    self.dim = (a, b)
    super().__init__(window, color, pygame.Rect(x, y, a, b), "Rectangle")

  def getArea(self):
    return self.dim[0] * self.dim[1]

  def draw(self):
    pygame.draw.rect(self.window, self.color, self.shape)

  def clickedInside(self, clickPos):
    if super().clickedInside(clickPos):
      return True
    else:
      return False
