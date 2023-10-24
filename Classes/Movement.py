from typing import Any
import cv2 as cv
from Classes.Object import Object as Obj
from dobotLib.DoBotArm import DoBotArm as Dbt
from functions.cdet import getField


class Movement:

  def __init__(self, port: int, home=None) -> None:
    if home is None:
      home = (250, 0, 50)
    self.dobot = Dbt(port, home[0], home[1], home[2])
    self.dobot.dobotConnect()
    self.__goHome__()

  def __goHome__(self) -> None:
    self.dobot.moveHome()

  def __moveTo__(self, pos: tuple) -> None:
    self.dobot.moveArmXY(pos[0], pos[1])

  def __pickAt__(self, height: int, suction: bool) -> None:
    self.dobot.pickToggle(height)
    self.dobot.suction(suction)
    self.dobot.pickToggle(height)

  def setBCord(self, frame: cv.Mat) -> None:
    field = getField(frame)
    if type(field) is not Obj:
      print("an Error occured, unable to locate the field")
      while True:
        pass
    self.field = field
    input("Place dobot in top left corner of the field and press [ENTER]")
    self.TL = self.dobot.getPosition()
    input("Place dobot in bottom right corner of the field and press [ENTER]")
    self.BR = self.dobot.getPosition()

  def moveObj(self, obj: Obj) -> None:

    if not self.field.collidesWith(obj.center):
      print("Err: selected object is outside of the pickup field")
      return None

    dXdobot = self.TL[0] - self.BR[0]
    dYdobot = self.TL[1] - self.BR[1]

    objNormPosX = (obj.center[0] - self.field.bBox['x']) / (
        self.field.bBox['x'] + self.field.bBox['w'])

    objNormPosY = (obj.center[1] - self.field.bBox['y']) / (
        self.field.bBox['y'] + self.field.bBox['y'])

    posX = self.TL[0] + dXdobot * objNormPosX
    posY = self.TL[1] + dYdobot * objNormPosY

    objectPos = (int(posX), int(posY))  # temp

    # move to [x,y]
    self.__moveTo__(objectPos)

    # pick up
    self.__pickAt__(20, True)

    # move to drop position
    self.__moveTo__(self.dropPos)

    # drop down
    self.__pickAt__(20, False)

    # go home
    self.dobot.moveHome()
