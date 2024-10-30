from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
import random


@dataclass
class Bet:
    """Data-class that implements bet

    Attributes
    ----------
    numbers : List[int]
        Pocket numbers in bet
    color : str
        Color of pockets in bet
    amount : List[int]
        Amount of bet
    bet_type : str
        Type of bet
    """

    numbers: List[int] = field(default_factory=list)
    color: str = ""
    amount: List[int] = field(default_factory=list)
    bet_type: str = ""


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
            return Bet(bet_type="none")

        chips_num = min(balance // min_bet, pockets_num // 2, max_bet // min_bet)

        bet_numbers = random.sample(range(pockets_num), chips_num)
        bet_amount = [min_bet for _ in range(chips_num)]
        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type="single")


class MartingaleStrategy(Strategy):
    def __init__(self):
        self._last_bet_amount: List[int] = []
        self._last_color: str
        self._is_first = True

    def make_bet(
        self,
        balance: int,
        min_bet: int,
        max_bet: int,
        pockets_num: int,
        last: bool = False,
    ) -> Bet:
        """Make bet on random color according to Martingale startegy

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
            return Bet(bet_type="none")

        bet_color = random.choice(["red", "black"])
        if self._is_first or last:
            self._is_first = False
            self._last_color = bet_color
            self._last_bet_amount = [min_bet]
            return Bet(color=bet_color, amount=self._last_bet_amount, bet_type="color")

        if (
            balance >= self._last_bet_amount[0] * 2
            and self._last_bet_amount[0] * 2 <= max_bet
        ):
            self._last_bet_amount = [self._last_bet_amount[0] * 2]
        else:
            self._last_bet_amount = [min_bet]

        return Bet(
            color=self._last_color, amount=self._last_bet_amount, bet_type="color"
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
            return Bet(bet_type="none")

        # choose one of three dozens
        num_dozen = random.choice([i + 1 for i in range(self._dozen_number)])
        # amount of numbers to bet on
        numbers_bet = pockets_num // self._dozen_number
        # numbers on wheel to bet on
        bet_numbers = [
            i + 1 for i in range(numbers_bet * (num_dozen - 1), numbers_bet * num_dozen)
        ]
        bet_amount = [
            min_bet
            for _ in range(min(balance // min_bet, numbers_bet, max_bet // min_bet))
        ]
        return Bet(numbers=bet_numbers, amount=bet_amount, bet_type="dozen")