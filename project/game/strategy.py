from abc import ABC, abstractmethod
from typing import List
from enum import Enum
from dataclasses import dataclass, field
import random


class ColorTypes(Enum):
    """Possible colors to bet on

    Attibutes
    ---------
    Black : str
    Red : str
    Green: str
    """

    Black: str = "black"
    Red: str = "red"
    Green: str = "green"


class BetTypes(Enum):
    """Types of bet

    Each bet type is represented by its payout ratio

    Attributes
    ----------
    Single : int
    Color : int
    Dozen : int
    """

    Single: int = 36
    Color: int = 2
    Dozen: int = 3


@dataclass
class Bet:
    """Data-class that implements bet

    Attributes
    ----------
    numbers : List[int]
        Pocket numbers in bet
    color : ColorTypes
        Color of pockets in bet
    amount : List[int]
        Amount of bet
    bet_type : BetTypes
        Type of bet
    """

    numbers: List[int] = field(default_factory=list)
    color: ColorTypes = ColorTypes.Green  # some default value
    amount: List[int] = field(default_factory=list)
    bet_type: BetTypes = BetTypes.Color  # some default value


class Strategy(ABC):
    """Abstract class that implements strategy for playing roulette"""

    @abstractmethod
    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """Make bet according to strategy.

        Random strategy: bet on randomly chosen half of pockets or less

        Color strategy: bet small amount on random color

        Dozen strategy: bet on one of dozens

        Parameters
        ----------
        balance : int
            Amount of money left
        min_bet : int
            Minimum bet amount
        max_bet : int
            Maximum bet amount
        pockets_num : int
            Number of pockets in wheel
        last : bool
            True if last bet won

        Return
        ------
        Bet
        """
        pass


class RandomStrategy(Strategy):
    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """Make bet on randomly chosen half of pockets or less

        Parameters
        ----------
        balance : int
            Amount of money left
        min_bet : int
            Minimum bet amount
        max_bet : int
            Maximum bet amount
        pockets_num : int
            Number of pockets in wheel
        last : bool
            True if last bet won

        Return
        ------
        Bet
        """
        if balance < min_bet:
            return Bet()

        chips_num = min(balance // min_bet, pockets_num // 2, max_bet // min_bet)

        bet_numbers = random.sample(range(pockets_num), chips_num)
        bet_amount = [min_bet for _ in range(chips_num)]
        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type=BetTypes.Single)


class MartingaleStrategy(Strategy):
    def __init__(self):
        self._last_bet_amount: List[int] = []
        self._last_color: ColorTypes
        self._is_first = True

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """Make bet on random color according to Martingale strategy

        If last bet lost then bet on same color with doubled amount

        If last bet won then bet on random color with min_bet

        Parameters
        ----------
        balance : int
            Amount of money left
        min_bet : int
            Minimum bet amount
        max_bet : int
            Maximum bet amount
        pockets_num : int
            Number of pockets in wheel
        last : bool
            True if last bet won

        Return
        ------
        Bet
        """
        if balance < min_bet:
            return Bet()

        bet_color = random.choice(list(ColorTypes))
        if self._is_first or last:
            self._is_first = False
            self._last_color = bet_color
            self._last_bet_amount = [min_bet]
            return Bet(
                color=bet_color,
                amount=self._last_bet_amount,
                bet_type=BetTypes.Color,
            )

        if (
            balance >= self._last_bet_amount[0] * 2
            and self._last_bet_amount[0] * 2 <= max_bet
        ):
            self._last_bet_amount = [self._last_bet_amount[0] * 2]
        else:
            self._last_bet_amount = [min_bet]

        return Bet(
            color=self._last_color,
            amount=self._last_bet_amount,
            bet_type=BetTypes.Color,
        )


class DozenStrategy(Strategy):
    def __init__(self):
        self._dozen_number = 3

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """Make bet on one of dozens

        Parameters
        ----------
        balance : int
            Amount of money left
        min_bet : int
            Minimum bet amount
        max_bet : int
            Maximum bet amount
        pockets_num : int
            Number of pockets in wheel
        last : bool
            True if last bet won

        Return
        ------
        Bet
        """
        if balance < min_bet:
            return Bet()

        # choose one of three dozens
        num_dozen = random.choice([i + 1 for i in range(self._dozen_number)])
        # amount of numbers to bet on
        numbers_bet = pockets_num // self._dozen_number
        # numbers on wheel to bet on
        bet_numbers = [
            i + 1 for i in range(numbers_bet * (num_dozen - 1), numbers_bet * num_dozen)
        ]
        bet_amount = [
            min_bet * min(balance // min_bet, numbers_bet, max_bet // min_bet)
        ]
        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type=BetTypes.Dozen)
