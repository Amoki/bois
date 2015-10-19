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

    def __str__(self):
        return self.description

    """
    Créer les objets Drink, set la valeur String au turn,
    """
    on_proc = ScriptField(blank=True, null=True, help_text="Called just after the turn is created. `rule` is the pending rule. `game` is the pending game. `turn` is the current turn. `players` is the list of players. `involved_players` is the list of players of this turn. `nb_sip` is the number of sips randomized for this turn.")

    def get_nb_sip(self):
        if not self.min_sip or not self.max_sip:
            return 0
        return random.randint(self.min_sip, self.max_sip)


class Category(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.PositiveIntegerField()
    weighting = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Game(models.Model, ContextModel):
    category = models.ForeignKey('Category')
    players = models.ManyToManyField('Player')
    mixte = models.BooleanField(default=True)
    turn_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Game %s" % (self.category)

    def select_rule(self):
        if self.mixte:
            rules = Rule.objects.filter(
                nb_players__lte=self.players.count(),
                category__difficulty__lte=self.category.difficulty
            )
        else:
            rules = Rule.objects.filter(
                nb_players__lte=self.players.count(),
                category__difficulty__lte=self.category.difficulty,
                mixte=False
            )

        weighted_rules = []
        for rule in rules:
            for x in range(rule.category.weighting):
                weighted_rules.append(rule)

        return random.choice(weighted_rules)

    def select_players(self, rule):
        return self.players.all().order_by('?')[:rule.nb_players]

    def next_turn(self):
        self.turn_number += 1
        self.save()
        try:
            # If a forced turn has been created, get it
            turn = self.turn_set.get(number=self.turn_number)
        except Turn.DoesNotExist:
            rule = self.select_rule()
            involved_players = self.select_players(rule)

            turn = Turn(rule=rule, game=self, number=self.turn_number)
            turn.save()
            turn.players.add(*list(involved_players))

        turn.execute()

        # Select a Rule
        # Select players according to rule number
        # Create the turn
        # execute the rule script
        # Signal to update player stats
        pass


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

    def drink(self, turn, sip=0, bottoms_up=None):
        Drink(turn=turn, player=self, sip=sip, bottoms_up=bottoms_up).save()


class Turn(models.Model):
    rule = models.ForeignKey('Rule')
    game = models.ForeignKey('Game')
    string = models.TextField()
    number = models.PositiveIntegerField()
    players = models.ManyToManyField('Player')

    def execute(self):
        self.rule.execute(self.game, self.players)

    def end(self, string):
        self.string = string
        self.save()


class Drink(models.Model):
    turn = models.ForeignKey('Turn')
    player = models.ForeignKey('Player')
    sip = models.PositiveIntegerField(null=True)
    bottoms_up = models.NullBooleanField()
