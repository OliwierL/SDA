import cv2 as cv
import numpy as np

from Classes.Object import Object as Obj
from functions.ObjD import detectObjects as detObj

from icecream import ic


def getField(frame: cv.Mat) -> Obj:
  obj = None
  for objD in detObj(frame):
    tObj = Obj(objD)
    if not tObj.notGray() and tObj.shape == "Rectangle":
      size = tObj.bBox['w'] + tObj.bBox['h']
      if size > 700:
        obj = tObj

  if obj == None:
    return -1
  else:
    return obj
