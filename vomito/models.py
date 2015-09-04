from django.db import models
import random


class Rule(models.Model):
    name = models.CharField(max_length=512)
    next = models.ForeignKey('Next', null=True, blank=True)
    category = models.ForeignKey('Category')
    mixte = models.BooleanField(default=True)
    nb_players = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Next(models.Model):
    rules = models.ManyToManyField('Rule', related_name="+")


class Category(models.Model):
    name = models.CharField(max_length=255)
    difficulty = models.PositiveIntegerField()
    weighting = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Game(models.Model):
    category = models.ForeignKey('Category')
    players = models.ManyToManyField('Player')
    mixte = models.BooleanField(default=True)

    def __unicode__(self):
        return "Game %s" % (self.category)

    def select_rule(self):
        if self.mixte:
            rules = Rule.Objects.filter(
                nb_players__lte=self.players.count(),
                category__difficulty__lte=self.category.difficulty
            )
        else:
            rules = Rule.Objects.filter(
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
        random.shuffle(self.players)
        return self.players[:rule.nb_players]


    def next_turn(self):
        rule = self.select_rule
        players = self.select_players(rule)

        turn = Turn(rule=rule, game=self)
        turn.save()




        # Select a Rule
        # Select players according to rule number
        # Create the turn
        # For each player, create a Drink
        # Signal to update player stats
        pass


class Player(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    sex = models.BooleanField(choices=CHOICES)

    class Meta:
        unique_together = (("first_name", "last_name"),)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Turn(models.Model):
    rule = models.ForeignKey('Rule')
    game = models.ForeignKey('Game')


class Drink(models.Model):
    turn = models.ForeignKey('Turn')
    player = models.ForeignKey('Player')
    sip = models.PositiveIntegerField(null=True)
    bottoms_up = models.NullBooleanField()


