from ast import Tuple
from math import sqrt
import cv2 as cv
import pygame
from sympy import false, true

from icecream import ic


class Object:

  def __init__(self, ObjSpec) -> None:
    self.contour = ObjSpec['contour']
    self.center = ObjSpec['center']
    self.shape = ObjSpec['shape']
    self.color = ObjSpec['color']
    self.bBox = ObjSpec['bBox']
    epsilon = 0.04 * cv.arcLength(ObjSpec['contour'], True)
    vertices = cv.approxPolyDP(ObjSpec['contour'], epsilon, True)
    vert = []
    for i in range(len(vertices)):
      vert.append(vertices[i][0])
    self.vert = vert

  def notGray(self) -> bool:
    ac = 20
    if abs(self.color[0] - self.color[1]) < ac and abs(
        self.color[1] - self.color[2]) < ac and abs(self.color[0] -
                                                    self.color[2]) < ac:
      return False
    else:
      return True

  def collidesWith(self, pos: tuple) -> bool:

    isColliding = pygame.Rect(self.bBox['x'], self.bBox['y'], self.bBox['w'],
                              self.bBox['h']).collidepoint(pos)

    if isColliding:

      if self.shape == "Circle":
        radious = (self.bBox['w'] + self.bBox['h']) / 4
        center = (self.bBox['x'] + self.bBox['w'] / 2,
                  self.bBox['y'] + self.bBox['h'] / 2)
        distance = sqrt(
            abs(center[0] - pos[0])**2 + (abs(center[1] - pos[1])**2))
        if distance < radious:
          return True
        else:
          return False

      elif self.shape == "Rectangle":
        n = len(self.vert)
        j = n - 1
        inside = False

        for i in range(n):
          xi, yi = self.vert[i]
          xj, yj = self.vert[j]

          if (yi < pos[1] and yj >= pos[1]) or (yj < pos[1] and yi >= pos[1]):
            if xi + (pos[1] - yi) / (yj - yi) * (xj - xi) < pos[0]:
              inside = not inside
          j = i
        return inside

      elif self.shape == "Triangle":
        p1 = self.vert[0]
        p2 = self.vert[1]
        p3 = self.vert[2]

        # area between points vert[0], vert[1], vert[2]
        tArea = abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] *
                     (p1[1] - p2[1])) / 2.0)

        p3 = pos
        # area between points vert[0], vert[1], click
        area1 = abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] *
                     (p1[1] - p2[1])) / 2.0)

        p1 = self.vert[2]
        # area between points vert[2], vert[1], click
        area2 = abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] *
                     (p1[1] - p2[1])) / 2.0)

        p2 = self.vert[0]
        # area between points vert[2], vert[0], click
        area3 = abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] *
                     (p1[1] - p2[1])) / 2.0)

        # if total area equals sum of all areas then the point is inside the triangle
        if tArea == (area1 + area2 + area3):
          return True
        else:
          return False

    else:
      return False

    pass
