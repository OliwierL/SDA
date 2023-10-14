import cv2 as cv
from functions.ObjD import *
from Classes.Object import Object as Obj


class Vision:

  def __init__(self, camera: cv.VideoCapture, resolution: tuple) -> None:
    self.cam = camera
    self.cam.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
    self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
    _, self.frame = self.cam.read()

  def __repr__(self) -> str:
    return f"Vision('camera':{self.cam})"

  def refresh(self) -> None:
    _, self.frame = self.cam.read()

  def GetObjects(self) -> list[Obj]:
    objSpecs = detectObjects(self.frame)
    objects = []
    for obD in objSpecs:
      if not obD['shape'] == "Unknown":
        ob = Obj(obD)
        if ob.notGray():
          objects.append(ob)

    return objects
