from project.game.strategy import Strategy, Bet


class Bot:
    """Class implements bot player

    Attributes
    ----------
    _strategy : Strategy
        Strategy of playing roulette
    _balance : int
        Amount of money left
    _initial_balance : int
        Amount of money at begining of game
    last_result : bool
        Flag to indicate winning in last made bet
    name : str
        Name of bot
    last_bet : Bet
        Last bet made by bot

    Methods
    -------
    bet(min_bet, max_bet, pockets_num)
        Make bet according to strategy
    is_bankrupt(min_bet)
        Determine if bot has no money left to play
    won()
        Determine if bot won or lost money at the end of game
    """

    def __init__(self, strategy: Strategy, balance: int, name: str = ""):
        """Set attributes

        Parameters
        ----------
        strategy : Strategy
            Strategy of playing roulette
        balance : int
            Amount of money in begining of game
        name : str
            Name of bot
        """
        self._strategy = strategy
        self._balance = balance
        self._initial_balance = balance
        self.last_result = False
        self.name = name
        self._last_bet = Bet()

    def bet(self, min_bet: int, max_bet: int, pockets_num: int) -> None:
        """Make bet according to strategy"""
        self._last_bet = self._strategy.make_bet(
            self._balance, min_bet, max_bet, pockets_num, self.last_result
        )

    @property
    def last_bet(self) -> Bet:
        return self._last_bet

    @property
    def balance(self) -> int:
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    def is_bankrupt(self, min_bet: int) -> bool:
        """Return True if balance is less then minimum bet"""
        return self._balance < min_bet

    def won(self) -> bool:
        """Return True if bot's balance increased"""
        return self.balance > self._initial_balance
