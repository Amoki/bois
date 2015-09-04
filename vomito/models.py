# -*- coding: utf-8 -*-
from django.db import models
import random

from bois.fields.script_field import ScriptField
from bois.lib.models import ScriptedModel, ContextModel


class Rule(ScriptedModel):
    description = models.CharField(max_length=512)
    next = models.ForeignKey('Next', null=True, blank=True)
    category = models.ForeignKey('Category')
    mixte = models.BooleanField(default=False)
    nb_players = models.PositiveIntegerField()
    # DOTO check min can't be bigger than max
    min_sip = models.PositiveIntegerField()
    max_sip = models.PositiveIntegerField()

    def __unicode__(self):
        return self.description

    """
    Créer les objets Drink, set la valeur String au turn,
    """
    on_proc = ScriptField(blank=True, null=True, help_text="Called just after the turn is created. `rule` is the pending rule, available without any context (you can't call `set_value`). `game` is the pending game. `turn` is the current turn. `players` is the list of players. `involved_players` is the list of players of this turn.")


class Next(models.Model):
    rules = models.ManyToManyField('Rule', related_name="+")


class Category(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.PositiveIntegerField()
    weighting = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Game(models.Model, ContextModel):
    category = models.ForeignKey('Category')
    players = models.ManyToManyField('Player')
    mixte = models.BooleanField(default=True)

    def __unicode__(self):
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
            for x in xrange(rule.category.weighting):
                weighted_rules.append(rule)

        return random.choice(weighted_rules)

    def select_players(self, rule):
        return self.players.all().order_by('?')[:rule.nb_players]

    def next_turn(self):
        rule = self.select_rule()
        involved_players = list(self.select_players(rule))

        turn = Turn(rule=rule, game=self)
        turn.save()

        rule.execute(self, involved_players)

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
    last_name = models.CharField(max_length=255)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, default=MALE)

    class Meta:
        unique_together = (("first_name", "last_name"),)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Turn(models.Model):
    rule = models.ForeignKey('Rule')
    game = models.ForeignKey('Game')
    string = models.TextField()


class Drink(models.Model):
    turn = models.ForeignKey('Turn')
    player = models.ForeignKey('Player')
    sip = models.PositiveIntegerField(null=True)
    bottoms_up = models.NullBooleanField()
