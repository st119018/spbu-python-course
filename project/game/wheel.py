from project.game.strategy import ColorTypes
from dataclasses import dataclass
import random


@dataclass
class Pocket:
    """Data-class that implements pocket on wheel

    Attributes
    ----------
    num : int
        Number in the pocket
    color : ColorTypes
        Color of pocket
    """

    num: int = 0
    color: ColorTypes = ColorTypes.Green


class Wheel:
    """Class implements wheel in roulette game

    Attributes
    ----------
    _pockets_num : int
        Number of pockets in wheel
    _pockets : List[Pocket]
        List of pockets on wheel"""

    def __init__(self):
        """Set appropriate values to pockets on wheel"""
        self._pockets_num = 37
        self._pockets = [Pocket()]

        numbers_of_same_color = (10, 18, 28)
        # make pockets on wheel
        flag = True
        for i in range(1, self._pockets_num):
            if flag:
                self._pockets.append(Pocket(i, ColorTypes.Red))
            else:
                self._pockets.append(Pocket(i, ColorTypes.Black))

            # color of all pockets alternates
            # except for pairs (10, 11), (18, 19), (28, 29)
            if i not in numbers_of_same_color:
                flag = not flag

    @property
    def pockets_num(self) -> int:
        """Return number of pockets in wheel"""
        return self._pockets_num

    def spin(self) -> Pocket:
        """Spin wheel and return winning pocket"""
        return random.choice(self._pockets)
