# -*- coding: utf-8 -*-
from django.db import models
import random

from bois.fields.script_field import ScriptField
from bois.lib.models import ScriptedModel, ContextModel


class Rule(ScriptedModel):
    description = models.CharField(max_length=512)
    category = models.ForeignKey('Category')
    mixte = models.BooleanField(default=False)
    nb_players = models.PositiveIntegerField()
    # TODO check min can't be bigger than max
    min_sip = models.PositiveIntegerField(null=True, blank=True)
    max_sip = models.PositiveIntegerField(null=True, blank=True)
    next = models.ForeignKey('Rule', null=True, blank=True)
    randomizable = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    """
    Créer les objets Drink, set la valeur String au turn,
    """
    on_proc = ScriptField(blank=True, null=True, help_text="Called just after the turn is created. `rule` is the pending rule. `game` is the pending game. `turn` is the current turn. `players` is the list of players. `involved_players` is the list of players of this turn. `nb_sip` is the number of sips randomized for this turn.")


class Category(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.PositiveIntegerField()
    weighting = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Game(models.Model, ContextModel):

    context_app = 'game'
    context_holder = '_GameVariable'
    context_model = 'game'

    category = models.ForeignKey('Category')
    players = models.ManyToManyField('Player')
    mixte = models.BooleanField(default=True)
    current_turn = models.ForeignKey('Turn', null=True, related_name='current_turn')

    def __str__(self):
        return "Game %s" % (self.category)

    def select_rule(self):
        rules = Rule.objects.exclude(
            randomizable=False
        ).filter(
            nb_players__lte=self.players.count(),
            category__difficulty__lte=self.category.difficulty
        )
        if not self.mixte:
            rules = rules.filter(mixte=False)

        weighted_rules = []
        for rule in rules:
            for x in range(rule.category.weighting):
                weighted_rules.append(rule)

        return random.choice(weighted_rules)

    def select_players(self, rule):
        return self.players.all().order_by('?')[:rule.nb_players]

    def next_turn(self):
        # If first turn
        next_turn_number = self.current_turn.number + 1 if self.current_turn else 1
        try:
            # If a forced turn has been created, get it
            turn = self.turn_set.get(number=next_turn_number)
        except Turn.DoesNotExist:
            rule = self.select_rule()
            involved_players = self.select_players(rule)

            turn = Turn(rule=rule, game=self, number=next_turn_number)
            turn.save()
            turn.players.add(*list(involved_players))

        self.current_turn = turn
        self.save()

        turn.execute()


class Player(models.Model):

    MALE = 'm'
    FEMALE = 'f'

    SEX_CHOICES = (
        (MALE, '♂'),
        (FEMALE, '♀')
    )

    first_name = models.CharField(max_length=255)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, default=MALE)

    def __str__(self):
        return self.first_name


class Turn(models.Model):
    rule = models.ForeignKey('Rule')
    game = models.ForeignKey('Game')
    string = models.TextField()
    number = models.PositiveIntegerField()
    players = models.ManyToManyField('Player')

    class Meta():
        unique_together = ("game", "number")

    def execute(self):
        self.rule.execute(self.game, self.players)


class Drink(models.Model):
    turn = models.ForeignKey('Turn')
    player = models.ForeignKey('Player')
    sip = models.PositiveIntegerField(null=True)
    bottom_up = models.NullBooleanField()
