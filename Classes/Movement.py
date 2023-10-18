from typing import Any

from networkx import triad_type
from Classes.Object import Object as Obj
from dobotLib.DoBotArm import DoBotArm as Dbt


class Movement:

  def __init__(self, home: tuple, dropPos: tuple) -> None:
    self.dobot = Dbt(home[0], home[1], home[2])
    self.dropPos = dropPos

    # this requires testing to set to proper values
    # dobot coordinates for Top Left Corner of the image
    self.TL = (0, 0)
    # dobot coordinates for Bottom Right Corner of the image
    self.BR = (200, 120)

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

  def moveObj(self, obj: Obj, res: tuple, TL=None, BR=None) -> None:
    if type(TL) == None or type(BR) == None:
      TL = self.TL
      BR = self.BR

    # Distance From Origin (0,0) or (TL)
    # where 0 is origin and 1 is max value
    DFO_X = obj.center[0] / res[0]
    DFO_Y = obj.center[1] / res[1]

    posX = TL[0] - (TL[0] - BR[0]) * DFO_X
    posY = TL[1] - (TL[1] - BR[1]) * DFO_Y

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
    pass
