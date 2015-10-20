import random

from vomito.models import Turn, Rule, Drink, Game


def turn_generate(self, string):
    self.string = string
    self.save()
Turn.generate = turn_generate


def future_turn(self, min_turn, max_turn, rule, players=None):
    if players is None:
        players = []

    # Find already reserved turns
    reserved_turns = Turn.objects.filter(game=self.game, number__gt=self.number).values_list('number', flat=True)
    # transorm absolute values into relatives from actual turn
    reserved_turns = [number - self.number for number in reserved_turns]

    potentials = [x for x in range(min_turn, max_turn + 1) if x not in reserved_turns]
    if len(potentials) > 0:
        random.shuffle(potentials)
        selected_turn = potentials[0]
    else:
        # If no turn is available
        selected_turn = next((x for x in range(max_turn, max(reserved_turns) + 2) if x not in reserved_turns))

    next_turn = Turn(game=self.game, number=self.number + selected_turn, rule=rule)
    next_turn.save()
    next_turn.players.add(*players)
    return next_turn
Turn.future = future_turn


def get_nb_sip(self):
    if not self.min_sip or not self.max_sip:
        return 0
    return random.randint(self.min_sip, self.max_sip)
Rule.get_nb_sip = get_nb_sip


def game_has_drink(self, player, sip=0, bottom_up=None):
    Drink(turn=self.current_turn, player=player, sip=sip, bottom_up=bottom_up).save()
Game.has_drink = game_has_drink
