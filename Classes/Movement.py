from typing import Any

from networkx import triad_type
from Classes.Object import Object as Obj
from dobotLib.DoBotArm import DoBotArm as Dbt


class Movement:

  def __init__(self, home: tuple, dropPos: tuple) -> None:
    self.dobot = Dbt(home[0], home[1], home[2])
    self.dropPos = dropPos
    self.dobot.dobotConnect()
    self.__goHome__()

  def __goHome__(self) -> None:
    self.dobot.moveHome()

  def __moveTo__(self, pos: tuple) -> None:
    self.dobot.moveArmXY(pos[0], pos[1])

  def __pickAt__(self, height, suction) -> None:
    self.dobot.pickToggle(height)
    self.dobot.suction(suction)
    self.dobot.pickToggle(height)

  def moveObj(self, obj: Obj) -> None:

    # TODO: pixel to mm conversion
    # TODO: img coordinates to real life conversion
    objectPos = (0, 0)  # temp

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
