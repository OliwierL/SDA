import pygame
from shapes.Shape import Shape


class Triangle(Shape):

  def __init__(self, window, vert, x, y, a, b, color):
    self.pos = (x, y)
    self.dim = (a, b)
    self.p1 = vert[0][0]
    self.p2 = vert[1][0]
    self.p3 = vert[2][0]

    super().__init__(window, color, pygame.Rect(x, y, a, b), "Triangle")

  def getArea(self, p1=None, p2=None, p3=None):
    if p1 is None:
      p1 = self.p1

    if p2 is None:
      p2 = self.p2

    if p3 is None:
      p3 = self.p3

    return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] *
                (p1[1] - p2[1])) / 2.0)

  def draw(self):
    pygame.draw.polygon(self.window, self.color, (self.p1, self.p2, self.p3))

  def clickedInside(self, clickPos):
    tArea = self.getArea()

    if super().clickedInside(clickPos):
      area1 = self.getArea(self.p1, self.p2, clickPos)
      area2 = self.getArea(self.p3, self.p2, clickPos)
      area3 = self.getArea(self.p3, self.p1, clickPos)
      if tArea == (area1 + area2 + area3):
        return True
    else:
      return False
