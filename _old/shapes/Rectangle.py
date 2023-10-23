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
      vert = [self.p1, self.p2, self.p3, self.p4]
      n = len(vert)
      j = n - 1
      inside = False

      for i in range(n):
        xi, yi = vert[i]
        xj, yj = vert[j]

        if (yi < clickPos[1] and yj >= clickPos[1]) or (yj < clickPos[1] and
                                                        yi >= clickPos[1]):
          if xi + (clickPos[1] - yi) / (yj - yi) * (xj - xi) < clickPos[0]:
            inside = not inside
        j = i

      return inside

    else:
      return False
