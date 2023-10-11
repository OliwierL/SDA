import pygame
from shapes.Shape import Shape


class Rectangle(Shape):

  def __init__(self, window, vert, x, y, a, b, color):
    self.pos = (x, y)
    self.dim = (a, b)
    self.p1 = vert[0][0]
    self.p2 = vert[1][0]
    self.p3 = vert[2][0]
    self.p4 = vert[3][0]
    super().__init__(window, color, pygame.Rect(x, y, a, b), "Rectangle")

  def getArea(self):
    return self.dim[0] * self.dim[1]

  def draw(self):
    pygame.draw.polygon(self.window, self.color,
                        (self.p1, self.p2, self.p3, self.p4))

  def clickedInside(self, clickPos):
    if super().clickedInside(clickPos):
      return True
    else:
      return False
