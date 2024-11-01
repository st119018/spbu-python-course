from project.game.bot import Bot
from project.game.strategy import BetTypes
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
    verbose : bool
        Flag to signal whether to print info
    verbose_file : bool
        Flag to signal whether to write to file
    is_over : bool
        Flag that indicates end of game
    current_round : int
        Number of round that is currently played
    file_name : str
        Path to file that stores example of playing game
    wheel : Wheel
        Wheel to determine winning pocket
    bankrupts: Set[int]
        Indexes of bots with no money to play

    Methods
    -------
    play(min_bet, max_bet)
        Start and play roulette
    play_round(min_bet, max_bet)
        Play one round of game
    determine_round_winners(min_bet, pocket)
        Determine winners of current round
    pay_off(bot)
        Calculate winning amount
    over(bankrupts)
        Determine if game is over
    game_state(min_bet, winners)
        Get current state of game
    get_bets(min_bet)
        Get bets made in current round
    write(msg)
        Write msg to file and print it if verbose is True
    """

    def __init__(
        self,
        bots: List[Bot],
        rounds_num: int = 10,
        verbose: bool = False,
        verbose_file: bool = False,
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
        """
        self.bots = bots
        self.rounds_num = rounds_num
        self.verbose = verbose
        self.verbose_file = verbose_file
        self.is_over = False
        self.current_round = 0
        self.file_name = "project/game/example/example.txt"
        self.wheel = Wheel()
        self.bankrupts: Set[int] = set()

    def play(self, min_bet: int = 1, max_bet: int = 100) -> Tuple[List[Bot], List[Bot]]:
        """Start and play roulette game. Return winners and losers of game

        If verbose flag is True then print process of game.

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
        self.write("Roulette\n\n")
        self.write(f"Minimum bet: {min_bet}\n")
        self.write(f"Maximum bet: {max_bet}\n")
        self.write(f"Number of rounds: {self.rounds_num}\n\n")
        self.write(self.game_state(min_bet, set()))

        while not self.is_over:
            self.play_round(min_bet, max_bet)
            self.over()

        self.write("\nGame is over\n\n")
        game_winners: List[Bot] = []
        game_losers: List[Bot] = []
        # show winners and losers of game
        for bot in self.bots:
            if bot.won():
                game_winners.append(bot)
            else:
                game_losers.append(bot)
            self.write(bot.name + (" won\n" if bot.won() else " lost\n"))

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
        self.write("=== ROUND " + str(self.current_round) + " ===\n\n")
        pocket = self.wheel.spin()

        self.write("The wheel is spinning\n\n")

        # bots make bet
        for i in range(len(self.bots)):
            if not self.bots[i].is_bankrupt(min_bet):
                self.bots[i].bet(min_bet, max_bet, self.wheel.pockets_num)
            else:
                self.bankrupts.add(i)

        self.write(self.get_bets(min_bet))
        self.write(
            f"The winning number and color: {str(pocket.num)} {str(pocket.color)}\n\n"
        )

        winners = self.determine_round_winners(min_bet, pocket)

        # collect bets and give the winnings to winners
        for i in range(len(self.bots)):
            self.bots[i].last_result = False
            if not self.bots[i].is_bankrupt(min_bet):
                self.bots[i].balance -= sum(self.bots[i].last_bet.amount)
                if i in winners:
                    self.bots[i].last_result = True
                    self.bots[i].balance += self.pay_off(self.bots[i])

        self.write(self.game_state(min_bet, winners))
        self.current_round += 1

    def determine_round_winners(self, min_bet: int, pocket: Pocket) -> Set[int]:
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
                # if self.bots[i].last_bet.bet_type == "color":
                if self.bots[i].last_bet.color == pocket.color:
                    winners.add(i)
                elif pocket.num in self.bots[i].last_bet.numbers:
                    winners.add(i)

        return winners

    def pay_off(self, bot: Bot) -> int:
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
        won = 0
        bet = bot.last_bet
        bet_types = BetTypes()
        match bet.bet_type:
            case BetTypes.single:
                won = bet.amount[0] * bet_types.payout_ratio[bet_types.single]
            case bet_types.color | bet_types.dozen:
                won = sum(bet.amount) * bet_types.payout_ratio[bet.bet_type]

        return won

    def over(self) -> None:
        """Determine if game is over and set is_over flag to True"""
        if (
            len(self.bankrupts) >= len(self.bots) - 1
            or self.current_round == self.rounds_num
        ):
            self.is_over = True

    def game_state(self, min_bet: int, winners: Set[int]) -> str:
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

    def get_bets(self, min_bet: int) -> str:
        """Return bets made by bots in current round as a string

        Parameters
        ----------
        min_bet : int
            Minimum possible bet
        """
        bet_types = BetTypes()
        msg = "Bets:\n----"
        for bot in self.bots:
            if not bot.is_bankrupt(min_bet):
                msg += (
                    "\n    "
                    + bot.name
                    + f" made a bet with {sum(bot.last_bet.amount)} chips on "
                )
                bet = bot.last_bet
                match bet.bet_type:
                    case bet_types.color:
                        msg += bet.color + " (color)"
                    case bet_types.single | bet_types.dozen:
                        msg += (
                            "".join(map(lambda n: str(n) + " ", bet.numbers))
                            + f"({bet.bet_type})"
                        )

        return msg + "\n\n"

    def write(self, msg: str) -> None:
        """Write msg to file if verbose_file flag is True

        If verbose flag is True then print msg
        """
        if self.verbose_file:
            with open(self.file_name, "a") as f:
                f.write(msg)

        if self.verbose:
            print(msg, end="")
