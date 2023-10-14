import pygame


class Shape:

  def __init__(self, window, color, shape, shapeType):
    self.window = window
    self.color = color
    self.shape = shape
    self.shapeType = shapeType

  def clickedInside(self, clickPos):
    if self.shape.collidepoint(clickPos):
      return True
    else:
      return False

  def getType(self):
    return self.shapeType

  def draw(self):
    pass

  def getArea():
    pass
