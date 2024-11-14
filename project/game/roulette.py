from project.game.strategy import ColorTypes
from project.game.bot import Bot
from project.game.wheel import Wheel, Pocket
from typing import List, Set, Tuple


class Roulette:
    """Class implements roulette game

    Attributes
    ----------
    bots : List[Bot]
        List of bots that play roulette
    rounds_num : int
        Maximum number of rounds
    _verbose : bool
        Flag to signal whether to print info
    _verbose_file : bool
        Flag to signal whether to write to file
    _is_over : bool
        Flag that indicates end of game
    current_round : int
        Number of round that is currently played
    _file_name : str
        Path to file that stores example of playing game
    _wheel : Wheel
        Wheel to determine winning pocket
    _bankrupts: Set[int]
        Indexes of bots with no money to play

    Methods
    -------
    play(min_bet, max_bet)
        Start and play roulette
    play_round(min_bet, max_bet)
        Play one round of game
    _determine_round_winners(min_bet, pocket)
        Determine winners of current round
    _pay_off(bot)
        Calculate winning amount
    _over()
        Determine if game is over
    _game_state(min_bet, winners)
        Get current state of game
    _get_bets(min_bet)
        Get bets made in current round
    _write(msg)
        Write msg to file and print it if _verbose is True
    """

    def __init__(
        self,
        bots: List[Bot],
        rounds_num: int = 10,
        verbose: bool = False,
        verbose_file: bool = False,
        *,
        file_name="project/game/example/example.txt",
    ):
        """Set attribites

        Parameters
        ----------
        bots : List[Bot]
            Bots that will play roulette
        rounds_num : int
            Maximum number of rounds
        verbose_file : bool
            Flag to signal whether to write to file
        verbose : bool
            Flag to signal whether to print info
        file_name
            Path to file
        """
        self.bots = bots
        self.rounds_num = rounds_num
        self._verbose = verbose
        self._verbose_file = verbose_file
        self._is_over = False
        self.current_round = 0
        self._file_name = file_name
        self._wheel = Wheel()
        self._bankrupts: Set[int] = set()

    def play(self, min_bet: int = 1, max_bet: int = 100) -> Tuple[List[Bot], List[Bot]]:
        """Start and play roulette game. Return winners and losers of game

        If _verbose flag is True then print process of game.

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        max_bet : int
            Maximum possible bet

        Return
        ------
        Tuple[List[Bot], List[Bot]]
        """
        self._write("Roulette\n\n")
        self._write(f"Minimum bet: {min_bet}\n")
        self._write(f"Maximum bet: {max_bet}\n")
        self._write(f"Number of rounds: {self.rounds_num}\n\n")
        self._write(self._game_state(min_bet, set()))

        while not self._is_over:
            self.play_round(min_bet, max_bet)
            self._over()

        self._write("\nGame is over\n\n")
        game_winners: List[Bot] = []
        game_losers: List[Bot] = []
        # show winners and losers of game
        for bot in self.bots:
            if bot.won():
                game_winners.append(bot)
            else:
                game_losers.append(bot)
            self._write(bot.name + (" won\n" if bot.won() else " lost\n"))

        return (game_winners, game_losers)

    def play_round(self, min_bet: int, max_bet: int) -> None:
        """Play one round of game

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        max_bet : int
            Maximum possible bet

        Return
        ------
        None
        """
        self._write("=== ROUND " + str(self.current_round + 1) + " ===\n\n")
        pocket = self._wheel.spin()

        self._write("The wheel is spinning\n\n")

        # bots make bet
        for i in range(len(self.bots)):
            if not self.bots[i].is_bankrupt(min_bet):
                self.bots[i].bet(min_bet, max_bet, self._wheel.pockets_num)
            else:
                self._bankrupts.add(i)

        self._write(self._get_bets(min_bet))
        self._write(
            f"The winning number and color: {str(pocket.num)} {str(pocket.color.value)}\n\n"
        )

        winners = self._determine_round_winners(min_bet, pocket)

        # collect bets and give the winnings to winners
        for i in range(len(self.bots)):
            self.bots[i].last_result = False
            if not self.bots[i].is_bankrupt(min_bet):
                self.bots[i].balance -= sum(self.bots[i].last_bet.amount)
                if i in winners:
                    self.bots[i].last_result = True
                    self.bots[i].balance += self._pay_off(self.bots[i])

        self._write(self._game_state(min_bet, winners))
        self.current_round += 1

    def _determine_round_winners(self, min_bet: int, pocket: Pocket) -> Set[int]:
        """Determine winners of current round and return their indexes

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        pocket : Pocket
            Winning pocket

        Return
        ------
        Set[int]
        """

        winners: Set[int] = set()
        for i in range(len(self.bots)):
            if not self.bots[i].is_bankrupt(min_bet):
                # check if color or number matches
                if self.bots[i].last_bet.color == pocket.color:
                    winners.add(i)
                elif pocket.num in self.bots[i].last_bet.numbers:
                    winners.add(i)

        return winners

    def _pay_off(self, bot: Bot) -> int:
        """Calculate winning amount in current round

        Parameters
        ----------
        bot : Bot
            Bot that has won current round
        pockets_num : int
            Number of pockets in wheel

        Return
        ------
        int
        """

        bet = bot.last_bet
        won = bet.amount[0] * bet.bet_type.value

        return won

    def _over(self) -> None:
        """Determine if game is over and set _is_over flag to True"""
        if (
            len(self._bankrupts) >= len(self.bots) - 1
            or self.current_round == self.rounds_num
        ):
            self._is_over = True

    def _game_state(self, min_bet: int, winners: Set[int]) -> str:
        """Return current state of game as a string"""

        msg = "Current game state:\n-------------------\n"
        bot_msg = "    Players: "
        win_msg = "    Winners of the round: "
        lose_msg = "    Bankrupts: "

        for bot in self.bots:
            bot_msg += bot.name + f"(balance={bot.balance}) "

        if all(not bot.is_bankrupt(min_bet) for bot in self.bots):
            lose_msg += "no bankrupts"
        else:
            for bot in self.bots:
                if bot.is_bankrupt(min_bet):
                    lose_msg += bot.name + " "

        if len(winners) == 0:
            win_msg += "no winners"
        else:
            for i in winners:
                win_msg += self.bots[i].name + " "
        msg += bot_msg + "\n" + win_msg + "\n" + lose_msg + "\n\n"
        return msg

    def _get_bets(self, min_bet: int) -> str:
        """Return bets made by bots in current round as a string

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        """
        msg = "Bets:\n----"
        for bot in self.bots:
            if not bot.is_bankrupt(min_bet):
                msg += (
                    "\n    "
                    + bot.name
                    + f" made a bet with {sum(bot.last_bet.amount)} chips on "
                )
                bet = bot.last_bet
                if bet.color != ColorTypes.Green:
                    msg += bet.color.value + " (color)"
                elif len(bet.numbers) != 0:
                    msg += (
                        "".join(map(lambda n: str(n) + " ", bet.numbers))
                        + f"({bet.bet_type.name.lower()})"
                    )

        return msg + "\n\n"

    def _write(self, msg: str) -> None:
        """Write msg to file if _verbose_file flag is True

        If _verbose flag is True then print msg
        """
        if self._verbose_file:
            with open(self._file_name, "a") as f:
                f.write(msg)

        if self._verbose:
            print(msg, end="")
