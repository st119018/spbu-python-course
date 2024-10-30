import pytest
from project.game.roulette import Roulette
from project.game.wheel import Wheel
from project.game.strategy import RandomStrategy, MartingaleStrategy, DozenStrategy, Bet
from project.game.bot import Bot


def test_game_wheel():
    wheel = Wheel()
    assert wheel.pockets_num == 37

    with pytest.raises(AttributeError):
        wheel.pockets_num = 26


@pytest.mark.parametrize(
    "strategy, bet_type",
    [
        (RandomStrategy(), "single"),
        (MartingaleStrategy(), "color"),
        (DozenStrategy(), "dozen"),
    ],
)
def test_game_strategy(strategy, bet_type):
    wheel = Wheel()
    bot = Bot(strategy, 100)
    bot.bet(1, 100, wheel.pockets_num)

    assert bot.last_bet.bet_type == bet_type
    assert sum(bot.last_bet.amount) <= bot.balance


def test_game_bot():
    bot = Bot(RandomStrategy(), balance=100)

    assert bot.balance == 100
    bot.balance -= 20
    assert bot.balance == 80

    with pytest.raises(AttributeError):
        bot.last_bet = Bet()


@pytest.fixture
def roulette():
    bot1 = Bot(RandomStrategy(), 100)
    bot2 = Bot(MartingaleStrategy(), 100)
    bot3 = Bot(DozenStrategy(), 100)
    bots = [bot1, bot2, bot3]
    return Roulette(bots)


def test_game_roulette(roulette):
    win, lose = roulette.play()

    assert roulette.current_round == roulette.rounds_num
    assert len(win) + len(lose) == len(roulette.bots)


def test_game_play_round(roulette):
    assert roulette.current_round == 1

    roulette.play_round(1, 100)

    assert roulette.current_round == 2
    # all bots made bet
    for bot in roulette.bots:
        assert bot.last_bet.bet_type != "none"
