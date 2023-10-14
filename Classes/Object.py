import cv2 as cv


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
      vert = vertices[i][0]
    self.vert = vert

  def isGray(self) -> bool:
    ac = 20
    if abs(self.color[0] - self.color[1]) < ac and abs(
        self.color[1] - self.color[2]) < ac and abs(self.color[0] -
                                                    self.color[2]) < ac:
      return True
    else:
      return False
